"""Current revisions cannot silently rewrite the frozen reference or execution."""
import copy
from pathlib import Path
import tempfile
import unittest
import reference_revisions as rr
import repository_types as rt
from expansion import check_model_pointer

W=Path(__file__).resolve().parents[1]

class ReferenceRevisionTests(unittest.TestCase):
    def setUp(self):
        self.reg=rt.validate(W);self.sources={s['id']:s for s in rt.select(self.reg,W,'all')}
        self.old={r['id']:r for r in rt.read(W/'STANDARD_SCORES.json')['repositories']}
    def fixture(self,rid):
        typ=self.sources[rid]['type_id'];entry=next(e for e in self.reg['suites'] if e['id']==typ)
        row=next(r for r in rt.read(rt.bound(W,entry['canonical_scores']))['repositories'] if r['id']==rid)
        return copy.deepcopy(row),rt.read(rt.bound(W,row['reference_revision'])),entry['contract']['sha256']
    def check(self,row,revision,contract):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=root/'revision.json';path.write_bytes(rt.encoded(revision))
            row['reference_revision']={'path':'revision.json','sha256':rt.sha(path.read_bytes())}
            return rr.validate(root,row,self.old[row['id']],self.sources[row['id']],contract)
    def test_only_two_old_references_have_explicit_current_revisions(self):
        revisions=[]
        for entry in self.reg['suites']:
            for row in rt.read(rt.bound(W,entry['canonical_scores']))['repositories']:
                if 'reference_revision' in row:
                    revisions.append(row['id']);rr.validate(W,row,self.old[row['id']],self.sources[row['id']],entry['contract']['sha256'])
        self.assertEqual(revisions,['APP-13','FW-14'])
    def test_rehashed_undeclared_leaf_change_rejected(self):
        row,revision,contract=self.fixture('APP-13')
        row['reference']['leaves'][0]['analysis']+=' changed'
        revision['current_reference_sha256']=rt.sha(rt.encoded(row['reference']))
        with self.assertRaisesRegex(ValueError,'Undeclared'):self.check(row,revision,contract)
    def test_rehashed_score_requires_rule_observations(self):
        row,revision,contract=self.fixture('APP-13');revision['changes'][0]['rule_inputs']['has_circular_dependency']=True
        with self.assertRaisesRegex(ValueError,'rule replay'):self.check(row,revision,contract)
    def test_reference_revision_cannot_alter_source_contract_or_baseline(self):
        for field in ['head','tree','contract_sha256','baseline_reference_sha256']:
            with self.subTest(field=field):
                row,revision,contract=self.fixture('APP-13');revision[field]='0'*len(revision[field])
                with self.assertRaises(ValueError):self.check(row,revision,contract)
    def test_historical_run_is_labeled_and_nine_inputs_bound(self):
        row,revision,contract=self.fixture('FW-14');binding=rt.read(rt.bound(W,revision['execution_rebinding']))['rebinding']
        self.assertNotEqual(binding['executed_head'],binding['current_head'])
        self.assertEqual(len(binding['inputs']),9)
        report=rt.read(W/binding['original_report']['container_path'])['structured'][0]
        self.assertEqual(binding['original_report']['canonical_json_sha256'],rt.sha(rt.encoded(report)))
        self.assertEqual(binding['executed_head'],report['head'])
        self.assertEqual(report['test_count'],25)

class ModelPointerTests(unittest.TestCase):
    def test_actual_parent_child_bindings_and_swaps(self):
        facts=rt.read(W/'suites/new-energy-matlab/evidence/NEM-10.json')
        inventory=rt.read(rt.bound(W,facts['source_inventory']))
        anchors=next(l for l in facts['reference']['leaves'] if l['name']=='dataflow')['evidence']
        for a in anchors:
            if a['evidence_type']!='facts':continue
            check_model_pointer(inventory,a)
            swapped=copy.deepcopy(a);i=int(a['json_pointer'].split('/')[2]);swapped['json_pointer']=a['json_pointer'].replace('/models/'+str(i)+'/', '/models/'+str(1-i)+'/')
            with self.assertRaisesRegex(ValueError,'different model'):check_model_pointer(inventory,swapped)
            missing=copy.deepcopy(a);del missing['model_path']
            with self.assertRaises(ValueError):check_model_pointer(inventory,missing)
    def test_layout_witness_keeps_nested_branch_geometry(self):
        facts=rt.read(W/'suites/new-energy-matlab/evidence/NEM-10.json');audit=rt.read(rt.bound(W,facts['acquisition_scope_audit']))
        self.assertEqual(len(audit['blocks']),322);self.assertEqual(len(audit['signature']['edges']),366)
        route=next(r for r in audit['routes'] if r['properties']['Src']=='214#out:1')
        self.assertTrue(route['branches'])
        self.assertIn('-162',str(route));self.assertIn('216#in:2',str(route))

if __name__=='__main__':unittest.main()
