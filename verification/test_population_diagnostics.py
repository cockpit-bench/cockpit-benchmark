import copy
from pathlib import Path
import unittest
import repository_types as rt
import evaluation_current as ec
import population_diagnostics as pd

W=Path(__file__).resolve().parents[1]

class PopulationDiagnosticsTests(unittest.TestCase):
    def test_current_single_matlab_closure_and_missing_bands_are_explicit(self):
        sources=rt.select(rt.validate(W),W,'all');assign={r['id']:'dev' for r in sources}
        batch=ec.prepare(W,'new-energy-matlab','source_only',assign);d=batch['population_diagnostics']
        self.assertEqual((d['repository_count'],d['source_group_count']),(11,1))
        self.assertEqual(d['independent_holdout']['status'],'structurally_unavailable')
        self.assertEqual(d['observed_band_cells'],39);self.assertEqual(d['legal_band_cells'],52)
        pairs={frozenset([p['left'],p['right']]) for p in d['deterministic_associations']}
        self.assertIn(frozenset(['release_branches','device_specificity']),pairs)
        result=ec.assess(batch,{'profile_sha256':batch['profile']['profile_sha256'],'leaves':[]})
        self.assertEqual(len(result['band_recall_and_confusion']),52)
        missing=next(b for b in result['band_recall_and_confusion'] if b['leaf']=='build_independence' and b['gold']==0)
        self.assertEqual((missing['count'],missing['recall'],missing['measurement_status']),(0,None,'unmeasured'))
    def test_new_cross_combination_removes_artificial_deterministic_association(self):
        leaves=[{'repository_id':rid,'name':name,'score':score,'allowed_scores':[0,1,2,3]}
                for rid,values in [('A',(0,0)),('B',(1,1)),('C',(0,1))] for name,score in zip(['x','y'],values)]
        original=copy.deepcopy(leaves);d=pd.analyze(leaves,[['A'],['B'],['C']])
        self.assertFalse(d['deterministic_associations']);self.assertEqual(d['independent_holdout']['status'],'not_certified')
        self.assertEqual(leaves,original)
        with self.assertRaises(ValueError):pd.analyze(leaves,[['A','B'],['B','C']])
    def test_saved_current_diagnostics_recompute(self):
        saved=rt.read(W/'docs/population-diagnostics.json');sources=rt.select(rt.validate(W),W,'all');assign={r['id']:'development' for r in sources}
        for typ in rt.TYPES:self.assertEqual(saved['types'][typ],ec.prepare(W,typ,'source_only',assign)['population_diagnostics'])

    def test_single_tiny_source_cannot_be_presented_as_generalization_support(self):
        leaves=[{'repository_id':rid,'name':'x','score':score,'allowed_scores':[0,1,2,3]}
                for rid,score in [('A',1),('B',3),('C',1)]]
        sizes={rid:dict(source_loc=loc,size_band=band) for rid,loc,band in [('A',40000,'medium'),('B',25,'small'),('C',90000,'large')]}
        result=pd.size_associations(leaves,[['A','C'],['B']],sizes)
        bands={b['score']:b for b in result['bands']}
        self.assertEqual(bands[3]['source_loc_max'],25)
        self.assertEqual(bands[3]['support'],'one_source_group_only')
        self.assertEqual(bands[1]['source_groups'],1)
        self.assertEqual(bands[2]['support'],'unmeasured')
        self.assertIsNone(bands[2]['source_loc_median'])
        self.assertTrue(all(b['generalization']=='not_established' for b in bands.values()))
        del sizes['A']
        with self.assertRaises(ValueError):pd.size_associations(leaves,[['A','C'],['B']],sizes)

    def test_unresolved_reference_is_reported_without_imputing_a_band(self):
        leaves=[{'repository_id':rid,'name':'x','score':score,'allowed_scores':[0,1,2,3]}
                for rid,score in [('A',None),('B',3)]]
        result=pd.analyze(leaves,[['A'],['B']])
        self.assertEqual(result['leaf_count'],2)
        self.assertEqual(result['unresolved_reference_leaves'],['A/x'])
        self.assertEqual(result['modal_baseline']['denominator'],1)
        self.assertEqual(result['observed_band_cells'],1)
        self.assertEqual(next(r for r in result['bands'] if r['score']==0)['count'],0)

if __name__=='__main__':unittest.main()
