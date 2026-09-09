"""Registry state, publication gates and real Git restoration regressions."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import suites

WRAPPER=Path(__file__).resolve().parents[1]

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'wrapper'
        self.root.mkdir()
        # Copy only metadata needed for these tests, never source/model payloads.
        for name in ['suites.json','manifest.json','STANDARD_SCORES.json','SCORE_RULES.md','suites']:
            src=WRAPPER/name;dst=self.root/name
            if src.is_dir():shutil.copytree(src,dst)
            else:shutil.copyfile(src,dst)

    def tearDown(self):self.temp.cleanup()

    def registry(self):return suites.read(self.root/'suites.json')
    def save(self,registry):(self.root/'suites.json').write_bytes(suites.encoded(registry))
    def change_artifact(self,registry,field,edit):
        entry=registry['suites'][1][field];p=self.root/entry['path'];value=suites.read(p)
        edit(value);p.write_bytes(suites.encoded(value));entry['sha256']=suites.sha(p.read_bytes())

    def test_finalized_local_state_is_valid(self):
        result=suites.validate(self.root)
        self.assertEqual(result['suites'][0]['score'], sum(r['total']['score'] for r in suites.read(self.root/'STANDARD_SCORES.json')['repositories']))
        self.assertEqual(result['suites'][1]['score'],338)
        if result['integration_status']!='published':
            with self.assertRaises(suites.InvalidSuite):suites.validate(self.root,True)

    def test_unready_matlab_and_all_fail_before_mutation_or_network(self):
        r=self.registry();r['integration_status']='prepared_not_published';r['suites'][1]['status']='verified_local';self.save(r)
        for choice in ['matlab-simulink','all']:
            destination=Path(self.temp.name)/choice
            with patch.object(suites,'git',side_effect=AssertionError('Network must not run')):
                with self.assertRaises(suites.InvalidSuite):suites.restore(self.root,choice,destination)
            self.assertFalse(destination.exists())

    def test_source_score_head_mismatch_is_rejected_after_rehash(self):
        r=self.registry()
        self.change_artifact(r,'canonical_scores',lambda s:s['repos'][0].update(head='1'*40))
        self.save(r)
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)

    def test_missing_native_cannot_be_hidden(self):
        r=self.registry()
        self.change_artifact(r,'readiness',lambda s:s['native_passed_ids'].remove('ML-05-B'))
        self.save(r)
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)

    def test_status_flag_cannot_promote_review(self):
        r=self.registry();r['suites'][1]['status']='published';r['suites'][1]['canonical_scores']=None
        self.change_artifact(r,'readiness',lambda s:s.update(status='published',canonical_ready=True,publication_ready=True))
        self.save(r)
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)
        # A rehashed completion summary cannot replace the complete evidence graph.
        r['suites'][1].update(published_repositories=9,score=338,version='v0.9.0',
                             release_url='https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.9.0')
        self.save(r)
        self.change_artifact(r,'readiness',lambda s:s.update(evidence_index={'path':'missing-raw-evidence.json','sha256':'0'*64}))
        self.save(r)
        with self.assertRaises((suites.InvalidSuite,KeyError)):suites.validate(self.root,True)

    def test_unknown_totals_and_cross_suite_ids_are_rejected(self):
        r=self.registry();r['total']=609;self.save(r)
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)
        del r['total']
        self.change_artifact(r,'manifest',lambda s:s['repositories'][0].update(id='APP-01'))
        self.save(r)
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)

    def test_changed_contract_bytes_and_path_escape_are_rejected(self):
        r=self.registry();p=self.root/'suites/matlab-simulink/SCORING_OVERRIDES.md'
        p.write_bytes(p.read_bytes()+b'changed')
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)
        for name in ['../other.json','C:/other.json','x/../../other.json','/tmp/other.json']:
            with self.assertRaises(suites.InvalidSuite):suites.safe_path(self.root,name)

    def test_non_contract_score_rejected_even_when_total_updated(self):
        r=self.registry()
        def mutate(s):
            row=s['repos'][0];row['scores']['unit_test']=4
            row['total']=sum(row['scores'].values());s['total']=sum(x['total'] for x in s['repos'])
        self.change_artifact(r,'canonical_scores',mutate);self.save(r)
        with self.assertRaises(suites.InvalidSuite):suites.validate(self.root)

    def test_all_dispatches_separate_destinations_and_preserves_options(self):
        registry=self.registry()
        destination=Path(self.temp.name)/'all-target'
        with patch.object(suites,'validate',return_value=registry), patch.object(suites.shutil,'which',return_value='powershell'), \
             patch.object(suites.subprocess,'run') as powershell, patch.object(suites,'restore_matlab') as matlab:
            suites.restore(self.root,'all',destination,resume=True,include_submodules=True)
        command=powershell.call_args.args[0]
        self.assertIn(str(destination/'android-validation18'),command)
        self.assertIn('-Resume',command);self.assertIn('-IncludeSubmodules',command)
        self.assertEqual(matlab.call_args.args[1],destination/'matlab-simulink')
        self.assertTrue(matlab.call_args.args[2])

class RestoreTests(unittest.TestCase):
    def test_git_restore_and_resume_validate_full_inventory_and_refs(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';source.mkdir()
            suites.git('init','-b','main',source)
            (source/'sample.txt').write_bytes(b'first\n');suites.git('-C',source,'add','sample.txt')
            suites.git('-C',source,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','first')
            suites.git('-C',source,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','tag','-a','v1','-m','frozen')
            suites.git('-C',source,'branch','platform/test')
            (source/'sample.txt').write_bytes(b'second\n');suites.git('-C',source,'add','sample.txt')
            suites.git('-C',source,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','second')
            refs=[]
            for line in suites.git('-C',source,'for-each-ref','--format=%(refname)|%(objectname)|%(objecttype)','refs/heads','refs/tags').splitlines():
                ref,oid,kind=line.split('|')
                refs.append(dict(ref=ref,object_oid=oid,object_type=kind,
                    commit_oid=suites.git('-C',source,'rev-parse',ref+'^{commit}'),tree_oid=suites.git('-C',source,'rev-parse',ref+'^{tree}')))
            body=b'second\n';blob=suites.git('-C',source,'rev-parse','HEAD:sample.txt')
            files=[dict(path='sample.txt',mode='100644',blob=blob,bytes=len(body),sha256=suites.sha(body))]
            digest=suites.sha(json.dumps(files,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
            url='https://github.com/cockpit-bench/suite-fixture.git'
            row=dict(id='ML-01',name='suite-fixture',head=suites.git('-C',source,'rev-parse','HEAD'),
                tree=suites.git('-C',source,'rev-parse','HEAD^{tree}'),refs=refs,files_sha256=digest,repository_url=url)
            original=suites.git
            # Redirect only the fixture transport; run real clone/fetch/fsck and checks.
            def transport(*args,**kwargs):
                value=original(*(str(source) if x==url else x for x in args),**kwargs)
                return url if args[-3:]==('remote','get-url','origin') and value==str(source) else value
            destination=root/'restored'
            with patch.object(suites,'git',side_effect=transport):
                result=suites.restore_matlab([row],destination)
                self.assertEqual(result[0]['head'],row['head'])
                self.assertFalse(result[0]['model_execution'])
                self.assertEqual(suites.restore_matlab([row],destination,True),result)
                (destination/row['name']/'sample.txt').write_bytes(b'modified\n')
                with self.assertRaises(suites.InvalidSuite):suites.restore_matlab([row],destination,True)
            interrupted=root/'interrupted';failed=False
            def interrupt_fetch(*args,**kwargs):
                nonlocal failed
                if 'fetch' in args and not failed:
                    failed=True
                    raise subprocess.CalledProcessError(1,['git','fetch'],stderr=b'fixture interruption')
                return transport(*args,**kwargs)
            with patch.object(suites,'git',side_effect=interrupt_fetch):
                with self.assertRaises(subprocess.CalledProcessError):suites.restore_matlab([row],interrupted)
                self.assertEqual(suites.restore_matlab([row],interrupted,True),result)

if __name__=='__main__':unittest.main()
