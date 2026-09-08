import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'scripts/verification/check_split.py'
if not PATH.exists():
    PATH = Path(__file__).resolve().parent/'check_split.py'
spec = importlib.util.spec_from_file_location('review_split', PATH)
split = importlib.util.module_from_spec(spec)
spec.loader.exec_module(split)


class LineageSplitTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {'repositories': [
            {'id': 'APP-14', 'delivery_status': 'active', 'family_id': 'frameworks-base'},
            {'id': 'FW-16', 'delivery_status': 'active', 'family_id': 'frameworks-base'},
            {'id': 'APP-03', 'delivery_status': 'active', 'family_id': 'handbook'},
            {'id': 'APP-20', 'delivery_status': 'pending'},
        ]}

    def test_same_family_cannot_cross(self):
        with self.assertRaisesRegex(ValueError, 'Same lineage crosses'):
            split.check_split(self.manifest, {'APP-14': 'train', 'FW-16': 'test'})

    def test_grouped_complete_assignment(self):
        result = split.check_split(self.manifest,
            {'APP-14': 'train', 'FW-16': 'train', 'APP-03': 'test'}, True)
        self.assertEqual(result['families'], 2)
        self.assertTrue(result['complete'])

    def test_invalid_inputs_cannot_pass(self):
        for assignment in [{}, {'APP-20': 'test'}, {'APP-14': ''}, []]:
            with self.subTest(assignment=assignment), self.assertRaises(ValueError):
                split.check_split(self.manifest, assignment)
        with self.assertRaisesRegex(ValueError, 'every active'):
            split.check_split(self.manifest, {'APP-14': 'test'}, True)


if __name__ == '__main__':
    unittest.main()
