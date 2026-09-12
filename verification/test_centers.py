"""New group contracts, source binding, isolated exports and dependency restore."""
import copy,json,shutil,tempfile,unittest,subprocess
from pathlib import Path
from unittest.mock import patch
import centers,repository_types as rt,suites,evaluation_current as ec
from population_diagnostics import analyze_mixed_contracts
W=Path(__file__).resolve().parents[1]

class CenterRegistryTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'wrapper';self.root.mkdir()
  for name in ['suites','suites.json','manifest.json','STANDARD_SCORES.json','SCORE_RULES.md']:
   src=W/name;dst=self.root/name
   shutil.copytree(src,dst) if src.is_dir() else shutil.copyfile(src,dst)
 def tearDown(self):self.temp.cleanup()
 def alter(self,field,mutate):
  r=rt.read(self.root/'suites.json');e=next(x for x in r['suites'] if x['id']=='ai-center');p=self.root/e[field]['path']
  data=rt.read(p);mutate(data);p.write_bytes(rt.encoded(data));e[field]['sha256']=rt.sha(p.read_bytes());(self.root/'suites.json').write_bytes(rt.encoded(r))
 def test_new_centers_add_511_leaves_without_changing_old_populations(self):
  r=rt.validate(self.root);self.assertEqual([x['score'] for x in r['suites'][:3]],[142,194,409])
  self.assertEqual(sum(x['leaf_count'] for x in r['suites'][3:]),511)
  self.assertEqual(sum(x['repository_count'] for x in r['suites']),66)
  self.assertEqual([x['name'] for x in r['suites'][3:]],['架构中心','人工智能中心','智能驾驶中心'])
 def test_numeric_tier_outside_center_contract_is_rejected_even_if_rehashed(self):
  self.alter('canonical_scores',lambda d:d['repositories'][0]['reference']['leaves'][0].update(score=4))
  with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
 def test_center_cannot_be_reclassified_by_implementation_kind(self):
  self.alter('manifest',lambda d:d['repositories'][0].update(type_id='app'))
  with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
 def test_source_file_identity_cannot_be_rehashed_away(self):
  def mutate(d):
   files=d['repositories'][0]['files'];files[next(iter(files))]='0'*64
  self.alter('manifest',mutate)
  with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
 def test_new_construction_and_dependency_closure_cannot_cross_splits(self):
  sources=rt.select(rt.validate(self.root),self.root,'all');a={r['id']:'dev' for r in sources};a['IDC-05']='test'
  with self.assertRaisesRegex(ValueError,'closure crosses splits'):ec.lineage(sources,a)
 def test_removed_legacy_ids_are_not_reused_by_centers(self):
  self.alter('manifest',lambda d:d['repositories'][0].update(id='NEM-10'))
  with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)

class CenterDependencyRestoreTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  self.child=self.repo('dep','int answer(void) { return 42; }\n')
  self.parent=self.repo('parent','dependency entry\n')
  head=rt.git('-C',self.child,'rev-parse','HEAD')
  (self.parent/'.gitmodules').write_bytes(b'[submodule "dep"]\n path = components/dep\n url = ../dep\n')
  rt.git('-C',self.parent,'add','.gitmodules');rt.git('-C',self.parent,'update-index','--add','--cacheinfo','160000,'+head+',components/dep');rt.git('-C',self.parent,'commit','-qm','Pin actual dependency')
  self.rows=[self.row(self.parent,'ARC-07'),self.row(self.child,'ARC-01')]
  self.rows[0]['gitlinks']=[dict(path='components/dep',repository_id='ARC-01',head=head)]
  self.mapping=self.root/'mapping.json';self.mapping.write_bytes(rt.encoded({'ARC-07':str(self.parent),'ARC-01':str(self.child)}))
  self.wrapper=self.root/'wrapper';self.wrapper.mkdir()
 def tearDown(self):self.temp.cleanup()
 def repo(self,name,text):
  p=self.root/name;p.mkdir();rt.git('init','-q','-b','main',p)
  rt.git('-C',p,'config','user.name','Fixture');rt.git('-C',p,'config','user.email','fixture@example.invalid');rt.git('-C',p,'config','core.autocrlf','false')
  (p/'logic.c').write_bytes(text.encode());rt.git('-C',p,'add','.');rt.git('-C',p,'commit','-qm','Initial implementation');return p
 def row(self,p,rid):
  files={}
  for entry in rt.git('-C',p,'ls-files','--stage','-z',binary=True).decode().split('\0')[:-1]:
   meta,name=entry.split('\t');
   if not meta.startswith('160000'):files[name]=rt.sha((p/name).read_bytes())
  return dict(id=rid,name=p.name,type_id='architecture-center',head=rt.git('-C',p,'rev-parse','HEAD'),tree=rt.git('-C',p,'rev-parse','HEAD^{tree}'),
   refs=dict(x.split('|') for x in rt.git('-C',p,'for-each-ref','--format=%(refname)|%(objectname)','refs/heads','refs/tags').splitlines()),
   publication_status='verified_local',repository_url=None,files=files,gitlinks=[])
 def test_full_dependency_history_bytes_and_resume_without_remotes(self):
  dest=self.root/'restored'
  with patch.object(rt,'validate',return_value={}),patch.object(rt,'select',return_value=self.rows):
   results=rt.restore(self.wrapper,'all',dest,source_map=self.mapping,include_submodules=True)
   self.assertEqual(len(results),2)
   child=dest/'architecture-center/parent/components/dep'
   rt.check_source(child,self.rows[1]);self.assertEqual((child/'logic.c').read_bytes(),(self.child/'logic.c').read_bytes())
   rt.restore(self.wrapper,'all',dest,source_map=self.mapping,include_submodules=True,resume=True)
   (child/'logic.c').write_bytes(b'user change\n')
   with self.assertRaises(suites.InvalidSuite):rt.restore(self.wrapper,'all',dest,source_map=self.mapping,include_submodules=True,resume=True)
 def test_git_clean_text_normalization_is_still_rejected(self):
  row=self.rows[1];rt.git('-C',self.child,'config','core.autocrlf','true');p=self.child/'logic.c';p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
  rt.git('-C',self.child,'add','--renormalize','logic.c')
  self.assertEqual(rt.git('-C',self.child,'write-tree'),row['tree'])
  self.assertFalse(rt.git('-C',self.child,'status','--porcelain'))
  with self.assertRaisesRegex(suites.InvalidSuite,'source bytes differ'):rt.check_source(self.child,row)
 def test_candidate_does_not_export_unregistered_stash_objects(self):
  (self.child/'unrelated.txt').write_bytes(b'Fixture unrelated temporary material\n')
  rt.git('-C',self.child,'stash','push','--include-untracked','-m','Unrelated fixture state')
  stash=rt.git('-C',self.child,'rev-parse','refs/stash');row=self.rows[1]
  rules=self.wrapper/'contract.json';rules.write_bytes(b'{"fixture":true}\n')
  row.update(center='架构中心',implementation_kind='native_c',scoring_contract={'path':'contract.json','sha256':rt.sha(rules.read_bytes())})
  with patch.object(rt,'validate',return_value={}),patch.object(rt,'select',return_value=[row]):
   dest=self.root/'candidate';centers.candidate(self.wrapper,self.root,row['id'],dest)
  advertised=rt.git('bundle','list-heads',dest/'source.bundle')
  self.assertNotIn('refs/stash',advertised)
  restored=self.root/'candidate-restored';rt.git('clone','--no-local',dest/'source.bundle',restored)
  with self.assertRaises(subprocess.CalledProcessError):rt.git('-C',restored,'cat-file','-e',stash)
 def test_shallow_local_transport_is_rejected_before_destination_creation(self):
  (self.child/'.git/shallow').write_bytes((self.rows[1]['head']+'\n').encode())
  dest=self.root/'must-not-create'
  with patch.object(rt,'validate',return_value={}),patch.object(rt,'select',return_value=self.rows):
   with self.assertRaisesRegex(suites.InvalidSuite,'Local transport history is shallow'):
    rt.restore(self.wrapper,'all',dest,source_map=self.mapping)
  self.assertFalse(dest.exists())

class MixedContractDiagnosticsTests(unittest.TestCase):
 def test_inapplicable_metrics_are_not_zero_filled(self):
  leaves=[dict(repository_id='A',name='model',score=2,allowed_scores=[0,1,2,3]),dict(repository_id='B',name='software',score=4,allowed_scores=[0,1,2,3,4])]
  d=analyze_mixed_contracts(leaves,[['A','B']],{'A':'m','B':'s'},{'m':{'model':[0,1,2,3]},'s':{'software':[0,1,2,3,4]}})
  self.assertEqual((d['repository_count'],d['leaf_count'],d['legal_band_cells']),(2,2,9))
  self.assertEqual(d['modal_baseline']['denominator'],2)
  self.assertTrue(all(b['count']==0 for b in d['bands'] if b['score']==0))
  self.assertEqual(d['deterministic_associations'],[])
 def test_missing_applicable_metric_is_rejected(self):
  row=dict(repository_id='A',name='first',score=1,allowed_scores=[0,1])
  with self.assertRaisesRegex(ValueError,'Incomplete applicable contract'):
   analyze_mixed_contracts([row],[['A']],{'A':'m'},{'m':{'first':[0,1],'missing':[0,1]}})

if __name__=='__main__':unittest.main()
