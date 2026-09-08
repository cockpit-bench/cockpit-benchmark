import copy
import importlib.util
from pathlib import Path
import unittest

source = Path(__file__).resolve().parents[1] / 'scripts/verification/evaluation_profile.py'
if not source.exists():
    source = Path(__file__).resolve().parent / 'evaluation_profile.py'
spec = importlib.util.spec_from_file_location('evaluation_profile', source)
ep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ep)


class EvaluationProfileTests(unittest.TestCase):
    def setUp(self):
        self.context = {'reference_id': 'v0.8.4', 'source_manifest_sha256': 'fixture'}
        self.data = {'leaves': [
            {'id': 'APP-02/ci', 'reference_id': 'v0.8.4', 'requires_external': True,
             'modes': {'source_only': {'state': 'supported', 'kind': 'source', 'basis': 'source exists', 'evidence_ids': ['git']},
                       'frozen_external': {'state': 'supported', 'kind': 'legacy_derived', 'basis': 'old summary', 'evidence_ids': ['summary']}}},
            {'id': 'other/leaf', 'reference_id': 'v0.8.4', 'requires_external': False,
             'modes': {'source_only': {'state': 'supported', 'kind': 'source', 'basis': 'bound source behavior', 'evidence_ids': ['git']}}}]}

    def test_source_external_not_guessable(self):
        p = ep.register(self.data, 'source_only', self.context)
        self.assertEqual(p['eligible'], ['other/leaf'])
        self.assertEqual(p['exclusions'][0]['reason'], 'external_evidence_required_or_unknown')

    def test_unknown_and_legacy_excluded(self):
        p = ep.register(self.data, 'frozen_external', self.context)
        self.assertFalse(p['eligible'])

    def test_raw_requires_matching_packet(self):
        row = self.data['leaves'][0]
        row['modes']['frozen_external'].update(kind='frozen_raw', raw_complete=True, packet_sha256='raw')
        self.assertFalse(ep.register(self.data, 'frozen_external', self.context)['eligible'])
        self.context['external_packet_sha256'] = 'raw'
        self.assertEqual(ep.register(self.data, 'frozen_external', self.context)['eligible'], ['APP-02/ci'])

    def test_live_cannot_compare_old_reference(self):
        self.context['capture_batch_id'] = 'today'
        self.data['leaves'][0]['modes']['live_environment'] = dict(state='supported', kind='live_raw', raw_complete=True, capture_batch_id='today', basis='raw', evidence_ids=['response'])
        self.assertFalse(ep.register(self.data, 'live_environment', self.context)['eligible'])
        self.data['leaves'][0]['reference_batch_id'] = 'today'
        self.assertEqual(ep.register(self.data, 'live_environment', self.context)['eligible'], ['APP-02/ci'])

    def test_abstention_and_missing_keep_denominator(self):
        p = ep.register(self.data, 'source_only', self.context)
        ref = {'context': self.context, 'leaves': [{'id': 'other/leaf', 'score': 3}]}
        c = {'profile_sha256': p['profile_sha256'], 'leaves': [{'id': 'other/leaf', 'status': 'abstain'}]}
        result = ep.compare(p, ref, c)
        self.assertEqual((result['common_eligible'], result['accuracy'], result['abstained']), (1, 0, 1))
        c['leaves'] = []
        self.assertEqual(ep.compare(p, ref, c)['missing'], 1)

    def test_common_fixed_before_predictions(self):
        p = ep.register(self.data, 'source_only', self.context)
        other = copy.deepcopy(self.data); other['leaves'][1]['modes'] = {}
        q = ep.register(other, 'source_only', self.context)
        common = ep.common([p, q]); self.assertEqual(common['eligible'], [])
        result = ep.compare(common, {'context': self.context, 'leaves': []}, {'profile_sha256': common['profile_sha256'], 'leaves': []})
        self.assertIsNone(result['accuracy'])

    def test_tamper_and_cross_mode_rejected(self):
        p = ep.register(self.data, 'source_only', self.context)
        tampered = copy.deepcopy(p); tampered['eligible'].append('APP-02/ci')
        with self.assertRaises(ValueError): ep.validate_profile(tampered)
        with self.assertRaises(ValueError): ep.common([p, ep.register(self.data, 'frozen_external', self.context)])

    def test_duplicate_inventory_rejected(self):
        self.data['leaves'].append(self.data['leaves'][0])
        with self.assertRaises(ValueError): ep.register(self.data, 'source_only', self.context)

    def test_inventory_snapshot_mismatch_is_rejected(self):
        self.data['source_manifest_sha256'] = 'different-snapshot'
        with self.assertRaisesRegex(ValueError, 'availability context mismatch'):
            ep.register(self.data, 'source_only', self.context)


if __name__ == '__main__': unittest.main()
