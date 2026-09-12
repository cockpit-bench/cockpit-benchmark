"""Source-bound references for the three center groups added in v0.12.0.

Restoring or replaying these records validates identity and arithmetic, not the
maintainer's semantic judgments. A source census is not execution evidence.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import suites as base

GROUPS={'architecture-center':('架构中心','Mixed'),
        'ai-center':('人工智能中心','Mixed'),
        'intelligent-driving-center':('智能驾驶中心','Mixed')}
PREFIXES={'architecture-center':'ARC','ai-center':'AIC','intelligent-driving-center':'IDC'}
KINDS={'matlab','native_c','native_cpp','android','android_library','python','integration'}
require=base.require;read=base.read;bound=base.bound;sha=base.sha;encoded=base.encoded;git=base.git

def contract(wrapper,kind):
    require(kind in {'software','matlab'},'Unknown center contract')
    item=read(Path(wrapper)/'suites/center-contracts'/f'{kind}.json')
    require(item['schema']=='center-scoring-contract-1' and item['kind']==kind,'Wrong center contract schema')
    leaves=item['leaves'];require(len({x['name'] for x in leaves})==len(leaves),'Duplicate contract leaf')
    for leaf in leaves:
        require(type(leaf['max_score']) is int and leaf['max_score'] in {3,4},'Invalid center maximum')
        require(leaf['allowed_scores']==list(range(leaf['max_score']+1)) and len(leaf['tiers'])==leaf['max_score']+1,'Invalid center tiers')
    require(item['leaf_count']==len(leaves) and item['max_score']==sum(x['max_score'] for x in leaves),'Center contract denominator differs')
    return item

def validate_entry(wrapper,entry,require_publishable=False):
    wrapper=Path(wrapper);group=entry['id'];require(group in GROUPS,'Unknown center')
    require((entry['name'],entry['technology'])==GROUPS[group],'Center label differs')
    index=read(bound(wrapper,entry['contract']));require(index['schema']=='center-contract-index-1','Wrong contract index')
    for kind in ['software','matlab']:
        require(bound(wrapper,index[kind])==wrapper/'suites/center-contracts'/f'{kind}.json','Wrong contract file');contract(wrapper,kind)
    manifest=read(bound(wrapper,entry['manifest']));standard=read(bound(wrapper,entry['canonical_scores']))
    require(manifest['type_id']==standard['type_id']==group,'Center payload grouping differs')
    sources=manifest['repositories'];rows=standard['repositories'];ids={s['id'] for s in sources}
    require(len(ids)==len(sources) and ids=={r['id'] for r in rows} and len(rows)==len(ids),'Center source/reference set differs')
    for source in sources:
        rid=source['id'];require(re.fullmatch(PREFIXES[group]+r'-\d{2}',rid) and source['type_id']==group,'Center ID differs')
        require(source['center']==entry['name'] and source['implementation_kind'] in KINDS,'Center/technology metadata differs')
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',source['name']),'Unsafe source name')
        for key in ['head','tree']:require(re.fullmatch(r'[0-9a-f]{40}',source[key]),'Invalid source identity')
        require(source['refs'] and all(re.fullmatch(r'refs/(heads|tags)/[^\s\\:]+',ref) and '..' not in ref and re.fullmatch('[0-9a-f]{40}',oid) for ref,oid in source['refs'].items()),'Invalid center refs')
        require(source['publication_status'] in {'published','verified_local'},'Invalid center publication status')
        require(source['repository_url']==('https://github.com/cockpit-bench/'+source['name']+'.git' if source['publication_status']=='published' else None),'Center publication target differs')
        require(source.get('family_id') and source.get('lineage',{}).get('construction_group'),'Missing conservative construction lineage')
        require(isinstance(source['files'],dict) and source['files'],'Missing center source bytes')
        for path,digest in source['files'].items():
            base.safe_path(wrapper,path);require(re.fullmatch('[0-9a-f]{64}',digest),'Invalid source file hash')
        links=source.get('gitlinks',[]);require(len({x['path'] for x in links})==len(links),'Duplicate dependency gitlink')
        for link in links:
            base.safe_path(wrapper,link['path']);require(re.fullmatch('[0-9a-f]{40}',link['head']) and link['repository_id'] in source['lineage']['related_ids'],'Unbound gitlink lineage')
        kind='matlab' if source['implementation_kind']=='matlab' else 'software';rules=contract(wrapper,kind)
        require(source['scoring_contract']==index[kind],'Source contract binding differs')
        row=next(r for r in rows if r['id']==rid);reference=row['reference']
        require(row['head']==source['head'] and row['name']==source['name'] and reference['id']==rid and reference['head']==source['head'] and reference['tree']==source['tree'],'Center reference identity differs')
        require(reference['contract']==index[kind] and reference['status']=='maintainer_reviewed','Reference contract/status differs')
        leaves=reference['leaves'];require(len(leaves)==rules['leaf_count'] and {x['name'] for x in leaves}=={x['name'] for x in rules['leaves']},'Center leaf set differs')
        for leaf in leaves:
            rule=next(x for x in rules['leaves'] if x['name']==leaf['name']);value=leaf['score']
            require(leaf['max_score']==rule['max_score'] and (value is None or type(value) is int and value in rule['allowed_scores']),'Illegal center score')
            require(leaf['reason'].strip() and leaf.get('evidence') and isinstance(leaf.get('limitations'),list),'Missing semantic reasoning or limitations')
            for evidence in leaf['evidence']:
                if evidence.get('kind')=='git':require(source['refs'].get(evidence['ref'])==evidence['oid'],'Review Git evidence differs')
                else:require(evidence['path'] in source['files'] and evidence['sha256']==source['files'][evidence['path']],'Review evidence not bound to current source')
                require(evidence.get('locator'),'Missing model/source evidence locator')
        facts=read(bound(wrapper,source['evidence']));inventory=read(bound(wrapper,source['inventory']))
        require(facts['id']==rid and facts['head']==source['head'] and facts['tree']==source['tree'] and facts['reference']==reference,'Evidence/reference source disagreement')
        require(inventory['id']==rid and inventory['head']==source['head'] and inventory['tree']==source['tree'] and inventory['refs']==source['refs'] and inventory['files']==source['files'] and inventory['gitlinks']==links,'Source inventory drift')
        require(inventory['full_history'] is True and inventory['clean'] is True and inventory['worktree_equals_git_blobs'] is True and inventory['remote_count']==0,'Incomplete source inventory verification')
        require(facts['execution']['status']=='passed' and facts['execution']['records'],'Source lacks successful actual execution')
        for record in facts['execution']['records']:
            run=read(bound(wrapper,record))
            require(run['schema']=='center-execution-summary-1' and run['id']==rid and run['head']==source['head'] and run['tree']==source['tree'] and run['status']=='passed','Execution identity differs')
            require(run['records'] and run['engines'] and run['limits'],'Incomplete execution scope')
            require(run['raw_packet']['sources'].get(rid)=={'head':source['head'],'tree':source['tree']},'Raw execution identity differs')
        profile=read(bound(wrapper,source['scan_profile']))
        require(profile['id']==rid and profile['head']==source['head'] and profile['tree']==source['tree'],'Scan comparison identity differs')
    values=[l for row in rows for l in row['reference']['leaves']];failed=sum(x['score'] is None for x in values)
    summary=dict(repository_count=len(rows),leaf_count=len(values),max_score=sum(x['max_score'] for x in values),score=None if failed else sum(x['score'] for x in values),failed_leaves=failed)
    require(standard['summary']==summary,'Center summary differs')
    for key,value in summary.items():require(entry[key]==value,'Center registry denominator differs: '+key)
    published=sum(s['publication_status']=='published' for s in sources)
    require(entry['published_repositories']==published and entry['status']==('published' if published==len(sources) else 'verified_local'),'Center registry publication differs')
    if require_publishable:require(published==len(sources),'Center contains unpublished sources')
    return ids

def verify_source_files(path,row):
    path=Path(path);actual={};links={}
    records=git('-C',path,'ls-files','--stage','-z',binary=True).decode('utf-8').split('\0')[:-1]
    for record in records:
        metadata,name=record.split('\t',1);mode,oid,stage=metadata.split();require(stage=='0','Source has unmerged entries')
        target=base.safe_path(path,name)
        if mode=='160000':links[name]=oid
        else:require(target.is_file(),'Source file missing');actual[name]=sha(target.read_bytes())
    require(actual==row['files'],'Center source bytes differ')
    require(links=={x['path']:x['head'] for x in row.get('gitlinks',[])},'Center gitlinks differ')

def restore_submodules(target,row,all_sources,mapping):
    links=row.get('gitlinks',[])
    declared=git('-C',target,'config','-f','.gitmodules','--get-regexp',r'^submodule\..*\.path$') if links else ''
    paths={line.split(' ',1)[1]:line.split(' ',1)[0][len('submodule.'):-len('.path')] for line in declared.splitlines()}
    require(set(paths)=={x['path'] for x in links},'Undeclared submodule path')
    for link in links:
        peer=all_sources[link['repository_id']];require(peer['head']==link['head'],'Dependency pin differs from admitted peer')
        if peer['id'] in mapping:
            origin=str(Path(mapping[peer['id']]).resolve());require((Path(origin)/'.git').is_dir(),'Dependency source is not a repository')
            protocol=['-c','protocol.allow=never','-c','protocol.file.allow=always']
        else:
            require(peer['publication_status']=='published','Unpublished dependency requires source map');origin=peer['repository_url'];protocol=['-c','protocol.allow=never','-c','protocol.https.allow=always']
        git('-C',target,'config','submodule.'+paths[link['path']]+'.url',origin)
        git(*protocol,'-c','core.autocrlf=false','-C',target,'submodule','update','--init','--checkout','--',link['path'])
        child=base.safe_path(target,link['path']);require(git('-C',child,'rev-parse','HEAD')==link['head'],'Dependency checkout differs')
        require(not git('-C',child,'status','--porcelain'),'Dependency contains changes')
        if 'origin' not in git('-C',child,'remote').splitlines():git('-C',child,'remote','add','origin',origin)
        git('-C',child,'fetch','origin','refs/heads/*:refs/heads/*','refs/tags/*:refs/tags/*')
        for remote in git('-C',child,'remote').splitlines():git('-C',child,'remote','remove',remote)
        if peer.get('gitlinks'):restore_submodules(child,peer,all_sources,mapping)
        from repository_types import check_source
        check_source(child,peer)

def replay(wrapper,source_root,ids=None):
    from repository_types import validate,select,check_source
    wrapper=Path(wrapper);registry=validate(wrapper);rows=[r for r in select(registry,wrapper,'all') if r['type_id'] in GROUPS]
    if ids is not None:
        require(set(ids)<={r['id'] for r in rows},'Unknown center ID');rows=[r for r in rows if r['id'] in ids]
    result=[]
    for row in rows:
        root=Path(source_root);path=root/row['name']
        if not path.exists():path=root/row['type_id']/row['name']
        check_source(path,row);facts=read(bound(wrapper,row['evidence']))
        result.append(dict(id=row['id'],head=row['head'],scores={x['name']:x['score'] for x in facts['reference']['leaves']},semantics_reassessed=False,execution_repeated=False))
    return {'repositories':result,'scope':'Source identity and bound reference replay only; no new execution or semantic reassessment.'}

def candidate(wrapper,source_root,rid,output):
    from repository_types import validate,select,check_source
    wrapper=Path(wrapper);registry=validate(wrapper);rows=select(registry,wrapper,'all',[rid]);row=rows[0]
    require(row['type_id'] in GROUPS,'Use the existing candidate exporter for the older groups')
    source=Path(source_root)/row['name']
    if not source.exists():source=Path(source_root)/row['type_id']/row['name']
    check_source(source,row);output=Path(output).resolve();require(not output.exists(),'Candidate destination exists')
    require(not output.is_relative_to(source.resolve()) and not source.resolve().is_relative_to(output),'Candidate destination overlaps source')
    require(not output.is_relative_to(wrapper.resolve()) and not wrapper.resolve().is_relative_to(output),'Candidate destination overlaps answers')
    # Only admitted refs and the evaluated HEAD belong in the candidate input.
    # --all would also export an unregistered stash, notes or private work ref.
    output.mkdir(parents=True);bundle=output/'source.bundle';git('-C',source,'bundle','create',bundle,'HEAD',*sorted(row['refs']));git('-C',source,'bundle','verify',bundle)
    (output/'scoring-contract.json').write_bytes(bound(wrapper,row['scoring_contract']).read_bytes())
    task=dict(schema='center-candidate-target-1',repository_id=rid,center=row['center'],name=row['name'],head=row['head'],tree=row['tree'],refs=row['refs'],implementation_kind=row['implementation_kind'],gitlinks=row.get('gitlinks',[]),limits='One scored target. Declared gitlinks are build dependencies; source.bundle contains their pinned links, not peer repositories or maintainer references. A runner may provision only these declared dependencies in a separate read-only area when execution is required.')
    (output/'target.json').write_bytes(encoded(task))
    text='Restore source.bundle with full Git history, check out the target HEAD, and evaluate only this repository under scoring-contract.json. Do not read the wrapper/reference files. Report each leaf with score, source evidence, uncertainty, and limitations. The runner is responsible for isolation and any permitted dependency provisioning.\n'
    (output/'README.txt').write_text(text,encoding='utf-8')
    files={p.name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in output.iterdir()}
    (output/'input-manifest.json').write_bytes(encoded(dict(schema='center-candidate-inputs-1',repository_id=rid,head=row['head'],files=files)))
    return {'repository_id':rid,'files':len(files)+1,'destination':str(output),'head':row['head']}

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for cmd in ['replay','candidate']:
        p=sub.add_parser(cmd);p.add_argument('--wrapper',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
        if cmd=='candidate':p.add_argument('--id',required=True)
        else:p.add_argument('--ids',nargs='+')
    args=parser.parse_args()
    try:
        result=candidate(args.wrapper,args.source_root,args.id,args.output) if args.command=='candidate' else replay(args.wrapper,args.source_root,args.ids)
        if args.command=='replay':args.output.write_bytes(encoded(result))
        print(json.dumps(result,ensure_ascii=False));return 0
    except (ValueError,KeyError,OSError) as err:print('REJECTED: '+str(err),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
