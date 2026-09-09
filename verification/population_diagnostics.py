"""Descriptive source-group, missing-band and association diagnostics.

No score, family or split is changed. Independence of unknown construction
history and representativeness of internal repositories cannot be inferred.
"""
from collections import Counter,defaultdict
from itertools import combinations
from statistics import median


def size_associations(leaves,components,sizes):
    """Observed size support for each score band, never a representativeness claim."""
    ids={r['repository_id'] for r in leaves}
    if set(sizes)!=ids or any(type(v['source_loc']) is not int or v['source_loc']<0 for v in sizes.values()):
        raise ValueError('Complete measured source sizes are required')
    groups={rid:i for i,c in enumerate(components) for rid in c if rid in ids}
    if set(groups)!=ids:raise ValueError('Size population has incomplete lineage')
    bands={}
    for row in leaves:
        for value in row['allowed_scores']:bands.setdefault((row['name'],value),[])
        if row['score'] is not None:bands[(row['name'],row['score'])].append(row['repository_id'])
    result=[]
    for (leaf,score),members in sorted(bands.items()):
        values=[sizes[r]['source_loc'] for r in members]
        group_count=len({groups[r] for r in members})
        result.append({'leaf':leaf,'score':score,'repositories':sorted(members),
                       'source_groups':group_count,'size_bands':dict(Counter(sizes[r]['size_band'] for r in members)),
                       'source_loc_min':min(values) if values else None,
                       'source_loc_median':median(values) if values else None,
                       'source_loc_max':max(values) if values else None,
                       'support':'unmeasured' if not members else 'one_source_group_only' if group_count==1 else 'multiple_recorded_groups',
                       'generalization':'not_established'})
    return {'schema':'android-size-band-support-v1','metric':'production_source_loc',
            'sources':sizes,'bands':result,
            'limits':'Descriptive conditional sizes; no internal joint-frequency data, independent sample guarantee or generalization accuracy. A represented band is not a completed coverage claim.'}


def analyze(leaves,components):
    by_repo=defaultdict(dict);allowed={}
    for row in leaves:
        name=row['name'];score=row['score'];tiers=row['allowed_scores']
        if score is not None and score not in tiers:raise ValueError('Illegal observation; do not impute')
        if name in by_repo[row['repository_id']]:raise ValueError('Duplicate population leaf')
        by_repo[row['repository_id']][name]=score
        if name in allowed and allowed[name]!=tiers:raise ValueError('Population contracts differ')
        allowed[name]=tiers
    if not by_repo or any(set(r)!=set(allowed) for r in by_repo.values()):raise ValueError('Incomplete population')
    ids=set(by_repo);groups=[sorted(ids.intersection(c)) for c in components if ids.intersection(c)]
    flattened=[r for g in groups for r in g]
    if set(flattened)!=ids or len(flattened)!=len(ids):raise ValueError('Lineage components do not partition this population')
    bands=[];constant=[];mode_hits=0
    for name,tiers in sorted(allowed.items()):
        counts=Counter(r[name] for r in by_repo.values() if r[name] is not None);mode_hits+=max(counts.values(),default=0)
        if len(counts)==1:constant.append(name)
        for score in tiers:
            members=sorted(rid for rid,row in by_repo.items() if row[name]==score)
            bands.append({'leaf':name,'score':score,'count':len(members),'repository_ids':members,
                          'measurement_status':'represented' if members else 'unmeasured'})
    associations=[]
    for left,right in combinations(sorted(allowed),2):
        if left in constant or right in constant:continue
        pairs=Counter((r[left],r[right]) for r in by_repo.values() if r[left] is not None and r[right] is not None)
        if not pairs:continue
        forward=defaultdict(set);reverse=defaultdict(set)
        for a,b in pairs:forward[a].add(b);reverse[b].add(a)
        if all(len(s)==1 for s in forward.values()) and all(len(s)==1 for s in reverse.values()):
            associations.append({'left':left,'right':right,'pairs':[{'left':a,'right':b,'count':n} for (a,b),n in sorted(pairs.items())],
                'status':'bidirectional_deterministic_in_sample','limits':'Observed categorical association, not causality or candidate accuracy.'})
    shortcuts=[]
    for predictor in sorted(allowed):
        if predictor in constant:continue
        hits=0;denominator=0
        for target in sorted(set(allowed)-{predictor}):
            grouped=defaultdict(Counter)
            for r in by_repo.values():
                if r[predictor] is not None and r[target] is not None:grouped[r[predictor]][r[target]]+=1
            hits+=sum(max(c.values()) for c in grouped.values());denominator+=sum(sum(c.values()) for c in grouped.values())
        shortcuts.append({'predictor':predictor,'other_leaf_hits':hits,'other_leaf_denominator':denominator,
                          'method':'Post-hoc conditional modes fitted and counted on the same repositories; not an experiment.'})
    return {'schema':'population-diagnostics-v1','repository_count':len(ids),'leaf_count':len(leaves),
            'observed_band_cells':sum(b['count']>0 for b in bands),'legal_band_cells':len(bands),'bands':bands,
            'unresolved_reference_leaves':sorted(r['repository_id']+'/'+r['name'] for r in leaves if r['score'] is None),
            'constant_leaves':constant,'modal_baseline':{'hits':mode_hits,'denominator':sum(r['score'] is not None for r in leaves),'status':'in_sample_only'},
            'source_groups':groups,'source_group_count':len(groups),
            'independent_holdout':{'status':'structurally_unavailable' if len(groups)<2 else 'not_certified',
                'reason':'All repositories are in one recorded source/dependency/construction closure.' if len(groups)<2 else 'Multiple recorded groups alone do not prove unexposed construction or independent adjudication.'},
            'deterministic_associations':associations,'conditional_mode_diagnostics':shortcuts,
            'limits':['Missing bands remain unmeasured; no scores or samples are manufactured to fill cells.',
                      'Original per-repository internal scans are unavailable; no representativeness certification.',
                      'Public current references remain Development/Regression, not a blind holdout.']}
