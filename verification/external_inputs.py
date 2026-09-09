"""Verify a frozen Git-input packet without extraction, networking or execution."""
import argparse
import base64
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile


def sha(data): return hashlib.sha256(data).hexdigest()


def verify(path, expected_sha256):
    raw = Path(path).read_bytes()
    if sha(raw) != expected_sha256:
        raise ValueError('external packet hash mismatch')
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)) or sum(i.file_size for i in infos) > 16 * 1024 * 1024:
            raise ValueError('duplicate or oversized packet')
        for item in infos:
            name = item.filename
            if (not name or ':' in name or '\\' in name or name.startswith('/')
                    or any(p in {'', '.', '..'} for p in name.split('/'))
                    or (item.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError('unsafe packet member')
        index = json.loads(archive.read('packet-index.json'))
        if index.get('schema') != 'frozen-git-inputs-v1' or not index.get('inputs'):
            raise ValueError('invalid packet index')
        expected = {'packet-index.json'}
        identifiers = set()
        for item in index['inputs']:
            for field in ['path', 'project', 'git_path', 'commit', 'sha256', 'encoding']:
                if not isinstance(item.get(field), str) or not item[field]:
                    raise ValueError('missing Git input ' + field)
            if not re.fullmatch('[0-9a-f]{40}', item['commit']):
                raise ValueError('Git input must bind an immutable commit')
            identity = (item['project'], item['commit'], item['git_path'])
            if identity in identifiers:
                raise ValueError('duplicate Git input identity')
            identifiers.add(identity)
            transport = item['transport']
            if item['path'] in expected or transport['path'] in expected or item['path'] == transport['path']:
                raise ValueError('duplicate input/transport path')
            expected.update([item['path'], transport['path']])
            for record in (item, transport):
                content = archive.read(record['path'])
                if type(record.get('bytes')) is not int or len(content) != record['bytes'] or sha(content) != record['sha256']:
                    raise ValueError('input or transport byte mismatch')
            endpoint = ('https://android.googlesource.com/' + item['project'] + '/+/'
                        + item['commit'] + '/' + item['git_path'])
            expected_url = endpoint + ('?format=TEXT' if item['encoding'] == 'base64_git_blob' else '?format=JSON')
            if (transport.get('status') != 200 or transport.get('request_url') != expected_url
                    or transport.get('response_url') != expected_url or transport.get('redirects') != []):
                raise ValueError('transport origin/status mismatch')
            headers = transport.get('headers')
            if not isinstance(headers, list) or not headers or any(
                    not isinstance(h, list) or len(h) != 2 or any(not isinstance(x, str) for x in h) for h in headers):
                raise ValueError('missing captured response headers')
            started = datetime.fromisoformat(transport['started_at'])
            finished = datetime.fromisoformat(transport['completed_at'])
            if started.tzinfo is None or finished.tzinfo is None or finished < started:
                raise ValueError('invalid capture interval')
            body = archive.read(item['path']); response = archive.read(transport['path'])
            if item['encoding'] == 'base64_git_blob':
                if base64.b64decode(b''.join(response.split()), validate=True) != body:
                    raise ValueError('decoded Git file differs from response')
            elif item['encoding'] == 'gitiles_json':
                if response != body or not body.startswith(b")]}'\n"):
                    raise ValueError('Gitiles JSON response mismatch')
                json.loads(body.split(b'\n', 1)[1])
            else:
                raise ValueError('unsupported input encoding')
        if expected != set(names):
            raise ValueError('missing or undeclared packet member')
    return {'packet_sha256': expected_sha256, 'input_count': len(identifiers),
            'decoded_bytes': sum(row['bytes'] for row in index['inputs']),
            'limit': 'Authenticates frozen declarations/bytes and decoding, not source semantic sufficiency or a build execution.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True); p.add_argument('--sha256', required=True)
    a = p.parse_args(); print(json.dumps(verify(a.packet, a.sha256), indent=2))


if __name__ == '__main__': main()
