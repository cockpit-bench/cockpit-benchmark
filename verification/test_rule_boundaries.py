"""Boundary regressions; synthetic rule inputs are not production execution claims."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts/verification'))
from rules import release, lsp, Missing
from coverage import analyze, render
from verify import check_substitution_execution, sha, encoded


def lsp_facts(implementations=1):
    return dict(parent_symbol='Device', child_symbols=['Impl'+str(i) for i in range(implementations)],
                empty_override_violation_count=0, unconditional_throw_violation_count=0,
                precondition_risk_count=0, postcondition_risk_count=0,
                multiple_unexplained_override_or_exception_risks=False,
                production_implementation_count=implementations, substitution_test_count=1,
                systematic_contract_tests_cover_exception_boundary_pre_post=True,
                evaluation_revision='a'*40)


def execution(facts, passed=None):
    children = facts['child_symbols'] if passed is None else passed
    return dict(revision=facts['evaluation_revision'], parent_symbol='Device', command='java ContractTest',
                status='passed', tests_passed=4, tests_failed=0,
                tested_implementations=children, passed_implementations=children,
                coverage=dict(exception=True, boundary=True, precondition=True, postcondition=True),
                report_path='executions/run.json', report_sha256='b'*64)


class RuleBoundaryTests(unittest.TestCase):
    def test_trunk_name_and_unrelated_branch_do_not_change_verified_policy(self):
        f=dict(ref_tree_differences_verify_release_policy=True, vehicle_specific_sop_channel=False,
               platform_shared_release_channel=False, cross_platform_unified_release_policy=True)
        for branches in [['refs/heads/main'], ['refs/heads/master'], ['refs/heads/trunk'],
                         ['refs/heads/main','refs/heads/develop']]:
            with self.subTest(branches=branches): self.assertEqual(release(dict(f,current_head_refs=branches)),10)
        self.assertEqual(release(dict(f, vehicle_specific_sop_channel=True)),3)
        self.assertEqual(release(dict(f, platform_shared_release_channel=True)),8)

    def test_absent_strategy_and_unknown_are_distinct(self):
        self.assertEqual(release({'current_head_refs':['refs/heads/main'], 'ref_tree_differences_verify_release_policy':False}),0)
        for f in [{'current_head_refs':['refs/heads/main']}, {'ref_tree_differences_verify_release_policy':None}]:
            with self.assertRaises(Missing): release(f)

    def test_test_count_or_coverage_flag_cannot_upgrade(self):
        for count in [0,1,100]:
            f=lsp_facts(); f['substitution_test_count']=count
            self.assertEqual(lsp(f),2)
        f=lsp_facts(2); self.assertEqual(lsp(f),3)

    def test_unrun_or_failed_execution_cannot_upgrade(self):
        for status in ['not_run','failed']:
            f=lsp_facts();f['substitution_execution']=dict(execution(f),status=status)
            self.assertEqual(lsp(f),2)

    def test_verified_execution_and_systematic_all_implementation_coverage(self):
        f=lsp_facts();f['substitution_execution']=execution(f);self.assertEqual(lsp(f),3)
        f=lsp_facts(2);f['substitution_execution']=execution(f);self.assertEqual(lsp(f),4)
        f['substitution_execution']['coverage']['exception']=False;self.assertEqual(lsp(f),3)
        f=lsp_facts(3);f['substitution_execution']=execution(f, ['Impl0','Impl1']);self.assertEqual(lsp(f),3)

    def test_stale_or_contradictory_positive_execution_rejected(self):
        for field,value in [('revision','c'*40),('tests_failed',1),('tests_passed',0),('parent_symbol','Other'),('passed_implementations',['Foreign'])]:
            f=lsp_facts();f['substitution_execution']=execution(f);f['substitution_execution'][field]=value
            with self.subTest(field=field), self.assertRaises(Missing): lsp(f)

    def test_execution_report_digest_and_revision_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'executions').mkdir();f=lsp_facts();e=execution(f)
            report={k:v for k,v in e.items() if k not in ['report_path','report_sha256']}
            body=encoded(report);e['report_sha256']=sha(body);f['substitution_execution']=e
            (root/e['report_path']).write_bytes(body);package={'files_sha256':{e['report_path']:sha(body)}}
            check_substitution_execution(f, f['evaluation_revision'], root, package)
            with self.assertRaisesRegex(ValueError,'revision'):check_substitution_execution(f,'d'*40,root,package)
            (root/e['report_path']).write_bytes(body+b' ')
            with self.assertRaisesRegex(ValueError,'hash'):check_substitution_execution(f,f['evaluation_revision'],root,package)
            (root/e['report_path']).write_bytes(body);e['tests_passed']=99
            with self.assertRaisesRegex(ValueError,'binding'):check_substitution_execution(f,f['evaluation_revision'],root,package)

    def test_coverage_prose_tracks_positive_absent_and_unknown(self):
        leaf='quality.integration_test'
        standard={'version':'fixture','repositories':[]};observations={}
        for i,state in enumerate([True,False,None]):
            rid='FW-'+str(i);standard['repositories'].append({'id':rid,'kind':'FRAMEWORK','leaves':[{'name':leaf,'score':1,'status':'scored'}]})
            observations[(rid,leaf)]={'facts':{'final_head_android_integration_execution_exists':state},'evidence':[],'method':'fixture'}
        text=render(analyze(standard,observations))
        self.assertIn('recorded 1，absent 1，未分类 1',text)
        self.assertNotIn('均为 absent',text)


if __name__ == '__main__': unittest.main()
