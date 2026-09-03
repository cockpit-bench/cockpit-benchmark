# Cockpit Code Health Benchmark

这是座舱代码健康度 benchmark 的精简公开版。核心交付是 6 个可直接浏览的源码仓、与冻结代码事实匹配的标准分，以及一个恢复入口；它不是 40 仓离线运输包。

## Organization 布局

| 仓库 | 用途 |
|---|---|
| [`cockpit-benchmark`](https://github.com/cockpit-bench/cockpit-benchmark) | 评分规则、标准分、证据、库存元数据和恢复脚本 |
| [`aurora-settings`](https://github.com/cockpit-bench/aurora-settings) | APP 高质量样例，标准分 33/40 |
| [`motion-control`](https://github.com/cockpit-bench/motion-control) | APP 中质量样例，标准分 26/40 |
| [`atlas-settings`](https://github.com/cockpit-bench/atlas-settings) | APP 低质量样例，标准分 15/40 |
| [`vehicle-hal-adapter`](https://github.com/cockpit-bench/vehicle-hal-adapter) | FW 高质量样例，标准分 63/72 |
| [`soa-gateway`](https://github.com/cockpit-bench/soa-gateway) | FW 中质量样例，标准分 52/72 |
| [`can-middleware`](https://github.com/cockpit-bench/can-middleware) | FW 低质量样例，标准分 34/72 |

APP 使用 8 个叶子、满分 40；FW 使用另一套 17 叶嵌入式 C/C++ 口径、满分 72。唯一评分合同是 [`SCORE_RULES.md`](SCORE_RULES.md)。

## 人类查看入口

- [`SCORECARD.md`](SCORECARD.md)：6 仓总表、APP/FW 子维度矩阵和 75 条逐叶证据。
- [`SCORECARD.csv`](SCORECARD.csv)：可直接用 Excel 筛选的同一套明细。
- [`STANDARD_SCORES.json`](STANDARD_SCORES.json)：机器可读标准答案。
- [`ACTIVE_SIX.md`](ACTIVE_SIX.md)：六仓范围与使用约束。
- [`facts/leaf-facts.json`](facts/leaf-facts.json)：小型逐叶事实摘要。
- [`manifest.json`](manifest.json)：6 个 active 仓完整 refs，以及 34 个 pending 仓的库存/provenance 元数据。

标准分不是由“高/中/低”标签反填。每一叶都绑定具体 HEAD、文件、行号、事实和评分规则；应逐叶比较评估 Agent 的结果，而不是只比较总分。

## 下载与恢复

Windows PowerShell：

```powershell
git clone https://github.com/cockpit-bench/cockpit-benchmark.git
Set-Location .\cockpit-benchmark
.\restore.ps1
```

脚本只下载 6 个 active 仓，恢复到 `repos/app/` 和 `repos/framework/`。它会校验四个冻结评分文件的 SHA-256、六仓 HEAD 以及每个 `refs/heads/*`、`refs/tags/*` 的 OID；34 个 pending 仓不会下载。成功后各子仓的临时 `origin` 会被移除，便于把单仓隔离交给评估 Agent。

也可以直接 clone 上表中的任一源码仓。进行 benchmark 时，一次只把一个源码仓根目录交给评估 Agent；不要把本 wrapper、`STANDARD_SCORES.json`、`SCORECARD.*` 或 `oracle/` 一同提供，否则会泄露答案。

## 当前交付内容

```text
cockpit-benchmark/
  README.md
  LICENSE
  NOTICE
  ACTIVE_SIX.md
  SCORE_RULES.md
  STANDARD_SCORES.json
  SCORECARD.md
  SCORECARD.csv
  manifest.json
  manifest.md
  delivery-scope.json
  facts/leaf-facts.json
  oracle/{APP-01,APP-11,APP-15,FW-03,FW-08,FW-19}.json
  restore.ps1
```

没有 tar、bundle、pack、离线单包、旧 calibration、trace、stderr 或 validation 自证报告。34 个 pending 仓仅保留元数据，未来只有在明确扩展 benchmark 范围时才会另行处理。

## 历史版本

旧的 40 仓大包和 `transport-v0.3.1` 历史保留在只读 archive：[`caobotao1234-star/cockpit-benchmark`](https://github.com/caobotao1234-star/cockpit-benchmark)。它用于追溯，不是当前推荐下载入口。

## 许可证边界

wrapper 使用根目录 `LICENSE` / `NOTICE`。每个源码仓继续保留自身原始许可证、NOTICE 和来源信息；wrapper 的许可证不会覆盖或替代子仓许可证。
