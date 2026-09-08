"""Reject evaluation splits that separate repositories with the same recorded lineage.

This validates an explicit repository-id -> split-name JSON assignment. It does
not certify unseen lineage or turn a public development set into a holdout.
"""
import argparse
import json
from pathlib import Path


def check_split(manifest, assignments, require_complete=False):
    entries = {r['id']: r for r in manifest['repositories'] if r['delivery_status'] == 'active'}
    if not isinstance(assignments, dict) or not assignments:
        raise ValueError('Assignments must be a nonempty repository-id -> split-name object')
    if set(assignments) - set(entries):
        raise ValueError('Unknown or pending repository in split assignment')
    if require_complete and set(assignments) != set(entries):
        raise ValueError('Complete assignment must include every active repository')
    families = {}
    for rid, split in assignments.items():
        if not isinstance(split, str) or not split.strip():
            raise ValueError('Split names must be nonempty strings')
        family = entries[rid].get('family_id')
        if not isinstance(family, str) or not family:
            raise ValueError('Missing family_id for ' + rid)
        group = families.setdefault(family, {'splits': set(), 'repositories': []})
        group['splits'].add(split)
        group['repositories'].append(rid)
    violations = {f: g for f, g in families.items() if len(g['splits']) != 1}
    if violations:
        details = '; '.join(f + ': ' + ','.join(sorted(g['repositories']))
                            for f, g in sorted(violations.items()))
        raise ValueError('Same lineage crosses evaluation splits: ' + details)
    return {'repositories': len(assignments), 'families': len(families),
            'complete': set(assignments) == set(entries),
            'limit': 'Checks recorded family_id only; not an independent holdout certificate.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wrapper', type=Path, required=True)
    parser.add_argument('--assignments', type=Path, required=True)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((args.wrapper / 'manifest.json').read_text(encoding='utf-8'))
    assignments = json.loads(args.assignments.read_text(encoding='utf-8'))
    print(json.dumps(check_split(manifest, assignments, args.require_complete), sort_keys=True))


if __name__ == '__main__':
    main()
