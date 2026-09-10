import copy,json,tempfile,unittest,shutil
from pathlib import Path
import ne_reality as ne

WRAPPER=Path(__file__).resolve().parents[1]
class RealityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        shutil.copytree(ne.location(WRAPPER),ne.location(self.root))
        self.cohort=ne.location(self.root)
    def tearDown(self):self.tmp.cleanup()
    def prediction(self):
        _,_,_,g,_=ne.load(self.root)
        return {'cohort_id':ne.COHORT,'contract_sha256':g['contract_sha256'],'repositories':[
          {'id':r['id'],'head':r['head'],'scores':copy.deepcopy(r['reference']['scores'])} for r in g['repositories']]}
    def test_complete_schema(self):
        _,_,_,g,_=ne.load(self.root);self.assertEqual(g['leaf_count'],143)
    def test_changed_contract_rejected(self):
        with (self.cohort/'SCORING_CONTRACT_PART7.md').open('a',encoding='utf-8') as f:f.write('mutation')
        with self.assertRaises(ValueError):ne.load(self.root)
    def test_corrupt_leaf_binding_rejected(self):
        g=ne.read(self.cohort/'STANDARD_SCORES.json');g['repositories'][0]['reference']['leaves']['interface']['evidence'][0]['sha256']='0'*64
        ne.write(self.cohort/'STANDARD_SCORES.json',g)
        with self.assertRaises(ValueError):ne.load(self.root)
    def test_wrong_tier_rejected(self):
        p=self.prediction();p['repositories'][0]['scores']['unit_test']=2
        with self.assertRaises(ValueError):ne.evaluate(self.root,p)
    def test_booleans_not_numeric_tiers(self):
        p=self.prediction();p['repositories'][0]['scores']['reuse']=True
        with self.assertRaises(ValueError):ne.evaluate(self.root,p)
    def test_equal_float_tier_accepted(self):
        p=self.prediction();p['repositories'][0]['scores']['reuse']=1.0
        self.assertEqual(ne.evaluate(self.root,p)['macro_accuracy'],1)
    def test_null_abstention_keeps_denominator(self):
        p=self.prediction();p['repositories'][0]['scores']['reuse']=None
        r=ne.evaluate(self.root,p);self.assertEqual(r['eligible_leaves'],143);self.assertEqual(r['leaf_metrics']['reuse']['answered'],10)
        self.assertEqual(r['leaf_metrics']['reuse']['accuracy_fixed_set'],10/11)
    def test_duplicate_repo_rejected(self):
        p=self.prediction();p['repositories'][-1]=p['repositories'][0]
        with self.assertRaises(ValueError):ne.evaluate(self.root,p)
    def test_stale_head_rejected(self):
        p=self.prediction();p['repositories'][0]['head']='0'*40
        with self.assertRaises(ValueError):ne.evaluate(self.root,p)
    def test_legacy_contract_rejected(self):
        p=self.prediction();p['contract_sha256']='0'*64
        with self.assertRaises(ValueError):ne.evaluate(self.root,p)
    def test_missing_leaf_rejected(self):
        p=self.prediction();del p['repositories'][0]['scores']['hierarchy']
        with self.assertRaises(ValueError):ne.evaluate(self.root,p)
    def test_shared_family_split_rejected(self):
        a={f'NEP-{i:02d}':'dev' for i in range(1,12)};a['NEP-11']='test'
        with self.assertRaises(ValueError):ne.check_split(self.root,a)
    def test_same_family_allowed(self):
        a={f'NEP-{i:02d}':'dev' for i in range(1,12)}
        self.assertFalse(ne.check_split(self.root,a)['independent_holdout'])
    def test_unsafe_source_path_rejected(self):
        m=ne.read(self.cohort/'manifest.json');m['repositories'][0]['files']['../outside']='0'*64;ne.write(self.cohort/'manifest.json',m)
        with self.assertRaises(ValueError):ne.load(self.root)
    def test_wrong_census_rejected(self):
        o=ne.read(self.cohort/'OBSERVATIONS.json');o['repositories'][0]['head']='0'*40;ne.write(self.cohort/'OBSERVATIONS.json',o)
        with self.assertRaises(ValueError):ne.load(self.root)
if __name__=='__main__':unittest.main()
