import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
import evaluation_current as ec
import evaluation_batch as eb
import evaluation_profile as ep
import repository_types as rt
from matlab_recompute import build_independence

W=Path(__file__).resolve().parents[1]

class CurrentEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.sources=rt.select(rt.validate(W),W,'all');self.assign={r['id']:'dev' for r in self.sources}
    def test_separate_current_populations(self):
        for kind,n,eligible in [('app',88,79),('fw',121,109),('new-energy-matlab',143,133)]:
            b=ec.prepare(W,kind,'source_only',self.assign)
            self.assertEqual((len(b['profile']['requested']),len(b['profile']['eligible'])),(n,eligible))
    def test_saved_summary_and_distribution_match_actual_reference(self):
        summary=rt.read(W/'docs/current-evaluation-summary.json');saved=rt.read(W/'docs/current-distribution.json')
        for kind in rt.TYPES:
            b=ec.prepare(W,kind,'source_only',self.assign);p=b['profile']
            self.assertEqual(summary[kind]['source_only'],{'requested':len(p['requested']),'eligible':len(p['eligible']),'excluded':len(p['exclusions'])})
            full=dict(p,eligible=[r['id'] for r in b['reference']['leaves'] if r['score'] is not None]);d=eb.distribution(full,b['reference'],{'leaves':[]})
            self.assertEqual(saved['types'][kind]['canonical_diagnostic']['modal_hits'],d['modal_hits'])
            self.assertEqual([x['gold_counts'] for x in saved['types'][kind]['canonical_diagnostic']['groups']],[{str(k):v for k,v in x['gold_counts'].items()} for x in d['groups']])
    def test_cross_type_dependency_and_construction_closure(self):
        for rid in ['FW-21','NEM-11','ML-04','APP-14']:
            a=dict(self.assign);a[rid]='test'
            with self.assertRaises(ValueError):ec.lineage(self.sources,a)
    def test_incomplete_assignments_rejected(self):
        del self.assign['FW-21']
        with self.assertRaises(ValueError):ec.prepare(W,'app','source_only',self.assign)
    def test_missing_external_inputs_not_silently_source_mode(self):
        with self.assertRaises(ValueError):ec.prepare(W,'fw','frozen_external',self.assign)
    def test_unsupported_live_mode_rejected(self):
        with self.assertRaises(ValueError):ec.prepare(W,'app','live_environment',self.assign)
    def test_wrong_candidate_profile_rejected(self):
        b=ec.prepare(W,'app','source_only',self.assign)
        with self.assertRaises(ValueError):ec.assess(b,{'profile_sha256':'wrong','leaves':[]})
    def test_fixed_denominator_missing_abstention_band_recall(self):
        b=ec.prepare(W,'app','source_only',self.assign);key=b['profile']['eligible'][0]
        c={'profile_sha256':b['profile']['profile_sha256'],'leaves':[{'id':key,'status':'abstain'}]}
        r=ec.assess(b,c)
        self.assertEqual((r['common_eligible'],r['abstained'],r['missing']),(79,1,78))
        self.assertEqual(sum(x['count'] for x in r['band_recall_and_confusion']),79)
        self.assertEqual(r['evidence_validity']['status'],'not_reviewed')
    def test_illegal_matlab_band_rejected(self):
        b=ec.prepare(W,'new-energy-matlab','source_only',self.assign)
        with self.assertRaises(ValueError):ec.assess(b,{'profile_sha256':b['profile']['profile_sha256'],'leaves':[{'id':'NEM-10/parameter_management','status':'scored','score':2}]})
    def test_equal_json_numeric_representations_have_equal_metrics(self):
        for kind in rt.TYPES:
            with self.subTest(kind=kind):
                b=ec.prepare(W,kind,'source_only',self.assign)
                candidate={'profile_sha256':b['profile']['profile_sha256'],'leaves':[
                    {'id':r['id'],'status':'scored','score':r['score']}
                    for r in b['reference']['leaves'] if r['score'] is not None]}
                integers=ec.assess(b,candidate)
                for row in candidate['leaves']:
                    row['score']=float(row['score']) if row['score'] else -0.0
                floats=ec.assess(b,json.loads(json.dumps(candidate)))
                self.assertEqual(integers['accuracy'],1.0)
                self.assertEqual(floats['accuracy'],1.0)
                self.assertEqual(integers['band_recall_and_confusion'],floats['band_recall_and_confusion'])
                self.assertTrue(all(r['recall']==1.0 for r in floats['band_recall_and_confusion'] if r['count']))
                self.assertTrue(all(r['recall'] is None and r['measurement_status']=='unmeasured' for r in floats['band_recall_and_confusion'] if not r['count']))
    def test_raw_packets_and_single_repository_export(self):
        root=os.environ.get('CURRENT_EXTERNAL_INPUTS')
        if not root:self.skipTest('Set CURRENT_EXTERNAL_INPUTS for archived raw-input verification')
        for kind,n in [('app',81),('fw',113),('new-energy-matlab',142)]:
            b=ec.prepare(W,kind,'frozen_external',self.assign,root);self.assertEqual(len(b['profile']['eligible']),n)
        spec=rt.read(W/'docs/current-evaluation.json')['packets']['sdk-repair']
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'candidate';ec.export_inputs(W,'FW-22',Path(root)/spec['name'],dest)
            self.assertEqual({p.name for p in dest.iterdir()},{'execution.json','message.log','sdk','input-manifest.json'})
            broken=Path(temp)/'broken.zip';broken.write_bytes(b'broken')
            with self.assertRaises(ValueError):ec.packet_check(broken,spec)
    def test_sdk_prerequisite_and_neutral_single_source_export(self):
        source=ec.prepare(W,'app','source_only',self.assign)
        key='APP-22/platform_reuse.platform_upgrade'
        self.assertNotIn(key,source['profile']['eligible'])
        root=os.environ.get('CURRENT_EXTERNAL_INPUTS')
        if not root:self.skipTest('Set CURRENT_EXTERNAL_INPUTS for complete SDK verification')
        frozen=ec.prepare(W,'app','frozen_external',self.assign,root)
        self.assertIn(key,frozen['profile']['eligible'])
        spec=rt.read(W/'docs/current-evaluation.json')['packets']['current-raw']
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'candidate';result=ec.export_inputs(W,'APP-22',Path(root)/spec['name'],dest)
            self.assertEqual(result['files'],5)
            self.assertEqual({p.name for p in dest.iterdir()},{'sdk','input-manifest.json'})
            files={p.name:p.read_bytes() for p in (dest/'sdk').iterdir()};binding=ec.sdk_check(files)
            self.assertEqual(binding,rt.read(W/'suites/app/evidence/APP-22.json')['external_static_inputs']['android_sdk'])
            self.assertIn('@Deprecated public class Camera {',files['android.txt'].decode().splitlines()[20351])
            files['android.txt']+=b'\n'
            with self.assertRaises(ValueError):ec.sdk_check(files)

    def test_all_repaired_sdk_inputs_exclude_source_and_bind_frozen_head(self):
        inventory=rt.read(W/'docs/current-evaluation.json')
        root=os.environ.get('CURRENT_EXTERNAL_INPUTS')
        if not root:self.skipTest('Set CURRENT_EXTERNAL_INPUTS for SDK binding verification')
        for rid,kind in [('APP-21','app'),('FW-21','fw'),('FW-22','fw')]:
            key=rid+'/platform_reuse.platform_upgrade'
            self.assertNotIn(key,ec.prepare(W,kind,'source_only',self.assign)['profile']['eligible'])
            self.assertIn(key,ec.prepare(W,kind,'frozen_external',self.assign,root)['profile']['eligible'])
            row=next(r for r in inventory['leaves'] if r['id']==key)
            packet=Path(root)/inventory['packets'][row['packet_id']]['name']
            ec.sdk_requirements_check(packet,row)
            for changed in [dict(row,head='0'*40),dict(row,sdk_requirements=[dict(directory='sdk',compile_sdk=33)])]:
                with self.assertRaisesRegex(ValueError,'Repository SDK binding differs'):
                    ec.sdk_requirements_check(packet,changed)

    def test_unresolved_reference_keeps_requested_denominator_without_scoring(self):
        context={'reference_id':'fixture','source_manifest_sha256':'fixture'}
        rows=[{'id':key,'reference_id':'fixture','reference_status':status,'requires_external':False,
               'modes':{'source_only':{'state':'supported','kind':'source','basis':'complete source','evidence_ids':[key]}}}
              for key,status in [('A/x','unresolved'),('B/x','resolved')]]
        profile=ep.register({'leaves':rows},'source_only',context)
        reference={'context':context,'leaves':[{'id':'A/x','score':None},{'id':'B/x','score':3}]}
        result=ep.compare(profile,reference,{'profile_sha256':profile['profile_sha256'],
                          'leaves':[{'id':'A/x','status':'scored','score':0},{'id':'B/x','status':'scored','score':3}]})
        self.assertEqual((result['requested'],result['common_eligible'],result['correct']),(2,1,1))
        self.assertEqual(result['exclusions'][0]['reason'],'reference_unresolved')
        self.assertEqual(result['excluded_predictions_ignored'],['A/x'])

class MatlabBuildBands(unittest.TestCase):
    def dep(self,**kwargs):return dict(delivery='source',version_managed=False,release_baseline=False,version_locked=False,interface_component=False,**kwargs)
    def test_all_contract_bands_and_mixed_closure(self):
        source=self.dep();binary=dict(source,delivery='protected_model');interface=dict(source,interface_component=True);stable=dict(source,version_managed=True,release_baseline=True,version_locked=True)
        self.assertEqual([build_independence(x) for x in [[],[source],[binary],[interface],[stable],[stable,source]]],[3,0,1,2,3,0])
    def test_unknown_never_fabricates_zero_or_three(self):
        for x in [None,['unclassified'],[{'delivery':'source'}],[dict(self.dep(),version_locked='yes')]]:self.assertIsNone(build_independence(x))

if __name__=='__main__':unittest.main()
