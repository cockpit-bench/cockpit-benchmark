"""Negative controls for full attachment replay (set MATLAB_EVIDENCE_ARCHIVE)."""
import copy
import os
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

import matlab_evidence as evidence
import matlab_validators
import suites

W=Path(__file__).resolve().parents[1]
ARCHIVE=os.environ.get('MATLAB_EVIDENCE_ARCHIVE')

@unittest.skipUnless(ARCHIVE,'Set MATLAB_EVIDENCE_ARCHIVE to the frozen release attachment')
class AttachmentTests(unittest.TestCase):
    def setUp(self):
        self.suite=next(s for s in suites.legacy_registry(W)['suites'] if s['id']=='matlab-simulink')

    def test_frozen_attachment_replays(self):
        result=evidence.verify(W,self.suite,ARCHIVE)
        self.assertEqual((result['leaves'],result['native_configurations'],result['property_assertions']),(117,12,1351118))

    def test_false_native_sample_count_fails_even_after_payload_access(self):
        original=evidence.Evidence.named
        def altered(instance,entry):
            value=original(instance,entry)
            if 'ML-05-B/native-replay/result.json' in entry['original_path'].replace('\\','/'):
                value=copy.deepcopy(value);value['samples']=0
            return value
        with patch.object(evidence.Evidence,'named',altered):
            with self.assertRaises((suites.InvalidSuite,matlab_validators.EvidenceError)):
                evidence.verify(W,self.suite,ARCHIVE)

    def test_raw_output_nonfinite_fails_beyond_catalog_hash_gate(self):
        original=evidence.Evidence.data
        def altered(instance,path,digest=None):
            value=original(instance,path,digest)
            if 'ML-05-B/native-replay/output.bin' in str(path).replace('\\','/'):
                return struct.pack('<d',float('inf'))+value[8:]
            return value
        with patch.object(evidence.Evidence,'data',altered):
            with self.assertRaises((suites.InvalidSuite,AssertionError)):
                evidence.verify(W,self.suite,ARCHIVE)

    def test_bound_property_counts_are_recomputed(self):
        original=evidence.Evidence.named
        def altered(instance,entry):
            value=original(instance,entry)
            if 'ML-05-B/properties.json' in entry['original_path'].replace('\\','/'):
                value=copy.deepcopy(value);value['streams']['native']['assertions']+=1;value['assertions']+=1
            return value
        with patch.object(evidence.Evidence,'named',altered):
            with self.assertRaises(suites.InvalidSuite):evidence.verify(W,self.suite,ARCHIVE)

if __name__=='__main__':unittest.main()
