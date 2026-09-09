"""Read-only replay of disclosed MATLAB evidence; never execute candidate code.

The attachment retains original evidence bytes. Its catalog resolves recorded
Windows paths without accessing those paths on the verifier's host. Source and
tool binaries remain hash-only provenance; model execution is not repeated.
"""
import argparse
import csv
import io
import json
import math
from pathlib import Path
import struct
import zipfile

from suites import require, sha, read, bound, safe_path, git
import matlab_validators as gates
from matlab_recompute import recompute
from matlab_properties import evaluate

IDS={'ML-%02d'%n for n in range(1,10)}
NATIVE=IDS|{'ML-02-B','ML-05-B','ML-08-B'}

def key(value):return str(value).replace('\\','/').lower().rstrip('/')

class Evidence:
    def __init__(self, archive, index):
        self.z=zipfile.ZipFile(archive)
        self.index=index
        self.catalog=index['catalog']
        self.by_path={key(x['original_path']):x for x in self.catalog}
        require(len(self.by_path)==len(self.catalog),'Duplicate evidence catalog paths')
        expected={x['payload'] for x in self.catalog if x['storage']=='payload'}
        names=self.z.namelist()
        require(len(names)==len(set(names)) and set(names)==expected,'Unexpected or missing archive members')
        self.cache={}
        for row in self.catalog:
            require(row['storage'] in {'payload','provenance_only'},'Unknown evidence storage')
            require(len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'Invalid evidence digest')
            if row['storage']=='payload':
                require(row['payload']=='sha256/'+row['sha256'],'Invalid content-addressed payload')
                data=self.z.read(row['payload'])
                require(len(data)==row['bytes'] and sha(data)==row['sha256'],'Evidence payload differs')
                self.cache[row['sha256']]=data
            else:require(row['reason'] in {'source_or_model','tool_binary','compiled_or_generated_artifact','other_binary_evidence'},'Unclassified omitted evidence')

    def record(self,path,digest=None):
        row=self.by_path.get(key(path))
        require(row is not None,'Evidence catalog misses '+str(path))
        if digest is not None:require(row['sha256']==digest,'Evidence inner binding differs: '+str(path))
        return row

    def data(self,path,digest=None):
        row=self.record(path,digest)
        require(row['storage']=='payload','Raw evidence was not exported: '+str(path))
        return self.cache[row['sha256']]

    def document(self,path,digest=None):return json.loads(self.data(path,digest))

    def named(self,entry):return self.document(entry['original_path'],entry['sha256'])

    def references(self,node):
        if isinstance(node,dict):
            path=node.get('path');digest=node.get('sha256')
            if isinstance(path,str) and isinstance(digest,str) and (':/' in path.replace('\\','/')):
                self.record(path,digest)
            for value in node.values():self.references(value)
        elif isinstance(node,list):
            for value in node:self.references(value)

def validate_index(wrapper,suite):
    readiness=read(bound(wrapper,suite['readiness']))
    index=read(bound(wrapper,readiness['evidence_index']))
    require(index['schema_version']=='matlab-evidence-1' and index['suite_id']==suite['id'],'Wrong evidence index')
    require({r['id'] for r in index['repositories']}==IDS and len(index['repositories'])==9,'Missing complete MATLAB facts')
    require({r['id'] for r in index['native']}==NATIVE and len(index['native'])==12,'Missing native configuration')
    require(index['local_finalization']['status']=='passed' and index['local_finalization']['leaves']==117,'Missing complete local finalization')
    require(index['local_finalization']['differences']==[],'Local score differences')
    require(index['attachment']['url']=='https://github.com/cockpit-bench/cockpit-benchmark/releases/download/'+suite['version']+'/'+index['attachment']['name'],'Wrong evidence attachment URL')
    require(index['attachment']['name']=='matlab-verification-data-'+suite['version']+'.zip','Wrong evidence attachment name')
    require(index['scope']=='disclosed_evidence_replay_not_model_execution','Evidence scope changed')
    # A readiness flag cannot substitute for this complete, cross-bound index.
    entries={key(r['original_path']):r for r in index['catalog']}
    require(len(entries)==len(index['catalog']) and bool(entries),'Empty/duplicate catalog')
    for row in index['repositories']:
        for field in ['facts','facts_repeat','snapshot','snapshot_repeat','api','api_repeat','leaf_evidence']:
            entry=row[field];record=entries.get(key(entry['original_path']))
            require(record is not None and record['sha256']==entry['sha256'] and record['storage']=='payload','Incomplete facts export')
        for first,second in [('facts','facts_repeat'),('snapshot','snapshot_repeat'),('api','api_repeat')]:
            require(row[first]['sha256']==row[second]['sha256'],'Repeated local evidence differs')
    for row in index['native']:
        for field in ['binding','result','vectors','api','acceptance_binding','source_snapshot']+([] if row['id']=='ML-01' else ['properties']):
            entry=row[field];record=entries.get(key(entry['original_path']))
            require(record is not None and record['sha256']==entry['sha256'] and record['storage']=='payload','Incomplete native export')
    return index

def verify(wrapper,suite,archive,sources_root=None):
    wrapper=Path(wrapper);archive=Path(archive);index=validate_index(wrapper,suite)
    require(archive.stat().st_size==index['attachment']['bytes'] and sha(archive.read_bytes())==index['attachment']['sha256'],'Wrong evidence archive')
    e=Evidence(archive,index)
    manifest=read(bound(wrapper,suite['manifest']));sources={r['id']:r for r in manifest['repositories']}
    scores=read(bound(wrapper,suite['canonical_scores']));scored={r['id']:r for r in scores['repos']}
    base=wrapper/'suites/matlab-simulink'
    table=list(csv.DictReader((base/'SCORECARD.csv').read_text(encoding='utf-8-sig').splitlines()))
    require(len(table)==9 and {r['id'] for r in table}==set(scored),'Scorecard repository set differs')
    for r in table:
        score=scored[r['id']]
        require(r['head']==score['head'] and int(r['total'])==score['total'] and int(r['max_score'])==61,'Scorecard binding differs')
        require(all(int(r[k])==v for k,v in score['scores'].items()),'Scorecard leaf differs')
    limits=read(base/'DATASET_LIMITS.json')
    for entry in limits['inputs']:bound(base,entry)
    source_cache={}
    def source_bytes(source,head,path):
        cache_key=(source['id'],head,path)
        if cache_key not in source_cache:
            repo=safe_path(Path(sources_root),source['name'])
            source_cache[cache_key]=git('-C',repo,'show',head+':'+path,binary=True)
        return source_cache[cache_key]
    leaves=0
    for row in index['repositories']:
        f=e.named(row['facts']);snap=e.named(row['snapshot']);api=e.named(row['api']);inventory=e.named(row['leaf_evidence'])
        source=sources[row['id']]
        gates.validate_frozen_snapshot(snap,source)
        require(f['head']==source['head'] and f['tree']==source['tree'],'Fact source mismatch')
        require(f['model_sha256']==inventory['model_sha256'] and inventory['head']==f['head'],'Leaf inventory model mismatch')
        require(recompute(f)==scored[row['id']]['scores'],'Independent MATLAB score replay differs')
        oracle=read(safe_path(wrapper,'suites/matlab-simulink/oracle/'+row['id']+'.json'))
        require(oracle['head']==source['head'] and oracle['tree']==source['tree'],'Oracle source mismatch')
        require(len(oracle['leaves'])==13 and {l['id'] for l in oracle['leaves']}==set(scored[row['id']]['scores']),'Oracle leaf set differs')
        blocks={b['sid']:b for b in api['blocks']};files={x['path']:x for x in snap['files']}
        for leaf in oracle['leaves']:
            require(leaf['score']==scored[row['id']]['scores'][leaf['id']] and bool(leaf['reason']),'Oracle score/reason differs')
            require(len(leaf['evidence'])>=2,'Missing evidence anchors')
            require(any(a.get('kind')=='artifact' and a.get('sha256')==row['leaf_evidence']['sha256'] and
                        a.get('json_pointer')=='/leaves/'+leaf['id'] for a in leaf['evidence']),'Missing detailed leaf evidence')
            for a in leaf['evidence']:
                if a.get('kind')=='artifact':
                    require(a['sha256']==row['leaf_evidence']['sha256'] and a['head']==f['head'] and a['model_sha256']==f['model_sha256'],'Artifact anchor differs')
                    require(gates.json_pointer(inventory,a['json_pointer']) not in (None,{},[]),'Empty leaf pointer')
                elif 'sid' in a:
                    require(a['sid'] in blocks and blocks[a['sid']]['path']==a['symbol'] and a['sha256']==f['model_sha256'] and a['ref']==f['head'],'Block anchor differs')
                elif 'line' in a:
                    require(a['path'] in files and a['sha256']==files[a['path']]['sha256'] and a['ref']==f['head'] and type(a['line']) is int and a['line']>0,'Line anchor binding differs')
                    if sources_root is not None:
                        raw=source_bytes(source,a['ref'],a['path'])
                        require(sha(raw)==a['sha256'] and a['line']<=len(raw.splitlines()),'Restored source line does not resolve')
                elif a.get('kind')=='git_refs':require(a['refs'] and all(x in snap['refs'] for x in a['refs']),'Ref anchor differs')
                else:require(a.get('tree')==snap['tree'] and a.get('ref')==snap['head'],'Tree anchor differs')
            leaves+=1
        e.references(f);e.references(inventory)
    native_samples=0;raw_samples=0;assertions=0
    for row in index['native']:
        b=e.named(row['binding']);result=e.named(row['result']);api=e.named(row['api']);ab=e.named(row['acceptance_binding'])
        snap=e.named(row['source_snapshot']);source=sources[row['id'][:5]]
        require(any(r['commit_oid']==snap['head'] and r['tree_oid']==snap['tree'] for r in source['refs']),'Native source is outside frozen refs')
        require(snap['clean'] is True and snap['remote_count']==0 and snap['shallow'] is False,'Native source snapshot is not complete/clean')
        require(any(f['path']==row['model_path'] and f['sha256']==row['model_sha256'] for f in snap['files']),'Native model absent from source snapshot')
        if sources_root is not None:require(sha(source_bytes(source,snap['head'],row['model_path']))==row['model_sha256'],'Native model differs from restored Git bytes')
        model=b['model'];e.references(b);e.references(ab)
        require(model==api['model'] and result['model']==model,'Native API/model differs')
        require(b['model_sha256_before']==b['model_sha256_after']==row['model_sha256'],'Native model changed')
        require(b['model_checksum']==api['model_checksum'] and ab['model_checksum']==b['model_checksum'],'Native/MIL checksum differs')
        require(ab['model_sha256_before']==ab['model_sha256_after']==row['model_sha256'],'Acceptance model differs')
        inputs=b['inputs'];roles={x['role'] for x in inputs}
        require({'model','generated_source','vectors','adapter','runner','replay_runner','compiler','linker'}<=roles,'Missing native input role')
        for role,name in [('runner','replay_fix.py'),('replay_runner','replay_generated.py' if row['id']=='ML-01' else 'replay_nine.py')]:
            require([x['sha256'] for x in inputs if x['role']==role]==[index['runners'][name]['sha256']],'Unexpected bound native runner')
        for role,field in [('vectors','vectors_sha256'),('adapter','adapter_sha256')]:
            selected=[x for x in inputs if x['role']==role]
            require(len(selected)==1 and selected[0]['sha256']==result[field],'Native result input hash differs')
        vector=[x for x in inputs if x['role']=='vectors'][0]
        require(any(x.get('role')=='vectors' and key(x['path'])==key(vector['path']) and x['sha256']==vector['sha256'] for x in ab['inputs']),'Native/MIL vectors differ')
        require(any(x['sha256']==row['result']['sha256'] and key(x['path'])==key(row['result']['original_path']) for x in b['result_artifacts']),'Native result not bound')
        require(any(x['path'].lower().endswith('.exe') and x['sha256']==result['executable_sha256'] for x in b['result_artifacts']),'Executable hash not bound')
        source_hashes={x['path'].replace('\\','/').split('/')[-1]:x['sha256'] for x in inputs if x['role']=='generated_source'}
        require(result.get('sources_sha256', {next(iter(source_hashes)):result.get('generated_source_sha256')})==source_hashes,'Generated source hashes differ')
        # Use the exact shared gate for finite errors, aliases, samples and cases.
        vector_data=e.data(vector['path'],vector['sha256'])
        vectors=json.loads(vector_data)
        original=gates.read_json
        try:
            gates.read_json=lambda _: vectors
            layout=gates.validate_vectors(None,model)
        finally:gates.read_json=original
        gates.validate_native_result(result,model,layout,scenario_error_limit=1e-9 if row['id']=='ML-01' else None)
        native_samples+=layout['samples']
        if row['id']!='ML-01':
            p=e.named(row['properties']);e.references(p)
            require(p['status']=='passed' and p['input_files_unchanged'] is True and p['model']==model,'Invalid property result')
            require(p['samples']==layout['samples'],'Property samples differ')
            require(p['property_script_sha256_before']==p['property_script_sha256_after'],'Property runner changed')
            require(p['property_script_sha256_before']==index['runners']['behavior_properties.py']['sha256'],'Unexpected property runner')
            require([x['sha256'] for x in p['inputs'] if x['role']=='vectors']==[vector['sha256']],'Property vectors differ')
            streams={}
            for stream,role,stage in [('mil','mil_output',ab),('native','native_output',b)]:
                records=[x for x in p['inputs'] if x['role']==role];require(len(records)==1,'Missing raw output')
                record=records[0]
                require(any(key(x['path'])==key(record['path']) and x['sha256']==record['sha256'] for x in stage['result_artifacts']),'Output not stage-bound')
                data=e.data(record['path'],record['sha256']);width=layout['output_count']
                require(len(data)==layout['samples']*width*8,'Raw output sample length differs')
                streams[stream]=list(struct.iter_unpack('<'+str(width)+'d',data))
                measured=evaluate({'id':row['id'],'domain':row['domain']},vectors,streams[stream])
                require(all(measured[k]==p['streams'][stream][k] for k in ['status','samples','assertions']),'Raw property assertions differ')
                assertions+=measured['assertions']
            max_error=0;max_mil=0
            for actual,expected,mil in zip(streams['native'],vectors['expected'],streams['mil']):
                for a,w,m in zip(actual,expected,mil):
                    tolerance=vectors['absolute_tolerance']+vectors['relative_tolerance']*abs(w)
                    require(math.isfinite(a) and math.isfinite(m) and abs(a-w)<=tolerance and abs(a-m)<=tolerance,'Raw native output exceeds tolerance')
                    max_error=max(max_error,abs(a-w));max_mil=max(max_mil,abs(a-m))
            require(max_error==result['max_abs_error'] and max_mil==result['max_mil_error'],'Reported maximum error differs from raw output')
            require(sum(p['streams'][s]['assertions'] for s in ['mil','native'])==p['assertions'],'Property assertion total differs')
            raw_samples+=layout['samples']
    require(leaves==117,'Incomplete score replay')
    return dict(status='passed',repositories=9,leaves=leaves,differences=[],native_configurations=12,
        archive_sha256=index['attachment']['sha256'],
        restored_source_anchors='checked' if sources_root is not None else 'not_requested',
        native_samples=native_samples,raw_output_samples=raw_samples,property_assertions=assertions,
        scope='Disclosed evidence and raw output replay; no new MATLAB/compiler/model execution; ML-01 native stdout was not retained, so its 615 samples use recorded case measurements.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--wrapper',type=Path,required=True);p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--sources',type=Path)
    args=p.parse_args()
    from suites import validate,encoded,legacy_registry
    validate(args.wrapper);registry=legacy_registry(args.wrapper)
    result=verify(args.wrapper,next(s for s in registry['suites'] if s['id']=='matlab-simulink'),args.archive,args.sources)
    if args.output:args.output.write_bytes(encoded(result))
    print(json.dumps(result))

if __name__=='__main__':main()
