"""Regression checks for stale published evidence and language-aware LOC."""
import copy
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/verification'))
import verify
from counting import count_production_lines, strip_c_like_comments


class LanguageCountTests(unittest.TestCase):
    def test_nested_kotlin_kdoc_is_not_production(self):
        text = '/** Example:\n * f(/* parameter */)\n * class Example {}\n */\nclass Actual\n'
        self.assertEqual(count_production_lines(text, language='Kotlin'), (1, []))
        self.assertEqual(count_production_lines(text, language='.kt'), (1, []))
        masked = strip_c_like_comments(text, language='Kotlin')
        self.assertEqual(len(masked), len(text))
        self.assertEqual([i for i, c in enumerate(masked) if c == '\n'],
                         [i for i, c in enumerate(text) if c == '\n'])

    def test_java_and_c_comments_do_not_nest(self):
        text = '/* outer-looking /* text */\nint actual;\n'
        for language in ['Java', 'C', 'C++', None]:
            with self.subTest(language=language):
                self.assertEqual(count_production_lines(text, language=language), (1, []))

    def test_kotlin_string_comment_tokens_are_preserved(self):
        text = 'val example = """\n/* not a comment */\n"""\n/* one /* two */ end */\nclass Actual\n'
        self.assertEqual(count_production_lines(text, language='Kotlin'), (4, []))


class DeliveryConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.head, self.tree = 'a' * 40, 'b' * 40
        self.write('SCORE_RULES.md', 'fixture contract\n')
        digest = verify.sha((self.root / 'SCORE_RULES.md').read_bytes())
        refs = {'refs/heads/main': self.head}
        self.anchor = dict(source='repository', evidence_type='code', path='A.java', commit=self.head,
                           start_line=1, end_line=1, symbol='class A', claim='An actual production class',
                           independent_group='class', source_sha256='c' * 64)
        leaf = dict(name='compilation.ci_independence', score=1, max_score=3, status='scored',
                    score_reasoning='Platform CI exists.', analysis='Only platform CI is present.', evidence=[self.anchor])
        repo = dict(id='CASE', name='fixture', kind='APP', quality_tier='medium', size_band='small',
                    head=self.head, tree=self.tree, total={'score': 1, 'max': 3}, leaves=[leaf])
        self.standard = dict(version='test', contract={'sha256': digest}, repositories=[repo],
                             summary=dict(repository_count=1, leaf_count=1, score=1, max_score=3, pending_repository_count=0))
        self.manifest = dict(repositories=[dict(id='CASE', name='fixture', kind='APP', quality_tier='medium',
                             size_band='small', source_loc=1, source_files=1, delivery_status='active',
                             oracle_path='oracle/CASE.json', delivery=dict(expected_head=self.head, refs=refs))])
        ref_summary = dict(path='manifest.json', json_pointer='/repositories/0/delivery/refs',
                           count=1, sha256=verify.sha(verify.encoded(refs)))
        self.facts = dict(repo_id='CASE', head=self.head, tree=self.tree, contract_sha256=digest,
                          source_evidence=[self.anchor], refs=ref_summary,
                          release_branch_facts={'complete_refs': ref_summary},
                          production_scope=dict(source_loc=1, source_file_count=1, size_band='small', path_set_sha256='d' * 64),
                          leaf_facts={leaf['name']: dict(decisive_facts={'valid_independent_ci_exists': False,
                                    'valid_platform_ci_exists': True}, evidence_indices=[0])})
        self.oracle = dict(schema_version='fixture-1', repo_id='CASE', repository=dict(head=self.head, tree=self.tree),
                           rubric={'sha256': digest}, quality_tier='medium', size_band='small',
                           facts_path='facts/CASE.json', canonical_total={'score': 1, 'max': 3}, canonical_leaves=[copy.deepcopy(leaf)])
        self.write_json('oracle/CASE.json', self.oracle)
        self.write_json('facts/CASE.json', self.facts)
        with (self.root / 'SCORECARD.csv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['id', 'name', 'kind', 'quality_tier', 'size_band', 'head', 'leaf', 'score', 'max_score', 'status', 'score_reasoning'])
            writer.writerow(['CASE', 'fixture', 'APP', 'medium', 'small', self.head, leaf['name'], 1, 3, 'scored', 'Platform CI exists.'])
        self.write('SCORECARD.md', '# Validation-18 test\n\n| ID | Repository | Size | Quality | Score |\n|---|---|---|---|---|\n'
                   '| CASE | fixture | small | medium | 1/3 |\n\n## CASE fixture\n\n| Leaf | Score | Reason |\n|---|---|---|\n'
                   '| compilation.ci_independence | 1/3 | Platform CI exists. |\n')

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def write_json(self, path, value):
        self.write(path, json.dumps(value))

    def check(self):
        return verify.check_delivery_consistency(self.root, self.standard, self.manifest)

    def test_consistent_delivery_and_disclosed_inputs_pass(self):
        self.assertEqual(set(self.check()), {'CASE'})
        scope = dict(self.facts['production_scope'], id='CASE', head=self.head)
        inputs = dict(head=self.head, leaves=[dict(name=name, facts=record['decisive_facts'], evidence=[self.anchor])
                                             for name, record in self.facts['leaf_facts'].items()])
        verify.check_disclosed_inputs(self.facts, scope, inputs)
        inputs['leaves'][0]['facts'] = {'valid_independent_ci_exists': True, 'valid_platform_ci_exists': True}
        with self.assertRaisesRegex(ValueError, 'decisive fact differs'):
            verify.check_disclosed_inputs(self.facts, scope, inputs)

    def test_same_score_stale_reason_and_evidence_are_rejected(self):
        for field, value in [('score_reasoning', 'Different strategy.'), ('analysis', 'New evidence.'), ('evidence', [])]:
            oracle = copy.deepcopy(self.oracle)
            oracle['canonical_leaves'][0][field] = value
            self.write_json('oracle/CASE.json', oracle)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'canonical leaf content differs'):
                self.check()

    def test_synchronized_oracle_and_standard_still_need_matching_facts(self):
        self.facts = copy.deepcopy(self.facts)
        self.facts['source_evidence'][0]['claim'] = 'Stale facts claim'
        self.write_json('facts/CASE.json', self.facts)
        with self.assertRaisesRegex(ValueError, 'Canonical/facts evidence differs'):
            self.check()

    def test_missing_oracle_is_not_a_successful_verification(self):
        (self.root / 'oracle/CASE.json').unlink()
        with self.assertRaises(FileNotFoundError):
            self.check()

    def test_scorecard_number_or_reason_tampering_fails(self):
        for filename, old, new in [('SCORECARD.csv', 'Platform CI exists.', 'Stale rationale.'),
                                    ('SCORECARD.md', '1/3', '2/3')]:
            path = self.root / filename
            original = path.read_text(encoding='utf-8')
            path.write_text(original.replace(old, new), encoding='utf-8')
            with self.subTest(filename=filename), self.assertRaisesRegex(ValueError, 'SCORECARD'):
                self.check()
            path.write_text(original, encoding='utf-8')

    def test_stale_platform_summary_cannot_survive_synchronized_leaf(self):
        old, name = 'compilation.ci_independence', 'platform_reuse.platform_upgrade'
        for path in self.root.rglob('*'):
            if path.is_file():
                path.write_text(path.read_text(encoding='utf-8').replace(old, name), encoding='utf-8')
        self.standard = json.loads(json.dumps(self.standard).replace(old, name))
        facts = json.loads((self.root / 'facts/CASE.json').read_text(encoding='utf-8'))
        facts['leaf_facts'][name]['decisive_facts'] = {'version_bound_status': 1}
        analysis = self.standard['repositories'][0]['leaves'][0]['analysis']
        facts['platform_seven'] = {'version_bound_status': 1, 'coverage_explanation': analysis,
                                   'binding_explanation': analysis}
        self.write_json('facts/CASE.json', facts)
        self.check()
        for key, value in [('version_bound_status', 2), ('coverage_explanation', 'Stale reason'),
                           ('binding_explanation', 'Stale binding')]:
            changed = copy.deepcopy(facts)
            changed['platform_seven'][key] = value
            self.write_json('facts/CASE.json', changed)
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Platform summary'):
                self.check()


class StructuredRepositoryAnchorTests(unittest.TestCase):
    def test_actual_git_json_pointer_and_hash_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.check_call(['git', 'init', '-q', str(repo)])
            body = b'{"api":{"baseline":"expected"},"empty":[]}\n'
            (repo / 'baseline.json').write_bytes(body)
            subprocess.check_call(['git', '-C', str(repo), 'add', '.'])
            subprocess.check_call(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'])
            head = verify.git(repo, 'rev-parse', 'HEAD').decode().strip()
            snap = verify.Snapshot(repo, head)
            e = dict(source='repository', evidence_type='structured_facts', commit=head, path='baseline.json',
                     source_sha256=verify.sha(body), json_pointer='/api/baseline')
            verify.check_anchor(snap, e)
            for key, value in [('json_pointer', ''), ('json_pointer', '/missing'), ('json_pointer', '/empty'),
                               ('source_sha256', '0' * 64), ('commit', 'd' * 40)]:
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    verify.check_anchor(snap, dict(e, **{key: value}))


if __name__ == '__main__':
    unittest.main()
