"""Maintainer-side fixed-set evaluation with distribution and evidence adjudication.

Prepare before inference, give candidates only the opaque profile digest and
allowed source/contract inputs, then assess saved outputs. This program does not
execute a model, enforce OS isolation, or certify when registration occurred.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

import evaluation_profile as ep
from check_split import check_split
from coverage import TIERS
from external_inputs import verify as verify_external_packet


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def prepare(wrapper, mode, assignments, profile=None, external_packet=None):
    """Bind the actual public snapshot and lineage before seeing predictions."""
    wrapper = Path(wrapper)
    context = read(wrapper / 'docs/evaluation-context.json')
    for field, path in [('canonical_standard_sha256', 'STANDARD_SCORES.json'),
                        ('contract_sha256', 'SCORE_RULES.md'),
                        ('source_manifest_sha256', 'manifest.json')]:
        if context.get(field) != file_sha(wrapper / path):
            raise ValueError('snapshot file mismatch: ' + path)
    standard = read(wrapper / 'STANDARD_SCORES.json')
    manifest = read(wrapper / 'manifest.json')
    split = check_split(manifest, assignments, require_complete=True)
    availability = read(wrapper / 'docs/evidence-availability.json')
    registered = ep.register(availability, mode, context)
    if profile is None:
        profile = registered
    else:
        ep.validate_profile(profile)
        if (profile['context'] != context or profile['mode'] != mode
                or profile['requested'] != registered['requested']
                or not set(profile['eligible']) <= set(registered['eligible'])):
            raise ValueError('common profile differs from snapshot/mode/available universe')
    # No silent environment-dependent fallback from a frozen/live batch.
    if not profile['eligible']:
        raise ValueError('no eligible leaves for this evidence mode')
    requires_packet = mode == 'frozen_external' and any(row['id'] in profile['eligible']
            and row.get('modes', {}).get(mode, {}).get('kind') == 'frozen_raw' for row in availability['leaves'])
    packet_check = None
    if requires_packet:
        if external_packet is None:
            raise ValueError('frozen batch requires the actual external packet before registration')
        packet_check = verify_external_packet(external_packet, context['external_packet_sha256'])
    elif external_packet is not None:
        raise ValueError('this profile does not permit/require an external Git packet')
    entries = {r['id']: r for r in manifest['repositories'] if r['delivery_status'] == 'active'}
    leaves = []
    for repo in standard['repositories']:
        if repo['id'] not in entries:
            raise ValueError('reference repository absent from active manifest')
        for leaf in repo['leaves']:
            leaves.append({'id': repo['id'] + '/' + leaf['name'], 'score': leaf['score'],
                           'kind': repo['kind'], 'name': leaf['name'], 'repository_id': repo['id'],
                           'allowed_scores': TIERS[leaf['name']], 'split': assignments[repo['id']]})
    if set(ep.indexed(leaves)) != set(profile['requested']):
        raise ValueError('profile/reference universe mismatch')
    reference = {'context': context, 'leaves': leaves}
    batch = {'schema': 'evaluation-batch-v1', 'profile': profile, 'reference': reference,
             'manifest_file_sha256': file_sha(wrapper / 'manifest.json'),
             'assignments': assignments, 'lineage_check': split, 'external_packet_check': packet_check,
             'limits': 'Public Dev/Regression; registration digest is not a timestamp or isolation proof.'}
    batch['batch_sha256'] = ep.digest(batch)
    return batch


def validate_batch(batch):
    if ep.digest({k: v for k, v in batch.items() if k != 'batch_sha256'}) != batch.get('batch_sha256'):
        raise ValueError('batch digest mismatch')
    ep.validate_profile(batch['profile'])
    if batch['reference']['context'] != batch['profile']['context']:
        raise ValueError('batch reference context mismatch')


def distribution(profile, reference, candidate):
    predictions = ep.indexed(candidate['leaves'])
    gold = ep.indexed(reference['leaves'])
    groups = defaultdict(list)
    for key in profile['eligible']:
        row = gold[key]
        groups[(row['split'], row['kind'], row['name'])].append(row)
    rows = []
    for (split, kind, name), selected in sorted(groups.items()):
        counts = Counter(r['score'] for r in selected)
        n = len(selected)
        correct = sum(predictions.get(r['id'], {}).get('status') == 'scored'
                      and ep.number(predictions[r['id']].get('score'))
                      and predictions[r['id']]['score'] == r['score'] for r in selected)
        rows.append({'split': split, 'kind': kind, 'name': name, 'eligible': n,
                     'gold_counts': dict(sorted(counts.items())),
                     'missing_bands': [s for s in selected[0]['allowed_scores'] if s not in counts],
                     'modal_scores': sorted(s for s, count in counts.items() if count == max(counts.values())),
                     'modal_hits': max(counts.values()), 'candidate_correct': correct,
                     'candidate_accuracy': correct / n, 'modal_accuracy': max(counts.values()) / n})
    n = len(profile['eligible'])
    return {'groups': rows, 'modal_hits': sum(r['modal_hits'] for r in rows),
            'modal_accuracy': sum(r['modal_hits'] for r in rows) / n if n else None,
            'macro_candidate_accuracy': sum(r['candidate_accuracy'] for r in rows) / len(rows) if rows else None,
            'macro_modal_accuracy': sum(r['modal_accuracy'] for r in rows) / len(rows) if rows else None,
            'baseline_scope': 'Post-hoc in-sample mode by split/type/leaf on exactly the eligible set; not model accuracy.'}


def review_plan(batch, candidate, sample_size, seed):
    """Freeze a reproducible sample before adjudication; never select on correctness."""
    validate_batch(batch)
    ep.compare(batch['profile'], batch['reference'], candidate)
    if not isinstance(sample_size, int) or isinstance(sample_size, bool) or sample_size < 0:
        raise ValueError('invalid sample size')
    population = sorted(batch['profile']['eligible'])
    if sample_size > len(population):
        raise ValueError('sample larger than eligible population')
    selected = sorted(sorted(population, key=lambda k: ep.digest([str(seed), k]))[:sample_size])
    plan = {'schema': 'evidence-review-plan-v1', 'batch_sha256': batch['batch_sha256'],
            'candidate_sha256': ep.digest(candidate), 'seed': str(seed), 'population': population,
            'selected': selected,
            'method': 'Deterministic hash sample of all eligible leaves, including missing/abstained outputs.'}
    plan['plan_sha256'] = ep.digest(plan)
    return plan


def evidence_metrics(batch, candidate, plan, adjudications):
    if (plan.get('batch_sha256') != batch['batch_sha256']
            or plan.get('candidate_sha256') != ep.digest(candidate)):
        raise ValueError('review plan batch/candidate mismatch')
    expected = review_plan(batch, candidate, len(plan['selected']), plan['seed'])
    if plan != expected:
        raise ValueError('review plan changed')
    if adjudications.get('plan_sha256') != plan['plan_sha256']:
        raise ValueError('adjudication plan mismatch')
    rows = ep.indexed(adjudications['leaves'])
    if set(rows) - set(plan['selected']):
        raise ValueError('adjudication outside fixed sample')
    counts = Counter()
    joint = 0
    predictions = ep.indexed(candidate['leaves'])
    gold = ep.indexed(batch['reference']['leaves'])
    for key in plan['selected']:
        row = rows.get(key)
        if row is None:
            counts['unreviewed'] += 1
            continue
        status = row.get('verdict')
        if status not in {'supported', 'contradicted', 'insufficient', 'no_output'}:
            raise ValueError('invalid evidence verdict')
        for field in ['reviewer', 'rationale', 'reviewed_at']:
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError('missing adjudication ' + field)
        pred = predictions.get(key, {})
        has_output = pred.get('status') == 'scored' and ep.number(pred.get('score'))
        if (status == 'no_output') == has_output:
            raise ValueError('verdict incompatible with candidate output')
        # Anchors are the reviewer-selected supporting/refuting evidence, not oracle text matches.
        if status == 'supported' and (not isinstance(pred.get('reasoning'), str)
                                       or not pred['reasoning'].strip() or not pred.get('evidence')):
            raise ValueError('supported verdict requires candidate reasoning and evidence')
        if status in {'supported', 'contradicted'}:
            if not isinstance(row.get('anchors'), list) or not row['anchors']:
                raise ValueError('semantic verdict requires reviewed anchors')
            for anchor in row['anchors']:
                if not isinstance(anchor, dict) or any(not isinstance(anchor.get(k), str)
                        or not anchor[k].strip() for k in ['path', 'revision', 'location', 'claim']):
                    raise ValueError('reviewed anchor requires path/revision/location/claim')
        counts[status] += 1
        joint += status == 'supported' and has_output and pred['score'] == gold[key]['score']
    n = len(plan['selected'])
    reviewed = n - counts['unreviewed']
    return {'sample_size': n, 'reviewed': reviewed, 'counts': dict(counts),
            'review_coverage': reviewed / n if n else None,
            'supported_fraction_of_reviewed': counts['supported'] / reviewed if reviewed else None,
            'supported_fraction_of_fixed_sample': counts['supported'] / n if n else None,
            'correct_score_and_supported_evidence': joint,
            'joint_fraction_of_fixed_sample': joint / n if n else None,
            'limit': 'Human semantic adjudication of sampled whole-leaf reasoning; not automated truth or full-population certification.'}


def assess(batch, candidate, plan=None, adjudications=None):
    validate_batch(batch)
    gold = ep.indexed(batch['reference']['leaves'])
    for row in candidate['leaves']:
        if (row.get('status') == 'scored' and row['id'] in batch['profile']['eligible']
                and (not ep.number(row.get('score')) or row['score'] not in gold[row['id']]['allowed_scores'])):
            raise ValueError('illegal score tier: ' + row['id'])
    result = ep.compare(batch['profile'], batch['reference'], candidate)
    result.update(batch_sha256=batch['batch_sha256'], candidate_sha256=ep.digest(candidate),
                  distribution=distribution(batch['profile'], batch['reference'], candidate))
    if (plan is None) != (adjudications is None):
        raise ValueError('review plan and adjudications must be supplied together')
    result['evidence_validity'] = (evidence_metrics(batch, candidate, plan, adjudications) if plan is not None
                                   else {'status': 'not_reviewed', 'accuracy': None})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare'); prep.add_argument('--wrapper', required=True)
    prep.add_argument('--mode', choices=sorted(ep.MODES), required=True)
    prep.add_argument('--assignments', required=True); prep.add_argument('--profile'); prep.add_argument('--external-packet')
    sample = sub.add_parser('sample'); sample.add_argument('--size', type=int, required=True)
    sample.add_argument('--seed', required=True)
    score = sub.add_parser('assess'); score.add_argument('--review-plan'); score.add_argument('--adjudications')
    for p in (sample, score):
        p.add_argument('--batch', required=True); p.add_argument('--candidate', required=True)
    for p in (prep, sample, score): p.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.command == 'prepare': result = prepare(args.wrapper, args.mode, read(args.assignments),
                                                  read(args.profile) if args.profile else None, args.external_packet)
    elif args.command == 'sample': result = review_plan(read(args.batch), read(args.candidate), args.size, args.seed)
    else: result = assess(read(args.batch), read(args.candidate),
                          read(args.review_plan) if args.review_plan else None,
                          read(args.adjudications) if args.adjudications else None)
    out = Path(args.output)
    if out.exists():
        raise ValueError('refusing to overwrite a saved batch, plan, or result; choose a new output path')
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
