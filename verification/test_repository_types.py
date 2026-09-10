"""Current business classification, publication and scoped restore regressions."""
import copy,json,shutil,subprocess,tempfile,unittest,os
from pathlib import Path
from unittest.mock import patch
import repository_types as rt
import suites

W=Path(__file__).resolve().parents[1]

class TypeRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'wrapper';self.root.mkdir()
        for name in ['suites','suites.json','manifest.json','STANDARD_SCORES.json','SCORE_RULES.md']:
            source=W/name;target=self.root/name
            shutil.copytree(source,target) if source.is_dir() else shutil.copyfile(source,target)
    def tearDown(self):self.temp.cleanup()
    def registry(self):return suites.read(self.root/'suites.json')
    def save(self,r):(self.root/'suites.json').write_bytes(suites.encoded(r))
    def alter(self,r,kind,field,mutation):
        entry=next(e for e in r['suites'] if e['id']==kind)[field];path=self.root/entry['path'];value=suites.read(path)
        mutation(value);path.write_bytes(suites.encoded(value));entry['sha256']=suites.sha(path.read_bytes());self.save(r)
    def test_three_separate_populations(self):
        r=rt.validate(self.root)
        self.assertEqual([s['id'] for s in r['suites']],['app','fw','new-energy-matlab'])
        self.assertEqual([s['repository_count'] for s in r['suites']],[11,11,11])
        self.assertEqual([s['leaf_count'] for s in r['suites']],[88,121,143])
        for entry in r['suites']:
            sources=suites.read(self.root/entry['manifest']['path'])['repositories']
            self.assertEqual(entry['published_repositories'],sum(s['publication_status']=='published' for s in sources))
        has_local=any(any(c['status']!='published' for c in suites.read(self.root/entry['cohorts']['path'])['cohorts']) for entry in r['suites'] if 'cohorts' in entry)
        if has_local:
            with self.assertRaisesRegex(suites.InvalidSuite,'unpublished local cohort'):
                rt.validate(self.root,True)
        else:self.assertEqual(rt.validate(self.root,True)['integration_status'],'published')
    def test_unpublished_cohort_still_blocks_publication(self):
        r=self.registry();entry=next(e for e in r['suites'] if 'cohorts' in e);binding=entry['cohorts'];p=self.root/binding['path']
        catalog=suites.read(p);catalog['cohorts'][-1]['status']='verified_local';p.write_bytes(suites.encoded(catalog));binding['sha256']=suites.sha(p.read_bytes());self.save(r)
        with self.assertRaisesRegex(suites.InvalidSuite,'unpublished local cohort'):rt.validate(self.root,True)
    def test_legacy_registry_remains_publishable_without_local_cohort(self):
        r=self.registry()
        # Exercise a published fixture independently of the current local
        # repair snapshot; do not treat its new source commits as published.
        entry=next(e for e in r['suites'] if e['id']=='new-energy-matlab')
        p=self.root/entry['manifest']['path'];manifest=suites.read(p)
        for source in manifest['repositories']:source['publication_status']='published'
        p.write_bytes(suites.encoded(manifest));entry['manifest']['sha256']=suites.sha(p.read_bytes())
        entry.update(status='published',published_repositories=len(manifest['repositories']))
        r['integration_status']='published'
        for entry in r['suites']:entry.pop('cohorts',None)
        self.save(r)
        self.assertEqual(rt.validate(self.root,True)['integration_status'],'published')
    def test_no_combined_score_or_generic_matlab_type(self):
        r=self.registry();r['score']=999;self.save(r)
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
        del r['score'];r['suites'][2]['name']='MATLAB';self.save(r)
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
    def test_selection_stays_in_business_type(self):
        r=rt.validate(self.root)
        self.assertTrue(all(s['id'].startswith('APP-') for s in rt.select(r,self.root,'app')))
        self.assertEqual(len(rt.select(r,self.root,'fw')),11)
        self.assertEqual(len(rt.select(r,self.root,'android-validation18')),22)
        self.assertEqual(len(rt.select(r,self.root,'all')),33)
        with self.assertRaises(suites.InvalidSuite):rt.select(r,self.root,'app',['FW-21'])
    def test_rehashed_head_change_is_rejected(self):
        r=self.registry();self.alter(r,'app','manifest',lambda m:m['repositories'][-1].update(head='1'*40))
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
    def test_rehashed_leaf_rename_is_rejected(self):
        r=self.registry();self.alter(r,'fw','canonical_scores',lambda s:s['repositories'][-1]['reference']['leaves'][0].update(name='invented.metric'))
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
    def test_legacy_whole_reference_preserved(self):
        r=self.registry();self.alter(r,'app','canonical_scores',lambda s:s['repositories'][0]['reference'].update(extra_unreviewed_note='changed'))
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
    def test_pending_ids_cannot_be_admitted(self):
        r=self.registry();self.alter(r,'app','manifest',lambda s:s['repositories'][-1].update(id='APP-04'))
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root)
    def test_unpublished_inputs_fail_before_network_or_destination(self):
        r=self.registry();r['integration_status']='local_expansion'
        entry=next(e for e in r['suites'] if e['id']=='app')
        entry.update(status='verified_local',published_repositories=10)
        self.alter(r,'app','manifest',lambda m:m['repositories'][-1].update(publication_status='verified_local',repository_url=None))
        with self.assertRaises(suites.InvalidSuite):rt.validate(self.root,True)
        dest=Path(self.temp.name)/'output'
        with patch.object(rt,'git',side_effect=AssertionError('No network or Git action allowed')):
            with self.assertRaises(suites.InvalidSuite):rt.restore(self.root,'all',dest)
        self.assertFalse(dest.exists())
    def test_current_aliases_do_not_falsely_claim_original_count(self):
        r=rt.validate(self.root)
        self.assertEqual({s['type_id'] for s in rt.select(r,self.root,'matlab-simulink')},{'new-energy-matlab'})
        self.assertEqual(len(rt.select(r,self.root,'matlab-simulink')),11)

class LocalRestoreTests(unittest.TestCase):
    def test_reality_restore_preserves_bytes_with_windows_autocrlf(self):
        expected=rt.git('-C',self.origin,'show','HEAD:logic.txt',binary=True)
        self.row.update(cohort_id='reality-proxy-20260910',files={'logic.txt':rt.sha(expected)})
        config=self.base/'global-config';config.write_text('[core]\n autocrlf = true\n')
        with patch.dict(os.environ,{'GIT_CONFIG_GLOBAL':str(config)}):self.restore()
        self.assertEqual((self.dest/'sample-app/logic.txt').read_bytes(),expected)
        self.assertEqual(rt.git('-C',self.dest/'sample-app','config','core.autocrlf'),'false')
    def test_git_clean_does_not_hide_reality_file_byte_drift(self):
        expected=rt.git('-C',self.origin,'show','HEAD:logic.txt',binary=True)
        self.row.update(cohort_id='reality-proxy-20260910',files={'logic.txt':rt.sha(expected)})
        self.restore();target=self.dest/'sample-app'
        rt.git('-C',target,'config','core.autocrlf','true')
        (target/'logic.txt').write_bytes(expected.replace(b'\n',b'\r\n'))
        # Re-normalizing into the index keeps the committed blob identical.
        rt.git('-C',target,'add','logic.txt')
        self.assertFalse(rt.git('-C',target,'status','--porcelain'))
        with self.assertRaisesRegex(suites.InvalidSuite,'file bytes differ'):self.restore(resume=True)
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name);self.origin=self.base/'source';self.origin.mkdir()
        def git(*args):return subprocess.check_output(['git','-C',str(self.origin),*args],stderr=subprocess.STDOUT,text=True).strip()
        self.git=git;git('init','-b','main');git('config','core.autocrlf','false');git('config','user.name','Restore test');git('config','user.email','restore@example.invalid')
        (self.origin/'logic.txt').write_bytes(b'first\n');git('add','.');git('commit','-m','first');git('tag','v1')
        (self.origin/'logic.txt').write_bytes(b'second\n');git('add','.');git('commit','-m','second')
        self.row={'id':'APP-21','name':'sample-app','type_id':'app','head':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}'),'refs':{k:v for k,v in (x.split('|') for x in git('for-each-ref','--format=%(refname)|%(objectname)','refs/heads','refs/tags').splitlines())},'publication_status':'verified_local','repository_url':None}
        self.mapping=self.base/'source-map.json';self.mapping.write_text(json.dumps({'APP-21':str(self.origin)}));self.wrapper=self.base/'wrapper';self.wrapper.mkdir();self.dest=self.base/'restored'
    def tearDown(self):self.temp.cleanup()
    def restore(self,**kwargs):
        with patch.object(rt,'validate',return_value={}),patch.object(rt,'select',return_value=[self.row]):
            return rt.restore(self.wrapper,'app',self.dest,source_map=self.mapping,**kwargs)
    def test_full_independent_history_refs_and_clean_remote_free_restore(self):
        result=self.restore();self.assertEqual(len(result),1);target=self.dest/'sample-app'
        self.assertEqual(subprocess.check_output(['git','-C',str(target),'rev-list','--count','HEAD'],text=True).strip(),'2')
        self.assertFalse((target/'.git/objects/info/alternates').exists());self.assertEqual(rt.check_source(target,self.row)['remote_count'],0)
        self.assertEqual(len(self.restore(resume=True,include_submodules=True)),1)
    def test_resume_refuses_user_edits(self):
        self.restore();(self.dest/'sample-app/logic.txt').write_text('user change\n')
        with self.assertRaises(suites.InvalidSuite):self.restore(resume=True)
        self.assertEqual((self.dest/'sample-app/logic.txt').read_text(),'user change\n')
    def test_ref_drift_is_rejected_before_destination(self):
        self.git('tag','unadvertised')
        with self.assertRaises(suites.InvalidSuite):self.restore()
        self.assertFalse(self.dest.exists())
    def test_completed_legacy_marker_survives_evidence_metadata_revision(self):
        self.row['evidence']={'path':'old-evidence.json','sha256':'b'*64}
        self.restore();marker=self.dest/'.restore-APP-21.json'
        marker.write_bytes(rt.encoded({'binding':rt.sha(rt.encoded(self.row)),'phase':'complete'}))
        self.row['evidence']={'path':'new-evidence.json','sha256':'a'*64}
        self.assertEqual(len(self.restore(resume=True)),1)
        self.assertEqual(rt.read(marker)['binding'],rt.restore_binding(self.row))
    def test_changed_incomplete_legacy_marker_is_not_rebound(self):
        self.row['evidence']={'path':'old-evidence.json','sha256':'b'*64}
        self.restore();marker=self.dest/'.restore-APP-21.json'
        old={'binding':rt.sha(rt.encoded(self.row)),'phase':'cloning'};marker.write_bytes(rt.encoded(old))
        self.row['evidence']={'path':'new-evidence.json','sha256':'a'*64}
        with self.assertRaisesRegex(suites.InvalidSuite,'Restore progress differs'):self.restore(resume=True)
        self.assertEqual(rt.read(marker),old)
    def test_completed_legacy_marker_cannot_hide_source_edits(self):
        self.restore();marker=self.dest/'.restore-APP-21.json'
        old={'binding':'0'*64,'phase':'complete'};marker.write_bytes(rt.encoded(old))
        (self.dest/'sample-app/logic.txt').write_text('user change\n')
        with self.assertRaises(suites.InvalidSuite):self.restore(resume=True)
        self.assertEqual(rt.read(marker),old)

if __name__=='__main__':unittest.main()
