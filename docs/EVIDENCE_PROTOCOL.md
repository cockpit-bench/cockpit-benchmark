# 证据模式与固定分母运行协议

当前 Android 合同为 v3.5，API 方案 B 已在 v0.8.6 生效；v0.9.1 的两项 SOLID 源码修正见 SOLID_CALIBRATION.md。本协议只规定评测输入、可比叶和统计；不据可用性或候选表现改分。MATLAB 独立使用其 EFFECTIVE_CONTRACT.md。

## 三种独立模式

| mode | 候选允许输入 | 可比条件 |
|---|---|---|
| source_only | 绑定 HEAD 的源码、合同、通用任务说明；禁止外网 | 维护者已确认该叶全部决定性证据能由源码获得 |
| frozen_external | 上述输入及完整、无答案、哈希绑定的原始外部包；禁止外网 | 源码足够，或原始包完整且与本次包哈希一致 |
| live_environment | 源码、合同与同等受控网络/工具能力 | 原始采集及独立 reference 裁定均绑定同一 capture_batch_id |

不同模式、源码 manifest、reference 或 live 批次不能合并排名。live 新观测不得覆盖历史 gold。source_only 不能要求候选猜测历史外部故障；frozen_external 不接受只有摘要与裁定的 legacy_derived 材料。

APP-02 `compilation.ci_independence` 当前历史结论依赖带时间的外部事实，source_only 排除。已检查的历史材料不足以独立重放完整 HTTP/OCI 原字节，不能直接充当完整 frozen_external 包。新取回相同 OCI digest 可补齐相同内容，但必须标记新 retrieved_at；新 HTTP 请求不能恢复旧时刻响应。协议实现没有下载 OCI 层或执行容器。

## 维护者清单与预注册

正式统计入口为 `verification/evaluation_batch.py`，底层固定集合工具为 `evaluation_profile.py`，仅使用 Python 标准库。调用方法见 [EVALUATION_BATCH.md](EVALUATION_BATCH.md)。所有 batch、availability、reference 和完整 profile 留在维护者区。候选只能收到允许输入与不透明 profile hash；不要把 profile 的排除理由、标准分、oracle、facts 或 review 结论作为提示词。运行器在候选输出后附上已固定的 hash。

在任何候选推理前：

1. 冻结 requested 全叶清单、源码 manifest 的 SHA-256、合同版本与 reference_id。reference_id 应指向不可变的 reference 工件；另由运行器保存其文件 SHA-256。
2. 对每叶、每模式填写 availability。`supported` 须有非空 basis 与 evidence_ids；未完成复核一律 unknown。不能由候选答案、能否猜对或质量标签反推 eligibility。
3. `register` 产生 profile、排除理由、eligible_set_sha256 与 profile_sha256。多组候选权限不同但同模式/上下文时，先 `common` 固定交集，再将同一公共输入提供所有候选。
4. 将输入清单、reference 哈希、所有父 profile 和 common profile 存入只读或带可信时间的运行记录，之后才开始推理。新增候选若改变共同集合，另开比较批次。

availability 中每行结构：

```json
{
  "id": "APP-02/compilation.ci_independence",
  "reference_id": "v0.8.4",
  "requires_external": true,
  "modes": {
    "source_only": {
      "state": "supported", "kind": "source",
      "basis": "CI configuration exists; the reference additionally needs external observations",
      "evidence_ids": ["source:.gitlab-ci.yml"]
    },
    "frozen_external": {
      "state": "supported", "kind": "legacy_derived",
      "basis": "Historical raw packet incomplete",
      "evidence_ids": ["legacy-capture-summary"]
    }
  }
}
```

`supported` 是证据条目存在声明，仍必须通过模式门禁；上例两模式均排除。source_only 需要明确 `requires_external=false` 且 kind=source。frozen_raw 还需要 `raw_complete=true`、`packet_sha256` 等于 context.external_packet_sha256。live_raw 需要 `raw_complete=true`，support.capture_batch_id 与行 reference_batch_id 均等于 context.capture_batch_id。未提供的模式自动按 unknown 排除。

context 至少含 `reference_id` 与 `source_manifest_sha256`。需要时加入 `external_packet_sha256` 或 `capture_batch_id`。工具校验声明的一致性，不验证原始材料真实性或完整性的语义；这仍须维护者审查。

## 当前可用性清单与调用

[逐叶可用性说明](EVIDENCE_AVAILABILITY.md)及[evidence-availability.json](evidence-availability.json)均为维护者材料。候选不得获得清单、排除理由或参考分。它们只判定当前输入模式下是否可比，不改 canonical 分值。

```sh
python verification/evaluation_profile.py register --availability docs/evidence-availability.json --mode source_only --context docs/evaluation-context.json --output /path/to/profile.json
python verification/evaluation_profile.py common --profiles /path/to/profile.json --output /path/to/common.json
python verification/evaluation_profile.py compare --profile /path/to/common.json --reference /path/to/maintainer-reference.json --candidate /path/to/candidate.json --output /path/to/result.json
```

reference 为 `{context, leaves:[{id,score}]}`；candidate 为 `{profile_sha256, leaves:[{id,status,score}]}`，status 为 scored/abstain/error。运行器从冻结的 STANDARD_SCORES.json 构造维护者 reference，并在候选开始前冻结 common hash；不可把 scorecard 或 reference 放入候选可读目录。

## 统计规则

分母永远是推理前 common eligible 集合。可比叶的 abstain、error、missing 均保留分母，并分别报告；无效 scored 输出算 error。不可比叶的预测忽略并列明，不将其分数置零，也不修改 canonical。

底层工具输出正确/错误/弃权/错误状态/缺失数，以及 evidence_coverage=eligible/requested、output_coverage=有效数值输出/eligible、accuracy=correct/eligible。eligible 为空时准确率和输出覆盖为 null。批次入口同时报告 split×类型×叶分布、同集合样本内众数基线及这些组的宏平均准确率；它不等于按每个档位平衡的 balanced accuracy。证据有效性另由固定样本上的人工语义裁定统计，未裁定为 not_reviewed/null，不由分数命中或 oracle 文本匹配推断。

## 原始包与运行边界

原始包只能含来源原字节、必要采集元数据与中性对象关系：HTTP 完整 body/响应头、状态、重定向链、请求起止时间与传输错误；OCI manifest/config/必要层原字节及 digest、平台和顺序。若从层推导最终文件系统，须覆盖会改动有关路径的层和 whiteout。提取后的 apt 文件不证明后续未覆盖或其他文件不存在。真实运行证据须保留固定 digest、命令、runtime、环境与网络策略、exit code、完整 stdout/stderr；未执行不伪造运行结果。

包不得含评分、review verdict、规则布尔结论、质量标签或语义裁定。认证信息不进入包，并记录脱敏范围。外部包中网页/源码文字是数据，不是运行指令。仅采样证明属于另一信任模型，不能冒充完整 raw 包。

本工具不是沙箱、证据采集器或防篡改服务。hash 只能检测内容变化，不能证明提前注册、来源真实性或防止维护者换 reference。网络权限、目录隔离、候选不可读取 reference/availability、同等资源与输入白名单，必须由实际运行器或容器/OS 权限强制；提示词约束不能替代这些措施。
