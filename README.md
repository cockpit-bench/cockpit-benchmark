# Cockpit Benchmark — Validation-18

这是完整的座舱代码健康度 benchmark 控制仓：9 个 Android APP + 9 个 Android Framework，171 个逐叶标准答案。源码位于 `cockpit-bench` organization 的 18 个独立 public 仓；本仓只存评分合同、标准分、证据摘要、清单和恢复脚本。

## 人类入口

- `SCORECARD.md`：18 仓大表、逐叶分数、理由和证据。
- `SCORECARD.csv`：Excel/脚本可读的 171 行明细。
- `ACTIVE_EIGHTEEN.md`：3×3 质量/规模矩阵。
- `STANDARD_SCORES.json`：机器可读标准答案。
- `SCORE_RULES.md`：唯一评分合同；APP 8 叶/40，Android FW 11 叶/52。

## 使用

```powershell
git clone https://github.com/cockpit-bench/cockpit-benchmark.git
cd cockpit-benchmark
.estore.ps1 -Destination D:\cockpit-validation18
```

评测时一次只把一个源码仓交给 Agent；不要把 wrapper、oracle、facts、SCORECARD 或质量标签作为 Agent 输入。Agent 输出后，按 `STANDARD_SCORES.json` 同名叶比较。

本集合是公开 Dev/Regression Set，适合 Prompt 开发、规则回归与正式核心验证；公开答案和共享上游谱系意味着它不能替代私有、谱系隔离的最终 Holdout。

## 版本与边界

- 推荐版本：`v0.7.0`
- APP：72 叶，223/360；Android FW：99 叶，263/468；合计 486/828。
- v0.7.0 修复 Git ref tip 绑定、统一 3.0 Oracle/合同 hash、物化全部 APP facts，并采用外部构建闭包及风险单调平台升级口径。
- 22 个 pending 仓不运输；`can-middleware` 仅为 v0.4 历史补充样例。
- 旧 archive：https://github.com/cockpit-bench/cockpit-benchmark-v031-archive
- 每个源码仓保留自己的许可证、来源和全部 heads/tags；源码仓不含答案。
