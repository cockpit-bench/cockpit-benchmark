# source_only 必要输入可得性裁定

本表只审现有 171 叶所需的决定性输入能否由「精确源码 HEAD、完整交付 refs/各 tip 树、合同」获得；无网络、无 facts/oracle/标准分、无额外 SDK 和执行日志。维护者参考了现有理由与 observations，候选不得看到本表。**不重新语义评分，不更改 canonical，也不宣称本轮重新编译或穷尽源码。**

结果为 **152 supported、18 unknown、1 unavailable**。18 个候选 HEAD 和全部 heads/tags 与当前 manifest 相同；229 个既有锚点文件的 Git 原字节哈希一致，另补查 FW-14 四份原始生产文件的 Java imports，共 233 个独立文件，无绑定失败。文件校验不是 233 文件完整语义重审。逐叶具体依据、missing、path/line/symbol、Git 字节哈希与 refs 在 `evidence-availability.json`；它可直接供 profile 的 register 命令使用。

| 特别裁定 | source_only 结论 |
|---|---|
| APP-01 CI | unknown：真实命令可读，但完整可执行的肯定事实涉及外部镜像/SDK/依赖状态；不能仅凭配置把这项当已对等。 |
| APP-02 CI | unavailable：历史参考决定性依赖带时间的 HTTP/OCI 事实，本模式明确不提供；不是将 canonical 改分或归零。 |
| FW-03 build | unknown：源码可看到 BLUETOOTH_MAP 调用，却无法由调用证明 SDK31 符号不存在。公开 SDK 编译失败日志目前是必要区分证据。 |
| FW-14 build | supported：POM 直接编译四份既有生产源，已查 imports 仅 Java 标准库，真实消费者在仓，整仓平台依赖也可读。局部生产单元的结构成立；历史 25 项执行是旁证，未要求候选重放它。 |
| FW-16 build | unknown：Spa 声明的 SDK/AndroidX 入口可读，但本次未补足整个局部源码外部接口闭包；成功 AAR 日志不能默认为候选可见。 |
| FW-02/FW-03 API | supported：分别有真实稳定 AIDL 冻结/当前签名及消费者；或仓内真实 Metalava diff 驱动、签名、发布 metadata/refs。这里审机制存在，不声称候选能离线重跑。 |
| FW-07/FW-08/FW-14/FW-16 API | unknown：生成式 Soong/defaults 或外部 `*.latest` 发布签名输入尚未对等；声明和 current 文件不自动补全已发布基线解析。 |
| 平台升级 | APP-01/02/11/17、FW-02/07/16 supported：有独立源码版本/权限/反射路线，或内部定义本来就在同仓。其余 11 叶 unknown：精确 deprecated/hidden/高版本变化定义在仓外，或当前锚点不足以另走独立源码路线。不得把另一 canonical 源仓的定义喂给单仓候选。 |

其余支持子集有逐叶锚点：架构依赖图/职责/命名、低档 CI 与手工版本/版本缺失、当前交付 refs 发布通道、声明的外部构建闭包、真实测试源码及 SOLID。FW 集成测试的当前参考走源码 1 档，合同明示无 HEAD 执行记录最高 1；这不表示外部从未执行。FW-07 LSP 有两个真实生产实现，可走源码父合同路线达到 3 档，不必依赖“一个实现通过 substitution test”的执行路线。

supported 表示本轮未发现必要的仓外输入缺口，不是候选必然能答对，也不保证无限范围的负面穷尽。unknown 表示列出的必要依赖或替代源码路线尚未封闭，不能作为错误或成功计分。注册时固定这 152 叶，候选在可比叶的 abstain/error/missing 继续保留分母；将来补齐 unknown 必须在候选推理前另行登记，不能看输出后选叶。API 合同仍按本轮约定保持现状，下一版再议。
