"""Portable, read-only reproduction of reviewed scope/counts and score mappings.

Does not execute repository build scripts or claim to infer semantic judgments.
Requires Python 3.11+ and Git. Inputs must be the published maintainer data pack.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from counting import strip_c_like_comments, count_production_lines
from rules import RULES, semantic_rule


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def git(repo, *args, data=None):
    return subprocess.check_output(['git', '-c', 'core.longpaths=true', '-c', 'core.quotePath=false', '-C', str(repo), *args], input=data)


def safe_path(path):
    p = PurePosixPath(path)
    require(path and not p.is_absolute() and chr(92) not in path and ':' not in path
            and all(x not in {'', '.', '..'} for x in path.split('/')), 'Unsafe input path: ' + path)
    return path


class Snapshot:
    def __init__(self, repo, head):
        self.repo, self.head, self.entries, self.cache = repo, head, {}, {}
        require(git(repo, 'rev-parse', 'HEAD').decode().strip() == head, 'HEAD mismatch: ' + str(repo))
        require(not git(repo, 'status', '--porcelain', '--ignore-submodules=all').strip(), 'Dirty worktree: ' + str(repo))
        for item in git(repo, 'ls-tree', '-rz', '--full-tree', head).split(b'\0'):
            if not item:
                continue
            meta, path = item.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            self.entries[safe_path(path.decode('utf-8'))] = {'mode': mode, 'kind': kind, 'oid': oid}

    def batch(self, paths):
        paths = list(dict.fromkeys(paths))
        for start in range(0, len(paths), 128):
            group = paths[start:start + 128]
            for p in group:
                safe_path(p)
                require(p in self.entries and self.entries[p]['kind'] == 'blob', 'Missing blob: ' + p)
            request = ''.join(self.entries[p]['oid'] + '\n' for p in group).encode()
            raw = git(self.repo, 'cat-file', '--batch', data=request)
            offset = 0
            for p in group:
                end = raw.index(b'\n', offset)
                oid, kind, size = raw[offset:end].decode().split()
                require(oid == self.entries[p]['oid'] and kind == 'blob', 'Batch object mismatch')
                offset = end + 1
                body = raw[offset:offset + int(size)]
                require(len(body) == int(size), 'Truncated blob')
                offset += int(size) + 1
                yield p, body
            require(offset == len(raw), 'Trailing batch bytes')

    def body(self, path):
        if path not in self.cache:
            self.cache[path] = next(self.batch([path]))[1]
        return self.cache[path]


def check_anchor(snap, e):
    require(e.get('commit') == snap.head, 'Evidence HEAD mismatch')
    if e.get('source') == 'git_inventory':
        if e['inventory_kind'] == 'tracked_paths':
            # Preserve the exact original Git inventory encoding (core.quotePath default).
            body = subprocess.check_output(['git', '-C', str(snap.repo), 'ls-files'])
        elif e['inventory_kind'] == 'refs':
            body = git(snap.repo, 'for-each-ref', '--format=%(refname)|%(objectname)|%(*objectname)|%(tree)|%(*tree)', 'refs/heads', 'refs/tags')
        else:
            raise ValueError('Unknown inventory kind')
        require(sha(body) == e['sha256'], 'Inventory SHA mismatch')
        return
    require(e.get('source') == 'repository', 'Unsupported evidence source')
    body = snap.body(e['path'])
    if 'source_sha256' in e:
        require(sha(body) == e['source_sha256'], 'Evidence SHA mismatch: ' + e['path'])
    lines = body.decode('utf-8').splitlines()
    a, b = e['start_line'], e['end_line']
    require(1 <= a <= b <= len(lines), 'Evidence line range invalid')
    require(e['symbol'] in '\n'.join(lines[a - 1:b]), 'Evidence symbol missing: ' + e['path'])


def check_scope(snap, scope, output):
    require(scope['head'] == snap.head and not scope['unresolved'], 'Scope unresolved or stale')
    rows = scope['included']
    paths = [r['path'] for r in rows]
    require(len(paths) == len(set(paths)), 'Duplicate production path')
    excluded = {x['path']: x for x in scope['excluded']}
    require(len(excluded) == len(scope['excluded']), 'Duplicate excluded path')
    require(not set(paths) & set(excluded), 'Included/excluded overlap')
    require(set(paths) | set(excluded) == set(snap.entries), 'Tracked inventory partition differs')
    actual_rows = []
    languages = {}
    ownership_files = set()
    for row, (path, body) in zip(rows, snap.batch(paths)):
        entry = snap.entries[path]
        require(row['blob'] == entry['oid'] and entry['mode'] in {'100644', '100755'}, 'Production blob differs: ' + path)
        require(sha(body) == row['source_sha256'], 'Production SHA differs: ' + path)
        text = body.decode('utf-8', 'replace')
        if row['count_method'] == 'generated_regions_then_c_like_comments':
            loc, regions = count_production_lines(text)
            require(regions == row['excluded_generated_regions'], 'Generated region difference: ' + path)
        elif row['count_method'] == 'c_like_comments':
            loc = sum(bool(x.strip()) for x in strip_c_like_comments(text).splitlines())
        else:
            raise ValueError('Unknown counting method')
        require(loc == row['source_loc'] and len(text.splitlines()) == row['physical_lines'], 'Count mismatch: ' + path)
        require(bool(row['owners']), 'Production path has no reviewed owner: ' + path)
        actual_rows.append({'path': path, 'blob': entry['oid'], 'source_sha256': sha(body), 'source_loc': loc,
                            'physical_lines': len(text.splitlines()), 'language': row['language']})
        q = languages.setdefault(row['language'], {'files': 0, 'source_loc': 0, 'physical_lines': 0})
        q['files'] += 1
        q['source_loc'] += loc
        q['physical_lines'] += len(text.splitlines())
    for path, record in excluded.items():
        require(record['entry'] == snap.entries[path] and bool(record['reason']), 'Exclusion inventory differs: ' + path)
    for record in scope['ownership_anchors']:
        path = record['path']
        body = snap.body(path)
        require(sha(body) == record['sha256'], 'Ownership anchor changed: ' + path)
        if record.get('line'):
            require(1 <= record['line'] <= len(body.decode('utf-8', 'replace').splitlines()), 'Ownership line invalid')
        ownership_files.add(path)
    loc = sum(x['source_loc'] for x in actual_rows)
    require(loc == scope['source_loc'] and len(actual_rows) == scope['source_file_count'], 'Scope aggregate mismatch')
    limits = (30000, 80000) if scope['kind'] == 'APP' else (80000, 200000)
    size = 'small' if loc < limits[0] else 'medium' if loc < limits[1] else 'large'
    require(loc > 0 and size == scope['size_band'], 'Size band differs')
    # Original wrapper's defined path-set digest is canonical JSON of sorted paths + LF.
    path_hash = sha(encoded(sorted(paths)))
    require(path_hash == scope['path_set_sha256'], 'Public path-set hash differs')
    summary = {'id': scope['id'], 'head': snap.head, 'source_file_count': len(rows), 'source_loc': loc,
               'physical_lines': sum(x['physical_lines'] for x in actual_rows), 'size_band': size,
               'language_composition': languages, 'path_set_sha256': path_hash,
               'excluded_count': len(excluded), 'ownership_anchor_files': len(ownership_files),
               'selection_method': 'Replay reviewed selection and owner anchors; not automatic proof of semantic ownership.'}
    output.mkdir(parents=True, exist_ok=True)
    (output / (scope['id'] + '-counts.json')).write_bytes(encoded({'summary': summary, 'files': actual_rows}))
    return summary


def compute_leaf(record):
    # No expected score, quality role, repository name or size reaches the rule.
    if record['method'] == 'semantic_observation_mapping':
        score, missing = semantic_rule(record['facts'])
        require(not missing and score is not None, 'Unresolved semantic observation')
        return score
    require(record['method'] == 'contract_rule_mapping', 'Unknown rule method')
    score = RULES[record['name']](record['facts'])
    require(isinstance(score, int), 'Failed or unresolved rule')
    return score


def check_substitution_execution(facts, head, data, package):
    execution = facts.get('substitution_execution')
    if not execution or execution.get('status') in {'not_run', 'failed'}:
        return
    require(facts.get('evaluation_revision') == head and execution.get('revision') == head,
            'Substitution execution revision differs')
    path = safe_path(execution['report_path'])
    require(path in package['files_sha256'], 'Unhashed substitution report')
    body = (data / path).read_bytes()
    require(sha(body) == execution['report_sha256'] == package['files_sha256'][path],
            'Substitution report hash differs')
    report = json.loads(body)
    for key in ['revision', 'parent_symbol', 'status', 'command', 'tests_passed', 'tests_failed',
                'tested_implementations', 'passed_implementations', 'coverage']:
        require(report.get(key) == execution.get(key), 'Substitution report binding differs: ' + key)


def verify(args):
    package = read(args.data / 'package.json')
    for name, digest in package['tool_source_sha256'].items():
        safe_path(name)
        require(sha((Path(__file__).resolve().parent / name).read_bytes()) == digest, 'Verifier version differs: ' + name)
    for name, digest in package['files_sha256'].items():
        safe_path(name)
        require(sha((args.data / name).read_bytes()) == digest, 'Input package hash differs: ' + name)
    require(sha((args.wrapper / 'SCORE_RULES.md').read_bytes()) in package['compatible_contract_sha256'], 'Unsupported contract')
    standard = read(args.wrapper / 'STANDARD_SCORES.json')
    manifest = read(args.wrapper / 'manifest.json')
    entries = {e['id']: e for e in manifest['repositories'] if e['delivery_status'] == 'active'}
    expected = {(r['id'], l['name']): l['score'] for r in standard['repositories'] for l in r['leaves']}
    require(len(entries) == 18 and len(expected) == 171, 'Wrong canonical denominator')
    summaries, predictions, seen = [], [], set()
    args.output.mkdir(parents=True, exist_ok=False)
    for record in package['repositories']:
        rid = record['id']
        for key in ['scope', 'rule_inputs', 'adjudication']:
            safe_path(record[key])
            require(record[key] in package['files_sha256'], 'Unhashed input: ' + record[key])
        require(rid in entries and rid not in seen, 'Unexpected/duplicate repository')
        seen.add(rid)
        entry = entries[rid]
        repo = args.sources / ('app' if entry['kind'] == 'APP' else 'framework') / entry['name']
        if not repo.exists():
            repo = args.sources / entry['name']
        snap = Snapshot(repo, entry['delivery']['expected_head'])
        refs = dict(x.split(' ', 1) for x in git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads', 'refs/tags').decode().splitlines())
        require(refs == entry['delivery']['refs'], 'Refs differ: ' + rid)
        scope = read(args.data / record['scope'])
        summaries.append(check_scope(snap, scope, args.output / 'counts'))
        inputs = read(args.data / record['rule_inputs'])
        require(inputs['head'] == snap.head, 'Rule inputs stale')
        for leaf in inputs['leaves']:
            require('score' not in leaf and 'quality_tier' not in leaf, 'Expected answer in rule input')
            require(leaf['evidence'], 'No evidence anchors')
            for anchor in leaf['evidence']:
                check_anchor(snap, anchor)
            if leaf['name'] == 'solid_principle.liskov_substitution':
                check_substitution_execution(leaf['facts'], snap.head, args.data, package)
            prediction = compute_leaf(leaf)
            key = (rid, leaf['name'])
            require(key in expected, 'Unexpected leaf')
            predictions.append({'id': rid, 'name': leaf['name'], 'score': prediction,
                                'expected': expected[key], 'match': prediction == expected[key], 'method': leaf['method']})
        print('PASS', rid, scope['source_file_count'], 'files', scope['source_loc'], 'LOC; anchors and rule mappings verified', flush=True)
    require(seen == set(entries), 'Missing repositories')
    require(len(predictions) == 171 and len({(p['id'], p['name']) for p in predictions}) == 171, 'Wrong leaf coverage')
    differences = [p for p in predictions if not p['match']]
    result = {'schema_version': 'verification-result-1', 'repositories': summaries, 'predictions': predictions,
              'leaf_count': len(predictions), 'difference_count': len(differences), 'differences': differences,
              'total': sum(p['score'] for p in predictions),
              'limits': ['Deterministic counts and rule mappings are recomputed from disclosed reviewed observations.',
                         'Evidence coordinates/hashes are checked, not the truth or exhaustiveness of human judgments.',
                         'No source build, device integration, dependency download or new semantic review is performed.']}
    (args.output / 'result.json').write_bytes(encoded(result))
    require(not differences, 'Scores differ; see result.json')
    print('PASS 18/18; 171 mappings; 0 differences; total=' + str(result['total']))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, required=True)
    ap.add_argument('--wrapper', type=Path, required=True)
    ap.add_argument('--sources', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True, help='New output directory outside wrapper/source inputs')
    args = ap.parse_args()
    for inp in [args.data, args.wrapper, args.sources]:
        require(not args.output.resolve().is_relative_to(inp.resolve()), 'Output must be outside inputs')
    verify(args)


if __name__ == '__main__':
    main()
