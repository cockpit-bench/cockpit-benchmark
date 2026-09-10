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

def validate_legacy(wrapper,require_publishable=False,registry=None):
    wrapper=Path(wrapper).resolve();registry=read(wrapper/'suites.json') if registry is None else registry
    require(set(registry)=={'schema_version','benchmark_id','planned_release','integration_status','default_suite','aggregation','suites'},'Unsupported registry keys (no combined score)')
    require(registry['schema_version']=='benchmark-suites-1' and registry['benchmark_id']=='cockpit-benchmark','Wrong registry')
    require(registry['aggregation']=='separate_suite_scores_no_raw_sum','Raw suite totals must remain separate')
    require(registry['default_suite']=='android-validation18','Android default changed')
    require(registry['integration_status'] in {'prepared_not_published','published'} and
            re.fullmatch(r'v\d+\.\d+\.\d+',registry['planned_release']),'Invalid integration version/state')
    suites=registry['suites'];require(len(suites)==1 and {s['id'] for s in suites}=={'android-validation18'},'Suite set changed')
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

def restore(wrapper,suite_id,destination,resume=False,include_submodules=False,source_map=None,ids=None):
    wrapper=Path(wrapper).resolve();registry=validate(wrapper)
    if registry.get('schema_version')=='benchmark-repository-types-2':
        from repository_types import restore as restore_types
        return restore_types(wrapper,suite_id,destination,resume,include_submodules,source_map,ids)
    raise InvalidSuite('Legacy restoration is retired; use the current repository-type registry')

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
