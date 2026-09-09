import base64
import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import external_inputs as ei


class ExternalInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'packet.zip'
        self.body = b'synthetic Git input, not production evidence\n'
        self.response = base64.b64encode(self.body)
        url = 'https://android.googlesource.com/platform/example/+/' + 'a'*40 + '/example.txt?format=TEXT'
        self.index = {'schema': 'frozen-git-inputs-v1', 'inputs': [{
            'path': 'inputs/example.txt', 'project': 'platform/example', 'commit': 'a'*40,
            'git_path': 'example.txt', 'encoding': 'base64_git_blob',
            'sha256': ei.sha(self.body), 'bytes': len(self.body),
            'transport': {'path': 'transport/response', 'sha256': ei.sha(self.response),
                          'bytes': len(self.response), 'status': 200, 'request_url': url,
                          'response_url': url, 'redirects': [], 'headers': [['Content-Type', 'text/plain']],
                          'started_at': '2026-09-09T00:00:00+00:00', 'completed_at': '2026-09-09T00:00:01+00:00'}}]}

    def write(self, extra=None):
        with zipfile.ZipFile(self.path, 'w') as z:
            z.writestr('packet-index.json', json.dumps(self.index))
            z.writestr('inputs/example.txt', self.body)
            z.writestr('transport/response', self.response)
            if extra: z.writestr(extra, b'undeclared')
        return ei.sha(self.path.read_bytes())

    def test_valid_packet(self):
        self.assertEqual(ei.verify(self.path, self.write())['input_count'], 1)

    def test_wrong_archive_hash(self):
        self.write()
        with self.assertRaisesRegex(ValueError, 'packet hash'): ei.verify(self.path, '0'*64)

    def test_response_decode_is_verified_even_with_rehashed_metadata(self):
        self.response = base64.b64encode(b'other')
        self.index['inputs'][0]['transport'].update(sha256=ei.sha(self.response), bytes=len(self.response))
        with self.assertRaisesRegex(ValueError, 'decoded Git file'): ei.verify(self.path, self.write())

    def test_traversal_and_undeclared_files_rejected(self):
        for name in ['../outside', 'answers.json']:
            with self.assertRaises(ValueError): ei.verify(self.path, self.write(name))

    def test_wrong_immutable_origin_rejected(self):
        self.index['inputs'][0]['commit'] = 'b'*40
        with self.assertRaisesRegex(ValueError, 'origin/status'): ei.verify(self.path, self.write())

    def test_headers_and_timestamps_required(self):
        self.index['inputs'][0]['transport']['headers'] = []
        with self.assertRaisesRegex(ValueError, 'headers'): ei.verify(self.path, self.write())


if __name__ == '__main__': unittest.main()
