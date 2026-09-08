# 叶 × 档位 × 证据状态覆盖

基线：v0.8.0 的 18 仓标准答案；不读取 Agent 预测。

样本内类型×叶众数基线：**130/171 = 76.0%**。这不是独立测试准确率，也不检查理由或证据质量。

覆盖 **42/81** 个类型×叶×合法档位组合；这是档位计数，不能替代真实任务能力验证。

| 类型 | 叶 | 分数:样本数 | 缺失档位 |
|---|---|---|---|
| APP | architecture.componentization | 0:1, 1:2, 3:1, 5:5 |  |
| APP | architecture.decoupling | 2:8, 3:1 | 0, 1 |
| APP | architecture.modularization | 0:1, 1:2, 2:3, 3:3 |  |
| APP | compilation.api_version_management | 0:2, 1:7 | 2, 3 |
| APP | compilation.ci_independence | 0:4, 1:2, 2:1, 3:2 |  |
| APP | compilation.compilation_independence | 0:2, 1:2, 2:5 | 3 |
| APP | platform_reuse.platform_upgrade | 0:2, 3:7 | 8, 10 |
| APP | platform_reuse.release_branch_strategy | 0:9 | 3, 8, 10 |
| FRAMEWORK | compilation.api_version_management | 0:2, 1:1, 3:6 | 2 |
| FRAMEWORK | compilation.ci_independence | 1:9 | 0, 2, 3 |
| FRAMEWORK | compilation.compilation_independence | 0:7, 1:2 | 2, 3 |
| FRAMEWORK | platform_reuse.platform_upgrade | 0:1, 3:8 | 8, 10 |
| FRAMEWORK | platform_reuse.release_branch_strategy | 0:9 | 3, 8, 10 |
| FRAMEWORK | quality.integration_test | 1:9 | 0, 2, 3 |
| FRAMEWORK | solid_principle.dependency_inversion | 1:2, 2:7 | 0, 3, 4 |
| FRAMEWORK | solid_principle.interface_segregation | 1:1, 2:1, 3:7 | 0, 4 |
| FRAMEWORK | solid_principle.liskov_substitution | 0:3, 3:6 | 1, 2, 4 |
| FRAMEWORK | solid_principle.open_closed | 2:4, 3:5 | 0, 1, 4 |
| FRAMEWORK | solid_principle.single_responsibility | 2:9 | 0, 1, 3, 4 |

完整 JSON 的 cells 列出每个档位的仓 ID、源码/库存锚点数量、输入方法和 Android 集成执行证据状态。
9 个 FW 集成测试叶的 final-HEAD Android 执行证据均为 absent；其他叶不凭此字段缺失推断未执行。
评分规则映射与人工语义观察映射分别记录；代码锚点存在不能证明判断正确或抽样完备。

## 优先对照

1. 发布策略 3/8/10：真实车型配置、平台共用和跨平台统一发布，必须有生效行为和 refs 证据。
2. 平台升级 8/10：私有 API 未隔离、隔离且降级、公开 API 与接口隔离的成对变化。
3. FW CI 和 Android 集成执行正例：不得用 host 测试替代 Android 执行及关键交互覆盖分母。
4. 命名不变性可作为诊断，但当前合同命名门槛仍有效；更改主分需另行版本化。

对照样本单独成集，同源变体共用 family_id；不混入 Validation-18 分母，也不拆到调参与独立验证两侧。
