# 当前六组评测（v0.12.0）

当前66仓、863个requested叶。三中心逐仓评分与合同修正见[SIX_GROUPS_20260912.md](SIX_GROUPS_20260912.md)。原APP/FW/NEP有效合同和352叶参考保持，NEP构建独立性争议继续暂停。正式候选运行0。

|报告组|source_only|frozen_external|requested|
|---|---:|---:|---:|
|APP|79|81|88|
|FW|109|113|121|
|New Energy MATLAB|143|143|143|
|架构中心|105|142|142|
|人工智能中心|132|187|187|
|智能驾驶中心|129|182|182|

六组独立注册和报告，不合并原始分数。[assignments示例](../verification/examples/current-assignments.json)必须恰好覆盖66个ID；源码/依赖/构造传递闭包不能跨split。新33仓保守合并，并记录与先前脚手架/工程方法的来源关联，不作为独立holdout。

新增中心的软件API、平台升级/设备/分支、集成测试，以及模型UT/设备/分支维度统一要求已登记raw。这是按维度预先固定的保守证据要求，与具体参考分值无关。source_only中这些叶保持requested并明确排除；frozen_external在验证单仓记录/原始输入SHA和HEAD后可评。不能拿排除后的accuracy冒充全体requested准确率。

新增原始包为[center-native-inputs-v0.12.0.zip](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.12.0)。下载到下面旧包所在raw目录后，可执行：

```sh
python verification/evaluation_current.py prepare --wrapper . --type architecture-center --mode frozen_external --assignments verification/examples/current-assignments.json --external-inputs C:/bench/raw --output C:/bench/architecture-batch.json
python verification/evaluation_current.py inputs --wrapper . --repository-id ARC-01 --packet C:/bench/raw/center-native-inputs-v0.12.0.zip --destination C:/candidate/raw
```

单仓raw只含该目标的输入、记录和绑定，不含维护者评分或其他目标的参考。三个AAR宿主断言提供实际执行源码的单仓摘录及原文件/已安装APK绑定；摘录本身未声称独立构建。集成目标的声明依赖属于运行输入，不能另计为被评分目标。

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
