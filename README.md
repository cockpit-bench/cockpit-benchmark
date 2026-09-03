# Cockpit Benchmark — APP-9 checkpoint

这是座舱代码健康度 benchmark 的 Android APP 半程交付。当前只包含 9 个 APP、72 个 canonical 叶子；FW 等待修正后的 Android Framework 评分规则，不在本版本中。

## 人类先看什么

- SCORECARD.md：9 仓总表及逐叶分数、理由、证据。
- SCORECARD.csv：可直接导入 Excel/脚本。
- STANDARD_SCORES.json：机器可读标准答案。
- SCORE_RULES.md：唯一 APP 评分合同。
- ACTIVE_NINE.md：本版本矩阵和边界。

## 布局

- wrapper：https://github.com/cockpit-bench/cockpit-benchmark
- 9 个源码仓：https://github.com/orgs/cockpit-bench/repositories
- oracle/：逐仓 canonical 记录，只供 benchmark 比对。
- facts/：精简 current-HEAD 事实摘要。
- manifest.json：40 仓库存元数据，其中 9 APP active、31 pending。
- restore.ps1：一次恢复并核验 9 仓 HEAD、全部 heads/tags 和零 remote。

## 使用

1. 克隆 wrapper。
2. 在 PowerShell 中运行：.\restore.ps1 -Destination D:\cockpit-app9
3. 评测时每次只把一个恢复后的源码仓交给 Agent。
4. Agent 输出后，按 STANDARD_SCORES.json 的同名叶子比较；不要把 wrapper、oracle、facts、SCORECARD 作为 Agent 输入。

## 版本

- 当前标签：v0.5.0-app9
- APP：9/9 已评分，72/72 叶有标准分与证据。
- FW：0/9，本版本明确 pending。
- v0.4.0 保留原 Dev-6 历史；其中 FW 使用的 embedded 旧口径不得继承到后续 Android FW 正式版本。

项目为 public benchmark 数据集。源码仓保留各自许可证和来源说明。
