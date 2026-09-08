"""Portable, read-only reproduction of reviewed scope/counts and score mappings.

Does not execute repository build scripts or claim to infer semantic judgments.
Requires Python 3.11+ and Git. Inputs must be the published maintainer data pack.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from counting import strip_c_like_comments, count_production_lines
from rules import RULES, semantic_rule, integration_execution_metrics, api_governance_boundaries


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
    if e.get('evidence_type') == 'structured_facts':
        require(bool(e.get('source_sha256')), 'Structured repository evidence needs a source hash')
        require(bool(e.get('json_pointer')), 'Structured repository evidence needs a JSON Pointer')
        value = json_pointer(json.loads(body), e['json_pointer'])
        require(value is not None and not (isinstance(value, (str, list, dict)) and not value),
                'Structured repository evidence points to an empty value')
        return
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
            loc, regions = count_production_lines(text, language=row['language'])
            require(regions == row['excluded_generated_regions'], 'Generated region difference: ' + path)
        elif row['count_method'] == 'c_like_comments':
            loc = sum(bool(x.strip()) for x in strip_c_like_comments(text, language=row['language']).splitlines())
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


def check_api_governance(facts, snap, data=None, package=None):
    require(facts.get('evaluation_revision') == snap.head, 'API evaluation revision differs')
    if data is not None:
        inventory=facts['api_governance'].get('source_inventory')
        require(isinstance(inventory,dict),'API source inventory missing')
        path=safe_path(inventory['path'])
        require(path in package['files_sha256'],'API source inventory not hashed')
        body=(data/path).read_bytes()
        require(sha(body)==inventory['sha256']==package['files_sha256'][path],'API source inventory hash differs')
        record=json.loads(body)
        require(record.get('head')==snap.head,'API source inventory stale')
        require(record.get('tracked_paths_sha256')==sha(encoded(sorted(snap.entries))),'API source inventory tree differs')
    for boundary in api_governance_boundaries(facts):
        bindings=boundary.get('binding_files',[])
        require(isinstance(bindings,list),'API binding files must be listed')
        paths=[]
        for artifact in bindings:
            path=safe_path(artifact['path']);paths.append(path)
            require(artifact.get('commit')==snap.head,'API artifact revision differs')
            body=snap.body(path)
            require(sha(body)==artifact['source_sha256'],'API artifact SHA differs: '+path)
            require(snap.entries[path]['oid']==artifact['git_blob'],'API artifact blob differs: '+path)
        require(len(paths)==len(set(paths)),'Duplicate API binding artifact')
        anchors=boundary['evidence']
        require(len({(e.get('path'), e.get('start_line'), e.get('end_line'), e.get('json_pointer')) for e in anchors})>=2,
                'API boundary needs independent source anchors')
        for anchor in anchors:
            require(anchor.get('source') == 'repository' and bool(anchor.get('source_sha256')), 'API evidence needs frozen source bytes')
            check_anchor(snap, anchor)


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


def check_integration_execution(facts, snap, data, package):
    """Check retained report/artifact bytes and remote workflow against the source.

    This binds disclosed observations. It neither runs Android tests nor proves
    that a supplied runner report is authentic or its interaction scope complete.
    """
    if integration_execution_metrics(facts) is None:
        return
    execution=facts['integration_execution']
    require(facts['evaluation_revision']==execution['revision']==snap.head,
            'Integration execution HEAD differs')
    def checked_file(path, digest):
        path=safe_path(path)
        require(path in package['files_sha256'], 'Unhashed integration report/artifact: '+path)
        body=(data/path).read_bytes()
        require(sha(body)==digest==package['files_sha256'][path], 'Integration report/artifact hash differs: '+path)
        return body
    body=checked_file(execution['report_path'],execution['report_sha256'])
    report=json.loads(body)
    expected={k:v for k,v in execution.items() if k not in {'report_path','report_sha256'}}
    require(report==expected,'Integration report binding differs')
    for artifact in execution['artifacts']:
        checked_file(artifact['path'],artifact['sha256'])
    if execution['mode']=='remote_ci':
        ci=execution['ci'];path=safe_path(ci['workflow_path'])
        require(ci['revision']==snap.head,'Integration CI HEAD differs')
        require(path in snap.entries and snap.entries[path]['kind']=='blob'
                and snap.entries[path]['oid']==ci['workflow_blob'],'Integration workflow blob differs')
        require(sha(snap.body(path))==ci['workflow_sha256'],'Integration workflow SHA differs')


def indexed(rows, key, label):
    result = {row[key]: row for row in rows}
    require(len(result) == len(rows), 'Duplicate ' + label)
    return result


def json_pointer(document, pointer):
    require(isinstance(pointer, str) and pointer.startswith('/'), 'Invalid JSON Pointer')
    value = document
    try:
        for token in pointer[1:].split('/'):
            require(not re.search(r'~(?![01])', token), 'Invalid JSON Pointer escape')
            key = token.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                require(bool(re.fullmatch(r'0|[1-9][0-9]*', key)), 'Invalid JSON Pointer array index')
                value = value[int(key)]
            else:
                value = value[key]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('JSON Pointer does not resolve: ' + pointer) from exc
    return value


def check_delivery_consistency(wrapper, standard, manifest):
    """Compare the complete canonical answers, facts and human score tables.

    This is a synchronization check, not a second semantic judgment. Comparing
    only numeric predictions misses stale reasons and evidence at the same score.
    """
    entries = indexed([e for e in manifest['repositories'] if e['delivery_status'] == 'active'], 'id', 'manifest repository')
    repos = indexed(standard['repositories'], 'id', 'standard repository')
    require(set(repos) == set(entries), 'Standard/manifest repositories differ')
    contract_hash = sha((wrapper / 'SCORE_RULES.md').read_bytes())
    require(standard['contract']['sha256'] == contract_hash, 'Standard contract differs')
    expected_csv, facts_by_id, schemas = {}, {}, set()
    md = ['# Validation-18 ' + standard['version'], '',
          '| ID | Repository | Size | Quality | Score |', '|---|---|---|---|---|']
    for rid, repo in repos.items():
        entry = entries[rid]
        for field in ['name', 'kind', 'quality_tier', 'size_band']:
            require(repo[field] == entry[field], 'Standard/manifest ' + field + ' differs: ' + rid)
        require(repo['head'] == entry['delivery']['expected_head'], 'Standard/manifest HEAD differs: ' + rid)
        oracle = read(wrapper / safe_path(entry['oracle_path']))
        facts = read(wrapper / safe_path(oracle['facts_path']))
        facts_by_id[rid] = facts
        schemas.add(oracle['schema_version'])
        require(oracle['repo_id'] == facts['repo_id'] == rid, 'Oracle/facts repository differs: ' + rid)
        require(oracle['repository']['head'] == facts['head'] == repo['head'], 'Oracle/facts HEAD differs: ' + rid)
        require(oracle['repository']['tree'] == facts['tree'] == repo['tree'], 'Oracle/facts tree differs: ' + rid)
        require(oracle['rubric']['sha256'] == facts['contract_sha256'] == contract_hash, 'Oracle/facts contract differs: ' + rid)
        for field in ['quality_tier', 'size_band']:
            require(oracle[field] == repo[field], 'Oracle ' + field + ' differs: ' + rid)
        leaves = indexed(repo['leaves'], 'name', 'standard leaf: ' + rid)
        adopted = indexed(oracle['canonical_leaves'], 'name', 'oracle leaf: ' + rid)
        require(leaves == adopted, 'Standard/oracle canonical leaf content differs: ' + rid)
        require(set(facts['leaf_facts']) == set(leaves), 'Facts leaf set differs: ' + rid)
        if 'platform_seven' in facts:
            name = 'platform_reuse.platform_upgrade'
            require(name in leaves, 'Platform summary has no canonical leaf: ' + rid)
            decisive = facts['leaf_facts'][name]['decisive_facts']
            for key, value in facts['platform_seven'].items():
                fact_key = 'non_compatible_api_all_covered' if key == 'all_noncompatible_covered' else key
                if fact_key in decisive:
                    require(value == decisive[fact_key], 'Platform summary fact differs: ' + rid + '/' + key)
                if key in {'coverage_explanation', 'binding_explanation'}:
                    require(value == leaves[name]['analysis'], 'Platform summary explanation differs: ' + rid + '/' + key)
        total = sum(l['score'] for l in leaves.values())
        maximum = sum(l['max_score'] for l in leaves.values())
        require(repo['total'] == oracle['canonical_total'] == {'score': total, 'max': maximum}, 'Repository total differs: ' + rid)
        ps = facts['production_scope']
        require(ps['source_loc'] == entry['source_loc'] and ps['source_file_count'] == entry['source_files']
                and ps['size_band'] == entry['size_band'], 'Manifest/facts production counts differ: ' + rid)
        for ref_summary in [facts['refs'], facts['release_branch_facts']['complete_refs']]:
            refs = json_pointer(manifest, ref_summary['json_pointer'])
            require(ref_summary['path'] == 'manifest.json' and refs == entry['delivery']['refs']
                    and ref_summary['count'] == len(refs) and ref_summary['sha256'] == sha(encoded(refs)),
                    'Facts/manifest refs differ: ' + rid)
        for leaf in leaves.values():
            name = leaf['name']
            indices = facts['leaf_facts'][name]['evidence_indices']
            require(all(type(i) is int and 0 <= i < len(facts['source_evidence']) for i in indices),
                    'Invalid facts evidence index: ' + rid + '/' + name)
            materialized = [facts['source_evidence'][i] for i in indices]
            require(materialized == leaf['evidence'], 'Canonical/facts evidence differs: ' + rid + '/' + name)
            for anchor in leaf['evidence']:
                require(anchor['commit'] == repo['head'], 'Canonical evidence HEAD differs: ' + rid)
                if anchor['source'] == 'repository':
                    continue  # Source hashes/coordinates checked with the actual Git snapshot below.
                path = safe_path(anchor['path'])
                require(path in {oracle['facts_path'], 'manifest.json'}, 'Unexpected canonical structured source')
                document = facts if path == oracle['facts_path'] else manifest
                json_pointer(document, anchor['json_pointer'])
            expected_csv[(rid, name)] = {
                'id': rid, 'name': repo['name'], 'kind': repo['kind'], 'quality_tier': repo['quality_tier'],
                'size_band': repo['size_band'], 'head': repo['head'], 'leaf': name,
                'score': str(leaf['score']), 'max_score': str(leaf['max_score']),
                'status': leaf['status'], 'score_reasoning': leaf['score_reasoning']}
        md.append(f"| {rid} | {repo['name']} | {repo['size_band']} | {repo['quality_tier']} | {total}/{maximum} |")
    require(len(schemas) == 1, 'Oracle schema versions differ')
    summary = standard['summary']
    require(summary['repository_count'] == len(repos) and summary['leaf_count'] == len(expected_csv)
            and summary['score'] == sum(r['total']['score'] for r in repos.values())
            and summary['max_score'] == sum(int(r['max_score']) for r in expected_csv.values())
            and summary['pending_repository_count'] == sum(e['delivery_status'] == 'pending' for e in manifest['repositories']),
            'Standard summary differs')
    with (wrapper / 'SCORECARD.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    actual_csv = {(r['id'], r['leaf']): r for r in rows}
    require(len(actual_csv) == len(rows) and actual_csv == expected_csv, 'SCORECARD.csv content differs')
    for repo in repos.values():
        md += ['', '## ' + repo['id'] + ' ' + repo['name'], '', '| Leaf | Score | Reason |', '|---|---|---|']
        for leaf in repo['leaves']:
            reason = leaf['score_reasoning'].replace('|', '\\|').replace('\n', ' ')
            md.append(f"| {leaf['name']} | {leaf['score']}/{leaf['max_score']} | {reason} |")
    require((wrapper / 'SCORECARD.md').read_text(encoding='utf-8').strip() == '\n'.join(md),
            'SCORECARD.md content differs')
    return facts_by_id


def check_disclosed_inputs(facts, scope, inputs):
    """The published compact facts must agree with the inputs actually replayed."""
    rid = facts['repo_id']
    require(scope['id'] == rid and scope['head'] == inputs['head'] == facts['head'], 'Disclosed input identity differs: ' + rid)
    for key in ['source_loc', 'source_file_count', 'size_band', 'path_set_sha256']:
        require(scope[key] == facts['production_scope'][key], 'Disclosed scope differs: ' + rid + '/' + key)
    leaves = indexed(inputs['leaves'], 'name', 'disclosed input leaf: ' + rid)
    require(set(leaves) == set(facts['leaf_facts']), 'Disclosed input leaf set differs: ' + rid)
    for name, record in facts['leaf_facts'].items():
        leaf = leaves[name]
        for key, value in record['decisive_facts'].items():
            require(key in leaf['facts'] and leaf['facts'][key] == value, 'Disclosed decisive fact differs: ' + rid + '/' + name + '/' + key)
        # Extra source anchors in the full pack are supplemental; every canonical
        # source anchor must still be present and verified against the same HEAD.
        supplied = {encoded(e) for e in leaf['evidence']}
        for index in record['evidence_indices']:
            e = facts['source_evidence'][index]
            if e['source'] == 'repository':
                require(encoded(e) in supplied, 'Disclosed canonical evidence missing: ' + rid + '/' + name)


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
    facts_by_id = check_delivery_consistency(args.wrapper, standard, manifest)
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
        check_disclosed_inputs(facts_by_id[rid], scope, inputs)
        for leaf in inputs['leaves']:
            require('score' not in leaf and 'quality_tier' not in leaf, 'Expected answer in rule input')
            require(leaf['evidence'], 'No evidence anchors')
            for anchor in leaf['evidence']:
                check_anchor(snap, anchor)
            if leaf['name'] == 'solid_principle.liskov_substitution':
                check_substitution_execution(leaf['facts'], snap.head, args.data, package)
            if leaf['name'] == 'quality.integration_test':
                check_integration_execution(leaf['facts'], snap, args.data, package)
            if leaf['name'] == 'compilation.api_version_management':
                check_api_governance(leaf['facts'], snap, args.data, package)
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
