# Validation-18 evidence correction — draft

**未审定草稿：63 个 FW 叶尚未独立复核，不能作为新的审定标准答案。**

本分支保存 v0.7.6 之后的证据修正候选。FW-08 LSP 从 3 调整为 2；APP 216/360、FW 268/468，暂存合计 484/828。

- `SCORECARD.md` / `SCORECARD.csv`：候选分数和证据。
- `STANDARD_SCORES.json`、`oracle/`、`facts/`：对应机器可读候选。
- 63 个待复核叶：9 FW 各自的 CI、非 LSP 四个 SOLID、平台升级和 release 策略。
- 已进行 108 叶输入事实公式重算，零差异；410 个证据对象绑定检查通过。上述检查不等同于新一轮源码语义复审。
- FW-14 DIP 改绑实际权限注入和引擎反射构造；通用 symbol 行段已修正。待复核类型声明不再被称为充分的行为证据。

本分支不创建发布 tag，restore.ps1 拒绝恢复未审定候选。已发布历史 v0.7.6 仍在 main/tag 中，可追溯，但其“171 叶独立重算”说明存在上述已知缺口。

源码仓 HEAD/refs 没有变化；22 个 pending 仓不评分、不运输。控制工作区脚本、测试及过程记录不属于此轻量 wrapper 的发布内容。
