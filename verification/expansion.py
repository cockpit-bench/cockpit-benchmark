"""Verify locally admitted expansion sources and independently replay reviewed facts.

No build or target code is executed by extract/verify. Android rules and the
MATLAB contract replay consume explicit reviewed observations; this is not a
second blind semantic judgment. Native run files are verified separately.
"""
import argparse,collections,hashlib,json,re,subprocess,sys,zipfile,io
from pathlib import Path
import xml.etree.ElementTree as ET
import rules,matlab_recompute
from counting import count_production_lines
from suites import read,encoded,sha,require,bound,git

def extract(repo,scope):
    repo=Path(repo).resolve();require(not git('-C',repo,'status','--porcelain'),'Dirty source')
    files=[];production=[];excluded=[];models=[]
    for line in git('-C',repo,'ls-tree','-r','HEAD').splitlines():
        metadata,path=line.split('\t',1);mode,kind,oid=metadata.split();require(kind=='blob','Unexpected nested source dependency')
        body=git('-C',repo,'show','HEAD:'+path,binary=True)
        files.append({'path':path,'blob':oid,'sha256':sha(body),'bytes':len(body)})
        if path in scope.get('models',[]):
            model={'path':path,'sha256':sha(body),'blocks':[],'lines':[],'stateflow':{'states':0,'transitions':0}}
            with zipfile.ZipFile(io.BytesIO(body)) as archive:
                for member in sorted(archive.namelist()):
                    if not member.endswith('.xml'):continue
                    if not(member=='simulink/blockdiagram.xml' or member.startswith('simulink/systems/') or member.startswith('simulink/stateflow/')):continue
                    tree=ET.fromstring(archive.read(member))
                    for block in tree.iter('Block'):
                        values={p.get('Name'):p.text for p in block.findall('P')}
                        model['blocks'].append({'member':member,'sid':block.get('SID'),'name':block.get('Name'),'type':block.get('BlockType'),'parameters':values})
                    for edge in tree.iter('Line'):
                        model['lines'].append({'member':member,**{p.get('Name'):p.text for p in edge.findall('P')}})
                    if 'stateflow' in member:
                        model['stateflow']['states']+=len(list(tree.iter('state')));model['stateflow']['transitions']+=len(list(tree.iter('transition')))
            model['block_types']=dict(sorted(collections.Counter(b['type'] for b in model['blocks']).items()))
            # Linked in-repository definitions are listed once; link instances/containers
            # and pure interface/routing/display blocks do not inflate size.
            routing={'Inport','Outport','SubSystem','ModelReference','Goto','From','DataStoreMemory','DataStoreRead','DataStoreWrite','Mux','Demux','BusCreator','BusSelector','Scope','Display','Terminator'}
            model['effective_logic_blocks']=sum(b['type'] not in routing and not(b['type']=='Reference' and (b['parameters'].get('SourceBlock') or '').startswith('BMSLib/')) for b in model['blocks'])
            models.append(model)
        suffix=Path(path).suffix.lower()
        if suffix in {'.java','.kt','.aidl','.c','.cpp','.h'}:
            roots=scope.get('production_roots',[])
            if any(path.startswith(root+'/') for root in roots):
                language={'.java':'Java','.kt':'Kotlin','.aidl':'AIDL','.c':'C','.cpp':'C++','.h':'C/C++ header'}[suffix]
                text=body.decode('utf-8-sig');loc,generated_ranges=count_production_lines(text,language='kotlin' if suffix=='.kt' else None)
                production.append({'path':path,'language':language,'physical_lines':len(text.splitlines()),'source_loc':loc,'build_owner':path.split('/')[0]})
            else:excluded.append({'path':path,'reason':'debug acceptance, sample consumer, or generated output outside declared production roots'})
    refs={ref:oid for ref,oid in (line.split('|') for line in git('-C',repo,'for-each-ref','--format=%(refname)|%(objectname)','refs/heads','refs/tags').splitlines())}
    source_loc=sum(row['source_loc'] for row in production);logic=sum(m['effective_logic_blocks'] for m in models)
    return {'head':git('-C',repo,'rev-parse','HEAD'),'tree':git('-C',repo,'rev-parse','HEAD^{tree}'),'refs':refs,'files':files,
            'scope':scope,'production':production,'excluded_source':excluded,'models':models,
            'size':{'source_files':len(production),'source_loc':source_loc,'physical_lines':sum(x['physical_lines'] for x in production),'effective_logic_blocks':logic},
            'ci_candidates':[x['path'] for x in files if x['path'].startswith('.github/workflows/') or Path(x['path']).name in {'.gitlab-ci.yml','Jenkinsfile','azure-pipelines.yml','APP_BUILD','PREUPLOAD.cfg','TEST_MAPPING'}]}

def recompute(facts):
    if facts['type_id']=='new-energy-matlab':return matlab_recompute.recompute(facts['rule_inputs'])
    result={}
    for leaf,values in facts['rule_inputs'].items():
        if leaf in rules.RULES:
            value=rules.RULES[leaf](values);result[leaf]=None if value=='failed' else value
        else:result[leaf]=rules.semantic_rule(values)[0]
    return result

def verify(wrapper,source_map,records_root=None):
    wrapper=Path(wrapper);mapping=read(source_map);result=[]
    for kind in ['app','fw','new-energy-matlab']:
        addition=read(wrapper/'suites'/kind/'additions.json')
        for entry in addition['repositories']:
            source=entry['source'];facts=read(bound(wrapper,source['evidence']));repo=Path(mapping[source['id']])
            first=extract(repo,facts['production_scope']);second=extract(repo,facts['production_scope'])
            require(encoded(first)==encoded(second),'Repeated source facts differ')
            require(first['head']==source['head'] and first['tree']==source['tree'] and first['refs']==source['refs'],'Source binding differs')
            require(sha(encoded(first))==facts['source_inventory_sha256'],'Source inventory differs')
            inventory=read(bound(wrapper,facts['source_inventory']));require(first==inventory,'Published inventory differs')
            from semantic_audits import parameter_inventory,reuse_inventory
            for field,producer in [('parameter_scope_audit',parameter_inventory),('reuse_scope_audit',reuse_inventory)]:
                if field in facts:
                    recorded=read(bound(wrapper,facts[field]))
                    require(recorded==producer(repo),'Semantic scope inventory differs: '+source['id'])
            declared={leaf['name']:leaf['score'] for leaf in facts['reference']['leaves']}
            actual=recompute(facts);require(actual==declared,'Independent rule recomputation differs: '+source['id'])
            def anchor(a):
                require(a['commit']==source['head'],'Stale evidence anchor')
                if a['evidence_type']=='code':
                    body=git('-C',repo,'show','HEAD:'+a['path'],binary=True).decode('utf-8-sig').splitlines()
                    require(1<=a['start_line']<=a['end_line']<=len(body),'Invalid code span')
                    require(a['symbol'] in '\n'.join(body[a['start_line']-1:a['end_line']]),'Symbol missing from code span')
                elif a['evidence_type']=='model':
                    model=next((m for m in inventory['models'] if m['path']==a['path']),None);require(model is not None,'Model outside production closure')
                    require(any(b['member']==a['member'] and b['sid']==a['sid'] and b['name']==a['symbol'] for b in model['blocks']),'Model element missing')
                elif a['evidence_type']=='facts':
                    value=inventory if a['source']=='source_inventory' else facts
                    for part in a['json_pointer'].strip('/').split('/'):
                        part=part.replace('~1','/').replace('~0','~');value=value[int(part)] if isinstance(value,list) else value[part]
                elif a['evidence_type']=='git_ref':require(source['refs'].get(a['ref'])==a['commit_oid'],'Ref anchor differs')
                else:raise ValueError('Unknown anchor type')
            for leaf in facts['reference']['leaves']:
                require(leaf['analysis'] and leaf['score_reasoning'] and leaf['evidence'],'Leaf explanation missing')
                for a in leaf['evidence']:anchor(a)
                require(len({a['independent_group'] for a in leaf['evidence']})>=2 or leaf.get('deterministic_absence') is True,'Independent evidence groups missing')
            if records_root:
                for record in facts['execution']['records']:
                    path=Path(records_root)/record['path'];require(path.is_file() and sha(path.read_bytes())==record['sha256'],'Native record differs: '+record['path'])
            result.append({'id':source['id'],'head':source['head'],'leaves':len(actual),'differences':0,'inventory_repeat_identical':True,'native_artifacts_checked':bool(records_root)})
    return {'status':'passed','repositories':result,'leaves':sum(r['leaves'] for r in result),'review_scope':'Shared explicit semantic observations, independent rule code and two deterministic source extractions; not blind semantic review'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--wrapper',type=Path,required=True);parser.add_argument('--source-map',type=Path,required=True);parser.add_argument('--records-root',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify(args.wrapper,args.source_map,args.records_root)
    if args.output:args.output.write_bytes(encoded(result))
    print(json.dumps(result,ensure_ascii=False));return 0
if __name__=='__main__':sys.exit(main())
