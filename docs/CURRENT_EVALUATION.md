# 当前33仓评测入口（v0.10.3）

APP、FW、新能源MATLAB分别注册，352个requested叶保留，其中351个数值参考。NEM-11参数待裁决，以reference_unresolved排除，不记零分。参数合同保持原文。

| 类型 | source_only | frozen_external | requested |
|---|---:|---:|---:|
| APP | 79 | 81 | 88 |
| FW | 109 | 113 | 121 |
| 新能源MATLAB | 133 | 142 | 143 |

将以下三个公开附件下载到同一维护者raw目录：

| packet | 文件 | SHA256 |
|---|---|---|
| current-raw | candidate-raw-inputs-v0.10.2.zip | `7ef2f66ea2c931ee2a448fbd20fa255bae140c5e663c6f590068f5b4397c0c6a` |
| legacy-fw07 | android-frozen-git-inputs-v0.9.1.zip | `1d7ecfa03c08c6916f047a5d0a403e651a193d6eab2a9391be38d41cb0def9d9` |
| sdk-repair | candidate-sdk-inputs-v0.10.3.zip | `3cc895264f5b561741cd0afa68205fac5b975f8136c0797e1448fbea4e78e670` |

新SDK包见[v0.10.3附件](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.10.3)；current-raw沿用[v0.10.2附件](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.10.2)；legacy-fw07沿用[v0.9.1附件](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.9.1)。不将完整维护者raw目录交给候选。

```sh
python verification/evaluation_current.py prepare --wrapper . --type fw --mode frozen_external --assignments C:/bench/assignments.json --external-inputs C:/bench/raw --output C:/bench/fw-batch.json
python verification/evaluation_current.py inputs --wrapper . --repository-id FW-22 --packet C:/bench/raw/candidate-sdk-inputs-v0.10.3.zip --destination C:/candidate/raw
```

每个候选只看到单仓源码、有效合同与允许的单仓raw。导出input-manifest.json绑定文件大小/SHA和来源包SHA；运行器应使用导出回执的manifest SHA绑定任务，不能让可一起改写的manifest自行证明真实性。SDK的原文解码、固定commit/blob、compileSdk和源码HEAD另有校验。

缺样本档位count=0/recall=null/unmeasured；源分组、生产LOC范围和未决参考见[诊断](population-diagnostics.json)。这些是样本描述，不是候选准确率或独立留出证明。旧171叶入口仅作冻结兼容。
