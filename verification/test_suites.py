import unittest
from pathlib import Path
from unittest.mock import patch
import suites,repository_types as rt
W=Path(__file__).resolve().parents[1]
class SuiteTests(unittest.TestCase):
 def test_current_entry_and_publication_gate(self):
  registry=suites.validate(W)
  self.assertEqual(len(rt.select(registry,W,'all')),33)
  if registry['integration_status']=='published':suites.validate(W,True)
  else:
   with self.assertRaises(suites.InvalidSuite):suites.validate(W,True)
 def test_retired_ids_rejected_before_network(self):
  with patch.object(rt,'git',side_effect=AssertionError('No Git or network expected')):
   for rid in [*[f'ML-{i:02d}' for i in range(1,10)],'NEM-10','NEM-11']:
    with self.assertRaises(ValueError):suites.restore(W,'all',W.parent/'must-not-create',ids=[rid])
 def test_current_matlab_alias(self):
  rows=rt.select(suites.validate(W),W,'matlab-simulink')
  self.assertEqual({r['id'] for r in rows},{f'NEP-{i:02d}' for i in range(1,12)})
 def test_android_frozen_reference_still_valid(self):
  self.assertEqual(len(suites.validate_legacy(W,True,suites.legacy_registry(W))['suites']),1)
