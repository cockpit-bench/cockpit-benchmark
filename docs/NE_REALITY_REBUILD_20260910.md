# 新能源 MATLAB 现实代理组：重建交付

已按两份用户资料重建 **11 个 Vc* 模型仓**，并与原新能源 11 仓联调组并存。主要差距已通过真实模型、接口表及工程工件修正；新组是可运行的合成业务代理，尚不能宣称复原内部 36 仓的算法、联合分布或质量分布。

本地新入口：`suites/new-energy-matlab/cohorts/reality-proxy-20260910`。APP/FW/新能源仍为三种业务类型；旧组使用原合同，新组单独使用已批准 Part 7 与构建空档补充，分数不合并。当前本地准入，未上传新源码或答案。

## 主要形态变化

下表真实值来自所提供扫描汇总，并非本机重新扫描内部源码。旧值沿用差异清单中的描述；清单个别断言与当前 v0.10.3 不一致，不把它当现行 gold。

| 项目 | 提供的真实汇总 | 新组实际结果 |
|---|---|---|
| 命名/分组 | Vc*；PROP 33 / TVC 3 | Vc* 11/11；PROP 10 / TVC 1 |
| 布局 | Documentation/Model/Src/UnitTest；少量包裹/拼写变体 | 11/11四类目录；1包裹层、1 UintTest |
| SLX + XLS | 36/36，旧清单仅1仓有XLS | 11/11；XLS为Excel实际转换的OLE/BIFF8 |
| XLSX | 94% | 11/11；11变更、8SWUT、5检查表 |
| C/H/A2L/HTML | 69% | 8/11（72.7%）；真实ERT输出、实际执行报告 |
| LAB / MAT / P | 56% / 53% / 31% | 6/11、6/11、3/11 |
| MEX / TLC | 22% | 2/11（18.2%）；原生编译且实际被模型调用 |
| M文件 | 近0，旧清单37个 | 候选仓0个；构建/验证脚本保留在维护者材料 |
| Inport / Outport中位 | 533 / 190 | 566 / 204 |
| SubSystem中位 / 最大 | 113 / 1012 | 116 / 822 |
| Constant中位 | 185 | 133 |
| From/Goto | 83% | 9/11（81.8%）；中位44/22，仍低于汇总64/41 |
| S-Function | 22/36 | 原生解析9/11；保存XML直接S-Function 5/11，另有Reference展开项 |
| Trigger / Enable / DataStore | 33/36、28/36、25% | 10/11、8/11、3/11，均连接业务或诊断 |
| Git | master恒1；tag中位4、最大71；auto23/36 | master均1；tag中位4、最大71；auto7/11 |
| 参数/接口命名 | scope+Vc模块+成员+后缀，掺默认端口 | 同体系；内部默认端口11.0%–15.9%，外部端口具名 |

原报告将38个模型的出现次数写成38/36仓，Reference甚至37/36；80份configSet也不是80仓。新组按11仓/11模型分别计算，原生解析和保存XML不混计。新组8个FixedStepDiscrete、3个VariableStepAuto；FixedStep为0.001×4、0.01×4、auto×3。11个SLX均含真实modelDictionary.xml，不伪造旧版codeDictionary或外置sldd。

## 实际业务与执行

每条已声明通道都参与范围/通信/时效检查、连续两次资格确认、工程转换及安全替代；物理输出、无效计数、边沿快照以及领域控制均有真实消费者。不同业务采用下列领域规律，未用未接线块或空系统凑体量。

| ID | 模块 / 业务 | 子系统 | 入/出端口（含内部） | 仿真采样 |
|---|---|---:|---:|---:|
| NEP-01 | VcVcuInD：整车输入采集与有效性网关 | 494 | 2415/869 | 6737 |
| NEP-02 | VcVcuOutQM：执行器扭矩输出与变化率限制 | 147 | 716/258 | 1977 |
| NEP-03 | VcVmcTrq：驱动扭矩与热/功率包络 | 106 | 514/186 | 1417 |
| NEP-04 | VcErcRgn：制动能量回收协调 | 96 | 462/167 | 1277 |
| NEP-05 | VcDmcDrv：驾驶模式及充电/碰撞互锁 | 86 | 414/149 | 1137 |
| NEP-06 | VcWrcWhl：车轮滑移与牵引限制 | 106 | 515/185 | 1417 |
| NEP-07 | VcDeChg：导引信号与高压充电协调 | 116 | 566/204 | 1557 |
| NEP-08 | VcPvcThm：电池/电机热需求与积分控制 | 187 | 915/330 | 2537 |
| NEP-09 | VcSfCPropR：推进扭矩偏差监控与故障保持 | 232 | 1144/412 | 3167 |
| NEP-10 | VcSfDPropR：多部件故障与通信监督 | 822 | 4135/1445 | 11217 |
| NEP-11 | VcScHv：高压预充、合闸、故障保持与复位 | 46 | 225/76 | 702 |

执行器输出包含变化率约束和紧急抑制；热管理含限幅积分状态；推进安全含连续异常确认与故障保持；高压模块包含预充、反馈合闸、超时和复位。需求与独立预期生成保留在维护者材料，候选仅获得本仓业务测试向量和实际报告。

原源与全新完整恢复副本均通过R2023b实际仿真：各 **33,142 采样 / 2,973,268 输出比较**，最大差异0。8仓生成C/H/A2L，并用LCC编译后在host MEX harness实际运行 **20,086 采样 / 1,116,274 输出比较**，最大差异0。8仓有原生Simulink Coverage记录；C语句覆盖率未测量，不映射或伪填。

恢复已验证11仓HEAD/tree/所有heads和annotated tags/逐文件SHA/完整历史/clean/remote=0/无alternates，并从恢复副本再次运行模型。随后Resume重新校验实际仓库状态。11份候选包各含一个完整Git bundle、Part 7、补充、合同索引和输入绑定，共55文件，不包含标准答案/维护者观察或其他仓。

## 标准答案与证据边界

新组按Part 7完成143叶，**385/671**，无failed叶。每叶绑定具体源码/表格或Git refs并保留理由及限制；原源、恢复副本的确定性普查和已裁决参考重放一致。该重放证明输入/输出绑定，不是第二次独立语义评审。

| 叶 | 实际分布（分数:仓数） |
|---|---|
| 层次分解 | 3:11 |
| 复用与标准化 | 1:11 |
| 接口设计 | 1:11 |
| 数据流与信号路由 | 1:10, 2:1 |
| 单元测试 | 0:3, 1:8 |
| 命名规范 | 3:11 |
| 目录结构 | 3:1, 5:10 |
| 构建独立性 | 0:6, 1:1, 2:4 |
| 模型版本管理 | 3:11 |
| 版本独立性 | 3:11 |
| release代码分支策略 | 0:7, 8:4 |
| 设备特有 | 8:4, 10:7 |
| 参数管理 | 1:10, 5:1 |

有观测档位21/52。不为填档反推设计或修改标准分；无观测档位仍为unmeasured。重复调理逻辑、内部默认端口、局部拥挤走线、散落业务标定和缺少仓内测试的缺陷均保留真实标签。

平台/设备两叶严格按用户指定Part 7的分支命名代理取证：平台refs按R1/R2，TVC与其它业务按R3/R4。**所有平台/auto分支都是同一源码快照的合成路由，不证明已实现平台差异；116个tag都是同一commit的导出别名，不证明八个月历史。**分支名与语义版本记录不可冒充真实多平台验证。

## 尚未证明的范围

- 原始36仓逐仓画像/扫描器不可访问：业务权重、模型与配置对应关系、联合频率、内部算法/真实标定无法复原；只对可观察结构和明确模块规则建立映射。
- 新组仍共用构造器及大量调理结构，属于一个构造族。旧组知识参与重建，不能把新旧组切开当独立holdout；正式候选运行0。
- 峰值Inport/Outport/子系统为4135/1445/822，低于汇总5262/3032/1012；Bus族仅2仓，稀少arxml/epp/MemMap及ISO26262正式评审没有伪造。不能声称全部尾部分布及90多种sheet模板逐一覆盖。
- BTC未运行，HTML为BTC命名形态的真实Simulink/host结果；A2L未链接ECU地址；没有物理设备、SIL/PIL/HIL或生产安全认证。LCC实际编译执行通过，保留编译告警，不声称无告警。
- 外部工作电脑的评分平台/采集器不在本仓交付范围；提供保存XML普查、固定参考、候选评测和单仓恢复接口以便接入，未声称远端平台已部署。

## 入口与复现

在wrapper根执行：

```text
python verification/ne_reality.py validate
python verification/ne_reality.py restore --bundle-root D:/Project/Git.temp/matlab-benchmark/realism-20260910/delivery-final --destination <新的恢复目录> --output <恢复回执.json>
python verification/ne_reality.py replay --source-root <恢复目录> --output <参考重放.json>
python verification/ne_reality.py candidate --bundle-root D:/Project/Git.temp/matlab-benchmark/realism-20260910/delivery-final --id NEP-01 --output <不存在的单仓输入目录>
python verification/ne_reality.py evaluate --input <候选输出.json> --output <评测结果.json>
```

候选输入目录不得指向整个维护者wrapper；运行器负责真正的进程/网络/文件权限隔离。`evaluate`固定11仓×13叶，允许null弃答，保留分母，拒绝错HEAD/旧合同/非法档位，数字得分与人工证据正确性分开报告。当前`evaluation_current.py`和默认旧restore为兼容入口，仍对应原公开33仓。新组必须使用上述独立选择器。

精确身份见 `manifest.json`，143叶见 `STANDARD_SCORES.json`，定性/定量观察见 `OBSERVATIONS.json`，原生运行绑定见 `EXECUTION.json`，可复算形态差异见 `PROFILE_COMPARISON.json`。
