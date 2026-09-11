# 当前三类型评测（v0.11.3）

NEP修复HEAD已公开，参考绑定已刷新；四项工程修复见[FIDELITY_REPAIR_20260910.md](FIDELITY_REPAIR_20260910.md)。143个数值保持，构建独立性叶沿用旧值、暂停重新裁决。正式候选运行0。

当前 33 仓：APP 11、FW 11、NEP 现实代理 11，共 352 个 requested 叶，352 个数值参考。旧新能源 ML-01..09、NEM-10/11 已删除出当前集合，其参考和合同不再参与评测。

| 类型 | source_only | frozen_external | requested |
|---|---:|---:|---:|
| APP | 79 | 81 | 88 |
| FW | 109 | 113 | 121 |
| 新能源现实代理 | 143 | 143 | 143 |

`evaluation_current.py prepare --type new-energy-matlab` 现在绑定 reality-proxy-20260910 的原 Part 7 合同、源码清单和 143 叶参考。可直接使用 [当前 assignments 示例](../verification/examples/current-assignments.json)。全局 assignments 必须恰好覆盖当前 33 ID；来源/依赖/构造闭包不能跨 split。旧 ID 或旧批次不自动映射到 NEP。

`ne_reality.py evaluate` 保留原新组格式；两个入口的数值参考一致。其 evidence_submitted 仅表示非空，不能当作证据正确率；统一入口的证据审阅亦须提供独立 review-plan/adjudications，未审阅时结果为 not_reviewed，不冒称联合正确。NEP-10 构建规则争议见 [评审核对](REVIEW_V0111.md)，本次不改合同或参考值。

新能源所需模型、工作簿和 Git 证据来自单仓源码；以下外部输入仅服务 Android 的既有必要输入。

将以下三个公开附件下载到同一维护者raw目录：

| packet | 文件 | SHA256 |
|---|---|---|
| current-raw | candidate-android-inputs-v0.11.1.zip | `4c4ca7548f42d1e8478bb217a4b942b97428622fef07c4e705380349cae85dd4` |
| legacy-fw07 | android-frozen-git-inputs-v0.9.1.zip | `1d7ecfa03c08c6916f047a5d0a403e651a193d6eab2a9391be38d41cb0def9d9` |
| sdk-repair | candidate-sdk-inputs-v0.10.3.zip | `3cc895264f5b561741cd0afa68205fac5b975f8136c0797e1448fbea4e78e670` |

Android SDK包见[v0.10.3附件](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.10.3)；current-raw使用已剔除旧MATLAB材料的[v0.11.1附件](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.11.1)；legacy-fw07沿用[v0.9.1附件](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.9.1)。不将完整维护者raw目录交给候选。

```sh
python verification/evaluation_current.py prepare --wrapper . --type fw --mode frozen_external --assignments C:/bench/assignments.json --external-inputs C:/bench/raw --output C:/bench/fw-batch.json
python verification/evaluation_current.py inputs --wrapper . --repository-id FW-22 --packet C:/bench/raw/candidate-sdk-inputs-v0.10.3.zip --destination C:/candidate/raw
```

每个候选只看到单仓源码、有效合同与允许的单仓raw。导出input-manifest.json绑定文件大小/SHA和来源包SHA；运行器应使用导出回执的manifest SHA绑定任务，不能让可一起改写的manifest自行证明真实性。SDK的原文解码、固定commit/blob、compileSdk和源码HEAD另有校验。

缺样本档位count=0/recall=null/unmeasured；源分组、生产LOC范围和未决参考见[诊断](population-diagnostics.json)。这些是样本描述，不是候选准确率或独立留出证明。旧171叶入口仅作冻结兼容。
