from pathlib import Path
import unittest
import effective_contract as ec


class EffectiveContractTests(unittest.TestCase):
    def test_published_composition_matches_frozen_inputs(self):
        root = Path(__file__).resolve().parents[1] / 'suites/matlab-simulink'
        text, binding = ec.build(root)
        self.assertEqual((root / 'EFFECTIVE_CONTRACT.md').read_bytes(), text.encode())
        self.assertEqual(ec.sha(text.encode()), binding['effective']['sha256'])
        self.assertEqual(text.count('## 2.'), 13)
        self.assertNotIn('线性插值', text)
        self.assertNotIn('源→0(封顶1)', text)
        self.assertIn('无仓外业务依赖', text)
        self.assertIn('decision coverage', text)
        self.assertIn('不以分支数≤1判 0', text)


if __name__ == '__main__': unittest.main()
