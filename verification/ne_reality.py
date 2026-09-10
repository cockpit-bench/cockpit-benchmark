"""New Energy reality cohort: separate contract, full-history restore and fixed-set evaluation.

Replay verifies source identity, deterministic census and manually adjudicated references.
It does not independently re-judge software semantics or run candidate models.
"""
import argparse, collections, hashlib, json, math, shutil, subprocess, tempfile
from pathlib import Path
import ne_reality_census as census
import ne_reality_restore as bundle_restore

COHORT='reality-proxy-20260910'
def require(value,message):
    if not value:raise ValueError(message)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):Path(p).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def safe(root,path):
    require(isinstance(path,str) and path and not Path(path).is_absolute() and ':' not in path and '\\' not in path and all(p not in {'','.','..'} for p in path.split('/')),'Unsafe relative path')
    result=(Path(root)/path).resolve();require(result.is_relative_to(Path(root).resolve()),'Escaping path');return result
def bound(root,binding):
    result=safe(root,binding['path']);require(sha(result)==binding['sha256'],'Artifact digest mismatch: '+binding['path']);return result
def location(wrapper):return Path(wrapper)/'suites/new-energy-matlab/cohorts'/COHORT

def load(wrapper):
    root=location(wrapper);contract=read(root/'contract-index.json');manifest=read(root/'manifest.json');gold=read(root/'STANDARD_SCORES.json');observations=read(root/'OBSERVATIONS.json')
    require(contract['cohort_id']==manifest['cohort_id']==gold['cohort_id']==COHORT,'Cohort mismatch')
    require(contract['repository_type']==manifest['repository_type']==gold['type_id']=='new-energy-matlab','Wrong business type')
    for binding in contract['authorities']:bound(root,binding)
    require(gold['contract_sha256']==sha(root/'contract-index.json'),'Stale contract binding')
    leaves={r['id']:r for r in contract['leaves']};require(len(leaves)==13 and sum(x['max_score'] for x in leaves.values())==61,'Wrong contract denominator')
    sources={x['id']:x for x in manifest['repositories']};refs={x['id']:x for x in gold['repositories']};obs={x['id']:x for x in observations['repositories']}
    require(len(sources)==len(manifest['repositories'])==len(gold['repositories'])==len(observations['repositories'])==11,'Duplicate/wrong repository count')
    require(set(sources)==set(refs)==set(obs)=={f'NEP-{i:02d}' for i in range(1,12)},'Wrong frozen repository set')
    for rid,source in sources.items():
        require(source.get('publication_status') in {'local-only','published'},'Invalid publication state')
        if source['publication_status']=='published':bundle_restore.public_source_url(source)
        ref=refs[rid]['reference'];require(refs[rid]['head']==ref['head']==obs[rid]['head']==source['head'],'Stale source/reference binding')
        require(refs[rid]['name']==ref['name']==source['name'],'Name mismatch')
        require(set(ref['scores'])==set(ref['leaves'])==set(leaves),'Missing/extra reference leaf')
        require(ref['total']==sum(ref['scores'].values()) and ref['max_score']==61,'Wrong reference sum')
        for key,value in ref['scores'].items():
            require(isinstance(value,(int,float)) and not isinstance(value,bool) and value in leaves[key]['allowed_scores'],'Illegal tier')
            detail=ref['leaves'][key];require(detail['score']==value and detail['max_score']==leaves[key]['max_score'] and detail['status']=='supported','Reference detail differs')
            require(bool(detail['reason'].strip()) and bool(detail['evidence']),'Missing semantic adjudication')
            for e in detail['evidence']:
                if e['path']=='git:refs/heads':require(e['head']==source['head'] and e['refs']=={k:v for k,v in source['refs'].items() if k.startswith('refs/heads/')},'Stale Git evidence')
                else:require(e['path'] in source['files'] and e['sha256']==source['files'][e['path']],'Unbound leaf evidence')
        for path in source['files']:safe(root,path)
        safe(root,source['bundle']['path'])
    require(gold['leaf_count']==143 and gold['max_score']==671 and gold['total']==sum(x['reference']['total'] for x in refs.values()),'Wrong cohort sum')
    return root,contract,manifest,gold,observations

def validate_catalog(wrapper,path=None):
    wrapper=Path(wrapper);catalog=read(path or wrapper/'suites/new-energy-matlab/cohorts.json')
    require(catalog['repository_type']=='new-energy-matlab' and catalog['default_analysis_cohort']==COHORT,'Wrong cohort routing')
    require([x['id'] for x in catalog['cohorts']]==[COHORT],'Only the current reality cohort is admitted')
    for entry in catalog['cohorts']:
        for key in ['manifest','canonical_scores','contract']:bound(wrapper,entry[key])
    _,_,manifest,_,_=load(wrapper)
    current=next(c for c in catalog['cohorts'] if c['id']==COHORT)
    if current['status']=='published':require(all(s['publication_status']=='published' for s in manifest['repositories']),'Published cohort contains a local source')
    return {'cohorts':1,'repository_type':'new-energy-matlab','new_cohort_repositories':11,'new_cohort_leaves':143}

def check_split(wrapper,assignments):
    _,_,manifest,_,_=load(wrapper);ids={r['id'] for r in manifest['repositories']}
    require(set(assignments)==ids,'Assignments must cover exactly this cohort')
    require(all(isinstance(v,str) and v.strip() for v in assignments.values()),'Invalid split label')
    require(len(set(assignments.values()))==1,'One construction family cannot cross train/test splits')
    return {'components':[sorted(ids)],'independent_holdout':False}

def replay(wrapper,source_root):
    _,_,manifest,gold,observations=load(wrapper);result=census.scan(manifest,source_root);obs={r['id']:r for r in observations['repositories']}
    for row in result['repositories']:
        digest=hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        require(digest==obs[row['id']]['census_sha256'],'Census differs: '+row['id'])
    return {'cohort_id':COHORT,'repositories':11,'leaves':143,'total':gold['total'],'max_score':671,'census_verified':True,
            'score_semantics':'Replays maintainer adjudications after source+census checks; not independent semantic scoring or new native execution.'}

def restore(wrapper,bundle_root,destination,receipt):
    _,_,manifest,_,_=load(wrapper)
    if bundle_root is None:
        result=bundle_restore.restore_public(manifest,destination);write(receipt,result);return result
    bundles=Path(bundle_root)
    # Bundle manifest must have precisely the admitted Git/file identities.
    supplied=read(bundles/'sources.json')
    for source in supplied['repositories']:source.pop('source_path',None)
    # Publication metadata may advance while the admitted source/bundle identity stays fixed.
    for value in (supplied,manifest):
        value.pop('status',None)
        for source in value['repositories']:
            for key in ['publication_status','repository_url']:source.pop(key,None)
    require(supplied==manifest,'Bundle manifest differs from admitted cohort')
    result=bundle_restore.restore(bundles/'sources.json',destination);write(receipt,result);return result

def evaluate(wrapper,predictions):
    _,contract,manifest,gold,_=load(wrapper);leaves={l['id']:l for l in contract['leaves']};refs={r['id']:r['reference'] for r in gold['repositories']}
    require(predictions.get('cohort_id')==COHORT and predictions.get('contract_sha256')==gold['contract_sha256'],'Wrong cohort or contract')
    rows=predictions['repositories'];require(len(rows)==len(refs) and {x['id'] for x in rows}==set(refs),'Predictions must cover fixed 11-repository set exactly')
    stats={key:{'eligible':11,'answered':0,'correct':0,'absolute_error':0,'confusion':collections.Counter(),'evidence_submitted':0} for key in leaves}
    for row in rows:
        ref=refs[row['id']];require(row.get('head')==ref['head'],'Stale candidate source HEAD')
        require(set(row['scores'])==set(leaves),'Missing/extra candidate leaf')
        evidence=row.get('evidence',{});require(isinstance(evidence,dict) and set(evidence)<=set(leaves),'Invalid candidate evidence keys')
        for key,predicted in row['scores'].items():
            s=stats[key];truth=ref['scores'][key]
            if predicted is None:s['confusion'][f'{truth}:abstain']+=1;continue
            require(isinstance(predicted,(int,float)) and not isinstance(predicted,bool) and math.isfinite(predicted) and predicted in leaves[key]['allowed_scores'],'Illegal candidate tier')
            predicted=int(predicted);s['answered']+=1;s['correct']+=int(predicted==truth);s['absolute_error']+=abs(predicted-truth);s['confusion'][f'{truth}:{predicted}']+=1
            s['evidence_submitted']+=int(bool(evidence.get(key)))
    for key,s in stats.items():
        s['accuracy_fixed_set']=s['correct']/11;s['answer_rate']=s['answered']/11;s['mae_answered']=s['absolute_error']/s['answered'] if s['answered'] else None
        s['confusion']=dict(sorted(s['confusion'].items()))
    return {'cohort_id':COHORT,'type_id':'new-energy-matlab','eligible_leaves':143,'leaf_metrics':stats,
            'macro_accuracy':sum(s['accuracy_fixed_set'] for s in stats.values())/13,
            'evidence_status':'Presence is counted only; semantic evidence correctness requires human review.',
            'independence':'One construction family. No within-cohort train/test split or independent holdout claim.'}

def candidate(wrapper,bundle_root,rid,output,source_root=None):
    root,contract,manifest,_,_=load(wrapper);source=next((s for s in manifest['repositories'] if s['id']==rid),None);require(source is not None,'Unknown repository')
    out=Path(output);require(not out.exists(),'Candidate output already exists')
    if bundle_root is not None:
        bundle=Path(bundle_root)/source['bundle']['path'];require(sha(bundle)==source['bundle']['sha256'],'Bad candidate bundle')
        out.mkdir(parents=True);shutil.copy2(bundle,out/bundle.name)
    else:
        require(source_root is not None,'Provide --source-root with restored public sources, or --bundle-root')
        repo=census.source_path(source_root,source);bundle_restore.verify_repository(repo,source)
        out.mkdir(parents=True);bundle=out/Path(source['bundle']['path']).name
        bundle_restore.git(repo,'bundle','create',str(bundle.resolve()),'--all')
    for e in contract['authorities']:shutil.copy2(bound(root,e),out/e['path'])
    shutil.copy2(root/'contract-index.json',out/'contract-index.json')
    bindings={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in out.iterdir() if p.is_file()}
    write(out/'candidate-input.json',{'id':rid,'name':source['name'],'head':source['head'],'tree':source['tree'],
          'cohort_id':COHORT,'source_bundle':bundle.name,'contract_sha256':sha(root/'contract-index.json'),'files':bindings,
          'instructions':'Restore only this complete Git bundle. Use repository-owned source and artifacts with the effective contract. Do not access the maintainer wrapper, other candidates, references or observations.'})
    return {'id':rid,'files':len(bindings)+1,'output':str(out),'gold_exported':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['validate','replay','restore','evaluate','candidate'])
    p.add_argument('--wrapper',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--source-root');p.add_argument('--bundle-root');p.add_argument('--destination');p.add_argument('--id');p.add_argument('--input');p.add_argument('--output');args=p.parse_args()
    if args.command=='validate':result=validate_catalog(args.wrapper)
    elif args.command=='replay':result=replay(args.wrapper,args.source_root)
    elif args.command=='restore':result=restore(args.wrapper,args.bundle_root,args.destination,args.output)
    elif args.command=='evaluate':result=evaluate(args.wrapper,read(args.input))
    else:result=candidate(args.wrapper,args.bundle_root,args.id,args.output,args.source_root)
    if args.output and args.command not in {'candidate','restore'}:write(args.output,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
