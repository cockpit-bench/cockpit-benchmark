"""Current three-type evaluation. Maintainer-side registration; never candidate input.

Assignments cover all current sources so cross-type lineage cannot cross splits.
The runner still owns process/network isolation and registration timing.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import zipfile

import evaluation_profile as ep
import evaluation_batch as legacy
import repository_types as rt
from coverage import TIERS
from external_inputs import verify as verify_git


def lineage(sources, assignments):
    entries={r['id']:r for r in sources}
    if set(assignments)!=set(entries) or any(not isinstance(v,str) or not v.strip() for v in assignments.values()):
        raise ValueError('Assignments must cover all 33 current sources, including other types')
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
        if len(names)!=len(set(names)) or sum(i.file_size for i in z.infolist())>64*1024*1024:raise ValueError('Duplicate/oversized raw packet')
        for name in names:
            if ':' in name or chr(92) in name or name.startswith('/') or any(p in {'','..','.'} for p in name.split('/')):raise ValueError('Unsafe raw path')
        index=json.loads(z.read('packet-index.json'))
        if index['schema']!='candidate-raw-inputs-v1':raise ValueError('Raw schema differs')
        if set(names)!={'packet-index.json'}|{r['path'] for r in index['files']}:raise ValueError('Undeclared raw files')
        for row in index['files']:
            body=z.read(row['path'])
            if len(body)!=row['bytes'] or rt.sha(body)!=row['sha256']:raise ValueError('Raw file differs')
    return {'sha256':spec['sha256'],'files':len(index['files'])}


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
    target.mkdir(parents=True)
    for name,body in selected.items():
        p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
    return {'repository_id':repository_id,'files':len(selected),'source_packet_sha256':spec['sha256']}


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
    availability={'leaves':rows};registered=ep.register(availability,mode,context)
    if profile is None:profile=registered
    else:
        ep.validate_profile(profile)
        if profile['context']!=context or profile['mode']!=mode or profile['requested']!=registered['requested'] or not set(profile['eligible'])<=set(registered['eligible']):raise ValueError('Common profile differs from current inputs')
    checks={}
    needed={r['packet_id'] for r in rows if r['id'] in profile['eligible'] and mode=='frozen_external' and r.get('packet_id')}
    if needed and external_inputs is None:raise ValueError('Frozen batch requires actual raw packets before registration')
    for pid in sorted(needed):
        spec=inventory['packets'][pid];checks[pid]=packet_check(Path(external_inputs)/spec['name'],spec)
    refs=rt.read(rt.bound(wrapper,entry['canonical_scores']))['repositories'];leaves=[]
    byid={r['id']:r for r in sources}
    for row in refs:
        for name,(score,maximum) in rt.leaf_values(row['reference']).items():
            allowed=TIERS[name] if type_id!='new-energy-matlab' else {3:[0,1,2,3],5:[0,1,3,5],10:[0,3,8,10]}[maximum]
            leaves.append({'id':row['id']+'/'+name,'repository_id':row['id'],'name':name,'score':score,'kind':type_id,'allowed_scores':allowed,'split':assignments[row['id']],'family_id':byid[row['id']]['family_id']})
    if set(ep.indexed(leaves))!=set(profile['requested']):raise ValueError('Current reference/availability universe differs')
    batch={'schema':'evaluation-batch-v2','profile':profile,'reference':{'context':context,'leaves':leaves},'assignments':assignments,'lineage_check':split,'external_packet_check':checks,'limits':'One business type per batch; source eligibility is independent of gold score. No OS isolation or blind-review claim.'}
    batch['batch_sha256']=ep.digest(batch)
    return batch


def assess(batch,candidate,plan=None,adjudications=None):
    result=legacy.assess(batch,candidate,plan,adjudications)
    predictions=ep.indexed(candidate['leaves']);groups=defaultdict(list)
    for row in batch['reference']['leaves']:
        if row['id'] in batch['profile']['eligible']:groups[(row['name'],row['score'])].append(row)
    bands=[]
    for (name,score),rows in sorted(groups.items()):
        confusion=Counter()
        for row in rows:
            p=predictions.get(row['id'],{});label=str(p['score']) if p.get('status')=='scored' else p.get('status','missing');confusion[label]+=1
        bands.append({'leaf':name,'gold':score,'count':len(rows),'recall':confusion[str(score)]/len(rows),'predictions':dict(confusion)})
    result['band_recall_and_confusion']=bands
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
