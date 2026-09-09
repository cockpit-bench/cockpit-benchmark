"""Explicit current-reference corrections without rewriting the frozen legacy set.

Checks bind the before/after objects, contract, source and changed leaves. Rule
replay uses disclosed observations; it does not certify their semantic truth.
"""
import argparse
import copy
from pathlib import Path

import rules
from suites import bound, encoded, git, read, require, sha
from verify import json_pointer


def validate(wrapper, row, baseline, source, contract_sha256):
    revision=read(bound(wrapper,row['reference_revision']))
    current=row['reference']
    require(revision['schema']=='current-reference-revision-v1','Unknown reference revision schema')
    require((revision['repository_id'],revision['head'],revision['tree'])==
            (source['id'],source['head'],source['tree']),'Reference revision source differs')
    require(revision['contract_sha256']==contract_sha256,'Reference revision contract differs')
    require(revision['baseline_reference_sha256']==sha(encoded(baseline)),
            'Reference revision baseline differs')
    require(revision['current_reference_sha256']==sha(encoded(current)),
            'Reference revision result differs')
    require(set(current)==set(baseline),'Reference revision changed object fields')
    require(all(current[k]==baseline[k] for k in baseline if k not in {'leaves','total'}),
            'Reference revision changed unrelated metadata')
    before={l['name']:l for l in baseline['leaves']}
    after={l['name']:l for l in current['leaves']}
    require(len(before)==len(baseline['leaves']) and len(after)==len(current['leaves'])
            and before.keys()==after.keys(),'Reference revision changed leaf universe')
    changed={name for name in before if before[name]!=after[name]}
    items=revision['changes'];declared={c['leaf'] for c in items}
    require(changed and changed==declared and len(items)==len(declared),
            'Undeclared or duplicate reference revision')
    for item in items:
        name=item['leaf'];old=before[name];new=after[name]
        require(item['before_sha256']==sha(encoded(old)) and
                item['after_sha256']==sha(encoded(new)),'Revised leaf binding differs')
        require(isinstance(item.get('reason'),str) and item['reason'].strip(),
                'Reference revision needs an explicit reason')
        require(old['max_score']==new['max_score'] and new['status']=='scored',
                'Reference revision changed contract or has no adjudication')
        if old['score']!=new['score']:
            require(name in rules.RULES and isinstance(item.get('rule_inputs'),dict),
                    'Changed score needs independently replayable observations')
            require(rules.RULES[name](item['rule_inputs'])==new['score'],
                    'Revised score differs from rule replay')
        for anchor in new['evidence']:
            require(anchor['commit']==source['head'],'Revised evidence HEAD differs')
            if anchor['source']=='current_reference_revision':
                path=bound(wrapper,{'path':anchor['path'],'sha256':anchor['source_sha256']})
                require(json_pointer(read(path),anchor['json_pointer']) is not None,
                        'Revised evidence pointer has no value')
    total=copy.deepcopy(baseline['total'])
    total['score']=sum(l['score'] for l in after.values())
    require(current['total']==total,'Reference revision total differs')
    return revision


def verify(wrapper,source_map):
    import repository_types as rt
    wrapper=Path(wrapper);registry=rt.validate(wrapper);mapping=read(source_map)
    sources={r['id']:r for r in rt.select(registry,wrapper,'all')};results=[]
    for entry in registry['suites']:
        for row in read(bound(wrapper,entry['canonical_scores']))['repositories']:
            if 'reference_revision' not in row:continue
            source=sources[row['id']];repo=Path(mapping[row['id']])
            require(git('-C',repo,'rev-parse','HEAD')==source['head'],'Revised source HEAD drift')
            require(not git('-C',repo,'status','--porcelain'),'Revised source is dirty')
            revision=read(bound(wrapper,row['reference_revision']))
            changed={c['leaf'] for c in revision['changes']};checked=[]
            for leaf in row['reference']['leaves']:
                if leaf['name'] not in changed:continue
                for a in leaf['evidence']:
                    if a['source']!='repository':continue
                    body=git('-C',repo,'show',source['head']+':'+a['path'],binary=True)
                    require(sha(body)==a['source_sha256'],'Revised source evidence bytes differ')
                    lines=body.decode('utf-8-sig').splitlines()
                    require(1<=a['start_line']<=a['end_line']<=len(lines),'Revised source span invalid')
                    require(a['symbol'] in '\n'.join(lines[a['start_line']-1:a['end_line']]),
                            'Revised source symbol missing')
                    checked.append({'path':a['path'],'sha256':sha(body)})
            if revision.get('execution_rebinding'):
                binding=read(bound(wrapper,revision['execution_rebinding']))['rebinding']
                original=binding['original_report']
                report=json_pointer(read(wrapper/original['container_path']),original['json_pointer'])
                require(sha(encoded(report))==original['canonical_json_sha256'],
                        'Embedded original execution report changed')
                require(report['head']==binding['executed_head'] and binding['current_head']==source['head'],
                        'Execution rebinding revisions differ')
                recorded=report['production_compile_inputs']+report['build_inputs']+report['test_inputs']
                require(binding['inputs']==[{'path':r['path'],'blob':r['blob'],'sha256':r['sha256']} for r in recorded],
                        'Execution rebinding scope differs from original inputs')
                for item in binding['inputs']:
                    old=git('-C',repo,'show',binding['executed_head']+':'+item['path'],binary=True)
                    new=git('-C',repo,'show',source['head']+':'+item['path'],binary=True)
                    require(old==new and sha(new)==item['sha256'],
                            'Execution input changed since the actual run: '+item['path'])
                    require(git('-C',repo,'rev-parse',source['head']+':'+item['path'])==item['blob'],
                            'Execution input Git blob differs')
            results.append({'id':row['id'],'head':source['head'],'changed_leaves':sorted(changed),
                            'source_anchors':checked,'execution_rebinding_checked':bool(revision.get('execution_rebinding'))})
    return {'status':'passed','revisions':results,'limits':'Source/leaf binding and rule replay; no new build or blind semantic review.'}


if __name__=='__main__':
    import json
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--wrapper',type=Path,required=True);p.add_argument('--source-map',type=Path,required=True)
    p.add_argument('--output',type=Path)
    a=p.parse_args();result=verify(a.wrapper,a.source_map)
    if a.output:a.output.write_bytes(encoded(result))
    print(json.dumps(result,ensure_ascii=False))
