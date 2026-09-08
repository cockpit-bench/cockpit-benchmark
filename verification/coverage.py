"""Describe score-band/evidence coverage and the in-sample type/leaf mode baseline."""
import argparse
import collections
import json
from pathlib import Path

TIERS = {
    'architecture.componentization': [0, 1, 3, 5],
    'architecture.decoupling': [0, 1, 2, 3],
    'architecture.modularization': [0, 1, 2, 3],
    'compilation.ci_independence': [0, 1, 2, 3],
    'compilation.compilation_independence': [0, 1, 2, 3],
    'compilation.api_version_management': [0, 1, 2, 3],
    'quality.integration_test': [0, 1, 2, 3],
    'platform_reuse.platform_upgrade': [0, 3, 8, 10],
    'platform_reuse.release_branch_strategy': [0, 3, 8, 10],
    **{'solid_principle.' + k: [0, 1, 2, 3, 4] for k in
       ['single_responsibility', 'open_closed', 'liskov_substitution', 'interface_segregation', 'dependency_inversion']},
}


def analyze(standard, observations):
    groups = collections.defaultdict(list)
    by_repo = []
    for repo in standard['repositories']:
        for leaf in repo['leaves']:
            record = observations[(repo['id'], leaf['name'])]
            score = leaf['score']
            if leaf['status'] != 'scored' or score not in TIERS[leaf['name']]:
                raise ValueError('Unsupported/unscored leaf; do not impute a score')
            evidence = record['evidence']
            facts = record['facts']
            executed = facts.get('final_head_integration_execution_exists',
                                 facts.get('final_head_android_integration_execution_exists'))
            runtime = (facts.get('integration_execution') or {}).get('runtime')
            if executed is True:
                state = ('android_execution_recorded' if runtime in {'android_device', 'android_emulator'}
                         else 'host_execution_recorded' if runtime in {'host_jvm', 'host_native'}
                         else 'execution_runtime_unclassified')
            else:
                state = ('android_execution_absent' if executed is False
                         else 'execution_not_classified_for_this_leaf')
            row = {'id': repo['id'], 'kind': repo['kind'], 'name': leaf['name'], 'score': score,
                   'status': leaf['status'], 'evidence_state': state, 'method': record['method'],
                   'code_anchor_count': sum(e.get('source') == 'repository' for e in evidence),
                   'inventory_anchor_count': sum(e.get('source') == 'git_inventory' for e in evidence)}
            by_repo.append(row)
            groups[(repo['kind'], leaf['name'])].append(row)
    baselines = collections.defaultdict(lambda: {'hits': 0, 'denominator': 0})
    cells, distributions = [], []
    for (kind, leaf), rows in sorted(groups.items()):
        counts = collections.Counter(r['score'] for r in rows)
        maximum = max(counts.values())
        modes = sorted(score for score, count in counts.items() if count == maximum)
        baselines[kind]['hits'] += maximum
        baselines[kind]['denominator'] += len(rows)
        distributions.append({'kind': kind, 'name': leaf, 'counts': dict(sorted(counts.items())),
                              'missing_bands': [s for s in TIERS[leaf] if s not in counts], 'mode_scores': modes,
                              'mode_hits': maximum, 'denominator': len(rows)})
        for score in TIERS[leaf]:
            selected = [r for r in rows if r['score'] == score]
            cells.append({'kind': kind, 'name': leaf, 'score': score, 'count': len(selected),
                          'repository_ids': [r['id'] for r in selected],
                          'evidence_states': dict(collections.Counter(r['evidence_state'] for r in selected)),
                          'input_methods': dict(collections.Counter(r['method'] for r in selected)),
                          'source_anchored_count': sum(r['code_anchor_count'] > 0 for r in selected),
                          'inventory_anchored_count': sum(r['inventory_anchor_count'] > 0 for r in selected)})
    total = {'hits': sum(v['hits'] for v in baselines.values()), 'denominator': len(by_repo)}
    return {'schema_version': 'leaf-band-evidence-coverage-1', 'source_version': standard['version'],
            'baseline_method': 'Post-hoc in-sample modal score by kind and leaf; no code or Agent prediction is read.',
            'baseline_by_kind': dict(baselines), 'baseline_total': total,
            'observed_band_cells': sum(c['count'] > 0 for c in cells), 'possible_band_cells': len(cells),
            'distributions': distributions, 'cells': cells, 'observations': by_repo,
            'limits': ['This is distribution diagnosis, not held-out accuracy or evidence correctness.',
                       'An empty band is untested even if accuracy on observed bands is 100%.',
                       'Evidence-state labels reflect supplied records, not a new execution.']}


def render(result):
    total = result['baseline_total']
    fw_tests = [r for r in result['observations'] if r['kind'] in {'FW', 'FRAMEWORK'}
                and r['name'] == 'quality.integration_test']
    execution_counts = collections.Counter(r['evidence_state'] for r in fw_tests)
    execution_summary = (f"{len(fw_tests)} 个 FW 集成测试叶的 final-HEAD Android 执行证据："
                         f"recorded {execution_counts['android_execution_recorded']}，"
                         f"absent {execution_counts['android_execution_absent']}，"
                         f"未分类 {execution_counts['execution_not_classified_for_this_leaf'] + execution_counts['execution_runtime_unclassified']}；"
                         f"另有 host recorded {execution_counts['host_execution_recorded']}，不计作设备执行。其他叶不凭此字段缺失推断未执行。")
    lines = ['# 叶 × 档位 × 证据状态覆盖', '',
             '基线：' + result['source_version'] + ' 的 18 仓标准答案；不读取 Agent 预测。', '',
             f"样本内类型×叶众数基线：**{total['hits']}/{total['denominator']} = {100*total['hits']/total['denominator']:.1f}%**。这不是独立测试准确率，也不检查理由或证据质量。", '',
             f"覆盖 **{result['observed_band_cells']}/{result['possible_band_cells']}** 个类型×叶×合法档位组合；这是档位计数，不能替代真实任务能力验证。", '',
             '| 类型 | 叶 | 分数:样本数 | 缺失档位 |', '|---|---|---|---|']
    for row in result['distributions']:
        lines.append('| ' + row['kind'] + ' | ' + row['name'] + ' | ' +
                     ', '.join(f'{k}:{v}' for k, v in row['counts'].items()) + ' | ' +
                     ', '.join(map(str, row['missing_bands'])) + ' |')
    lines += ['', '完整 JSON 的 cells 列出每个档位的仓 ID、源码/库存锚点数量、输入方法和 Android 集成执行证据状态。',
              execution_summary,
              '评分规则映射与人工语义观察映射分别记录；代码锚点存在不能证明判断正确或抽样完备。', '',
              '## 优先对照', '',
              '1. 发布策略 3/8/10：真实车型配置、平台共用和跨平台统一发布，必须有生效行为和 refs 证据。',
              '2. 平台升级 8/10：私有 API 未隔离、隔离且降级、公开 API 与接口隔离的成对变化。',
              '3. FW CI 和 Android 集成执行正例：不得用 host 测试替代 Android 执行及关键交互覆盖分母。',
              '4. 命名不变性可作为诊断，但当前合同命名门槛仍有效；更改主分需另行版本化。', '',
              '对照样本单独成集，同源变体共用 family_id；不混入 Validation-18 分母，也不拆到调参与独立验证两侧。', '']
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--wrapper', type=Path, required=True)
    ap.add_argument('--data', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True, help='Output stem; .json and .md are written')
    a = ap.parse_args()
    standard = json.loads((a.wrapper/'STANDARD_SCORES.json').read_text(encoding='utf-8'))
    package = json.loads((a.data/'package.json').read_text(encoding='utf-8'))
    observations = {}
    for repo in package['repositories']:
        d = json.loads((a.data/repo['rule_inputs']).read_text(encoding='utf-8'))
        for leaf in d['leaves']:
            observations[(repo['id'], leaf['name'])] = leaf
    result = analyze(standard, observations)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    a.output.with_suffix('.md').write_text(render(result), encoding='utf-8')
    print(result['baseline_by_kind'], result['baseline_total'], result['observed_band_cells'], '/', result['possible_band_cells'])


if __name__ == '__main__':
    main()
