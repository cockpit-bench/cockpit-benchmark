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
git clone --branch v0.7.7 --depth 1 https://github.com/cockpit-bench/cockpit-benchmark.git
cd cockpit-benchmark
.\restore.ps1 -Destination D:\cockpit-validation18
```

评测时一次只把一个源码仓复制到独立临时目录交给 Agent；其工作目录及父目录不得包含 wrapper、oracle、facts、SCORECARD 或质量标签。Agent 输出后，按 `STANDARD_SCORES.json` 同名叶比较。

Evaluator 必须拒绝缺叶、重复叶、合同外叶、非法分值和伪造证据；`failed` 叶保持 null，不补零；仓总分必须等于合法 scored 叶求和。Release 3 分必须引用含车型身份且有真实差异的单车型 SOP ref；通用年份 SOP 线不算车型线。理由中的“锁定 X”必须与机器分相同。

本集合是公开 Dev/Regression Set，适合 Prompt 开发、规则回归与正式核心验证；公开答案和共享上游谱系意味着它不能替代私有、谱系隔离的最终 Holdout。

## 版本与边界

- 推荐版本：`v0.7.7`
- APP：72 叶，216/360；Android FW：99 叶，239/468；合计 455/828。
- v0.7.7 完成 63 个 FW 叶的源码证据复核与事实驱动重算，修正 FW-08 LSP、SOLID 行为证据和私有 API/ABI 风险事实；旧 v0.7.6 及草稿分支仅供追溯。
- SOLID 为明确记录的语义裁决：严重违反、多处跨边界违反、局部改进项与正向隔离证据分别支持合同档位。机械程序验证源码绑定并独立映射档位，不声称能自动证明软件设计质量。
- 22 个 pending 仓不运输；`can-middleware` 仅为 v0.4 历史补充样例。
- 旧 archive：https://github.com/cockpit-bench/cockpit-benchmark-v031-archive
- 每个源码仓保留自己的许可证、来源和全部 heads/tags；源码仓不含答案。
