"""Synthetic governance gates; no Android execution or semantic audit implied."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/verification'))
from rules import api, Missing
from verify import check_api_governance, sha, encoded


def fixture():
    body=b'interface Public {}\nclass Consumer {}\n'
    anchors=[dict(source='repository',path='api.java',commit='a'*40,
                  start_line=i,end_line=i,symbol=s,source_sha256=sha(body))
             for i,s in [(1,'Public'),(2,'Consumer')]]
    boundary=dict(id='sdk',type='java',role='provided',owner='SDK',consumer='separate client',
        critical=True,owns_contract=True,scope_basis='Separately published production SDK consumed by client',
        version_baseline='released API',mechanism='real source extraction and compatibility diff',
        covered=True,version_controlled=True,real_compatibility_check=True,
        fixed_external_responsibility_verified=False,current_binding='current source target',
        released_binding='released baseline target',coverage_reason='entire SDK signature scope',evidence=anchors)
    return dict(evaluation_revision='a'*40,semantic_api_versioning=False,manual_api_version_exists=True,
        api_governance=dict(revision='a'*40,inventory_complete=True,unresolved=[],
                            scope_basis='Build and production consumer inventory',boundaries=[boundary]))


class ApiGovernanceTests(unittest.TestCase):
    def test_all_and_partial_coverage(self):
        f=fixture();self.assertEqual(api(f),3)
        uncovered=copy.deepcopy(f['api_governance']['boundaries'][0])
        uncovered.update(id='binder',covered=False,real_compatibility_check=False)
        f['api_governance']['boundaries'].append(uncovered)
        self.assertEqual(api(f),2)

    def test_versions_without_real_compatibility(self):
        f=fixture();f['api_governance']['boundaries'][0].update(covered=False,real_compatibility_check=False)
        self.assertEqual(api(f),1)
        f['manual_api_version_exists']=False;self.assertEqual(api(f),0)
        f['semantic_api_versioning']=True;self.assertEqual(api(f),2)

    def test_old_flags_and_unknown_scope_do_not_score(self):
        with self.assertRaises(Missing):api(dict(api_version_controlled=True,real_public_api_or_abi_compatibility_diff=True))
        for key,value in [('inventory_complete',False),('unresolved',['HAL']),('boundaries',[]),('revision','b'*40)]:
            f=fixture();f['api_governance'][key]=value
            with self.subTest(key=key),self.assertRaises(Missing):api(f)

    def test_invalid_covered_claims_and_bindings(self):
        for key,value in [('version_controlled',False),('real_compatibility_check',False),
                          ('critical',False),('current_binding',''),('released_binding',''),('covered','true')]:
            f=fixture();f['api_governance']['boundaries'][0][key]=value
            with self.subTest(key=key),self.assertRaises(Missing):api(f)

    def test_external_responsibility_cannot_cover_owned_provider(self):
        f=fixture();b=f['api_governance']['boundaries'][0]
        b.update(real_compatibility_check=False,fixed_external_responsibility_verified=True)
        with self.assertRaises(Missing):api(f)
        b['role']='consumed';b['owns_contract']=False;self.assertEqual(api(f),3)
        other=copy.deepcopy(b);other.update(id='other',covered=False,fixed_external_responsibility_verified=False)
        f['api_governance']['boundaries'].append(other)
        self.assertEqual(api(f),2)  # verified external compatibility responsibility is partial governance

    def test_external_defined_provider_can_delegate_definition_governance(self):
        f=fixture();b=f['api_governance']['boundaries'][0]
        b.update(role='provided',owns_contract=False,real_compatibility_check=False,
                 fixed_external_responsibility_verified=True,owner='external IDL owner; local implementation')
        self.assertEqual(api(f),3)

    def test_duplicate_or_excluded_inventory_cannot_create_full_coverage(self):
        f=fixture();f['api_governance']['boundaries']*=2
        with self.assertRaises(Missing):api(f)
        f=fixture();f['api_governance']['boundaries'][0].update(critical=False,covered=False,real_compatibility_check=False)
        self.assertEqual(api(f),1)

    def test_source_evidence_is_bound_to_current_head_and_bytes(self):
        class Snapshot:
            head='a'*40
            def body(self,path):return b'interface Public {}\nclass Consumer {}\n'
        f=fixture();check_api_governance(f,Snapshot())
        for key,value in [('commit','b'*40),('source_sha256','0'*64),('symbol','Missing')]:
            f=fixture();f['api_governance']['boundaries'][0]['evidence'][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):check_api_governance(f,Snapshot())
        f=fixture();b=f['api_governance']['boundaries'][0];b['evidence']=[b['evidence'][0]]*2
        with self.assertRaises(ValueError):check_api_governance(f,Snapshot())

    def test_pack_inventory_is_bound_and_cannot_be_silently_removed(self):
        class Snapshot:
            head='a'*40
            entries={'api.java':{}}
            def body(self,path):return b'interface Public {}\nclass Consumer {}\n'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);f=fixture();package={'files_sha256':{}}
            with self.assertRaises(ValueError):check_api_governance(f,Snapshot(),root,package)
            body=encoded(dict(head='a'*40,tracked_paths_sha256=sha(encoded(['api.java']))))
            (root/'inventory.json').write_bytes(body)
            f['api_governance']['source_inventory']=dict(path='inventory.json',sha256=sha(body))
            package['files_sha256']['inventory.json']=sha(body)
            check_api_governance(f,Snapshot(),root,package)
            (root/'inventory.json').write_bytes(body+b' ')
            with self.assertRaises(ValueError):check_api_governance(f,Snapshot(),root,package)

    def test_binding_artifact_bytes_and_git_object_are_checked(self):
        class Snapshot:
            head='a'*40
            entries={'api.java':{'oid':'b'*40}}
            def body(self,path):return b'interface Public {}\nclass Consumer {}\n'
        f=fixture();b=f['api_governance']['boundaries'][0]
        b['binding_files']=[dict(path='api.java',commit='a'*40,git_blob='b'*40,
                                 source_sha256=sha(Snapshot().body('api.java')))]
        check_api_governance(f,Snapshot())
        b['binding_files'][0]['git_blob']='c'*40
        with self.assertRaises(ValueError):check_api_governance(f,Snapshot())


if __name__=='__main__':unittest.main()
