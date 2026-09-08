import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import contextlib
import io
import os

try:
    from scripts.verification import boundary
except ModuleNotFoundError as exc:
    if exc.name not in ('scripts', 'scripts.verification'):
        raise
    import boundary
DEFAULT_REFERENCE = boundary.DEFAULT_REFERENCE
ROOT = boundary.ROOT
evaluate = boundary.evaluate
verify_reference = boundary.verify_reference
default_paths = boundary.default_paths


class BoundaryRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = json.loads(DEFAULT_REFERENCE.read_text(encoding='utf-8'))
        source_env = os.environ.get('BOUNDARY_SOURCE_ROOT')
        local = ROOT / cls.reference['source_root']
        cls.source_root = Path(source_env) if source_env else (local if not boundary.PUBLIC_LAYOUT and local.is_dir() else None)
        cls.contract = Path(os.environ.get('BOUNDARY_CONTRACT', str(boundary.DEFAULT_CONTRACT)))

    def sources(self):
        if self.source_root is None:
            self.skipTest('source binding requires BOUNDARY_SOURCE_ROOT in public layout')
        return self.source_root

    def test_actual_source_bindings(self):
        result = verify_reference(self.reference, self.sources(), self.contract)
        self.assertEqual(result, {'cases': 8, 'files': 94, 'family_count': 1, 'source_binding': 'verified'})

    def test_wrong_head_rejected(self):
        ref = copy.deepcopy(self.reference)
        ref['cases'][0]['head'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'HEAD mismatch'):
            verify_reference(ref, self.sources(), self.contract)

    def test_wrong_file_rejected(self):
        ref = copy.deepcopy(self.reference)
        ref['cases'][0]['file_inventory'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'file hash mismatch'):
            verify_reference(ref, self.sources(), self.contract)

    def test_wrong_symbol_rejected(self):
        ref = copy.deepcopy(self.reference)
        ref['cases'][0]['decisive_anchors'][0]['symbol'] = 'doesNotExistAnywhere('
        with self.assertRaisesRegex(ValueError, 'anchor symbol mismatch'):
            verify_reference(ref, self.sources(), self.contract)

    def test_public_and_local_defaults(self):
        root, reference, contract, public = default_paths(ROOT / 'wrapper/verification/boundary.py')
        self.assertTrue(public)
        self.assertEqual(reference, root / 'docs/boundary-reference.json')
        self.assertEqual(contract, root / 'SCORE_RULES.md')
        root, reference, contract, public = default_paths(ROOT / 'scripts/verification/boundary.py')
        self.assertFalse(public)
        self.assertEqual(reference, ROOT / 'staging/validation18-discrimination-20260908/boundary-reference.json')
        self.assertEqual(contract, ROOT / 'score-rules.md')

    def test_public_requires_sources(self):
        stderr = io.StringIO()
        with patch.object(boundary, 'PUBLIC_LAYOUT', True), patch('sys.argv', ['boundary.py']), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as cm:
                boundary.main()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn('explicit --sources', stderr.getvalue())

    def test_wrong_tag_oid_rejected(self):
        ref = copy.deepcopy(self.reference)
        row = next(r for r in ref['cases'] if r['case'] == 'channel-e')
        next(r for r in row['refs'] if r['ref'].startswith('refs/tags/'))['object_oid'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'object_oid mismatch'):
            verify_reference(ref, self.sources(), self.contract)

    def test_all_correct(self):
        scores = [{'case': r['case'], 'score': r['score']} for r in self.reference['cases']]
        result = evaluate(self.reference, scores)
        self.assertEqual(result['overall']['accuracy'], 1)
        self.assertEqual(result['macro_recall'], 1)
        self.assertEqual(result['macro_denominator'], 7)
        self.assertEqual(result['in_sample_leaf_mode_baseline']['hits'], 3)
        self.assertEqual(result['in_sample_leaf_mode_baseline']['accuracy'], 3/8)

    def test_abstentions_keep_denominators(self):
        result = evaluate(self.reference, [{'case': 'channel-d', 'score': 10}, {'case': 'device-a', 'score': None}])
        self.assertEqual(result['overall']['denominator'], 8)
        self.assertEqual(result['overall']['accuracy'], 1/8)
        self.assertEqual(result['overall']['abstained'], 7)
        self.assertEqual(result['leaf_band_strata']['platform_reuse.release_branch_strategy:10']['accuracy'], 1/2)
        self.assertAlmostEqual(result['macro_recall'], 1/14)

    def test_zero_is_answer_not_abstention(self):
        result = evaluate(self.reference, [{'case': 'channel-a', 'score': 0}])
        self.assertEqual(result['overall']['answered'], 1)
        self.assertEqual(result['overall']['correct'], 1)

    def test_invalid_predictions_rejected(self):
        for predictions in [[{'case': 'bogus', 'score': 3}],
                            [None], [{'case': [], 'score': 3}],
                            [{'case': 'channel-a', 'score': 0}] * 2,
                            [{'case': 'channel-a', 'score': True}],
                            [{'case': 'channel-a', 'score': 9}],
                            [{'case': 'channel-a', 'leaf': 'architecture.foo', 'score': 0}]]:
            with self.subTest(predictions=predictions), self.assertRaises(ValueError):
                evaluate(self.reference, predictions)


if __name__ == '__main__':
    unittest.main()
