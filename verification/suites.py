"""Validate independent benchmark suites and restore only published source suites.

No model, source script, compiler or build is executed. Hash and schema checks
authenticate disclosed bindings, not semantic judgments or execution claims.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

class InvalidSuite(ValueError):pass

def require(value,message):
    if not value:raise InvalidSuite(message)

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')

def safe_path(root,name):
    require(isinstance(name,str) and name and not re.search(r'[:\\]',name),'Unsafe artifact path')
    require(not name.startswith('/') and all(x not in {'','.','..'} for x in name.split('/')),'Unsafe artifact path')
    root=Path(root).resolve();target=(root/name).resolve()
    require(target.is_relative_to(root) and target!=root,'Artifact escapes suite wrapper')
    return target

def bound(root,entry):
    require(isinstance(entry,dict) and set(entry)=={'path','sha256'},'Expected path/SHA-256 binding')
    path=safe_path(root,entry['path'])
    require(isinstance(entry['sha256'],str) and re.fullmatch('[0-9a-f]{64}',entry['sha256']),'Invalid hash')
    require(path.is_file() and sha(path.read_bytes())==entry['sha256'],'Missing or changed artifact: '+entry['path'])
    return path

def integer(value):return type(value) is int and value>=0

def validate_matlab(wrapper,suite):
    require(suite['status'] in {'reviewed_unverified','verified_local','published'},'Invalid MATLAB state')
    manifest=read(bound(wrapper,suite['manifest']))
    contract_path=bound(wrapper,suite['contract']);contract=read(contract_path)
    require(contract['suite_id']==manifest['suite_id']==suite['id']=='matlab-simulink','MATLAB suite identity mismatch')
    require(contract['repo_max_score']==61 and contract['target_leaf_count']==117 and contract['target_repo_count']==9 and
            contract['nominal_max_score']==549 and contract['interpolation'] is False,'MATLAB contract denominator changed')
    require(contract['precedence']==['user_overrides','original_contract','generation_guide'],'MATLAB contract precedence changed')
    for key in ['original','overrides']:bound(contract_path.parent,contract[key])
    leaves=contract['leaves'];allowed={l['id']:l['allowed_scores'] for l in leaves}
    require(len(leaves)==len(allowed)==13 and sum(l['max_score'] for l in leaves)==61,'MATLAB leaf contract mismatch')
    for leaf in leaves:
        require(leaf['allowed_scores']=={3:[0,1,2,3],5:[0,1,3,5],10:[0,3,8,10]}.get(leaf['max_score']),'Unsupported score tiers')
    rows=manifest['repositories'];ids=[r['id'] for r in rows]
    require(set(ids)=={'ML-%02d'%n for n in range(1,10)} and len(ids)==9,'MATLAB source IDs differ')
    require(len({r['name'] for r in rows})==9,'Duplicate MATLAB source name')
    for row in rows:
        require(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',row['name']),'Unsafe repository name')
        require(row['repository_url']=='https://github.com/cockpit-bench/'+row['name']+'.git','Wrong publication target')
        require(row['suite_id']==suite['id'],'Mixed suite source')
        for key in ['head','tree']:require(re.fullmatch('[0-9a-f]{40}',row[key]),'Invalid Git OID')
        require(re.fullmatch('[0-9a-f]{64}',row['files_sha256']),'Invalid source file inventory hash')
        safe_path(wrapper,row['model_path'])
        refs=row['refs'];require(refs and len({x['ref'] for x in refs})==len(refs),'Duplicate/empty source refs')
        for ref in refs:
            require(re.fullmatch(r'refs/(heads|tags)/[^\s\\:]+',ref['ref']) and '..' not in ref['ref'],'Unsafe source ref')
            for key in ['object_oid','commit_oid','tree_oid']:require(re.fullmatch('[0-9a-f]{40}',ref[key]),'Invalid ref OID')
            require(ref['object_type'] in {'tag','commit'},'Invalid ref type')
        require(any(r['commit_oid']==row['head'] and r['tree_oid']==row['tree'] for r in refs),'HEAD absent from frozen refs')
    readiness=read(bound(wrapper,suite['readiness']))
    require(readiness['suite_id']==suite['id'] and readiness['status']==suite['status'],'Readiness state mismatch')
    require(type(readiness['canonical_ready']) is bool and type(readiness['publication_ready']) is bool,'Readiness flags must be boolean')
    required={'ML-%02d'%n for n in range(1,10)}
    native=required|{'ML-02-B','ML-05-B','ML-08-B'}
    require(set(readiness['required_extraction_ids'])==required and len(readiness['required_extraction_ids'])==9,'Required facts changed')
    require(set(readiness['native_required_ids'])==native and len(readiness['native_required_ids'])==12,'Required native configurations changed')
    passed=readiness['native_passed_ids'];complete=readiness['completed_extraction_ids']
    require(len(passed)==len(set(passed)) and set(passed)<=native,'Invalid native passed set')
    require(len(complete)==len(set(complete)) and set(complete)<=required,'Invalid complete extraction set')
    require(set(readiness['blocked_native_ids'])==native-set(passed),'Hidden native execution gap')
    if suite['status']!='reviewed_unverified':
        require(set(passed)==native and set(complete)==required and not readiness['blocked_native_ids'],'Incomplete finalized MATLAB execution')
        require(readiness['canonical_ready'] is True and readiness['canonical_scores']==suite['canonical_scores'],'Canonical binding mismatch')
        require(suite['reviewed_scores'] is None and suite['version'] is not None,'Finalized suite contains review scores')
        require(manifest['status']==suite['status'],'Manifest status mismatch')
        published=suite['status']=='published'
        count=9 if published else 0
        require(suite['published_repositories']==manifest['published_repositories']==readiness['published_repositories']==count,'Publication count differs')
        require(readiness['publication_ready']==published,'Publication readiness differs')
        require(all(r['publication_status']==('published' if published else 'unpublished') for r in rows),'Mixed publication state')
        require(suite['release_url']==('https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/'+suite['version'] if published else None),'Release URL differs')
        if published:
            require(readiness['missing_items']==[],'Published suite has missing items')
            restoration=read(bound(wrapper,readiness['public_restore']))
            require(restoration['suite_id']==suite['id'] and restoration['completed_repositories']==9 and restoration['execution']=='not_run','Missing public restore')
            require(len(restoration['repositories'])==9 and {x['id'] for x in restoration['repositories']}==required,'Incomplete public restore IDs')
            for item in restoration['repositories']:
                source=next(r for r in rows if r['id']==item['id'])
                require(all(item[k]==source[k] for k in ['head','tree','files_sha256']) and item['clean'] is True and item['remote_count']==0 and item['full_history'] is True,'Public restore source mismatch')
        from matlab_evidence import validate_index
        validate_index(wrapper,suite)
        scores=read(bound(wrapper,suite['canonical_scores']))
        require(scores['status']=='local_reference_scores','Unsupported canonical score format')
    else:
        require(not readiness['canonical_ready'] and not readiness['publication_ready'],
            'Unverified MATLAB promoted without completed validation')
        require(suite['canonical_scores'] is None and readiness['canonical_scores'] is None and
            readiness['final_verification'] is None and suite['score'] is None,'Unverified canonical scores present')
        require(suite['published_repositories']==manifest['published_repositories']==readiness['published_repositories']==0,'Unpublished source count changed')
        require(suite['version'] is None and suite['release_url'] is None,'Unpublished MATLAB has release metadata')
        require(readiness['missing_items'] and manifest['status']=='reviewed_unverified','Missing unresolved gate declaration')
        require(all(r['publication_status']=='unpublished' for r in rows),'Mixed MATLAB publication status')
        scores=read(bound(wrapper,suite['reviewed_scores']))
        require(scores['status']=='reviewed_scores_not_final_verified_suite','Wrong review score state')
    require(scores['suite_id']==suite['id'] and scores['leaf_count']==117 and scores['max_score']==549,'MATLAB score denominator mismatch')
    scored=scores['repos'];require(len(scored)==9 and {x['id'] for x in scored}==set(ids),'MATLAB score source set differs')
    for row in scored:
        source=next(x for x in rows if x['id']==row['id'])
        require(source['head']==row['head'],'Stale MATLAB score HEAD')
        require(set(row['scores'])==set(allowed) and row['max_score']==61,'MATLAB score leaves differ')
        require(all(type(value) is int and value in allowed[key] for key,value in row['scores'].items()),'Non-contract MATLAB score')
        require(row['total']==sum(row['scores'].values()),'MATLAB repository total differs')
    require(scores['total']==sum(x['total'] for x in scored),'MATLAB suite total differs')
    if suite['status']=='reviewed_unverified':require(scores['total']==suite['reviewed_score']==readiness['reviewed_total'],'Registry score differs')
    else:require(scores['total']==suite['score'],'Canonical registry score differs')
    return rows

def validate_legacy(wrapper,require_publishable=False,registry=None):
    wrapper=Path(wrapper).resolve();registry=read(wrapper/'suites.json') if registry is None else registry
    require(set(registry)=={'schema_version','benchmark_id','planned_release','integration_status','default_suite','aggregation','suites'},'Unsupported registry keys (no combined score)')
    require(registry['schema_version']=='benchmark-suites-1' and registry['benchmark_id']=='cockpit-benchmark','Wrong registry')
    require(registry['aggregation']=='separate_suite_scores_no_raw_sum','Raw suite totals must remain separate')
    require(registry['default_suite']=='android-validation18','Android default changed')
    require(registry['integration_status'] in {'prepared_not_published','published'} and
            re.fullmatch(r'v\d+\.\d+\.\d+',registry['planned_release']),'Invalid integration version/state')
    suites=registry['suites'];require(len(suites)==2 and {s['id'] for s in suites}=={'android-validation18','matlab-simulink'},'Suite set changed')
    if registry['integration_status']=='published':
        require(all(s['status']=='published' for s in suites),'Published registry contains unfinished suite')
    all_ids=set()
    for suite in suites:
        required={'id','name','status','version','contract','manifest','canonical_scores','reviewed_scores','readiness',
                  'repository_count','leaf_count','max_score','score','published_repositories','restore','release_url'}
        require(required<=set(suite)<=required|{'reviewed_score'},'Unsupported suite keys (no combined score)')
        require(suite['status'] in {'published','reviewed_unverified','verified_local'},'Unsupported suite state')
        require(all(integer(suite[k]) for k in ['repository_count','leaf_count','max_score','published_repositories']),'Invalid denominator')
        if suite['id']=='android-validation18':
            manifest=read(bound(wrapper,suite['manifest']));scores=read(bound(wrapper,suite['canonical_scores']))
            bound(wrapper,suite['contract'])
            rows=[r for r in manifest['repositories'] if r['delivery_status']=='active']
            require(len(rows)==18 and sum(r['delivery_status']=='pending' for r in manifest['repositories'])==22,'Android active/pending set changed')
            require(suite['status']=='published' and suite['published_repositories']==18,'Android published baseline changed')
            require((suite['repository_count'],suite['leaf_count'],suite['max_score'])==(18,171,828),'Android denominator changed')
            require(len(scores['repositories'])==18 and sum(len(r['leaves']) for r in scores['repositories'])==171,'Android score set changed')
            require(sum(l['max_score'] for r in scores['repositories'] for l in r['leaves'])==828,'Android maximum changed')
            require(scores['summary']['score']==suite['score'] and suite['version']==scores['version'],'Android reference differs')
            require(suite['reviewed_scores'] is None and suite['readiness'] is None and suite['restore']=='android','Invalid Android entry')
        else:
            require((suite['repository_count'],suite['leaf_count'],suite['max_score'])==(9,117,549),'MATLAB denominator changed')
            require(suite['restore']=='matlab','Wrong MATLAB restore handler')
            rows=validate_matlab(wrapper,suite)
        ids={r['id'] for r in rows}
        require(len(ids)==suite['repository_count'] and not ids&all_ids,'Duplicate/cross-suite IDs')
        all_ids|=ids
        if require_publishable:require(suite['status']=='published',suite['id']+': not finally validated/published; do not release preparation')
    return registry

def validate(wrapper,require_publishable=False):
    registry=read(Path(wrapper)/'suites.json')
    if registry.get('schema_version')=='benchmark-repository-types-2':
        from repository_types import validate as validate_types
        return validate_types(wrapper,require_publishable)
    return validate_legacy(wrapper,require_publishable,registry)

def legacy_registry(wrapper):
    registry=read(Path(wrapper)/'suites.json')
    if registry.get('schema_version')=='benchmark-repository-types-2':
        return read(bound(wrapper,registry['legacy_baseline']))
    return registry

def git(*args,binary=False):
    env=dict(os.environ,GIT_TERMINAL_PROMPT='0')
    command=['git','-c','credential.helper=','-c','core.askPass=','-c','credential.interactive=false',
             '-c','http.extraHeader=','-c','core.longpaths=true','-c','core.quotePath=false',*map(str,args)]
    result=subprocess.run(command,env=env,check=True,capture_output=True)
    return result.stdout if binary else result.stdout.decode('utf-8').strip()

def check_source(repo,row):
    require(git('-C',repo,'rev-parse','HEAD')==row['head'] and git('-C',repo,'rev-parse','HEAD^{tree}')==row['tree'],'Restored source HEAD/tree differs')
    require(git('-C',repo,'rev-parse','--is-shallow-repository')=='false','Shallow source history')
    require(not git('-C',repo,'remote') and not git('-C',repo,'status','--porcelain'),'Source not clean and remote-free')
    require(not (repo/'.git/objects/info/alternates').exists() and not list((repo/'.git/objects/pack').glob('*.promisor')),'External or incomplete source objects')
    actual={}
    for line in git('-C',repo,'for-each-ref','--format=%(refname)|%(objectname)|%(objecttype)','refs/heads','refs/tags').splitlines():
        name,oid,kind=line.split('|');actual[name]=(oid,kind)
    require(actual=={r['ref']:(r['object_oid'],r['object_type']) for r in row['refs']},'Restored refs differ')
    for ref in row['refs']:
        require(git('-C',repo,'rev-parse',ref['ref']+'^{commit}')==ref['commit_oid'] and
                git('-C',repo,'rev-parse',ref['ref']+'^{tree}')==ref['tree_oid'],'Restored peeled ref differs')
    files=[]
    for line in git('-C',repo,'ls-tree','-rz','--full-tree','HEAD',binary=True).split(b'\0'):
        if not line:continue
        meta,name=line.split(b'\t',1);mode,kind,oid=meta.decode().split()
        require(kind=='blob','Unexpected submodule in MATLAB source')
        body=git('-C',repo,'cat-file','blob',oid,binary=True)
        files.append(dict(path=name.decode(),mode=mode,blob=oid,bytes=len(body),sha256=sha(body)))
    inventory=sha(json.dumps(files,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
    require(inventory==row['files_sha256'],'Restored file inventory differs')
    git('-C',repo,'fsck','--full','--no-progress','--no-dangling')
    return dict(id=row['id'],head=row['head'],tree=row['tree'],files_sha256=inventory,
                clean=True,remote_count=0,full_history=True,model_execution=False)

def restore_matlab(rows,destination,resume=False):
    require(not destination.exists() or (resume and destination.is_dir()),'Destination exists; use --resume to verify existing sources')
    # Check all advertised refs before any filesystem creation.
    for row in rows:
        advertised={name:oid for oid,name in (line.split() for line in git('ls-remote','--heads','--tags',row['repository_url']).splitlines()) if not name.endswith('^{}')}
        require(advertised=={r['ref']:r['object_oid'] for r in row['refs']},'Published source refs differ: '+row['id'])
    destination.mkdir(parents=True,exist_ok=True);results=[]
    for row in rows:
        target=safe_path(destination,row['name'])
        progress=safe_path(destination,'.restore-'+row['id']+'.json')
        expected=sha(encoded(row));owned=False
        if progress.exists():
            state=read(progress)
            require(resume and state.get('source_binding')==expected and state.get('name')==row['name'],
                    'Restore progress does not match this source')
            owned=state.get('phase') in {'cloning','cloned','checked_out'}
        if not target.exists():
            progress.write_bytes(encoded(dict(source_binding=expected,name=row['name'],phase='cloning')))
            git('clone','--no-checkout',row['repository_url'],target)
            progress.write_bytes(encoded(dict(source_binding=expected,name=row['name'],phase='cloned')))
            owned=True
        else:require(resume and (target/'.git').is_dir(),'Existing source is not a completed repository')
        if owned:
            # Only resume this invocation's recorded partial clone. Do not force
            # checkout, discard edits, or rewrite unrelated existing refs.
            remotes=git('-C',target,'remote').splitlines()
            if remotes:
                require(remotes==['origin'] and git('-C',target,'remote','get-url','origin')==row['repository_url'],
                        'Partial clone remote differs')
                state=read(progress)
                if state['phase'] in {'cloning','cloned'}:
                    contents=[p for p in target.iterdir() if p.name!='.git']
                    require(not contents or (git('-C',target,'rev-parse','HEAD')==row['head'] and
                            not git('-C',target,'status','--porcelain')),'Partial clone contains user changes')
                    git('-C',target,'checkout','--detach',row['head'])
                    progress.write_bytes(encoded(dict(source_binding=expected,name=row['name'],phase='checked_out')))
                require(git('-C',target,'rev-parse','HEAD')==row['head'] and not git('-C',target,'status','--porcelain'),
                        'Partial source has changed; refusing to overwrite it')
                allowed={r['ref']:r['object_oid'] for r in row['refs']}
                present=[line.split('|') for line in git('-C',target,'for-each-ref','--format=%(refname)|%(objectname)','refs/heads','refs/tags').splitlines()]
                require(all(allowed.get(name)==oid for name,oid in present),'Partial source contains unrelated refs')
                git('-C',target,'fetch','origin','refs/heads/*:refs/heads/*','refs/tags/*:refs/tags/*')
                git('-C',target,'remote','remove','origin')
        results.append(check_source(target,row))
        progress.write_bytes(encoded(dict(source_binding=expected,name=row['name'],phase='complete')))
        (destination/'restore-state.json').write_bytes(encoded(dict(suite_id='matlab-simulink',repositories=results,
            completed_repositories=len(results),execution='not_run')))
    return results

def restore(wrapper,suite_id,destination,resume=False,include_submodules=False,source_map=None,ids=None):
    wrapper=Path(wrapper).resolve();registry=validate(wrapper)
    if registry.get('schema_version')=='benchmark-repository-types-2':
        from repository_types import restore as restore_types
        return restore_types(wrapper,suite_id,destination,resume,include_submodules,source_map,ids)
    selected=[s for s in registry['suites'] if suite_id=='all' or s['id']==suite_id]
    require(selected,'Unknown suite')
    for suite in selected:
        require(suite['status']=='published' and suite['published_repositories']==suite['repository_count'],
                suite['id']+': final verification/publication incomplete; no sources downloaded')
    destination=Path(destination).resolve()
    require(destination!=wrapper and not destination.is_relative_to(wrapper) and not wrapper.is_relative_to(destination),
            'Destination must be separate from the wrapper and its parents')
    for suite in selected:
        target=destination/suite['id'] if suite_id=='all' else destination
        if suite['restore']=='android':
            shell=shutil.which('pwsh') or shutil.which('powershell')
            require(shell,'PowerShell is required for Android restore')
            command=[shell,'-NoProfile','-File',str(wrapper/'restore.ps1'),'-Destination',str(target)]
            if resume:command.append('-Resume')
            if include_submodules:command.append('-IncludeSubmodules')
            subprocess.run(command,check=True)
        else:restore_matlab(read(bound(wrapper,suite['manifest']))['repositories'],target,resume)

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    check=sub.add_parser('validate');check.add_argument('--wrapper',type=Path,required=True)
    check.add_argument('--require-publishable',action='store_true')
    fetch=sub.add_parser('restore');fetch.add_argument('--wrapper',type=Path,required=True)
    fetch.add_argument('--suite',choices=['app','fw','new-energy-matlab','android-validation18','matlab-simulink','all'],required=True)
    fetch.add_argument('--destination',type=Path,required=True);fetch.add_argument('--resume',action='store_true')
    fetch.add_argument('--include-submodules',action='store_true')
    fetch.add_argument('--source-map',type=Path);fetch.add_argument('--ids',nargs='+')
    args=parser.parse_args()
    try:
        if args.command=='validate':
            registry=validate(args.wrapper,args.require_publishable)
            print(json.dumps({'status':'valid_registry','integration_status':registry['integration_status'],
                'suites':[{'id':s['id'],'state':s['status'],'leaves':s['leaf_count'],'max_score':s['max_score']} for s in registry['suites']]}))
        else:restore(args.wrapper,args.suite,args.destination,args.resume,args.include_submodules,args.source_map,args.ids)
    except (InvalidSuite,KeyError,ValueError,OSError,subprocess.CalledProcessError) as exc:
        print('REJECTED: '+str(exc),file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
