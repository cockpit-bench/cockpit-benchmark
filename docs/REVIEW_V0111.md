v0.11.2 补丁：恢复测试夹具显式设置 LF 和 Git autocrlf，不再依赖本机全局设置；实际恢复逻辑、源码、合同和参考分均保持。

v0.11.1：旧新能源联调11个GitHub源码仓已按用户确认永久删除，逐仓已登录API与匿名网页均返回404。当前集合为33仓；默认恢复与评测入口已统一。

# v0.11.0 Pro 评审核对与旧组退役

本轮核对输入固定为 v0.11.0 wrapper `ac6ffa46096993853dc7871413a9efe008bec2ec`。用户要求阅读评审，同时明确删除旧新能源11仓，并进一步确认永久删除对应GitHub源码仓。本轮完成退役与当前入口迁移，不把评审全文当成已授权的合同修改或样本扩建计划。

## 核对结论

| 评审意见 | 本轮核对 | 处理状态 |
|---|---|---|
| 两组新能源并存，默认all只走旧33仓 | 原注册/restore/evaluation_current确有该行为 | 本轮移除旧11仓，默认恢复和统一评测改为APP11、FW11、NEP11；旧ID拒绝 |
| NEP-10构建2分的合同优先级有歧义 | 补充仅限定单SLX无外部源码依赖；Part7有源依赖封顶1；NEP-10已有真实FaultComponentLibrary.slx | 成立，不能断言2必然正确或必改1。保留当前参考与合同，列为待裁决叶，勿用它调Prompt消除“错题” |
| ne_reality.evaluate证据字段可以缺失 | 代码默认空dict，仅用bool计数；正确分数可得到数值满分 | 成立。数值、证据定位、语义支持须分开；本轮未新增证据正确性实现或宣称关闭 |
| replay不是独立语义重评 | 实现核验身份/census后返回既有gold合计 | 成立，保留明确限制 |
| 大范围层次/命名判断缺完整元素清单 | 现有主模型/少量SID/说明文档绑定不足以自动重建所有人工分类分子 | 需要补足可复核清单；本轮不是143叶独立语义审阅 |
| 新组6个恒定叶、众数123/143、21/52档位 | 用当前143叶重算一致 | 成立；删除旧组不改善新组区分度，不宣称泛化改善 |
| 分支/设备按名称给分不等于真实多平台能力 | 现合同接受命名代理，原平台refs仍指基线 | 成立；不据此擅自改分 |
| APP-21解耦3与组件/模块0可以并存，FW-21 LSP3有合理依据 | 属于不同构念，评审提供了定点源码依据 | 未发现据此直接改分的理由；本轮不声称重新全仓审阅Android |
| .sldd不能一概按ZIP/XML解析 | 核对MathWorks工具说明支持文本JSON和压缩二进制 | 技术问题成立；未发现当前11仓因该条产生错分，合同修订尚未实施 |
| 缺档、规模混杂、独立留出与正式候选实验缺失 | 当前登记/诊断与公开限制一致 | 仍开放；不以删除旧组、更多hash或复制源码冒充完成 |

格式核查来源：[MathWorks Simulink Data Explorer](https://github.com/mathworks/data-explorer-vscode)、[原生数据字典API](https://www.mathworks.com/help/simulink/slref/simulink.data.dictionary.open.html)。解析能力不足应保留unknown，不能把打不开当作不存在；这里是评审核对意见，没有改写候选可见合同。

## 本轮退役范围

删除旧 ML-01..09、NEM-10/11 在主线的manifest、参考分、合同、独立审阅和专用回放入口。当前源码登记只含APP11、FW11、NEP11；四个私有预留仓不在目标内。旧wrapper历史tag未重写，旧源码URL删除后不再可恢复。

| 旧ID | 已删除并核验404的GitHub仓 |
|---|---|
| ML-01 | cockpit-bench/torque-request-controller |
| ML-02 | cockpit-bench/coolant-fan-controller |
| ML-03 | cockpit-bench/charge-interlock-controller |
| ML-04 | cockpit-bench/battery-power-manager |
| ML-05 | cockpit-bench/axle-traction-coordinator |
| ML-06 | cockpit-bench/cabin-thermal-coordinator |
| ML-07 | cockpit-bench/energy-domain-supervisor |
| ML-08 | cockpit-bench/thermal-network-controller |
| ML-09 | cockpit-bench/vehicle-actuator-supervisor |
| NEM-10 | cockpit-bench/battery-energy-calibration |
| NEM-11 | cockpit-bench/battery-contactor-control |

当前三类参考分别142/440、194/572、409/671；三个有效合同及全部352叶数值保持。此次没有源码改动、原生执行或正式候选实验。具体发布、删除和验证结果以本轮发布回执为准。
