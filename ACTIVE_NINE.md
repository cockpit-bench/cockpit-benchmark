# APP-9 交付范围

本检查点仅交付 Android APP benchmark。FW 正在等待修正后的 Android
Framework 评分合同，未评分、未运输，也不计入本版本分母。

| 角色/规模 | small | medium | large |
|---|---|---|---|
| 高 | APP-03 climatix-hvac | APP-02 horizon-launcher | APP-01 aurora-settings |
| 中 | APP-13 market-hub | APP-11 motion-control | APP-14 cockpit-shell |
| 低 | APP-17 thermo-control | APP-16 nova-launcher | APP-15 atlas-settings |

- 仓库：9
- canonical 叶子：72（每仓 8）
- 总分：242/360
- 评分合同：SCORE_RULES.md 的 APP 部分
- 标准答案：STANDARD_SCORES.json
- 人类表格：SCORECARD.md / SCORECARD.csv
- 评估输入：每次只给一个源码仓，禁止把 wrapper、oracle、facts 或评分表放进输入。

源码仓均为独立 public Git 仓；源码仓内不包含质量标签或标准答案。
