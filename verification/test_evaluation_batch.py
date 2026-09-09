import copy
from pathlib import Path
import unittest

import evaluation_batch as eb


class EvaluationBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wrapper = Path(__file__).resolve().parents[1]
        manifest = eb.read(cls.wrapper / 'manifest.json')
        cls.assignments = {r['id']: 'development' for r in manifest['repositories'] if r['delivery_status'] == 'active'}
        cls.batch = eb.prepare(cls.wrapper, 'source_only', cls.assignments)

    def candidate(self):
        return {'profile_sha256': self.batch['profile']['profile_sha256'],
                'leaves': [{'id': r['id'], 'status': 'scored', 'score': r['score'],
                            'reasoning': 'Synthetic fixture only.', 'evidence': [{'path': 'fixture-only'}]}
                           for r in self.batch['reference']['leaves']]}

    def test_real_fixed_set_and_baseline(self):
        result = eb.assess(self.batch, self.candidate())
        self.assertEqual(result['common_eligible'], 155)
        self.assertEqual(result['correct'], 155)
        self.assertEqual(len(result['excluded_predictions_ignored']), 16)
        self.assertEqual(sum(r['eligible'] for r in result['distribution']['groups']), 155)
        self.assertEqual(result['evidence_validity']['status'], 'not_reviewed')

    def test_family_overlap_rejected(self):
        assignments = dict(self.assignments, **{'APP-14': 'train', 'FW-16': 'test'})
        with self.assertRaisesRegex(ValueError, 'lineage crosses'):
            eb.prepare(self.wrapper, 'source_only', assignments)

    def test_missing_keeps_every_denominator(self):
        candidate = self.candidate(); candidate['leaves'] = []
        result = eb.assess(self.batch, candidate)
        self.assertEqual((result['accuracy'], result['missing']), (0, 155))
        self.assertEqual(result['distribution']['macro_candidate_accuracy'], 0)

    def test_illegal_tier_and_bool_rejected(self):
        for value in (2, True, float('nan')):
            candidate = self.candidate()
            candidate['leaves'][0]['score'] = value  # componentization permits 0/1/3/5
            with self.assertRaises(ValueError): eb.assess(self.batch, candidate)

    def test_batch_tampering_rejected(self):
        batch = copy.deepcopy(self.batch); batch['assignments']['APP-01'] = 'test'
        with self.assertRaisesRegex(ValueError, 'batch digest'):
            eb.assess(batch, self.candidate())

    def test_review_is_separate_from_score(self):
        candidate = self.candidate()
        plan = eb.review_plan(self.batch, candidate, 3, 'fixed-before-adjudication')
        rows = [{'id': key, 'verdict': verdict, 'reviewer': 'synthetic-test-reviewer',
                 'reviewed_at': 'fixture', 'rationale': 'Synthetic semantic adjudication fixture.',
                 'anchors': [{'path': 'fixture-only', 'revision': 'fixture', 'location': 'fixture',
                              'claim': 'Synthetic test observation'}]} for key, verdict in
                zip(plan['selected'], ['supported', 'contradicted', 'insufficient'])]
        result = eb.assess(self.batch, candidate, plan, {'plan_sha256': plan['plan_sha256'], 'leaves': rows})
        self.assertEqual(result['accuracy'], 1)
        self.assertEqual(result['evidence_validity']['supported_fraction_of_fixed_sample'], 1/3)

    def test_partial_adjudication_and_abstention(self):
        candidate = self.candidate(); candidate['leaves'] = []
        plan = eb.review_plan(self.batch, candidate, 3, 'seed')
        rows = [{'id': plan['selected'][0], 'verdict': 'no_output', 'reviewer': 'fixture',
                 'reviewed_at': 'fixture', 'rationale': 'No output.'}]
        result = eb.assess(self.batch, candidate, plan, {'plan_sha256': plan['plan_sha256'], 'leaves': rows})
        self.assertEqual(result['evidence_validity']['counts']['unreviewed'], 2)
        self.assertEqual(result['evidence_validity']['review_coverage'], 1/3)

    def test_review_cannot_be_reused_for_other_candidate(self):
        candidate = self.candidate(); plan = eb.review_plan(self.batch, candidate, 3, 'seed')
        candidate['leaves'].pop()
        with self.assertRaisesRegex(ValueError, 'candidate mismatch'):
            eb.assess(self.batch, candidate, plan, {'plan_sha256': plan['plan_sha256'], 'leaves': []})

    def test_cherry_picked_sample_rejected(self):
        candidate = self.candidate(); plan = eb.review_plan(self.batch, candidate, 3, 'seed')
        plan['selected'] = self.batch['profile']['eligible'][:3]
        with self.assertRaisesRegex(ValueError, 'plan changed'):
            eb.assess(self.batch, candidate, plan, {'plan_sha256': plan['plan_sha256'], 'leaves': []})

    def test_excluded_invalid_prediction_is_ignored(self):
        candidate = self.candidate()
        for row in candidate['leaves']:
            if row['id'] not in self.batch['profile']['eligible']: row['score'] = 'invalid-excluded'
        self.assertEqual(eb.assess(self.batch, candidate)['correct'], 155)

    def test_common_profile_binds_and_cannot_expand(self):
        profile = eb.ep.common([self.batch['profile']])
        self.assertEqual(eb.prepare(self.wrapper, 'source_only', self.assignments, profile)['profile'], profile)
        profile['mode'] = 'frozen_external'
        profile['profile_sha256'] = eb.ep.digest({k: v for k, v in profile.items() if k != 'profile_sha256'})
        with self.assertRaisesRegex(ValueError, 'common profile differs'):
            eb.prepare(self.wrapper, 'source_only', self.assignments, profile)

    def test_empty_reason_cannot_be_supported(self):
        candidate = self.candidate()
        for row in candidate['leaves']: row.pop('reasoning')
        plan = eb.review_plan(self.batch, candidate, 1, 'seed')
        row = {'id': plan['selected'][0], 'verdict': 'supported', 'reviewer': 'fixture',
               'reviewed_at': 'fixture', 'rationale': 'fixture'}
        with self.assertRaisesRegex(ValueError, 'candidate reasoning'):
            eb.assess(self.batch, candidate, plan, {'plan_sha256': plan['plan_sha256'], 'leaves': [row]})

    def test_frozen_profile_cannot_register_without_actual_packet(self):
        with self.assertRaisesRegex(ValueError, 'requires the actual external packet'):
            eb.prepare(self.wrapper, 'frozen_external', self.assignments)

    def test_source_only_refuses_external_packet(self):
        with self.assertRaisesRegex(ValueError, 'does not permit'):
            eb.prepare(self.wrapper, 'source_only', self.assignments, external_packet='not-read.zip')


if __name__ == '__main__': unittest.main()
