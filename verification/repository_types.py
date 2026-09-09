"""Three business repository types, with preserved legacy evidence and scoped restore.

APP and FW are separate scoring populations. MATLAB is technology metadata;
the current business type is New Energy MATLAB. No cross-type score is emitted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import suites as legacy

TYPES={'app':('APP','Android',8,40),'fw':('FW','Android',11,52),
       'new-energy-matlab':('New Energy MATLAB','MATLAB / Simulink',13,61)}
ANDROID_COMMON={'compilation.ci_independence':3,'compilation.compilation_independence':3,'compilation.api_version_management':3,'platform_reuse.platform_upgrade':10,'platform_reuse.release_branch_strategy':10}
LEAF_LIMITS={'app':{**ANDROID_COMMON,'architecture.componentization':5,'architecture.decoupling':3,'architecture.modularization':3},'fw':{**ANDROID_COMMON,'quality.integration_test':3,**{'solid_principle.'+n:4 for n in ['single_responsibility','open_closed','liskov_substitution','interface_segregation','dependency_inversion']}},'new-energy-matlab':{'hierarchy':3,'reuse':3,'interface':3,'dataflow':3,'unit_test':5,'naming':5,'directory':5,'build_independence':3,'model_version':3,'version_independence':3,'release_branches':10,'device_specificity':10,'parameter_management':5}}
ALIASES={'android-validation18':['app','fw'],'matlab-simulink':['new-energy-matlab']}
require=legacy.require;read=legacy.read;bound=legacy.bound;encoded=legacy.encoded;sha=legacy.sha;git=legacy.git

def leaf_values(reference):
    if 'leaves' in reference:
        return {leaf['name']:(leaf.get('score'),leaf['max_score']) for leaf in reference['leaves']}
    limits=LEAF_LIMITS['new-energy-matlab']
    return {name:(value,limits[name]) for name,value in reference['scores'].items()}

def summarize(rows):
    values=[pair for row in rows for pair in leaf_values(row['reference']).values()]
    incomplete=sum(value is None for value,_ in values)
    return {'repository_count':len(rows),'leaf_count':len(values),'max_score':sum(maximum for _,maximum in values),
            'score':None if incomplete else sum(value for value,_ in values),'failed_leaves':incomplete}

def validate(wrapper,require_publishable=False):
    wrapper=Path(wrapper).resolve();registry=read(wrapper/'suites.json')
    require(set(registry)=={'schema_version','benchmark_id','integration_status','default_suite','aggregation','legacy_baseline','suites'},'Unsupported type registry keys')
    require(registry['schema_version']=='benchmark-repository-types-2' and registry['benchmark_id']=='cockpit-benchmark','Wrong type registry')
    require(registry['aggregation']=='separate_repository_type_scores_no_raw_sum','Repository types must not be combined')
    require(registry['default_suite']=='all' and registry['integration_status'] in {'local_expansion','published'},'Invalid integration state/default')
    baseline=read(bound(wrapper,registry['legacy_baseline']));legacy.validate_legacy(wrapper,True,baseline)
    entries=registry['suites'];require(len(entries)==3 and {x['id'] for x in entries}==set(TYPES),'APP, FW, and New Energy MATLAB are required separately')
    old_android=read(wrapper/'STANDARD_SCORES.json')['repositories'];old_matlab=read(wrapper/'suites/matlab-simulink/STANDARD_SCORES.json')['repos']
    old_refs={r['id']:r for r in old_android+old_matlab};seen=set();preserved=set()
    old_manifest=read(wrapper/'manifest.json')['repositories'];old_ml_manifest=read(wrapper/'suites/matlab-simulink/manifest.json')['repositories']
    pending={r['id'] for r in old_manifest if r['delivery_status']=='pending'}
    old_sources={r['id']:r for r in old_manifest if r['delivery_status']=='active'}|{r['id']:r for r in old_ml_manifest}
    for entry in entries:
        required={'id','name','technology','status','contract','manifest','canonical_scores','repository_count','leaf_count','max_score','score','failed_leaves','published_repositories'}
        require(set(entry)==required,'Unsupported type fields')
        type_id=entry['id'];name,technology,leaves,maximum=TYPES[type_id]
        require(entry['name']==name and entry['technology']==technology,'Business type/technology mismatch')
        require(entry['status'] in {'verified_local','published'},'Unverified type cannot be admitted')
        bound(wrapper,entry['contract']);manifest=read(bound(wrapper,entry['manifest']));scores=read(bound(wrapper,entry['canonical_scores']))
        require(manifest['type_id']==scores['type_id']==type_id,'Cross-type payload')
        sources=manifest['repositories'];rows=scores['repositories'];ids=[r['id'] for r in sources]
        require(len(ids)==len(set(ids)) and not seen.intersection(ids),'Duplicate/cross-type repository')
        seen.update(ids);require({r['id'] for r in rows}==set(ids) and len(rows)==len(ids),'Source/score set differs')
        for source in sources:
            require(source['type_id']==type_id and re.fullmatch(r'(APP|FW|ML|NEM)-\d+',source['id']),'Source type/ID mismatch')
            expected_type='app' if source['id'].startswith('APP-') else 'fw' if source['id'].startswith('FW-') else 'new-energy-matlab'
            require(expected_type==type_id,'Repository moved between business types')
            require(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',source['name']),'Unsafe source name')
            for key in ['head','tree']:require(re.fullmatch('[0-9a-f]{40}',source[key]),'Invalid source binding')
            require(source['refs'] and all(re.fullmatch(r'refs/(heads|tags)/[^\s\\:]+',ref) and '..' not in ref and re.fullmatch('[0-9a-f]{40}',oid) for ref,oid in source['refs'].items()),'Invalid source refs')
            require(source['publication_status'] in {'published','verified_local'},'Invalid publication state')
            if source['publication_status']=='published':require(source['repository_url']=='https://github.com/cockpit-bench/'+source['name']+'.git','Publication target differs')
            else:require(source['repository_url'] is None,'Unpublished source must not claim a public URL')
            row=next(r for r in rows if r['id']==source['id']);require(row['head']==source['head'] and row['name']==source['name'],'Stale score source binding')
            values=leaf_values(row['reference']);require(len(values)==leaves and sum(m for _,m in values.values())==maximum,'Wrong leaf contract')
            require({name:maximum for name,(_,maximum) in values.items()}==LEAF_LIMITS[type_id],'Leaf names or maxima differ from the contract')
            if source['id'] in old_refs:
                if row['reference']!=old_refs[source['id']]:
                    require('reference_revision' in row,'A preserved reference changed without an explicit current revision')
                    from reference_revisions import validate as validate_revision
                    validate_revision(wrapper,row,old_refs[source['id']],source,entry['contract']['sha256'])
                else:require('reference_revision' not in row,'A reference revision declares no change')
                old=old_sources[source['id']]
                head=old.get('head',old.get('delivery',{}).get('expected_head'))
                refs=old.get('refs',old.get('delivery',{}).get('refs'))
                if isinstance(refs,list):refs={r['ref']:r['object_oid'] for r in refs}
                require(source['head']==head and source['refs']==refs,'A preserved source HEAD/ref changed')
                preserved.add(source['id'])
            else:
                require(source['id'] not in pending,'A frozen pending slot was reused')
                require(source.get('lineage') and source.get('scan_profile') and source.get('evidence'),'New source lacks provenance/profile/evidence')
                facts=read(bound(wrapper,source['evidence']))
                require(facts['id']==source['id'] and facts['head']==source['head'] and facts['tree']==source['tree'],'New evidence source differs')
                require(facts['state']=='verified_local' and facts['execution']['status']=='passed','New execution has not passed')
                require(facts['reference']==row['reference'],'Reference/evidence disagreement')
                require(row['reference']['id']==source['id'] and row['reference']['head']==source['head'] and row['reference']['tree']==source['tree'],'Reference revision differs')
                require(facts['execution'].get('records') and facts['source_inventory_sha256'],'Missing execution/source inventory bindings')
                inventory=read(bound(wrapper,facts['source_inventory']))
                require(sha(encoded(inventory))==facts['source_inventory_sha256'] and inventory['head']==source['head'] and inventory['tree']==source['tree'] and inventory['refs']==source['refs'],'Inventory source binding differs')
                from expansion import recompute
                require(recompute(facts)=={name:value for name,(value,_) in values.items()},'Rule facts and reference scores differ')
            for value,limit in values.values():
                allowed={3:{0,1,2,3},4:{0,1,2,3,4},5:{0,1,3,5},10:{0,3,8,10}}[limit]
                require(value is None or type(value) is int and value in allowed,'Illegal leaf score')
        summary=summarize(rows);require(scores['summary']==summary,'Scorecard summary differs')
        for key,value in summary.items():require(entry[key]==value,'Registry denominator/score differs: '+key)
        published=sum(r['publication_status']=='published' for r in sources)
        require(entry['published_repositories']==published,'Publication count differs')
        require(entry['status']==('published' if published==len(sources) else 'verified_local'),'Type publication state differs')
        if require_publishable:require(entry['status']=='published',type_id+': local additions are not published')
    require(preserved==set(old_refs),'Frozen baseline repository omitted')
    if registry['integration_status']=='published':require(all(x['status']=='published' for x in entries),'Published registry contains local additions')
    return registry

def select(registry,wrapper,type_id,ids=None):
    selected=set(TYPES) if type_id=='all' else set(ALIASES.get(type_id,[type_id]))
    require(selected<=set(TYPES),'Unknown repository type')
    rows=[row for entry in registry['suites'] if entry['id'] in selected for row in read(bound(wrapper,entry['manifest']))['repositories']]
    if ids is not None:
        require(len(ids)==len(set(ids)) and set(ids)<={r['id'] for r in rows},'Requested IDs outside selected type')
        rows=[r for r in rows if r['id'] in ids]
    require(rows,'Empty repository selection');return rows

def check_source(path,row):
    require(git('-C',path,'rev-parse','HEAD')==row['head'] and git('-C',path,'rev-parse','HEAD^{tree}')==row['tree'],'Restored HEAD/tree differs')
    refs=dict(line.split('|') for line in git('-C',path,'for-each-ref','--format=%(refname)|%(objectname)','refs/heads','refs/tags').splitlines())
    require(refs==row['refs'],'Restored refs differ')
    require(git('-C',path,'rev-parse','--is-shallow-repository')=='false','Main source history is shallow')
    require(not git('-C',path,'status','--porcelain') and not git('-C',path,'remote'),'Source is dirty or has remotes')
    require(not (Path(path)/'.git/objects/info/alternates').exists(),'Source borrows objects through alternates')
    git('-C',path,'fsck','--full','--no-progress','--no-dangling')
    return {'id':row['id'],'type_id':row['type_id'],'head':row['head'],'tree':row['tree'],'full_history':True,'clean':True,'remote_count':0,'execution':'not_run'}

def restore_binding(row):
    # Score/evidence/profile edits do not change the Git material to restore.
    return sha(encoded({k:row[k] for k in ['id','type_id','name','head','tree','refs','publication_status','repository_url']}))

def restore(wrapper,type_id,destination,resume=False,include_submodules=False,source_map=None,ids=None):
    wrapper=Path(wrapper).resolve();registry=validate(wrapper);rows=select(registry,wrapper,type_id,ids)
    destination=Path(destination).resolve();mapping=read(source_map) if source_map else {}
    require(isinstance(mapping,dict),'Source map must map repository IDs to local paths')
    require(destination!=wrapper and not destination.is_relative_to(wrapper) and not wrapper.is_relative_to(destination),'Destination overlaps wrapper')
    # Reject every missing/unpublished input before any clone, network or output mutation.
    transports={}
    for row in rows:
        if row['id'] in mapping:
            origin=Path(mapping[row['id']]).resolve();require((origin/'.git').is_dir(),'Local source is not a repository')
            require(destination!=origin and not destination.is_relative_to(origin) and not origin.is_relative_to(destination),'Destination overlaps a source')
            transports[row['id']]=str(origin)
        else:
            require(row['publication_status']=='published',row['id']+': unpublished source requires --source-map')
            transports[row['id']]=row['repository_url']
    require(not destination.exists() or resume,'Destination exists; use --resume')
    for row in rows:
        advertised={name:oid for oid,name in (line.split() for line in git('ls-remote','--heads','--tags',transports[row['id']]).splitlines()) if not name.endswith('^{}')}
        require(advertised==row['refs'],'Transport refs differ: '+row['id'])
    destination.mkdir(parents=True,exist_ok=True);results=[]
    for row in rows:
        parent=destination/row['type_id'] if type_id in {'all','android-validation18'} else destination
        parent.mkdir(parents=True,exist_ok=True);target=legacy.safe_path(parent,row['name']);marker=parent/('.restore-'+row['id']+'.json');binding=restore_binding(row)
        owned=False
        if marker.exists():
            state=read(marker);require(resume and state.get('phase') in {'cloning','complete'},'Restore progress differs')
            if state.get('binding') not in {binding,sha(encoded(row))}:
                # Legacy complete markers included mutable evidence metadata.
                # Rebind only after verifying the actual full, clean Git source.
                # An unknown in-progress clone retains the strict rejection.
                require(state['phase']=='complete' and target.is_dir(),'Restore progress differs')
                check_source(target,row)
            owned=state['phase']!='complete'
        if not target.exists():
            marker.write_bytes(encoded({'binding':binding,'phase':'cloning'}));git('clone','--no-local','--no-checkout',transports[row['id']],target);owned=True
        elif not resume:raise legacy.InvalidSuite('Target exists')
        if owned:
            require(not git('-C',target,'status','--porcelain') or not any(p.name!='.git' for p in target.iterdir()),'Partial source contains local changes')
            if 'origin' not in git('-C',target,'remote').splitlines():git('-C',target,'remote','add','origin',transports[row['id']])
            git('-C',target,'checkout','--detach',row['head']);git('-C',target,'fetch','origin','refs/heads/*:refs/heads/*','refs/tags/*:refs/tags/*')
            git('-C',target,'remote','remove','origin')
        if include_submodules:
            # Existing complete main repositories still need this requested gate.
            git('-c','protocol.allow=never','-c','protocol.https.allow=always','-C',target,'submodule','update','--init','--recursive','--checkout','--depth','1')
            for line in git('-C',target,'submodule','status','--recursive',binary=True).decode().splitlines():
                require(line.startswith(' '),'Submodule differs from pinned gitlink')
                child=legacy.safe_path(target,line.strip().split()[1])
                require(not git('-C',child,'status','--porcelain'),'Dirty submodule')
                for remote in git('-C',child,'remote').splitlines():git('-C',child,'remote','remove',remote)
        results.append(check_source(target,row));marker.write_bytes(encoded({'binding':binding,'phase':'complete'}))
        (destination/'restore-state.json').write_bytes(encoded({'repository_types':sorted({r['type_id'] for r in results}),'repositories':results,'completed_repositories':len(results),'execution':'not_run'}))
    return results

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for command in ['validate','restore']:
        p=sub.add_parser(command);p.add_argument('--wrapper',type=Path,required=True)
        if command=='validate':p.add_argument('--require-publishable',action='store_true')
        else:
            p.add_argument('--type',choices=[*TYPES,*ALIASES,'all'],required=True);p.add_argument('--destination',type=Path,required=True)
            p.add_argument('--source-map',type=Path);p.add_argument('--ids',nargs='+');p.add_argument('--resume',action='store_true');p.add_argument('--include-submodules',action='store_true')
    args=parser.parse_args()
    try:
        if args.command=='validate':
            registry=validate(args.wrapper,args.require_publishable)
            print(json.dumps({'status':'valid','types':[{k:e[k] for k in ['id','repository_count','leaf_count','score','max_score','published_repositories']} for e in registry['suites']]}))
        else:print(json.dumps(restore(args.wrapper,args.type,args.destination,args.resume,args.include_submodules,args.source_map,args.ids)))
    except (ValueError,KeyError,OSError) as error:print('REJECTED: '+str(error),file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
