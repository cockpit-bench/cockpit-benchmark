"""Contract boundaries for genuine partial runs and malformed native counts."""
import unittest
from matlab_recompute import unit_test


class NativeTestScoring(unittest.TestCase):
    def run_score(self, passed, total, covered, decisions):
        return unit_test(dict(present=True, all_passed=passed == total,
                              passed=passed, total=total, decision=[covered, decisions]))

    def test_coverage_does_not_substitute_for_passing_tests(self):
        for passed in [0, 4, 5]:
            self.assertEqual(self.run_score(passed, 10, 8, 10), 1)
        self.assertEqual(self.run_score(6, 10, 8, 10), 3)
        self.assertEqual(self.run_score(10, 10, 8, 10), 5)

    def test_decision_thresholds_and_no_objectives(self):
        for covered, total, expected in [(49,100,1),(50,100,3),(79,100,3),(80,100,5),(0,0,1)]:
            self.assertEqual(self.run_score(10,10,covered,total),expected)

    def test_missing_partial_pass_counts_remain_unknown(self):
        self.assertIsNone(unit_test(dict(present=True,all_passed=False,decision=[8,10])))
        self.assertEqual(unit_test(dict(present=True,all_passed=True,decision=[13,15])),5)
        self.assertEqual(unit_test(dict(present=True,all_passed=True,decision=None)),1)

    def test_invalid_coverage_cannot_be_scored(self):
        for cv in [[16,15],[-1,15],[0,-1],[True,1],[1.0,2],[1], '80%']:
            with self.subTest(cv=cv),self.assertRaises(ValueError):
                unit_test(dict(present=True,all_passed=True,decision=cv))

    def test_invalid_or_contradictory_test_status_cannot_be_scored(self):
        baseline=dict(present=True,all_passed=True,decision=[8,10],passed=10,total=10)
        for changes in [dict(all_passed=False),dict(passed=11),dict(passed=-1),
                        dict(passed=True),dict(total=None),dict(present=False),
                        dict(all_passed='yes'),dict(passed=0,total=0,all_passed=False)]:
            with self.subTest(changes=changes),self.assertRaises(ValueError):
                unit_test(dict(baseline,**changes))
        self.assertEqual(unit_test(dict(present=False,all_passed=False,decision=None)),0)


if __name__=='__main__':unittest.main()
