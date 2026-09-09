# 当前三类固定集合评测

入口 `verification/evaluation_current.py` 适用 v0.10.2 的 APP、FW、新能源 MATLAB，每次必须选择一种类型。`evaluation_batch.py` 的 prepare 和旧 171 叶说明保持 v0.9.4 冻结兼容；不能混用两套分母或版本比较模型进步。

| 类型 | 全部参考叶 | source_only 可评 | frozen_external 可评 |
|---|---:|---:|---:|
| APP | 88 | 80 | 81 |
| FW | 121 | 111 | 113 |
| 新能源 MATLAB | 143 | 134 | 143 |

未纳入的叶保留 unknown/unavailable，不改标准分、不按零分计算。集合在候选运行前登记，比较相同类型/参考/合同/输入模式的同一 eligible 集合。三类原始分不相加。众数和覆盖分布见 [当前统计](current-distribution.json)，都是样本内事后诊断，不能当成候选模型成绩。

source_only 允许固定源码 HEAD、完整 refs/trees、仓内跟踪材料及有效合同，禁止网络与维护者 oracle/facts。ML-01/02/04/05/07/08 虽跟踪过覆盖报告，部分与最终比例不同；ML-03/06/09 缺少仓内报告。九仓最终模型/执行/覆盖绑定位于外部，因此 unit_test 在 source_only 中均保留 unknown，不能让候选猜最终报告。新两仓 unit_test=1 的成立条件可从实际测试定义确定，未把其额外 MIL 通过记录当作 source_only 必需输入。

frozen_external 额外使用以下原始包，登记时必须已下载到 `--external-inputs` 同一目录并通过实际字节校验，禁止失败后静默改用 source_only：

- [既有 FW-07 外部 Git 输入](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.9.1/android-frozen-git-inputs-v0.9.1.zip)：使其 API 叶可评，其他旧 Android 缺口保持。
- [v0.10.2 候选原始输入](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.10.2/candidate-raw-inputs-v0.10.2.zip)：九个旧 MATLAB 的最终 acceptance binding、原始 MIL/coverage/vectors，以及 FW-22 单独投影的源版本/环境/Instrumentation 命令和原始 log；另补 APP-22 实际 compileSdk 34 的完整SDK定义与原始返回。精确 SHA/字节绑定见 [输入清单](current-evaluation.json) 的 packets。九仓接受结果的模型 SHA 与 final 模型一致，覆盖比例支持当前合同档位。

新包没有标准分、oracle、语义布尔量或裁决。旧 MATLAB 文件原字节保留，source-binding 从已发布 snapshot 投影 HEAD/模型 SHA，另记录执行脚本与交付脚本的 SHA 对照。ML-01 两份脚本仅 CRLF/LF 不同，已逐字比较归一化文本，并单独保留执行时的原始脚本字节；其余八仓脚本逐字节一致。FW-22 从既有多仓记录投影环境、该仓 binding 和 message 条目，声明原文件 SHA 与 JSON Pointer。这是已有执行材料的拆分，不是新运行，也不把原多仓执行报告整体交给候选。

```sh
# 维护者：先确定全部 33 仓 split；示例全部为 development，不是假 holdout
python verification/evaluation_current.py prepare --wrapper . --type fw --mode frozen_external --assignments verification/examples/current-assignments.json --external-inputs /maintainer/raw --output /maintainer/fw-batch.json

# 维护者：只导出本次候选仓所需原始材料，不给候选完整总包或 wrapper
python verification/evaluation_current.py inputs --wrapper . --repository-id FW-22 --packet /maintainer/raw/candidate-raw-inputs-v0.10.2.zip --destination /candidate/allowed-raw

# 保存候选输出后，按预先登记的固定分母统计
python verification/evaluation_current.py assess --batch /maintainer/fw-batch.json --candidate /maintainer/candidate.json --output /maintainer/result.json

# 人工证据抽审沿用已支持新 batch 摘要的 sample 入口
python verification/evaluation_batch.py sample --batch /maintainer/fw-batch.json --candidate /maintainer/candidate.json --size 20 --seed review-1 --output /maintainer/review-plan.json
```

每次候选只获得一个源码仓、该类型有效合同、允许的单仓 raw 目录和 opaque profile_sha256。候选输出包含 `profile_sha256` 和 `leaves` 数组，每项有 `id`（`仓库ID/叶名`）、`status`（scored/abstain/error）；scored 还须有合法 `score`，语义审查另外要求 `reasoning` 和 `evidence`。不要给候选 batch/reference、availability、分布、来源角色或其他仓源码。新能源 MATLAB 的有效合同用 [EFFECTIVE_CONTRACT.md](../suites/matlab-simulink/EFFECTIVE_CONTRACT.md)，无需让候选读取含答案的 wrapper。

assignments 始终覆盖全部 33 仓，检查 family_id、related_ids、construction_group 的传递闭包；APP-14/FW-16、APP-21/FW-21、ML-04/NEM-10 以及同构造批次不会跨 split。保守合并意味着独立组数可能很少；工具不认证未知谱系，也不把公开开发集变成独立测试集。

输出包括固定分母准确率、输出覆盖、逐叶宏平均、每个实际出现档位的召回/混淆、弃答、来源族分层及众数。没有该档样本时不能算该档识别能力。提供固定抽审计划和人工 adjudications 后另报“分数正确且证据支持”的联合比例；未抽审时明确 not_reviewed。live_environment 尚无新捕获的同批参考，入口拒绝该模式。运行器负责真实输入/网络/进程隔离，注册 hash 不证明时间先后或隔离已经执行。

APP-22 的 Camera1 风险需要外部SDK废弃定义，source_only保留unknown；frozen_external导出该仓的sdk目录（四个文件）。实际SDK版本取video/build.gradle的34，不能用模拟器API35替换。完整原始响应与解码文件使总包解压大小为68,842,664字节，校验器仍限制解压不超过96MiB。

本版本数值统计将合法等值浮点分数归一到整数档位。全部合法档位均输出：无样本时count=0、recall=null、measurement_status=unmeasured。每个批次和结果携带population_diagnostics，显示来源闭包、缺档、常量叶和样本内确定性关联；不把缺档记为0%或100%。当前新能源独立留出状态为structurally_unavailable，APP/FW为not_certified。详见[修复与未关闭建设项](REVIEW_V0102.md)及[诊断](population-diagnostics.json)。
