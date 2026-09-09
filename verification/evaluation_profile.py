"""Pre-register evidence eligibility and compare results on a fixed leaf set.

Maintainer-side only. This validates declarations, not raw-packet authenticity,
network isolation, or whether a profile was actually saved before inference.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

MODES = {'source_only', 'frozen_external', 'live_environment'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def indexed(rows):
    if not isinstance(rows, list):
        raise ValueError('leaves must be a list')
    result = {}
    for row in rows:
        key = row.get('id')
        if not isinstance(key, str) or not key or key in result:
            raise ValueError('missing or duplicate leaf id')
        result[key] = row
    return result


def register(availability, mode, context):
    if mode not in MODES:
        raise ValueError('unknown evidence mode')
    for key in ('reference_id', 'source_manifest_sha256'):
        if not isinstance(context.get(key), str) or not context[key]:
            raise ValueError('missing context ' + key)
        if key in availability and availability[key] != context[key]:
            raise ValueError('availability context mismatch: ' + key)
    if mode == 'live_environment' and not context.get('capture_batch_id'):
        raise ValueError('live mode requires capture_batch_id')
    leaves = indexed(availability['leaves'])
    if not leaves:
        raise ValueError('empty availability inventory')
    eligible, exclusions = [], []
    for key, row in sorted(leaves.items()):
        support = row.get('modes', {}).get(mode, {})
        reason = None
        if row.get('reference_status') == 'unresolved':
            reason = 'reference_unresolved'
        elif row.get('reference_id') != context['reference_id']:
            reason = 'reference_mismatch'
        elif support.get('state') != 'supported':
            reason = 'evidence_unknown_or_unavailable'
        elif not support.get('basis') or not support.get('evidence_ids'):
            reason = 'missing_support_basis'
        elif mode == 'source_only' and (row.get('requires_external') is not False
                                      or support.get('kind') != 'source'):
            reason = 'external_evidence_required_or_unknown'
        elif mode == 'frozen_external':
            if support.get('kind') == 'source':
                if row.get('requires_external') is not False:
                    reason = 'external_evidence_required_or_unknown'
            elif support.get('kind') != 'frozen_raw':
                reason = 'raw_packet_required'
            elif (support.get('raw_complete') is not True
                  or not context.get('external_packet_sha256')
                  or support.get('packet_sha256') != context['external_packet_sha256']):
                reason = 'raw_packet_incomplete_or_mismatch'
        elif mode == 'live_environment':
            if (support.get('kind') != 'live_raw' or support.get('raw_complete') is not True
                    or support.get('capture_batch_id') != context['capture_batch_id']
                    or row.get('reference_batch_id') != context['capture_batch_id']):
                reason = 'live_reference_or_capture_batch_mismatch'
        if reason:
            exclusions.append({'id': key, 'reason': reason,
                               'detail': support.get('basis', '')})
        else:
            eligible.append(key)
    profile = {'schema': 'evaluation-profile-v1', 'mode': mode, 'context': context,
               'availability_sha256': digest(availability), 'requested': sorted(leaves),
               'eligible': eligible, 'exclusions': exclusions,
               'eligible_set_sha256': digest(eligible)}
    profile['profile_sha256'] = digest(profile)
    return profile


def validate_profile(profile):
    body = {k: v for k, v in profile.items() if k != 'profile_sha256'}
    if digest(body) != profile.get('profile_sha256'):
        raise ValueError('profile digest mismatch')
    if digest(profile['eligible']) != profile['eligible_set_sha256']:
        raise ValueError('eligible set digest mismatch')
    if (len(set(profile['requested'])) != len(profile['requested'])
            or len(set(profile['eligible'])) != len(profile['eligible'])
            or set(profile['eligible']) | {x['id'] for x in profile['exclusions']}
            != set(profile['requested'])
            or set(profile['eligible']) & {x['id'] for x in profile['exclusions']}):
        raise ValueError('invalid profile partition')


def common(profiles):
    """Compute before candidate runs; different modes/snapshots cannot share a ranking."""
    if not profiles:
        raise ValueError('no profiles')
    for p in profiles:
        validate_profile(p)
    first = profiles[0]
    if any((p['mode'], p['context'], p['requested']) !=
           (first['mode'], first['context'], first['requested']) for p in profiles):
        raise ValueError('different mode, reference, snapshot, batch, or requested universe')
    selected = sorted(set.intersection(*(set(p['eligible']) for p in profiles)))
    result = dict(first, eligible=selected, eligible_set_sha256=digest(selected))
    result['parent_profiles'] = sorted(p['profile_sha256'] for p in profiles)
    result['exclusions'] = [{'id': k, 'reason': 'not_eligible_in_all_profiles',
                             'parent_exclusions': [e for p in profiles for e in p['exclusions']
                                                   if e['id'] == k]}
                            for k in first['requested'] if k not in selected]
    result.pop('profile_sha256')
    result['profile_sha256'] = digest(result)
    return result


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def compare(profile, reference, candidate):
    validate_profile(profile)
    if reference.get('context') != profile['context']:
        raise ValueError('reference context mismatch')
    if candidate.get('profile_sha256') != profile['profile_sha256']:
        raise ValueError('candidate profile mismatch')
    gold = indexed(reference['leaves']); predictions = indexed(candidate['leaves'])
    if set(predictions) - set(profile['requested']):
        raise ValueError('unknown candidate leaf')
    counts = {'correct': 0, 'incorrect': 0, 'abstained': 0, 'error': 0, 'missing': 0}
    for key in profile['eligible']:
        if key not in gold or not number(gold[key].get('score')):
            raise ValueError('missing or invalid eligible reference score: ' + key)
        row = predictions.get(key)
        if row is None:
            counts['missing'] += 1
        elif row.get('status') == 'abstain':
            counts['abstained'] += 1
        elif row.get('status') == 'error':
            counts['error'] += 1
        elif row.get('status') == 'scored' and number(row.get('score')):
            counts['correct' if row['score'] == gold[key]['score'] else 'incorrect'] += 1
        else:
            counts['error'] += 1
    n = len(profile['eligible']); total = len(profile['requested'])
    return {'profile_sha256': profile['profile_sha256'], 'mode': profile['mode'],
            'requested': total, 'common_eligible': n, 'exclusions': profile['exclusions'],
            'excluded_predictions_ignored': sorted(set(predictions) - set(profile['eligible'])),
            'evidence_coverage': n / total if total else None,
            'output_coverage': (counts['correct'] + counts['incorrect']) / n if n else None,
            'accuracy': counts['correct'] / n if n else None, **counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    reg = sub.add_parser('register'); reg.add_argument('--availability', required=True)
    reg.add_argument('--mode', choices=sorted(MODES), required=True); reg.add_argument('--context', required=True)
    com = sub.add_parser('common'); com.add_argument('--profiles', nargs='+', required=True)
    cmp = sub.add_parser('compare'); cmp.add_argument('--profile', required=True)
    cmp.add_argument('--reference', required=True); cmp.add_argument('--candidate', required=True)
    for item in (reg, com, cmp): item.add_argument('--output', required=True)
    args = parser.parse_args()
    def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
    if args.command == 'register': result = register(read(args.availability), args.mode, read(args.context))
    elif args.command == 'common': result = common([read(p) for p in args.profiles])
    else: result = compare(read(args.profile), read(args.reference), read(args.candidate))
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
