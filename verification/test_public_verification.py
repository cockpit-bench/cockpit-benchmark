"""Meaningful negative checks for the portable verification boundary."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts/verification'))
import verify
from coverage import analyze


class PublicVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root/'repo'
        self.repo.mkdir()
        subprocess.check_call(['git', 'init', '-q', str(self.repo)])
        (self.repo/'src').mkdir()
        (self.repo/'src/A.java').write_text('class A {\n  String url = "https://example.test"; // comment\n}\n', encoding='utf-8')
        (self.repo/'Android.bp').write_text('java_library { name: "runtime", srcs: ["src/*.java"] }\n', encoding='utf-8')
        subprocess.check_call(['git', '-C', str(self.repo), 'add', '.'])
        subprocess.check_call(['git', '-C', str(self.repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'])
        self.head = verify.git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        self.snap = verify.Snapshot(self.repo, self.head)
        body = self.snap.body('src/A.java')
        self.scope = {'id': 'CASE', 'head': self.head, 'kind': 'APP', 'unresolved': [], 'source_loc': 3,
                      'source_file_count': 1, 'size_band': 'small', 'path_set_sha256': verify.sha(verify.encoded(['src/A.java'])),
                      'included': [{'path': 'src/A.java', 'blob': self.snap.entries['src/A.java']['oid'], 'source_sha256': verify.sha(body),
                                    'source_loc': 3, 'physical_lines': 3, 'owners': ['runtime'], 'language': 'Java',
                                    'count_method': 'c_like_comments'}],
                      'excluded': [{'path': 'Android.bp', 'reason': 'build metadata', 'entry': self.snap.entries['Android.bp']}],
                      'ownership_anchors': [{'path': 'Android.bp', 'sha256': verify.sha(self.snap.body('Android.bp')), 'line': 1}]}

    def test_recounts_non_gradle_production_and_preserves_string_slashes(self):
        result = verify.check_scope(self.snap, self.scope, self.root/'out')
        self.assertEqual(result['source_loc'], 3)

    def test_count_tampering_fails(self):
        self.scope['included'][0]['source_loc'] = 4
        with self.assertRaisesRegex(ValueError, 'Count mismatch'):
            verify.check_scope(self.snap, self.scope, self.root/'out')

    def test_missing_partition_entry_fails(self):
        self.scope['excluded'] = []
        with self.assertRaisesRegex(ValueError, 'partition differs'):
            verify.check_scope(self.snap, self.scope, self.root/'out')

    def test_stale_owner_anchor_fails(self):
        self.scope['ownership_anchors'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'Ownership anchor changed'):
            verify.check_scope(self.snap, self.scope, self.root/'out')

    def test_dirty_source_rejected(self):
        (self.repo/'src/A.java').write_text('class B {}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Dirty worktree'):
            verify.Snapshot(self.repo, self.head)

    def test_source_anchor_semantics_are_not_claimed(self):
        e = {'source': 'repository', 'commit': self.head, 'path': 'src/A.java', 'start_line': 1, 'end_line': 1,
             'symbol': 'class A', 'source_sha256': verify.sha(self.snap.body('src/A.java')),
             'claim': 'A claim deliberately not interpreted by this deterministic checker'}
        verify.check_anchor(self.snap, e)
        e['symbol'] = 'class Missing'
        with self.assertRaisesRegex(ValueError, 'symbol missing'):
            verify.check_anchor(self.snap, e)

    def test_unresolved_semantic_observation_is_not_imputed(self):
        with self.assertRaisesRegex(ValueError, 'Unresolved semantic'):
            verify.compute_leaf({'method': 'semantic_observation_mapping', 'facts': {'scope_sufficient': False, 'observation': 'unknown'}})

    def test_paths_cannot_escape_package(self):
        for p in ['../x', '/x', 'C:/x', 'a/../x', 'a\\x']:
            with self.assertRaises(ValueError):
                verify.safe_path(p)

    def test_missing_scores_are_not_counted_as_zero(self):
        standard = {'version': 'test', 'repositories': [{'id': 'x', 'kind': 'APP', 'leaves': [{'name': 'compilation.ci_independence', 'score': None, 'status': 'failed'}]}]}
        with self.assertRaisesRegex(ValueError, 'Unsupported/unscored'):
            analyze(standard, {('x', 'compilation.ci_independence'): {}})


if __name__ == '__main__':
    unittest.main()
