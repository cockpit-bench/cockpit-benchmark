"""Synthetic execution records test binding, not an actual Android test run."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

source = Path(__file__).resolve().parents[1]/'scripts/verification'
sys.path.insert(0,str(source if source.exists() else Path(__file__).resolve().parent))
import verify
from rules import integration, Missing


class IntegrationExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.repo=self.root/'repo';self.repo.mkdir()
        subprocess.check_call(['git','init','-q',str(self.repo)])
        (self.repo/'.gitattributes').write_text('* -text\n')
        workflow=self.repo/'.github/workflows/android.yml';workflow.parent.mkdir(parents=True)
        workflow.write_text('name: synthetic fixture\nsteps:\n  - run: adb shell am instrument fixture.Runner\n')
        (self.repo/'Service.java').write_text('class Service {}\n')
        subprocess.check_call(['git','-C',str(self.repo),'add','.'])
        subprocess.check_call(['git','-C',str(self.repo),'-c','user.name=Fixture','-c','user.email=fixture@invalid.local','commit','-qm','synthetic source'])
        self.head=verify.git(self.repo,'rev-parse','HEAD').decode().strip()
        self.snap=verify.Snapshot(self.repo,self.head)
        self.data=self.root/'data';self.data.mkdir()
        raw=b'Synthetic runner output; no Android execution is claimed by this fixture.\n'
        (self.data/'runner.txt').write_bytes(raw)
        self.e=dict(revision=self.head,mode='local',runtime='android_emulator',runtime_environment='Synthetic Android 35 emulator fixture',target_id='fixture-emulator',
                    android_api=35,build_fingerprint='synthetic/fingerprint',runner='fixture.Runner',
                    command='adb shell am instrument fixture.Runner',status='completed',
                    objectives='Verify service to manager delivery',expected_outcomes='Observed payload equals input',
                    tests_passed=2,tests_failed=0,tests_skipped=0,tests_total=2,pass_ratio=1.0,
                    coverage=dict(name='critical edge proxy',definition='Unique exercised directed component edges / declared critical edges',
                                  scope='fixture service-manager-routing components',all_edges=[['Service','Manager'],['Manager','Router']],
                                  covered_edges=[['Service','Manager']],numerator=1,denominator=2,ratio=0.5,threshold=0.5),
                    artifacts=[dict(path='runner.txt',sha256=verify.sha(raw),kind='runner_log',summary='Synthetic runner fixture')],
                    report_path='execution.json',report_sha256='0'*64)
        self.f=dict(valid_integration_assertions_and_interface_behavior=True,
                    final_head_android_integration_execution_exists=True,evaluation_revision=self.head,integration_execution=self.e)
        self.package={'files_sha256':{'runner.txt':verify.sha(raw)}}
        self.publish()

    def publish(self):
        body=verify.encoded({k:v for k,v in self.e.items() if k not in {'report_path','report_sha256'}})
        self.e['report_sha256']=verify.sha(body)
        (self.data/self.e['report_path']).write_bytes(body)
        self.package['files_sha256'][self.e['report_path']]=verify.sha(body)

    def checked_prediction(self):
        verify.check_integration_execution(self.f,self.snap,self.data,self.package)
        return verify.compute_leaf({'name':'quality.integration_test','method':'contract_rule_mapping','facts':self.f})

    def remote(self):
        path='.github/workflows/android.yml'
        self.e.update(mode='remote_ci',ci=dict(provider='fixture-ci',run_id='42',run_url='https://ci.invalid/runs/42',
                      revision=self.head,workflow_path=path,workflow_blob=self.snap.entries[path]['oid'],
                      workflow_sha256=verify.sha(self.snap.body(path)),job_id='integration',job_conclusion='success'))
        self.publish()

    def test_local_and_ci_reports_bound_to_actual_git_snapshot(self):
        self.assertEqual(self.checked_prediction(),3)
        self.remote();self.assertEqual(self.checked_prediction(),3)

    def test_host_reports_bind_without_claiming_device_execution(self):
        # This is a synthetic report/binding test, not evidence of executing its tests.
        for key in ['target_id','android_api','build_fingerprint']:del self.e[key]
        self.f['final_head_integration_execution_exists']=True
        self.f['final_head_android_integration_execution_exists']=False
        for runtime,environment,command in [('host_jvm','Synthetic OpenJDK 17 / Robolectric 4 fixture','./gradlew integrationTest'),
                                            ('host_native','Synthetic Linux x86_64 / gtest fixture','./integration_tests')]:
            self.e.update(runtime=runtime,runtime_environment=environment,command=command)
            self.publish();self.assertEqual(self.checked_prediction(),3)
            self.e.update(tests_passed=3,tests_failed=1,tests_total=4,pass_ratio=0.75)
            self.publish();self.assertEqual(self.checked_prediction(),2)
            self.e.update(tests_passed=2,tests_failed=0,tests_total=2,pass_ratio=1)
        self.e['runtime']='android_device';self.publish()
        with self.assertRaises(Missing):self.checked_prediction()

    def test_host_needs_environment_real_behavior_and_complete_coverage(self):
        self.e.update(runtime='host_jvm',runtime_environment='Synthetic OpenJDK 17 fixture');self.publish()
        self.f['valid_integration_assertions_and_interface_behavior']=False
        self.assertEqual(self.checked_prediction(),0)
        self.f['valid_integration_assertions_and_interface_behavior']=True
        self.e['runtime_environment']=' ';self.publish()
        with self.assertRaises(Missing):self.checked_prediction()
        self.e['runtime_environment']='Synthetic OpenJDK 17 fixture'
        self.e['coverage']['scope']='';self.publish()
        with self.assertRaises(Missing):self.checked_prediction()

    def test_generic_execution_flag_takes_precedence_over_historical_alias(self):
        self.f['final_head_integration_execution_exists']=False
        with self.assertRaises(Missing):self.checked_prediction()
        self.f['final_head_integration_execution_exists']=True
        del self.f['final_head_android_integration_execution_exists']
        self.assertEqual(self.checked_prediction(),3)

    def test_partial_pass_skip_and_coverage_are_recomputed(self):
        self.e.update(tests_passed=3,tests_failed=1,tests_total=4,pass_ratio=0.75);self.publish()
        self.assertEqual(self.checked_prediction(),2)
        self.e.update(tests_passed=3,tests_failed=0,tests_skipped=1,pass_ratio=0.75);self.publish()
        self.assertEqual(self.checked_prediction(),2)
        self.e.update(tests_passed=2,tests_failed=1,tests_skipped=1,pass_ratio=0.5);self.publish()
        self.assertEqual(self.checked_prediction(),1)
        self.e.update(tests_passed=4,tests_failed=0,tests_skipped=0,pass_ratio=1)
        self.e['coverage'].update(covered_edges=[],numerator=0,ratio=0);self.publish()
        self.assertEqual(self.checked_prediction(),1)

    def test_no_execution_stays_one_and_bare_true_cannot_promote(self):
        f={'valid_integration_assertions_and_interface_behavior':True}
        verify.check_integration_execution(f,self.snap,self.data,self.package)
        self.assertEqual(integration(f),1)
        f.update(final_head_android_integration_execution_exists=False)
        self.assertEqual(integration(f),1)
        f.update(final_head_android_integration_execution_exists=True,majority_tests_pass=True,
                 defined_key_interaction_coverage_ratio=1,executed_test_pass_ratio=1)
        with self.assertRaises(Missing):verify.check_integration_execution(f,self.snap,self.data,self.package)
        with self.assertRaises(Missing):integration(f)

    def test_positive_claim_requires_report_file_and_package_hash(self):
        del self.package['files_sha256']['execution.json']
        with self.assertRaisesRegex(ValueError,'Unhashed'):self.checked_prediction()
        self.publish();(self.data/'execution.json').unlink()
        with self.assertRaises(FileNotFoundError):self.checked_prediction()

    def test_report_bytes_hash_and_field_binding_are_checked(self):
        (self.data/'execution.json').write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError,'hash differs'):self.checked_prediction()
        self.publish();self.e['command']='different command'
        with self.assertRaisesRegex(ValueError,'binding differs'):self.checked_prediction()
        self.publish();self.package['files_sha256']['execution.json']='d'*64
        with self.assertRaisesRegex(ValueError,'hash differs'):self.checked_prediction()

    def test_artifacts_require_listing_bytes_digest_and_summary(self):
        del self.package['files_sha256']['runner.txt']
        with self.assertRaisesRegex(ValueError,'Unhashed'):self.checked_prediction()
        self.package['files_sha256']['runner.txt']=self.e['artifacts'][0]['sha256']
        (self.data/'runner.txt').write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError,'hash differs'):self.checked_prediction()
        self.e['artifacts'][0]['summary']=''
        with self.assertRaises(Missing):self.checked_prediction()

    def test_head_runtime_mode_and_incomplete_records_fail_closed(self):
        for key,value in [('runtime','unclassified'),('runtime_environment',''),('mode','unclassified'),('status','running'),('android_api',True),
                          ('command',' '),('target_id',''),('objectives',''),('tests_passed',True)]:
            previous=self.e[key];self.e[key]=value;self.publish()
            with self.subTest(key=key),self.assertRaises(Missing):self.checked_prediction()
            self.e[key]=previous
        self.e['revision']='a'*40;self.f['evaluation_revision']='a'*40;self.publish()
        with self.assertRaisesRegex(ValueError,'HEAD differs'):self.checked_prediction()

    def test_false_declaration_cannot_hide_completed_execution(self):
        self.f['final_head_android_integration_execution_exists']=False
        with self.assertRaises(Missing):self.checked_prediction()

    def test_inconsistent_math_and_edge_sets_are_rejected(self):
        original=copy.deepcopy(self.e)
        mutations=[('tests_total',3),('tests_failed',-1),('tests_skipped',1),('pass_ratio',0.75),
                   ('coverage.denominator',3),('coverage.numerator',2),('coverage.ratio',float('nan')),
                   ('coverage.threshold',0.1),('coverage.all_edges',[]),
                   ('coverage.all_edges',[['Service','Manager'],['Service','Manager']]),
                   ('coverage.covered_edges',[['Unknown','Manager']]),('coverage.covered_edges',[['Service','Service']])]
        for key,value in mutations:
            self.e.clear();self.e.update(copy.deepcopy(original))
            if '.' in key:self.e['coverage'][key.split('.')[1]]=value
            else:self.e[key]=value
            self.publish()
            with self.subTest(key=key,value=value),self.assertRaises(Missing):self.checked_prediction()

    def test_legacy_numeric_claims_must_agree_with_report(self):
        for key,value in [('majority_tests_pass',False),('executed_test_pass_ratio',0.8),('defined_key_interaction_coverage_ratio',1)]:
            self.f[key]=value
            with self.subTest(key=key),self.assertRaises(Missing):self.checked_prediction()
            del self.f[key]

    def test_ci_metadata_and_actual_workflow_binding_are_required(self):
        self.remote();original=copy.deepcopy(self.e['ci'])
        for key in ['provider','run_id','run_url','revision','workflow_path','workflow_blob','workflow_sha256','job_id','job_conclusion']:
            self.e['ci']=copy.deepcopy(original);del self.e['ci'][key];self.publish()
            with self.subTest(missing=key),self.assertRaises(Missing):self.checked_prediction()
        for key,value in [('revision','a'*40),('job_conclusion','cancelled')]:
            self.e['ci']=copy.deepcopy(original);self.e['ci'][key]=value;self.publish()
            with self.subTest(key=key),self.assertRaises(Missing):self.checked_prediction()
        for key,value in [('workflow_blob','a'*40),('workflow_sha256','a'*64),('workflow_path','Service.java')]:
            self.e['ci']=copy.deepcopy(original);self.e['ci'][key]=value;self.publish()
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'workflow'):self.checked_prediction()


if __name__=='__main__':unittest.main()
