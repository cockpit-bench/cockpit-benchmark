"""Source-bound, single-family APP boundary regression; separate from canonical18."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

def default_paths(script):
    script = Path(script).resolve()
    public = script.parent.name == 'verification' and script.parent.parent.name != 'scripts'
    root = script.parent.parent if public else script.parents[2]
    reference = root / 'docs/boundary-reference.json' if public else root / 'staging/validation18-discrimination-20260908/boundary-reference.json'
    return root, reference, root / ('SCORE_RULES.md' if public else 'score-rules.md'), public


ROOT, DEFAULT_REFERENCE, DEFAULT_CONTRACT, PUBLIC_LAYOUT = default_paths(__file__)
ALLOWED = {'platform_reuse.release_branch_strategy', 'platform_reuse.platform_upgrade'}
BANDS = (0, 3, 8, 10)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE)


def verify_reference(reference, source_root, contract):
    """Validate bound source bytes/refs/evidence, without executing target code."""
    if sha(Path(contract).read_bytes()) != reference['contract_sha256']:
        raise ValueError('contract hash mismatch')
    cases = reference['cases']
    if len(cases) != 8 or len({r['case'] for r in cases}) != 8:
        raise ValueError('reference requires exactly eight unique cases')
    if reference.get('canonical_member') is not False or reference.get('independent_holdout') is not False:
        raise ValueError('boundary scope must remain separate and non-holdout')
    if len({r['family_id'] for r in cases}) != 1:
        raise ValueError('all eight cases must share one family')
    files = 0
    for row in cases:
        name = row['case']
        if Path(name).name != name or '/' in name or '\\' in name or name in ('.', '..'):
            raise ValueError('invalid case name')
        repo = Path(source_root) / name
        if row['leaf'] not in ALLOWED or type(row['score']) is not int or row['score'] not in BANDS:
            raise ValueError(f'{name}: invalid leaf or score')
        if not row.get('reason') or not row.get('decisive_anchors'):
            raise ValueError(f'{name}: missing adjudication')
        if git(repo, 'rev-parse', 'HEAD').decode().strip() != row['head']:
            raise ValueError(f'{name}: HEAD mismatch')
        if git(repo, 'status', '--porcelain'):
            raise ValueError(f'{name}: dirty source')
        actual_refs = git(repo, 'for-each-ref', '--format=%(refname)').decode().splitlines()
        expected_refs = [r['ref'] for r in row['refs']]
        if len(set(expected_refs)) != len(expected_refs) or sorted(actual_refs) != sorted(expected_refs):
            raise ValueError(f'{name}: refs mismatch')
        for ref in row['refs']:
            for suffix, key in [('', 'object_oid'), ('^{commit}', 'commit_oid'), ('^{tree}', 'tree_oid')]:
                if git(repo, 'rev-parse', ref['ref'] + suffix).decode().strip() != ref[key]:
                    raise ValueError(f'{name}: {ref["ref"]} {key} mismatch')
            asset = git(repo, 'show', ref['ref'] + ':app/src/main/assets/fleet.properties')
            if sha(asset) != ref['asset_sha256'] or asset.decode().splitlines() != ref['asset_lines']:
                raise ValueError(f'{name}: ref asset mismatch')
            if git(repo, 'diff', 'main', ref['ref']).decode().strip() != ref['diff_from_main']:
                raise ValueError(f'{name}: ref diff mismatch')
            if ref.get('annotation') is not None:
                if git(repo, 'for-each-ref', '--format=%(contents)', ref['ref']).decode().strip() != ref['annotation']:
                    raise ValueError(f'{name}: annotation mismatch')
        inventory = {e['path']: e for e in row['file_inventory']}
        tracked = git(repo, 'ls-files', '-z').decode().strip('\0').split('\0')
        if len(inventory) != len(row['file_inventory']) or set(tracked) != set(inventory):
            raise ValueError(f'{name}: tracked inventory mismatch')
        for path, entry in inventory.items():
            target = (repo / path).resolve()
            if not target.is_relative_to(repo.resolve()):
                raise ValueError(f'{name}: invalid evidence path')
            data = target.read_bytes()
            if sha(data) != entry['sha256'] or sha(git(repo, 'show', row['head'] + ':' + path)) != entry['sha256']:
                raise ValueError(f'{name}: file hash mismatch: {path}')
            if entry['start_line'] != 1 or entry['end_line'] != len(data.decode().splitlines()):
                raise ValueError(f'{name}: inventory line mismatch')
            files += 1
        for anchor in row['decisive_anchors']:
            if anchor['path'] not in inventory or not anchor.get('symbol'):
                raise ValueError(f'{name}: missing anchor path/symbol')
            if not 1 <= anchor['start_line'] <= anchor['end_line'] <= inventory[anchor['path']]['end_line']:
                raise ValueError(f'{name}: anchor range mismatch')
            lines = (repo / anchor['path']).read_text(encoding='utf-8').splitlines()
            if anchor['symbol'] not in '\n'.join(lines[anchor['start_line']-1:anchor['end_line']]):
                raise ValueError(f'{name}: anchor symbol mismatch')
    return {'cases': len(cases), 'files': files, 'family_count': 1, 'source_binding': 'verified'}


def evaluate(reference, predictions):
    """Missing or null scores abstain; every accuracy/recall denominator is frozen."""
    cases = reference['cases']
    expected = {r['case']: r for r in cases}
    submitted = {}
    if not isinstance(predictions, list):
        raise ValueError('predictions must be a list')
    for p in predictions:
        if not isinstance(p, dict) or not isinstance(p.get('case'), str):
            raise ValueError('each prediction needs a string case')
        name = p.get('case')
        if name not in expected or name in submitted:
            raise ValueError('unknown or duplicate prediction case')
        if p.get('leaf', expected[name]['leaf']) != expected[name]['leaf']:
            raise ValueError('prediction leaf mismatch')
        score = p.get('score')
        if score is not None and (type(score) is not int or score not in BANDS):
            raise ValueError('score must be 0, 3, 8, 10 or null')
        submitted[name] = score
    rows = [dict(case=r['case'], leaf=r['leaf'], expected=r['score'], predicted=submitted.get(r['case']),
                 correct=submitted.get(r['case']) == r['score'], abstained=submitted.get(r['case']) is None) for r in cases]
    def metric(group):
        n = len(group)
        correct = sum(r['correct'] for r in group)
        answered = sum(not r['abstained'] for r in group)
        return dict(denominator=n, correct=correct, answered=answered, abstained=n-answered,
                    accuracy=correct/n if n else None, coverage=answered/n if n else None,
                    abstention_rate=(n-answered)/n if n else None)
    strata = {leaf + ':' + str(band): metric([r for r in rows if r['leaf'] == leaf and r['expected'] == band])
              for leaf, band in sorted({(r['leaf'], r['expected']) for r in rows})}
    confusion = {str(b): dict(Counter('abstain' if r['predicted'] is None else str(r['predicted'])
                                    for r in rows if r['expected'] == b)) for b in BANDS}
    mode_hits = sum(max(Counter(r['score'] for r in cases if r['leaf'] == leaf).values())
                    for leaf in {r['leaf'] for r in cases})
    return dict(scope='APP specified-leaf boundary regression only', canonical_member=False,
                independent_holdout=False, family_count=1, overall=metric(rows),
                in_sample_leaf_mode_baseline={'hits':mode_hits,'denominator':len(cases),
                    'accuracy':mode_hits/len(cases),'method':'Post-hoc distribution diagnosis, not Agent or holdout performance'},
                by_leaf={leaf: metric([r for r in rows if r['leaf'] == leaf]) for leaf in sorted(ALLOWED)},
                by_true_band={str(b): metric([r for r in rows if r['expected'] == b]) for b in BANDS},
                leaf_band_strata=strata, macro_recall=sum(m['accuracy'] for m in strata.values())/len(strata),
                macro_denominator=len(strata), confusion=confusion, rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument('--sources', type=Path)
    parser.add_argument('--contract', type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument('--predictions', type=Path, help='JSON list or object containing predictions list')
    args = parser.parse_args()
    if PUBLIC_LAYOUT and args.sources is None:
        parser.error('public wrapper requires explicit --sources; no implicit staging source root')
    reference = json.loads(args.reference.read_text(encoding='utf-8'))
    source_root = args.sources or ROOT / reference['source_root']
    try:
        result = {'binding': verify_reference(reference, source_root, args.contract)}
        if args.predictions:
            predictions = json.loads(args.predictions.read_text(encoding='utf-8'))
            if isinstance(predictions, dict):
                predictions = predictions['predictions']
            result['evaluation'] = evaluate(reference, predictions)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f'boundary verification failed: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
