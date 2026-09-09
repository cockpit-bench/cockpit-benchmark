"""Build the candidate-facing MATLAB contract from frozen clauses and approved overrides."""
import argparse
import hashlib
import json
from pathlib import Path
import re


OVERRIDE_TEXT = {
    'interface': '范围：全部生产根模型公开 Inport/Outport、跨模型依赖及影响公开边界的 Goto/From/DataStore。完整性、命名、类型、单位、范围、受控变更均使用同一范围。内部子系统仍纳入层次分解、数据流及命名审阅。',
    'unit_test': '覆盖率专指 decision coverage；多生产模型按 covered/total 目标数汇总，不平均百分比。排除 harness，复用定义去重，显式记录过滤。无 decision 目标不自动算 100%。有效测试无覆盖证据可得 1；无 BTC 文件名不直接判 0，真实 Simulink 报告可用。',
    'release_branches': '单一主分支通过配置支持多个平台可得 10，不以分支数≤1判 0。按统一主线、平台分支、车型分支或无计划策略裁定。可使用已接受的分支命名近似，不新增跨平台执行门禁。记录型号 token 及角色，任意字母数字串不自动视为车型；auto 分支追踪来源。',
    'device_specificity': '本轮接受分支名近似：无车型或平台代号可认定设备通用，得 10。与 release 共用一次分支事实；记录明确识别的 token/角色及 auto 分支来源。不新增 N/A 出口或跨平台执行门禁；该近似不代表实际全平台验证。',
    'parameter_management': '参数不限形式、位置或扩展名。核对所有应管理业务参数的集中性、准确性及实际消费者；准确性包括值、类型、单位适配与记录一致。模型工作区、脚本、字典、接口表均可。类型、范围和变更记录保留事实，但不是额外的 5 分门槛。',
    'build_independence': '以仓库为边界；同仓源码、预编译、保护模型依赖均属正常模块化。MATLAB/Simulink 基础工具环境单列，不算外部业务依赖。高档优先，版本化接口组件采用源码交付不覆盖其高档条件；实际构建成功与评分分别报告。',
}
REPLACEMENT_TIERS = {
    'build_independence': [
        '0＝存在未受控的仓外业务源码依赖，构建需加载对方源码。',
        '1＝仓外业务依赖仅以预编译或保护模型交付，未满足更高档。',
        '2＝仓外业务依赖采用带端口、Bus、Mask 参数的接口化可复用组件，未满足 3 分。',
        '3＝无仓外业务依赖；或仓外依赖为版本管理、发布基线及版本锁定引用的稳定组件库。'],
    'parameter_management': [
        '0＝大量业务数值硬编码，未参数化。',
        '1＝部分关键参数变量化，但多数仍散落、未集中。',
        '3＝全部可调参数变量化且集中，分类结构清晰，尚未满足 5 分的集中且准确并实际使用要求。',
        '5＝所有应管理的业务参数集中、准确且实际被模型使用。'],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def build(root):
    root = Path(root)
    index = json.loads((root / 'contract-index.json').read_text(encoding='utf-8'))
    for key in ('original', 'overrides'):
        if sha((root / index[key]['path']).read_bytes()) != index[key]['sha256']:
            raise ValueError('contract input drift: ' + key)
    # Remove transport escaping/duplicated emphasis, not normative words.
    original = (root / index['original']['path']).read_text(encoding='utf-8')
    cleaned = re.sub(r'\\([\\`*_{}\[\]()#+.!|<>~\-])', r'\1', original).replace('**', '')
    sections = dict(re.findall(r'### (2\.\d+) ([\s\S]*?)(?=### 2\.\d+ |## 3\.|\Z)', cleaned))
    lines = ['# MATLAB/Simulink 当前有效评分合同', '',
             '候选执行入口。由冻结原文与已批准裁定合成；只含 13 叶，满分 61，独立于 Android。',
             '从高档向低档匹配；不插值、不平均、不按目标角色倒推。证据不足标 failed，不编造数字。',
             '真实行为、连线与断言是事实基础；静态解析、模型加载/更新、仿真、代码生成、编译及 SIL/PIL/HIL 分别报告，不能相互替代。',
             '源码、版本与证据必须绑定；计数与文件存在性不能代替职责、命名、复用或准确性的语义判断。', '',
             '每叶输出 id、status、score、理由、具体证据及审阅范围；failed 的 score 为 null。证据标明仓库 HEAD、路径、行段/模型元素和支持的事实。', '']
    for leaf in index['leaves']:
        section = sections[leaf['section']]
        tierpart = section.split('tiers', 1)[1].split('checks', 1)[0]
        tiers = [m.group(1).strip() for m in re.finditer(r'^\s*-\s*([0-9]+\s*＝.*)$', tierpart, re.M)]
        tiers = REPLACEMENT_TIERS.get(leaf['id'], tiers)
        if len(tiers) != 4 or [int(re.match(r'\d+', t).group()) for t in tiers] != leaf['allowed_scores']:
            raise ValueError('unrecognized tiers: ' + leaf['id'])
        lines += [f"## {leaf['section']} {leaf['name']} (`{leaf['id']}`)", '',
                  f"满分 {leaf['max_score']}；合法分值：" + '/'.join(map(str, leaf['allowed_scores'])) + '。', '']
        lines += ['- ' + t for t in tiers]
        if leaf['id'] not in {'build_independence', 'parameter_management', 'unit_test'}:
            checks = section.split('checks', 1)[1].split('evidence_fields', 1)[0]
            checks = checks.strip('：: \n-')
            lines += ['', '审阅事实：' + checks]
        if leaf['id'] in OVERRIDE_TEXT:
            lines += ['', OVERRIDE_TEXT[leaf['id']]]
        if leaf['id'] == 'unit_test':
            lines += ['', '审阅测试输入、预期、方法、断言、通过率、绑定版本的真实报告及覆盖目标分子/分母。']
        if leaf['id'] == 'version_independence':
            lines += ['', '语义化三段附 build 标记（例如 11.x.x_0 的实际数字版本）仍可符合 3 分。']
        lines += ['']
    lines += ['## 统一边界', '',
              '不评价 CI 独立性、版本策略、发布与回滚、平台升级影响、单平台或跨平台代码复用率六个排除维度。',
              'D01—D15 只作为检查线索，不自动决定分数；无某扩展名、指定目录名或指定报告名不能替代实质判断。',
              '生产范围包含全部有效模型实现；harness、停用块、生成码与无业务填充不算生产规模。仓内库和引用模型定义去重；供应商库内部实现不展开凑数。',
              '规模以有效生产逻辑块计：1–199 小型、200–799 中型、≥800 大型；纯接口/路由/显示及容器不计。规模角色不决定任何叶分。', '']
    result = '\n'.join(lines)
    binding = {'schema': 'effective-contract-v1', 'suite_id': index['suite_id'],
               'original': index['original'], 'overrides': index['overrides'],
               'contract_index_sha256': sha((root / 'contract-index.json').read_bytes()),
               'effective': {'path': 'EFFECTIVE_CONTRACT.md', 'sha256': sha(result.encode())},
               'composition': 'Original normative tiers/checks, approved replacements, no generation defect maps or historical interpolation.'}
    return result, binding


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--suite', type=Path, required=True); p.add_argument('--check', action='store_true')
    a = p.parse_args(); text, binding = build(a.suite)
    outputs = {'EFFECTIVE_CONTRACT.md': text,
               'effective-contract-binding.json': json.dumps(binding, ensure_ascii=False, indent=2) + '\n'}
    for name, content in outputs.items():
        if a.check:
            if (a.suite / name).read_bytes() != content.encode():
                raise ValueError('effective contract drift: ' + name)
        else: (a.suite / name).write_bytes(content.encode())


if __name__ == '__main__': main()
