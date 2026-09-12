"""Current six-group evaluation. Maintainer-side registration; never candidate input.

Assignments cover all current sources so cross-type lineage cannot cross splits.
The runner still owns process/network isolation and registration timing.
"""
import argparse
import base64
import hashlib
from collections import Counter, defaultdict
import json
from pathlib import Path
import zipfile

import evaluation_profile as ep
import evaluation_batch as legacy
import repository_types as rt
from coverage import TIERS
from external_inputs import verify as verify_git
from population_diagnostics import analyze as population_diagnostics, size_associations


def lineage(sources, assignments):
    entries={r['id']:r for r in sources}
    if set(assignments)!=set(entries) or any(not isinstance(v,str) or not v.strip() for v in assignments.values()):
        raise ValueError(f'Assignments must cover all {len(entries)} current sources, including other types')
    parent={rid:rid for rid in entries}
    def root(a):
        while parent[a]!=a:a=parent[a]
        return a
    def union(a,b):
        if b not in entries:raise ValueError('Unknown related source '+b)
        parent[root(a)]=root(b)
    groups=defaultdict(list)
    for rid,row in entries.items():
        if not row.get('family_id'):raise ValueError('Missing source family')
        groups['family:'+row['family_id']].append(rid)
        info=row.get('lineage',{})
        if info.get('construction_group'):groups['construction:'+info['construction_group']].append(rid)
        for other in info.get('related_ids',[]):union(rid,other)
    for members in groups.values():
        for rid in members[1:]:union(members[0],rid)
    components=defaultdict(list)
    for rid in entries:components[root(rid)].append(rid)
    components=sorted(sorted(g) for g in components.values())
    if any(len({assignments[r] for r in group})!=1 for group in components):
        raise ValueError('Source/dependency/construction transitive closure crosses splits')
    return {'repositories':len(entries),'components':components,'limits':'Conservative recorded lineage only; no independent holdout certification.'}


def packet_check(path,spec):
    path=Path(path)
    if legacy.file_sha(path)!=spec['sha256']:raise ValueError('Raw packet hash differs')
    if spec['format']=='frozen-git-inputs-v1':return verify_git(path,spec['sha256'])
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        # Complete raw + decoded SDK 34 definitions take the current packet
        # above 64 MiB; retain a bounded expansion size of 96 MiB.
        if len(names)!=len(set(names)) or sum(i.file_size for i in z.infolist())>96*1024*1024:raise ValueError('Duplicate/oversized raw packet')
        for name in names:
            if ':' in name or chr(92) in name or name.startswith('/') or any(p in {'','..','.'} for p in name.split('/')):raise ValueError('Unsafe raw path')
        index=json.loads(z.read('packet-index.json'))
        if index['schema']!='candidate-raw-inputs-v1':raise ValueError('Raw schema differs')
        if set(names)!={'packet-index.json'}|{r['path'] for r in index['files']}:raise ValueError('Undeclared raw files')
        for row in index['files']:
            body=z.read(row['path'])
            if len(body)!=row['bytes'] or rt.sha(body)!=row['sha256']:raise ValueError('Raw file differs')
        center_bindings={}
        for name in names:
            if name.endswith('/source-binding.json') and json.loads(z.read(name)).get('schema')=='sdk-source-binding-v1':
                sdk_check({n[len(name.rsplit('/',1)[0])+1:]:z.read(n) for n in names if n.startswith(name.rsplit('/',1)[0]+'/')})
            if name.endswith('/source-binding.json') and json.loads(z.read(name)).get('schema')=='center-execution-source-binding-1':
                binding=json.loads(z.read(name));rid=binding['id'];prefix=rid+'/'
                if name!=prefix+'source-binding.json' or rid in center_bindings:raise ValueError('Center raw target path differs')
                identity={'head':binding['head'],'tree':binding['tree']}
                if spec.get('sources',{}).get(rid)!=identity:raise ValueError('Center raw source identity differs')
                declared={prefix+r['path']:r for r in binding['records']}
                actual={n for n in names if n.startswith(prefix)}-{name}
                if set(declared)!=actual or len(declared)!=len(binding['records']):raise ValueError('Center raw records differ')
                for path,record in declared.items():
                    data=z.read(path)
                    if len(data)!=record['bytes'] or rt.sha(data)!=record['sha256']:raise ValueError('Center execution record differs')
                if not binding.get('source_files') or not binding.get('engines'):raise ValueError('Center raw source/engine binding missing')
                center_bindings[rid]=identity
            if name.endswith('/capture.json') and json.loads(z.read(name)).get('schema')=='official-source-capture-v1':
                prefix=name.rsplit('/',1)[0]+'/'
                official_source_check({n[len(prefix):]:z.read(n) for n in names if n.startswith(prefix)})
        if spec.get('sources') is not None and center_bindings!=spec['sources']:raise ValueError('Center raw source set differs')
    return {'sha256':spec['sha256'],'files':len(index['files'])}


def sdk_check(files):
    binding=json.loads(files['source-binding.json']);raw=files['android.txt.base64'];decoded=files['android.txt'];directory=files['directory.json']
    if binding['schema']!='sdk-source-binding-v1':raise ValueError('SDK binding schema differs')
    if base64.b64decode(raw,validate=True)!=decoded:raise ValueError('SDK raw and decoded bytes differ')
    for key,body in [('raw_response_sha256',raw),('decoded_sha256',decoded),('directory_response_sha256',directory)]:
        if rt.sha(body)!=binding[key]:raise ValueError('SDK content binding differs')
    blob=hashlib.sha1(b'blob '+str(len(decoded)).encode()+b'\0'+decoded).hexdigest()
    listing=json.loads(directory.decode().removeprefix(")]}'\n"))
    if blob!=binding['git_blob'] or not any(e['name']=='android.txt' and e['id']==blob for e in listing['entries']):raise ValueError('SDK Git blob/directory differs')
    path=str(binding['compile_sdk'])+'/public/api/android.txt'
    if binding['path']!=path or binding['url']!=binding['upstream']+'/+/'+binding['commit']+'/'+path+'?format=TEXT':raise ValueError('SDK revision/path binding differs')
    return binding


def official_source_check(files):
    binding=json.loads(files['capture.json']);revision=files['revision.json']
    if rt.sha(revision)!=binding['revision_sha256']:raise ValueError('Official revision response differs')
    commit=json.loads(revision.decode().removeprefix(")]}'\n"))['commit']
    if commit!=binding['commit']:raise ValueError('Official revision binding differs')
    for row in binding['files']:
        raw=files[row['file']+'.base64'];decoded=files[row['file']]
        if base64.b64decode(raw,validate=True)!=decoded or rt.sha(raw)!=row['raw_sha256'] or rt.sha(decoded)!=row['decoded_sha256']:
            raise ValueError('Official source bytes differ')
        blob=hashlib.sha1(b'blob '+str(len(decoded)).encode()+b'\0'+decoded).hexdigest()
        if blob!=row['git_blob'] or row['url']!=binding['upstream']+'/+/'+commit+'/'+row['path']+'?format=TEXT':
            raise ValueError('Official source revision/path differs')
    return binding


def export_inputs(wrapper,repository_id,packet,output):
    inventory=rt.read(Path(wrapper)/'docs/current-evaluation.json')
    keys={r['packet_id'] for r in inventory['leaves'] if r['id'].split('/')[0]==repository_id and r.get('packet_id')}
    if len(keys)!=1:raise ValueError('Repository has no single registered external packet')
    spec=inventory['packets'][keys.pop()];packet_check(packet,spec)
    target=Path(output)
    if target.exists():raise ValueError('Candidate input destination already exists')
    with zipfile.ZipFile(packet) as z:
        prefix=repository_id+'/'
        selected={n[len(prefix):]:z.read(n) for n in z.namelist() if n.startswith(prefix)} if spec['format']=='candidate-raw-inputs-v1' else {n:z.read(n) for n in z.namelist()}
    if not selected:raise ValueError('Repository has no raw input files')
    if 'input-manifest.json' in selected:raise ValueError('Reserved input manifest name in packet')
    heads={r['head'] for r in inventory['leaves'] if r['id'].split('/')[0]==repository_id}
    if len(heads)!=1:raise ValueError('Candidate repository HEAD differs across leaves')
    manifest={'schema':'candidate-input-manifest-v1','repository_id':repository_id,'head':heads.pop(),
              'source_packet_sha256':spec['sha256'],
              'files':[{'path':name,'bytes':len(body),'sha256':rt.sha(body)} for name,body in sorted(selected.items())]}
    selected['input-manifest.json']=rt.encoded(manifest)
    target.mkdir(parents=True)
    for name,body in selected.items():
        p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
    return {'repository_id':repository_id,'files':len(selected),'source_packet_sha256':spec['sha256'],
            'input_manifest_sha256':rt.sha(selected['input-manifest.json'])}


def sdk_requirements_check(packet,row):
    """Check declared platform inputs against this repository and SDK version."""
    rid=row['id'].split('/')[0]
    with zipfile.ZipFile(packet) as z:
        for requirement in row.get('sdk_requirements',[]):
            directory=requirement['directory']
            if directory not in {'sdk','sdk33','sdk34'}:raise ValueError('Invalid SDK input directory')
            prefix=rid+'/'+directory+'/'
            files={n[len(prefix):]:z.read(n) for n in z.namelist() if n.startswith(prefix)}
            try:
                sdk=sdk_check(files);binding=json.loads(files['repository-binding.json'])
            except (KeyError,json.JSONDecodeError) as exc:
                raise ValueError('Missing complete repository SDK input') from exc
            if (sdk['compile_sdk']!=requirement['compile_sdk'] or
                binding.get('schema')!='repository-sdk-input-v1' or
                binding.get('repository_id')!=rid or binding.get('head')!=row['head'] or
                binding.get('compile_sdk')!=sdk['compile_sdk'] or not binding.get('build_files')):
                raise ValueError('Repository SDK binding differs')


def android_source_sizes(wrapper,sources):
    sizes={}
    for source in sources:
        rid=source['id'];kind=source['type_id']
        if kind not in {'app','fw'}:continue
        if 'evidence' in source:
            facts=rt.read(rt.bound(wrapper,source['evidence']))
            inventory=rt.read(rt.bound(wrapper,facts['source_inventory']))
            loc=inventory['size']['source_loc'];files=inventory['size']['source_files']
        else:
            facts=rt.read(Path(wrapper)/'facts'/f'{rid}.json')
            if facts['head']!=source['head']:raise ValueError('Source size HEAD differs')
            loc=facts['production_scope']['source_loc'];files=facts['production_scope']['source_file_count']
        lower,upper=(30000,80000) if kind=='app' else (80000,200000)
        sizes[rid]={'head':source['head'],'source_loc':loc,'source_files':files,
                    'size_band':'small' if loc<lower else 'medium' if loc<upper else 'large'}
    return sizes


def prepare(wrapper,type_id,mode,assignments,external_inputs=None,profile=None):
    wrapper=Path(wrapper);registry=rt.validate(wrapper)
    if type_id not in rt.TYPES:raise ValueError('One current business type is required')
    if mode not in {'source_only','frozen_external'}:raise ValueError('Live mode needs a separately captured reference batch')
    sources=rt.select(registry,wrapper,'all');split=lineage(sources,assignments)
    inventory=rt.read(wrapper/'docs/current-evaluation.json')
    if inventory['registry_sha256']!=legacy.file_sha(wrapper/'suites.json'):raise ValueError('Current registry drift')
    entry=next(e for e in registry['suites'] if e['id']==type_id)
    context={'reference_id':inventory['reference_id'],'type_id':type_id,'source_manifest_sha256':entry['manifest']['sha256'],
             'canonical_standard_sha256':entry['canonical_scores']['sha256'],'contract_sha256':entry['contract']['sha256'],
             'external_packet_sha256':ep.digest(inventory['packets']),'registry_sha256':inventory['registry_sha256']}
    rows=[r for r in inventory['leaves'] if r['type_id']==type_id]
    refs=rt.read(rt.bound(wrapper,entry['canonical_scores']))['repositories']
    unresolved={r['id']+'/'+name for r in refs for name,(score,_) in rt.leaf_values(r['reference']).items() if score is None}
    availability={'leaves':[dict(r,reference_status='unresolved' if r['id'] in unresolved else 'resolved') for r in rows]}
    registered=ep.register(availability,mode,context)
    if profile is None:profile=registered
    else:
        ep.validate_profile(profile)
        if profile['context']!=context or profile['mode']!=mode or profile['requested']!=registered['requested'] or not set(profile['eligible'])<=set(registered['eligible']):raise ValueError('Common profile differs from current inputs')
    checks={}
    needed={r['packet_id'] for r in rows if r['id'] in profile['eligible'] and mode=='frozen_external' and r.get('packet_id')}
    if needed and external_inputs is None:raise ValueError('Frozen batch requires actual raw packets before registration')
    for pid in sorted(needed):
        spec=inventory['packets'][pid];checks[pid]=packet_check(Path(external_inputs)/spec['name'],spec)
    if mode=='frozen_external':
        for row in rows:
            if row['id'] in profile['eligible'] and row.get('sdk_requirements'):
                spec=inventory['packets'][row['packet_id']]
                sdk_requirements_check(Path(external_inputs)/spec['name'],row)
    leaves=[]
    byid={r['id']:r for r in sources}
    for row in refs:
        for name,(score,maximum) in rt.leaf_values(row['reference']).items():
            if type_id in rt.GROUPS:allowed=list(range(maximum+1))
            else:allowed=TIERS[name] if type_id!='new-energy-matlab' else {3:[0,1,2,3],5:[0,1,3,5],10:[0,3,8,10]}[maximum]
            leaves.append({'id':row['id']+'/'+name,'repository_id':row['id'],'name':name,'score':score,'kind':type_id,'allowed_scores':allowed,'split':assignments[row['id']],'family_id':byid[row['id']]['family_id']})
    if set(ep.indexed(leaves))!=set(profile['requested']):raise ValueError('Current reference/availability universe differs')
    batch={'schema':'evaluation-batch-v2','profile':profile,'reference':{'context':context,'leaves':leaves},'assignments':assignments,'lineage_check':split,'external_packet_check':checks,'limits':'One business type per batch; source eligibility is independent of gold score. No OS isolation or blind-review claim.'}
    if type_id in rt.GROUPS:
        from population_diagnostics import analyze_mixed_contracts
        from centers import contract
        selected={r['id']:('matlab' if r['implementation_kind']=='matlab' else 'software') for r in sources if r['type_id']==type_id}
        contracts={kind:{l['name']:l['allowed_scores'] for l in contract(wrapper,kind)['leaves']} for kind in set(selected.values())}
        batch['population_diagnostics']=analyze_mixed_contracts(leaves,split['components'],selected,contracts)
    else:batch['population_diagnostics']=population_diagnostics(leaves,split['components'])
    if type_id in {'app','fw'}:
        sizes=android_source_sizes(wrapper,[s for s in sources if s['type_id']==type_id])
        batch['population_diagnostics']['size_support']=size_associations(leaves,split['components'],sizes)
    batch['batch_sha256']=ep.digest(batch)
    return batch


def assess(batch,candidate,plan=None,adjudications=None):
    result=legacy.assess(batch,candidate,plan,adjudications)
    predictions=ep.indexed(candidate['leaves']);groups=defaultdict(list)
    for row in batch['reference']['leaves']:
        for score in row['allowed_scores']:groups.setdefault((row['name'],score),[])
        if row['id'] in batch['profile']['eligible']:groups[(row['name'],row['score'])].append(row)
    bands=[]
    for (name,score),rows in sorted(groups.items()):
        confusion=Counter()
        for row in rows:
            # legacy.assess has already validated the numeric value against
            # integer contract tiers; JSON 3, 3.0 and -0.0 retain that meaning.
            p=predictions.get(row['id'],{});label=str(int(p['score'])) if p.get('status')=='scored' else p.get('status','missing');confusion[label]+=1
        bands.append({'leaf':name,'gold':score,'count':len(rows),'recall':confusion[str(score)]/len(rows) if rows else None,'predictions':dict(confusion),
                      'measurement_status':'measured' if rows else 'unmeasured'})
    result['band_recall_and_confusion']=bands
    result['population_diagnostics']=batch.get('population_diagnostics')
    n=result['common_eligible'];result['abstention_fraction']=result['abstained']/n if n else None
    result['family_strata']=[]
    for family in sorted({r['family_id'] for r in batch['reference']['leaves']}):
        rows=[r for r in batch['reference']['leaves'] if r['family_id']==family and r['id'] in batch['profile']['eligible']]
        correct=sum(predictions.get(r['id'],{}).get('status')=='scored' and predictions[r['id']].get('score')==r['score'] for r in rows)
        result['family_strata'].append({'family':family,'eligible':len(rows),'correct':correct,'accuracy':correct/len(rows) if rows else None})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    prep=sub.add_parser('prepare');prep.add_argument('--wrapper',required=True);prep.add_argument('--type',choices=sorted(rt.TYPES),required=True);prep.add_argument('--mode',choices=['source_only','frozen_external'],required=True);prep.add_argument('--assignments',required=True);prep.add_argument('--external-inputs');prep.add_argument('--profile')
    score=sub.add_parser('assess');score.add_argument('--batch',required=True);score.add_argument('--candidate',required=True);score.add_argument('--review-plan');score.add_argument('--adjudications')
    export=sub.add_parser('inputs');export.add_argument('--wrapper',required=True);export.add_argument('--repository-id',required=True);export.add_argument('--packet',required=True);export.add_argument('--destination',required=True)
    for parser in [prep,score]:parser.add_argument('--output',required=True)
    a=p.parse_args()
    if a.command=='inputs':
        print(json.dumps(export_inputs(a.wrapper,a.repository_id,a.packet,a.destination)));return
    if a.command=='prepare':result=prepare(a.wrapper,a.type,a.mode,rt.read(a.assignments),a.external_inputs,rt.read(a.profile) if a.profile else None)
    else:result=assess(rt.read(a.batch),rt.read(a.candidate),rt.read(a.review_plan) if a.review_plan else None,rt.read(a.adjudications) if a.adjudications else None)
    out=Path(a.output)
    if out.exists():raise ValueError('Refusing to overwrite saved registration/results')
    out.write_bytes(rt.encoded(result))

if __name__=='__main__':main()
