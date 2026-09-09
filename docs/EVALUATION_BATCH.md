# 固定集合评测入口

`verification/evaluation_batch.py` 将冻结集合、同源切分检查、合法分值校验、逐叶分布、基线和证据裁定合为一条统计流程。当前入口用于 Android 18 仓；MATLAB 仍独立，不能套用 Android availability 或累加两个套件原始分。

候选运行前在维护者目录准备 assignments.json：18 个 active 仓 ID 各映射一个 split 名。当前公开集建议统一写 `development`。APP-14/FW-16 必须同 split；未知、pending、缺失条目或同 family 跨 split 都会拒绝。切分校验只约束已记录 lineage，不构成独立 holdout。

```sh
python verification/evaluation_batch.py prepare --wrapper . --mode source_only --assignments /maintainer/assignments.json --output /maintainer/batch.json
```

工具验证合同、标准分、源码 manifest 的实际文件 SHA，固定 eligible、reference、split 与 batch hash；已存在输出不会覆盖。以下均按当前标准分和各自实际 eligible 集合计算，类型×叶组内取众数，是样本内事后基线，不是 Agent 成绩。

<!-- current-baselines:start -->
当前参考版本：`v0.9.4`。

| 集合 | 众数命中/分母 | 样本内比例 |
|---|---:|---:|
| 完整集 | 124/171 | 72.51% |
| source_only | 113/155 | 72.90% |
| frozen_external | 114/156 | 73.08% |

<!-- current-baselines:end -->

已有多组同模式 profile 时，先通过 `evaluation_profile.py common` 固定交集，再向 prepare 传 `--profile /maintainer/common.json`。工具拒绝与快照、模式或当前支持集合不一致的交集。frozen_external 还须用 `--external-packet` 提供并校验[实际原始包](EXTERNAL_GIT_INPUTS.md)；只声明摘要不能注册缺包的 frozen 批次。当前两种模式的集合与基线见上表；frozen 模式必须另有实际外部输入包，不能仅凭这张表注册。

batch 含标准分和排除理由，必须留在维护者侧。候选只得到单仓绑定 HEAD/all refs 的源码、有效合同、中性任务说明、允许的原始输入；协调器保留不透明 profile hash 并将其附到保存输出。Android 有效合同入口 `SCORE_RULES.md`；MATLAB 为 `suites/matlab-simulink/EFFECTIVE_CONTRACT.md`。候选不得读 wrapper、标准分、quality tier、oracle、facts、profile 或本说明中的分布结果。

运行器负责保存推理前注册时间、允许输入文件哈希、源码 refs、模型配置和资源记录，并用容器/OS 权限限制目录和网络。此 Python 工具是维护者统计入口，不会执行模型，也不提供 OS 沙箱；不能把一次夹具回归宣称为实际模型评测。

保存的候选 JSON：

```json
{"profile_sha256":"预先固定的摘要","leaves":[{"id":"APP-01/architecture.componentization","status":"scored","score":1,"reasoning":"候选理由","evidence":[{"path":"源码路径","commit":"HEAD","start_line":1,"end_line":2,"claim":"事实"}]}]}
```

`status` 可为 scored/abstain/error；missing、abstain、error 不缩分母。可比叶非法档位会拒绝整次统计以便修正输出格式；排除叶的预测只列出并忽略。不同 batch 不直接排名。

```sh
python verification/evaluation_batch.py assess --batch /maintainer/batch.json --candidate /runs/candidate.json --output /maintainer/scores.json
python verification/evaluation_batch.py sample --batch /maintainer/batch.json --candidate /runs/candidate.json --size 30 --seed review-01 --output /maintainer/review-plan.json
```

输出含逐组 gold 分布、缺档、候选准确率和相同分母的众数基线；macro 是 split×类型×叶各组等权。多 split 的结果保留分组，不把训练分布当测试成绩。默认不声称证据正确。

证据抽检 seed 和样本数应在读答案前登记，随后按 seed 对全部 eligible 叶（包括无输出）确定样本。人工裁定的是“所给理由及证据是否足以支持整个叶判定”，不要求同文件、同行号或逐字复现 oracle。验证 claim 存在后，还要检查范围、反例和上下档理由；引用真实文件本身不足以判 supported。

adjudications.json：`{"plan_sha256":"固定计划摘要","leaves":[...]}`。每行含 id、verdict、reviewer、reviewed_at、rationale；supported/contradicted 还须 anchors 数组，每个锚点含字符串 path、revision、location、claim。verdict 为 supported（足以支持结论）、contradicted（被源码反驳）、insufficient（存在输出但证据/范围不足）或 no_output（无有效评分输出）。supported 还要求候选自身给出非空 reasoning 和 evidence。锚点保存实际核查的 HEAD、路径、位置、事实；工具验证绑定与必要字段，语义由审阅者负责，不能填夹具来冒充人工复核。未提供行保持 unreviewed。

```sh
python verification/evaluation_batch.py assess --batch /maintainer/batch.json --candidate /runs/candidate.json --review-plan /maintainer/review-plan.json --adjudications /maintainer/adjudications.json --output /maintainer/reviewed-result.json
```

证据指标分别报告抽样数、已审数、审阅覆盖率、各 verdict 数、固定样本支持比例，以及“分数正确且证据支持”的联合比例。未审不能计成功；部分抽检不能宣称全量证据正确。重新抽样或换候选必须另建计划，旧裁定不能直接复用。
