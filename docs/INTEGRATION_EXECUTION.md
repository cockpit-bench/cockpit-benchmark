# 集成测试执行证据格式

本文说明现行合同 3.5 的执行记录结构与绑定校验，不改变评分合同。主机上的真实跨组件集成测试可以提供相应范围的执行证据；`host_jvm`、`host_native` 不代表 Android 设备或模拟器运行。下面的示例仅用于解释格式，不是已完成的测试报告。

## 评分事实入口

`quality.integration_test` 的 `facts` 使用以下字段：

| 字段 | 类型和含义 |
| --- | --- |
| `valid_integration_assertions_and_interface_behavior` | 必填布尔值；真实测试断言及接口行为是否符合合同，须由源码语义证据支持。 |
| `final_head_integration_execution_exists` | 推荐的通用布尔标志。提供时优先于历史别名。 |
| `final_head_android_integration_execution_exists` | 通用标志缺失时使用的历史别名；名称不能证明设备执行。 |
| `evaluation_revision` | 声明有执行时必填，40 位小写十六进制 Git commit OID。 |
| `integration_execution` | 声明有执行时必填的执行对象，格式见下文。 |

标志缺失或为 `false` 时，执行对象只能缺失、为 `null`、`{}` 或 `{"status":"not_run"}`。不能用 false 标志隐藏完整执行记录。完整执行声明但缺字段、绑定失败或事实矛盾时，验证失败，不自动降为 1 分。没有执行且存在有效测试行为时为 1 分；没有有效测试行为为 0 分。

若保留 `majority_tests_pass`、`defined_key_interaction_coverage_ratio`、`executed_test_pass_ratio`，它们必须与重新计算的结果一致，不能代替执行记录。

## 执行对象

以下字段均必填，条件字段另列：

| 字段 | 约束 |
| --- | --- |
| `revision` | 等于 `evaluation_revision`，并由验证器核对等于被评估源码快照的 final HEAD。 |
| `mode` | `local` 或 `remote_ci`；标识执行来源，不由评分器执行测试。 |
| `runtime` | `android_device`、`android_emulator`、`host_jvm` 或 `host_native`。 |
| `runtime_environment` | 非空字符串，明确操作系统、架构、运行时及相关版本等实际环境。 |
| `runner`、`command` | 非空字符串；记录实际测试运行器和执行命令。 |
| `status` | 必须为 `completed`。 |
| `objectives`、`expected_outcomes` | 非空字符串；记录实际测试目标和合理预期。 |
| `tests_passed`、`tests_failed`、`tests_skipped`、`tests_total` | 非负整数，不接受布尔值；total 必须大于零并等于前三项之和。 |
| `pass_ratio` | 有限数值，等于 passed / total；跳过项计入分母。 |
| `coverage` | 下节所述的可复算关键跨组件交互覆盖代理。 |
| `artifacts` | 必须显式提供数组；没有单独附件时可为空，有 JUnit、coverage、运行日志等附件时记录并固化其摘要及 digest。 |
| `report_path`、`report_sha256` | 留存 JSON 报告在证据包中的安全相对路径及报告原始字节的 64 位小写十六进制 SHA-256。 |

`runtime` 为设备或模拟器时，还必须提供非空 `target_id`、正整数 `android_api`、非空 `build_fingerprint`。主机执行不要求这些设备字段；即使出现 Android API 配置等元数据，也不能据此宣称进行了设备执行。缺少设备字段的主机记录改标为设备会被拒绝，但验证器不能单靠字段判断伪造记录。

每个 `artifacts` 条目必须含非空 `path`、`kind`、`summary` 以及 64 位小写十六进制 `sha256`。附件路径必须唯一，不能指回报告自身。报告和所有附件均须列入证据包 `package.json` 的 `files_sha256`；实际字节 digest、执行对象 digest、包内 digest 必须相等。

报告解析后的 JSON 对象必须**严格等于** `integration_execution` 删除 `report_path` 和 `report_sha256` 两个顶层键后的对象。没有额外包装层；`artifacts`、`coverage` 和条件 `ci` 对象均保留。报告自身 SHA-256 基于实际保存的原始字节计算，避免把报告自己的 digest 写回报告造成循环。

## 覆盖分母与评分

`coverage` 必须含非空字符串 `name`、`definition`、`scope`，以及以下字段：

| 字段 | 约束 |
| --- | --- |
| `all_edges` | 非空数组；每项为两个不同、非空组件名组成的数组，如 `["Service","Manager"]`。边有方向，不得重复。 |
| `covered_edges` | 同样格式且无重复，必须是 all_edges 的子集，可为空。 |
| `numerator`、`denominator` | 非负整数，分别等于 covered_edges 和 all_edges 的唯一边数量。 |
| `ratio` | numerator / denominator。 |
| `threshold` | 合同门槛 0.5。 |

比例核对使用有限数值及绝对误差容限 `1e-12`；评分直接使用计数复算值。测试文件数、断言数及随意删减的交互边不能替代合理的关键交互范围。native 子目录测试只能支持所披露范围，不能被描述为整仓覆盖。

在有效真实测试行为和完整执行绑定成立后，通过率严格大于 0.5 且交互覆盖率大于或等于 0.5 才满足 2 分。满足上述条件且通过率恰为 1 才得 3 分；存在 skipped 项不能达到 100% 通过。其他有效测试行为情况为 1 分。

## 远程 CI 的附加绑定

`mode=remote_ci` 时必填 `ci` 对象：

| 字段 | 约束 |
| --- | --- |
| `provider`、`run_id`、`job_id` | 非空字符串。 |
| `run_url` | 非空 HTTPS URL。 |
| `revision` | 等于被评估 final HEAD。 |
| `workflow_path` | 源码仓内安全相对路径。 |
| `workflow_blob` | 40 位小写十六进制 OID，必须等于 final HEAD 对应路径的 Git blob。 |
| `workflow_sha256` | 64 位小写十六进制 SHA-256，必须匹配该 blob 的实际内容。 |
| `job_conclusion` | `success` 或 `failure`，表示作业已结束；集成测试通过率从测试计数计算，不从作业名称或整体结论推断。 |

`mode=local` 时 `ci` 只能缺失、为 `null` 或 `{}`。远程 CI 可以运行主机测试；mode 与 runtime 是不同信息。

## 合成示例与验证边界

下面仅是字段片段，用于展示主机运行与覆盖计算。它不是完整记录，缺少实际 final HEAD、报告、附件及其 digest，不能用于评分或声称已经执行：

```json
{
  "runtime": "host_jvm",
  "runtime_environment": "SYNTHETIC EXAMPLE: Linux x86_64, OpenJDK 17, Robolectric fixture",
  "mode": "local",
  "runner": "SYNTHETIC EXAMPLE: JUnit runner",
  "command": "SYNTHETIC EXAMPLE: ./gradlew integrationTest",
  "tests_passed": 3,
  "tests_failed": 0,
  "tests_skipped": 1,
  "tests_total": 4,
  "pass_ratio": 0.75,
  "coverage": {
    "name": "Synthetic critical interaction proxy",
    "definition": "Unique exercised directed edges divided by declared critical edges",
    "scope": "Synthetic Service, Manager and Router example only",
    "all_edges": [["Service", "Manager"], ["Manager", "Router"]],
    "covered_edges": [["Service", "Manager"]],
    "numerator": 1,
    "denominator": 2,
    "ratio": 0.5,
    "threshold": 0.5
  }
}
```

公开回归测试用临时 Git 仓及合成报告字节检验上述绑定、拒绝路径和规则映射；它们不是实际 Android 或主机集成测试的运行回执。不得把示例保存成冒充真实执行的报告。

验证器证明的是留存字节、版本、字段及计数一致性。它不自动证明运行器报告真实、测试确实运行、断言有效、交互边范围完整或目标合理。高分仍需独立检查真实测试源码、跨组件接口行为和实际执行证据；不能用合成报告、裸 true 标志或自述字段替代这些证据。此格式本身不会提高现有样本分数。
