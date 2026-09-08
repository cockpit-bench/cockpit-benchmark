"""Fail-closed checks shared by extraction, final verification and frozen restore.

Run evidence schema 1.0 is deliberately explicit: each stage has run-binding.json,
binding the immutable model, consumed inputs and produced result artifacts. Coverage
uses cvdata's checksum namespace, never the BlockDiagram execution checksum.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path


class EvidenceError(ValueError):
    """Missing, stale or contradictory evidence; not a successful empty result."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def read_json(path):
    path = Path(path)
    require(path.is_file(), f'Missing evidence: {path}')
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError, UnicodeError) as exc:
        raise EvidenceError(f'Invalid JSON: {path}: {exc}') from exc


def digest(path):
    path = Path(path)
    require(path.is_file(), f'Missing artifact: {path}')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_digest(files):
    """Digest exactly snapshot.files, including paths, modes, blob IDs and hashes."""
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False).encode('utf-8')).hexdigest()


def resolve_path(value, base):
    require(isinstance(value, str) and bool(value), 'Artifact path must be nonempty')
    path = Path(value)
    return path.resolve() if path.is_absolute() else (Path(base) / path).resolve()


def verify_hash(path, expected):
    require(isinstance(expected, str) and re.fullmatch(r'[0-9a-f]{64}', expected),
            f'Invalid SHA-256 for {path}')
    actual = digest(path)
    require(actual == expected, f'Artifact hash mismatch: {path}: {actual} != {expected}')
    return actual


def verify_artifacts(records, base):
    require(isinstance(records, list) and bool(records), 'Artifact list must not be empty')
    checked = {}
    for record in records:
        require(isinstance(record, dict), 'Artifact entry must be an object')
        path = resolve_path(record.get('path'), base)
        verify_hash(path, record.get('sha256'))
        if path in checked:
            require(checked[path] == record['sha256'], f'Conflicting artifact hashes: {path}')
        checked[path] = record['sha256']
    return checked


def validate_frozen_snapshot(snap, expected):
    for key in ('head', 'tree', 'refs'):
        require(key in expected, f'Frozen manifest missing {key}')
        require(snap.get(key) == expected[key], f'Frozen manifest {key} mismatch')
    require(isinstance(expected.get('files_sha256'), str), 'Frozen manifest missing files_sha256')
    require(files_digest(snap['files']) == expected['files_sha256'], 'Frozen manifest files_sha256 mismatch')
    require(snap.get('clean') is True and snap.get('remote_count') == 0 and snap.get('shallow') is False,
            'Repository must be clean, remote-free and complete history')


def count(value, name, *, positive=False):
    require(type(value) is int and value >= (1 if positive else 0), f'Invalid {name}: {value!r}')
    return value


def decision_count(value, name='decision'):
    require(isinstance(value, list) and len(value) == 2, f'Invalid {name} pair: {value!r}')
    covered, total = (count(x, name) for x in value)
    require(covered <= total, f'{name}: covered exceeds total')
    return [covered, total]


def finite_number(value, name, *, allow_bool=False):
    valid_type = type(value) in (int, float) or (allow_bool and type(value) is bool)
    try:
        valid = valid_type and math.isfinite(value)
    except (OverflowError, TypeError, ValueError):
        valid = False
    require(valid, f'Invalid finite number for {name}: {value!r}')
    return value


def finite_vector(values, length, name, *, boolean=False):
    require(isinstance(values, list) and len(values) == length, f'{name} length mismatch')
    for index, value in enumerate(values):
        finite_number(value, f'{name}[{index}]', allow_bool=True)
        if boolean:
            require(value in (0, 1), f'{name}[{index}] must be boolean or 0/1')


def finite_matrix(rows, width, name):
    require(isinstance(rows, list) and bool(rows), f'Empty {name}')
    for index, row in enumerate(rows):
        finite_vector(row, width, f'{name}[{index}]')


def result_alias(result, primary, alias):
    """Accept documented old names, but never choose between contradictions."""
    if primary in result and alias in result:
        try:
            left = json.dumps(result[primary], sort_keys=True, allow_nan=False)
            right = json.dumps(result[alias], sort_keys=True, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise EvidenceError(f'Invalid {primary}/{alias} aliases') from exc
        require(left == right, f'Conflicting {primary}/{alias} aliases')
    return result.get(primary, result.get(alias))


def test_cases(result):
    """Normalize the actual MIL `tests` and native `cases` result formats."""
    cases = result_alias(result, 'tests', 'cases')
    if 'tests' in result or 'cases' in result:
        require(isinstance(cases, list) and bool(cases), 'Empty test cases')
        require(all(isinstance(case, dict) for case in cases), 'Test case must be an object')
    return cases


def measured_error(value, label, error_bound=None, *, strict=False):
    value = finite_number(value, label)
    require(value >= 0, f'Invalid negative {label}')
    if error_bound is not None:
        bound = finite_number(error_bound, 'comparison error bound')
        require(bound >= 0, 'Comparison error bound must be nonnegative')
        require(value < bound if strict else value <= bound,
                f'{label} exceeds the actual comparison tolerance: {value!r} '
                f'{">=" if strict else ">"} {bound!r}')
    return value


def validate_test_result(result, model, samples, output_count, input_count=None, *,
                         case_layout=None, error_bound=None, strict_error_bound=False,
                         require_errors=False):
    """Validate actual success, never infer success from a file's existence."""
    require(isinstance(result, dict), 'Test result must be an object')
    require(result.get('model') == model, f'Test model mismatch: {result.get("model")} != {model}')
    require(result.get('status') == 'passed', f'Test status is not passed: {result.get("status")}')
    if 'failed' in result:
        require(count(result['failed'], 'failed') == 0, 'Test failures were recorded')
    if 'all_passed' in result:
        require(result['all_passed'] is True, 'all_passed is not true')
    actual_samples = count(result_alias(result, 'samples', 'sample_count'), 'samples', positive=True)
    require(actual_samples == samples, f'Test sample mismatch: {actual_samples} != {samples}')
    require(count(result_alias(result, 'output_count', 'outputs'), 'output_count', positive=True) == output_count,
            'Test output_count mismatch')
    if input_count is not None:
        require(count(result.get('input_count'), 'input_count', positive=True) == input_count,
                'Test input_count mismatch')
    tests = test_cases(result)
    if case_layout is not None:
        require(isinstance(case_layout, list), 'Expected case layout must be explicit')
        if case_layout:
            require(tests is not None, 'Result missing the bound vector cases')
        else:
            require(tests is None, 'Result has cases absent from the bound vector layout')
    case_errors, case_mil_errors = [], []
    if tests is not None:
        require(all(t.get('passed') is True for t in tests), 'A test case did not pass')
        names = [t.get('name') for t in tests]
        require(all(isinstance(name, str) and bool(name) for name in names) and len(set(names)) == len(names),
                'Test case names must be nonempty and unique')
        counts = [count(t.get('samples'), 'case samples', positive=True) for t in tests]
        require(sum(counts) == actual_samples,
                'Case samples do not sum to result samples')
        require(count(result.get('passed'), 'passed') == len(tests), 'Passed case count mismatch')
        if 'case_count' in result:
            require(count(result['case_count'], 'case_count', positive=True) == len(tests),
                    'Case count mismatch')
        if case_layout is not None:
            require([{'name': name, 'samples': n} for name, n in zip(names, counts)] == case_layout,
                    'Result cases differ from the bound vector case layout')
        for test in tests:
            if 'max_abs_error' in test or require_errors:
                case_errors.append(measured_error(test.get('max_abs_error'), 'case max_abs_error',
                                                  error_bound, strict=strict_error_bound))
            if 'max_mil_error' in test:
                case_mil_errors.append(measured_error(test['max_mil_error'], 'case max_mil_error',
                                                      error_bound, strict=strict_error_bound))
            if 'comparisons' in test:
                require(count(test['comparisons'], 'case comparisons', positive=True) == test['samples'] * output_count,
                        'Case comparison count mismatch')
    coverage = result.get('coverage')
    if isinstance(coverage, dict):
        for metric in ('decision', 'condition', 'mcdc', 'execution'):
            if metric in coverage:
                decision_count(coverage[metric], metric)
    error = None
    if 'max_abs_error' in result or (require_errors and tests is None):
        error = measured_error(result.get('max_abs_error'), 'max_abs_error',
                               error_bound, strict=strict_error_bound)
    if case_errors:
        if error is not None:
            require(len(case_errors) == len(tests) and error == max(case_errors),
                    'Aggregate max_abs_error contradicts case errors')
        else:
            error = max(case_errors)
    if 'max_mil_error' in result:
        mil_error = measured_error(result['max_mil_error'], 'max_mil_error',
                                   error_bound, strict=strict_error_bound)
        if case_mil_errors:
            require(len(case_mil_errors) == len(tests) and mil_error == max(case_mil_errors),
                    'Aggregate max_mil_error contradicts case errors')
    if 'comparisons' in result:
        require(count(result['comparisons'], 'comparisons', positive=True) == actual_samples * output_count,
                'Test comparison count mismatch')
    verified = {'present': True, 'all_passed': True, 'samples': actual_samples,
                'input_count': input_count, 'output_count': output_count}
    if error is not None:
        verified['max_abs_error'] = error
    return verified


def validate_vectors(path, model):
    vectors = read_json(path)
    require(isinstance(vectors, dict), 'Vector document must be an object')
    if 'model' in vectors:
        require(vectors['model'] == model, 'Vector model mismatch')
    if 'cases' in vectors:
        cases = vectors['cases']
        require(isinstance(cases, list) and bool(cases), 'Empty scenario vectors')
        require(all(isinstance(case, dict) for case in cases), 'Scenario case must be an object')
        names = [case.get('name') for case in cases]
        require(all(isinstance(name, str) and bool(name) for name in names) and len(set(names)) == len(names),
                'Scenario names must be nonempty and unique')
        samples = 0
        for case in cases:
            inputs = case.get('inputs')
            finite_matrix(inputs, 5, 'scenario inputs')
            n = len(inputs)
            for index, row in enumerate(inputs):
                require(all(row[column] in (0, 1) for column in (1, 2, 4)),
                        f'Scenario boolean input is not 0/1: row {index}')
            for key in ('time', 'expected_torque', 'expected_allowed', 'mil_torque', 'mil_allowed'):
                finite_vector(case.get(key), n, f'Scenario {key}', boolean=key.endswith('_allowed'))
            require(all(a < b for a, b in zip(case['time'], case['time'][1:])),
                    'Scenario time must be strictly increasing')
            samples += n
        return {'samples': samples, 'input_count': 5, 'output_count': 2,
                'case_layout': [{'name': case['name'], 'samples': len(case['inputs'])} for case in cases],
                'comparison_kind': 'scenario_runner'}
    inputs, outputs = vectors.get('input_names'), vectors.get('output_names')
    for names, label in ((inputs, 'input'), (outputs, 'output')):
        require(isinstance(names, list) and bool(names) and
                all(isinstance(name, str) and bool(name) for name in names) and len(set(names)) == len(names),
                f'Invalid {label} names')
    rows, expected = vectors.get('inputs'), vectors.get('expected')
    require(isinstance(rows, list) and bool(rows) and isinstance(expected, list) and len(rows) == len(expected),
            'Vector sample lengths mismatch')
    finite_matrix(rows, len(inputs), 'vector inputs')
    finite_matrix(expected, len(outputs), 'vector expected')
    period = finite_number(vectors.get('period'), 'period')
    require(period > 0, 'Vector period must be positive')
    finite_number((len(rows) - 1) * period, 'last sample time')
    for key in ('absolute_tolerance', 'relative_tolerance'):
        value = finite_number(vectors.get(key), key)
        require(value >= 0, f'Invalid {key}')
    maximum_limit = 0
    for row in expected:
        for value in row:
            limit = finite_number(vectors['absolute_tolerance'] + vectors['relative_tolerance'] * abs(value),
                                  'effective comparison tolerance')
            maximum_limit = max(maximum_limit, limit)
    return {'samples': len(rows), 'input_count': len(inputs), 'output_count': len(outputs),
            'case_layout': [], 'comparison_kind': 'absolute_relative_vectors',
            'max_error_bound': maximum_limit}


def validate_native_result(result, model, layout, *, scenario_error_limit=None):
    """Check native measurements against vectors and an explicit runner contract.

    The caller must verify the actual runner before supplying a scenario limit.
    Never derive a permitted limit from result/comparison_policy/tolerance fields.
    A flat trace only reports a maximum, so its necessary summary ceiling is the
    largest per-observation allowance derived from the bound expected values.
    This metadata check does not replace the runner's individual comparisons.
    """
    require(isinstance(layout, dict) and 'case_layout' in layout,
            'Native validation requires the bound vector case layout')
    kind = layout.get('comparison_kind')
    if kind == 'scenario_runner':
        limit = finite_number(scenario_error_limit, 'actual scenario runner error limit')
        require(limit > 0, 'Scenario runner error limit must be positive')
        require(bool(layout['case_layout']), 'Scenario runner requires vector cases')
        strict = True
    else:
        require(kind == 'absolute_relative_vectors' and layout['case_layout'] == [],
                'Unsupported native vector comparison layout')
        require(scenario_error_limit is None, 'Scenario error limit cannot override bound matrix tolerances')
        limit = finite_number(layout.get('max_error_bound'), 'bound vector error limit')
        require(limit >= 0, 'Bound vector error limit must be nonnegative')
        strict = False
        require(isinstance(result, dict) and 'max_mil_error' in result,
                'Native matrix result missing measured MIL error')
        require('passed' not in result and 'case_count' not in result,
                'Case pass count has no bound case layout')
    return validate_test_result(result, model, layout['samples'], layout['output_count'],
                                case_layout=layout['case_layout'], error_bound=limit,
                                strict_error_bound=strict, require_errors=True)


def validate_run_binding(path, repo, model_path, model, *, required_roles, result_path, expected_checksum=None):
    path, repo, model_path = Path(path), Path(repo).resolve(), Path(model_path).resolve()
    binding = read_json(path)
    require(binding.get('schema_version') in ('1.0', '1.0.0'), f'Unsupported run binding schema: {path}')
    require(binding.get('model') == model, f'Run binding model mismatch: {path}')
    current_hash = digest(model_path)
    require(binding.get('model_sha256_before') == binding.get('model_sha256_after') == current_hash,
            f'Run binding model hash changed or is stale: {path}')
    checksum = binding.get('model_checksum')
    require(checksum not in (None, '', [], {}), f'Run binding missing model checksum: {path}')
    if expected_checksum is not None:
        require(checksum == expected_checksum, f'Run model checksum mismatch: {path}')
    inputs = binding.get('inputs')
    verify_artifacts(inputs, repo)
    roles = {x.get('role') for x in inputs}
    require(set(required_roles) <= roles, f'Missing run input roles {set(required_roles) - roles}: {path}')
    model_inputs = [x for x in inputs if x.get('role') == 'model']
    require(any(resolve_path(x['path'], repo) == model_path and x['sha256'] == current_hash for x in model_inputs),
            f'Run binding does not list the executed model: {path}')
    results = verify_artifacts(binding.get('result_artifacts'), path.parent)
    require(Path(result_path).resolve() in results, f'Run result is not hash-bound: {result_path}')
    return binding


def role_paths(binding, role, repo):
    return [resolve_path(x['path'], repo) for x in binding['inputs'] if x.get('role') == role]


def validate_coverage_dataset(dataset, repo, model, current, artifacts, denominator=None):
    require(isinstance(dataset, dict) and dataset.get('status') == 'accepted', 'Missing accepted coverage dataset facts')
    count(dataset.get('index'), 'coverage dataset index', positive=True)
    require(dataset.get('coverage_checksum') == current, 'Coverage dataset checksum mismatch')
    raw = decision_count(dataset.get('decision_unfiltered'), 'unfiltered production decision')
    filtered = decision_count(dataset.get('decision_filtered'), 'reported filtered decision')
    if denominator is not None:
        require(raw[1] == denominator, 'Unfiltered production denominator differs from fresh coverage')
    require(filtered[1] <= raw[1], 'Filtered denominator exceeds unfiltered production scope')
    scope = dataset.get('scope_assessment')
    require(isinstance(scope, dict) and scope.get('policy') == 'unfiltered_full_production' and
            scope.get('production_exclusions_applied') is False and scope.get('scoring_decision') == raw and
            scope.get('filter_reapplication_verified') is True,
            'Coverage dataset does not restore and verify full production scope')
    require(count(scope.get('denominator_removed_by_report_filter'), 'filtered denominator delta') == raw[1] - filtered[1],
            'Filter denominator delta mismatch')
    filters, objects = dataset.get('filter_files'), dataset.get('affected_objects')
    require(isinstance(filters, list) and isinstance(objects, list), 'Missing actual filter/object inventory')
    require(type(scope.get('filters_present')) is bool and scope['filters_present'] == bool(filters),
            'Filter presence contradicts recorded artifacts')
    for record in filters:
        require(isinstance(record, dict), 'Filter record must be an object')
        path = resolve_path(record.get('path'), repo)
        require(path in artifacts and artifacts[path] == record.get('sha256'), 'Applied filter is absent from bound artifacts')
        verify_hash(path, record.get('sha256'))
        rules = record.get('rules')
        require(isinstance(rules, list), 'Missing actual filter rules')
        for rule in rules:
            require(isinstance(rule, dict) and rule.get('mode') in ('Exclude', 'Justify'), 'Unknown filter rule mode')
            for key in ('rationale', 'selector_class', 'selector_type', 'selector_id', 'sid', 'object_path', 'description', 'constructor'):
                require(isinstance(rule.get(key), str), f'Missing filter rule {key}')
            require(rule['selector_class'] and rule['selector_type'] and rule['constructor'], 'Incomplete filter selector')
            if rule['sid']:
                require(rule['sid'].startswith(model + ':') and (rule['object_path'] == model or rule['object_path'].startswith(model + '/')) and
                        rule.get('object_status') == 'resolved', 'Filter selector does not resolve in production model')
            else:
                require(rule.get('object_status') == 'not_block_specific', 'Unresolved filter object')
            if rule['selector_class'] == 'slcoverage.MetricSelector':
                count(rule.get('objective_index'), 'filter objective index', positive=True)
                count(rule.get('outcome_index'), 'filter outcome index', positive=True)
    object_ids = []
    for obj in objects:
        require(isinstance(obj, dict) and isinstance(obj.get('sid'), str) and obj['sid'].startswith(model + ':'),
                'Affected filter object SID is invalid')
        require(isinstance(obj.get('path'), str) and obj['path'].startswith(model + '/') and
                isinstance(obj.get('block_type'), str) and bool(obj['block_type']), 'Affected filter object is incomplete')
        before = decision_count(obj.get('decision_unfiltered'), 'object unfiltered decision')
        after = decision_count(obj.get('decision_filtered'), 'object filtered decision')
        require(before != after and after[1] <= before[1] <= raw[1], 'Invalid affected-object decision counts')
        object_ids.append(obj['sid'])
    require(len(set(object_ids)) == len(object_ids), 'Duplicate affected filter objects')
    if not filters:
        require(raw == filtered and not objects, 'Undisclosed filter changed production coverage')
    elif raw != filtered:
        require(bool(objects) and any(record['rules'] for record in filters), 'Changed coverage lacks filter rules and affected objects')
    return raw


def validate_coverage_inventory(inventory, repo, snap, model):
    require(inventory.get('schema_version') == '1.1', 'Unsupported coverage inventory schema; re-extract actual filter metadata')
    require(inventory.get('model') == model, 'Coverage inventory model mismatch')
    model_row = next((x for x in snap['models'] if Path(x['path']).stem == model), None)
    require(model_row is not None and inventory.get('model_sha256') == model_row['sha256'],
            'Coverage inventory SLX hash mismatch')
    current = inventory.get('current_coverage_checksum')
    require(current not in (None, '', [], {}), 'Missing current cvdata checksum')
    scope = inventory.get('scope')
    require(isinstance(scope, dict) and scope.get('policy') == 'unfiltered_full_production' and
            scope.get('model_scope') == 'single_production_model' and scope.get('filters_change_canonical_scope') is False and
            isinstance(scope.get('rationale'), str) and bool(scope['rationale']), 'Missing explicit production coverage scope')
    artifacts = verify_artifacts(inventory.get('artifacts'), repo)
    fresh = inventory.get('fresh_reference')
    require(isinstance(fresh, dict), 'Missing fresh coverage reference')
    fresh_path = resolve_path(fresh.get('path'), repo)
    require(fresh_path in artifacts and artifacts[fresh_path] == fresh.get('sha256'), 'Fresh CVT is absent from coverage artifacts')
    fresh_raw = validate_coverage_dataset(fresh.get('dataset'), repo, model, current, artifacts)
    tracked = {x['path']: x for x in snap['files'] if x['path'].lower().endswith('.cvt')}
    rows = inventory.get('files')
    require(isinstance(rows, list), 'Coverage inventory files must be a list')
    paths = [x.get('path') for x in rows]
    require(len(set(paths)) == len(paths) and set(paths) == set(tracked),
            'Coverage inventory must account for every tracked CVT exactly once')
    accepted = []
    for item in rows:
        path = item['path']; src = resolve_path(path, repo)
        require(item.get('source_blob_sha256') == tracked[path]['sha256'], f'CVT Git blob hash mismatch: {path}')
        verify_hash(src, item.get('runtime_bytes_sha256'))
        require(type(item.get('accepted')) is bool, f'CVT accepted must be boolean: {path}')
        require(isinstance(item.get('reason'), str) and bool(item['reason']), f'CVT decision requires a reason: {path}')
        if item.get('decision') not in (None, []):
            decision_count(item['decision'], f'CVT {path}')
        if item['accepted']:
            require(item.get('coverage_checksum') == current, f'Accepted CVT checksum mismatch: {path}')
            datasets = item.get('datasets')
            require(isinstance(datasets, list) and bool(datasets), f'Accepted CVT lacks dataset/filter records: {path}')
            counts, indexes = [], []
            for dataset in datasets:
                require(isinstance(dataset, dict), 'Coverage dataset entry must be an object')
                indexes.append(count(dataset.get('index'), 'coverage dataset index', positive=True))
                if dataset.get('status') == 'stale':
                    require(dataset.get('coverage_checksum') != current, 'Current dataset mislabeled stale')
                else:
                    counts.append(validate_coverage_dataset(dataset, repo, model, current, artifacts, fresh_raw[1]))
            require(len(set(indexes)) == len(indexes) and bool(counts), 'Duplicate or absent current coverage datasets')
            pair = decision_count(item.get('decision'), f'CVT {path}')
            require(pair[1] == fresh_raw[1] and max(x[0] for x in counts) <= pair[0] <= min(pair[1], sum(x[0] for x in counts)),
                    'Source CVT union does not use unfiltered full-production datasets')
            accepted.append(pair)
    union = inventory.get('union_decision')
    if not accepted:
        require(union is None, 'Coverage union without accepted source CVTs')
        return None
    union = decision_count(union, 'coverage union')
    require(union[1] == fresh_raw[1] and all(x[1] == union[1] for x in accepted), 'Coverage union target denominator mismatch')
    require(max(x[0] for x in accepted) <= union[0] <= min(union[1], sum(x[0] for x in accepted)),
            'Coverage union counts contradict accepted CVTs')
    artifact = inventory.get('union_artifact')
    require(isinstance(artifact, dict), 'Actual union CVT artifact is required')
    verify_artifacts([artifact], repo)
    return union


def validate_native_hashes(result, binding, repo, generated_dir):
    """Validate internal hashes, not only the hash of result.json itself."""
    require(isinstance(result, dict), 'Native replay result must be an object')
    require(result.get('status') == 'passed', 'Native replay did not pass')
    if 'failed' in result:
        require(count(result['failed'], 'native failures') == 0, 'Native replay recorded failures')
    cases = test_cases(result)
    if cases is not None:
        require(all(x.get('passed') is True for x in cases), 'Native replay case failure')
    vectors = role_paths(binding, 'vectors', repo)
    adapters = role_paths(binding, 'adapter', repo)
    require(len(vectors) == len(adapters) == 1, 'Native replay requires one vector file and one adapter')
    verify_hash(vectors[0], result.get('vectors_sha256'))
    verify_hash(adapters[0], result.get('adapter_sha256'))
    exe_hash = result.get('executable_sha256')
    executables = [x for x in binding['result_artifacts'] if Path(x['path']).suffix.lower() == '.exe']
    require(any(x.get('sha256') == exe_hash for x in executables), 'Native executable is not bound in result artifacts')
    generated_dir = Path(generated_dir)
    sources = sorted(x for x in generated_dir.glob('*.c') if x.name not in ('ert_main.c', 'rt_main.c'))
    require(bool(sources), 'Missing generated sources')
    hashes = result.get('sources_sha256')
    if hashes is None and len(sources) == 1:
        hashes = {sources[0].name: result.get('generated_source_sha256')}
    require(isinstance(hashes, dict) and set(hashes) == {x.name for x in sources}, 'Generated source hash inventory mismatch')
    bound_sources = set(role_paths(binding, 'generated_source', repo))
    for source in sources:
        verify_hash(source, hashes[source.name])
        require(source.resolve() in bound_sources, f'Generated source not in run binding: {source}')
    headers = {p.resolve() for p in generated_dir.glob('*.h')}
    require(headers <= set(role_paths(binding, 'generated_header', repo)), 'A generated header is absent from the native binding')
    return validate_vectors(vectors[0], binding['model'])


def json_pointer(document, pointer):
    require(isinstance(pointer, str) and (not pointer or pointer.startswith('/')), 'Invalid JSON pointer')
    value = document
    for token in pointer.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        try:
            value = value[int(token)] if isinstance(value, list) else value[token]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise EvidenceError(f'Unresolvable JSON pointer: {pointer}') from exc
    return value


def validate_properties(result, repo, model, samples, bindings, run):
    require(result.get('schema_version') == '1.1', 'Unsupported property evidence schema')
    require(result.get('status') == 'passed' and result.get('input_files_unchanged') is True,
            'Property assertions failed or inputs changed during execution')
    require(result.get('model') == model, 'Property evidence model mismatch')
    require(count(result.get('samples'), 'property samples', positive=True) == samples, 'Property sample count mismatch')
    require(count(result.get('assertions'), 'property assertions', positive=True) > 0, 'No property assertions')
    verify_artifacts(result.get('inputs'), repo)
    roles = {r.get('role') for r in result['inputs']}
    require({'property_script', 'vectors', 'mil_output', 'native_output'} <= roles, 'Missing property evidence inputs')
    scripts = role_paths(result, 'property_script', repo)
    require(len(scripts) == 1 and result.get('property_script_sha256_before') ==
            result.get('property_script_sha256_after') == digest(scripts[0]), 'Property script changed or hash is stale')
    require(role_paths(result, 'vectors', repo) == role_paths(bindings['acceptance'], 'vectors', repo),
            'Property evidence does not use the bound acceptance vectors')
    for stream, role, stage in [('mil', 'mil_output', 'acceptance'), ('native', 'native_output', 'native-replay')]:
        paths = role_paths(result, role, repo)
        require(len(paths) == 1, f'Property {role} must identify one output artifact')
        recorded = {resolve_path(r['path'], Path(run) / stage) for r in bindings[stage]['result_artifacts']}
        require(paths[0] in recorded, f'Property {role} is not in the stage output binding')
        outcome = result.get('streams', {}).get(stream, {})
        require(outcome.get('status') == 'passed' and outcome.get('samples') == samples,
                f'Property {stream} outcome mismatch')
    return [resolve_path(x['path'], repo) for x in result['inputs']]
