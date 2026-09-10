"""Restore frozen local bundles without credentials, remotes, shallow history or resets."""
import argparse, hashlib, json, subprocess
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(p, *args):
    return subprocess.check_output(['git', '-C', str(p), *args], text=True, encoding='utf-8').strip()
def restore(manifest_path, destination):
    manifest_path=Path(manifest_path).resolve(); destination=Path(destination).resolve()
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')); results=[]
    def within(root,relative):
        assert isinstance(relative,str) and relative and ':' not in relative and '\\' not in relative
        assert not Path(relative).is_absolute() and all(x not in {'','.','..'} for x in relative.split('/'))
        value=(root/relative).resolve();assert value.is_relative_to(root) and value!=root
        return value
    targets=[]
    for row in manifest['repositories']:
        bundle=within(manifest_path.parent,row['bundle']['path'])
        repo=within(destination,row['group']+'/'+row['name'])
        assert not repo.is_relative_to(manifest_path.parent) and not manifest_path.parent.is_relative_to(repo),'Destination overlaps delivery'
        targets.append((bundle,repo))
    for row,(bundle,repo) in zip(manifest['repositories'],targets):
        assert sha(bundle)==row['bundle']['sha256'], f'Bundle digest: {bundle}'
        repo.mkdir(parents=True, exist_ok=True)
        if not (repo/'.git').exists():
            assert not list(repo.iterdir()), f'Nonempty target: {repo}'
            git(repo,'init','-b','unborn-restore'); git(repo,'config','core.autocrlf','false')
        head=subprocess.run(['git','-C',str(repo),'rev-parse','--verify','HEAD'],capture_output=True)
        if head.returncode:
            assert not git(repo,'status','--porcelain'), f'Uncommitted target: {repo}'
            git(repo,'fetch',str(bundle),'refs/heads/*:refs/heads/*','refs/tags/*:refs/tags/*')
            git(repo,'switch','master')
        assert git(repo,'rev-parse','HEAD')==row['head'], f'HEAD mismatch: {repo}'
        assert git(repo,'rev-parse','HEAD^{tree}')==row['tree']
        refs=dict(line.split(' ',1)[::-1] for line in git(repo,'show-ref','--heads','--tags').splitlines())
        assert refs==row['refs'], f'Refs mismatch: {repo}'
        assert git(repo,'rev-parse','--is-shallow-repository')=='false'
        assert not git(repo,'remote'), f'Remotes present: {repo}'
        assert not (repo/'.git/objects/info/alternates').exists()
        assert not git(repo,'status','--porcelain'), f'Working tree modified: {repo}'
        files={p:sha(repo/p) for p in git(repo,'-c','core.quotepath=false','ls-files').splitlines()}
        assert files==row['files'], f'File mismatch: {repo}'
        git(repo,'fsck','--full')
        results.append({'id':row['id'],'path':str(repo),'head':row['head'],'tree':row['tree'],
                        'files':len(files),'refs':len(refs),'full_history':True,'clean':True,'remotes':0})
        print('RESTORE_PASS',row['id'],len(files),len(refs),flush=True)
    return {'cohort_id':manifest['cohort_id'],'repositories':results,'verified':len(results)}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',required=True); parser.add_argument('--destination',required=True)
    parser.add_argument('--receipt',required=True)
    args=parser.parse_args(); result=restore(args.manifest,args.destination)
    Path(args.receipt).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
