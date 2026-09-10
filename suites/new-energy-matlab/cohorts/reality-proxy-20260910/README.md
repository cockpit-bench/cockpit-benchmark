# 新能源现实代理 11 仓：v0.11.0 发布

六项具体审阅问题已完成修复、原生验证和参考重审，本版公开11个Vc*源码仓。公开集合共44仓：APP11、FW11、新能源22（旧联调11与现实代理11分别统计）。四个私有预留仓不纳入发布；原33源码历史和参考不变。

## 六项修复与证据

| 问题 | 当前结果 | 验证 |
|---|---|---|
| 1. 调理模板代替业务差异 | 模拟量、数字量、枚举走不同调理路径；新增/重建49个具名业务组件实例。NEP-10用真实库复用160个数字资格、16个组件监督实例 | 各仓业务输入有明确消费者；98条独立业务属性全部通过。NEP-10展开子系统从822降至373 |
| 2. 高温降额变负扭矩 | 降额限制在0..1，驾驶意图、方向、功率和稳定性仲裁分离 | 180°C降额=0；合法温度边界和最大制动输入检查通过；负降额变体被检出 |
| 3. 时间状态测试失效 | 增加未饱和积分、2/3次异常及恢复的独立断言，每组状态测试先复位 | 关闭积分、提前一次锁存的变体均失败；保留失败属性与原生输出 |
| 4. 预充多接受10 ms | 用整数采样计时；500 ms内（含边界）可完成，510 ms必须失败 | 490/500/510 ms独立检查通过；延后截止的变体被检出 |
| 5. 全double与错误单位 | 实际boolean/uint8/int16/uint16/uint32/single；原始计数与工程值显式区分，流量单位L/min | 编译端口、11份BIFF8接口表、参数类型以及8仓生成C接口对齐 |
| 6. 复制错误变更记录 | 按仓写入真实前后逻辑及逐信号增删/类型/单位/范围差异 | 11份变更表与Git父版本/InterfaceChanges.json一致；无跨仓TargetSoc单位修正声明 |

“六项修复完成”限上表具体缺陷，不表示已复原内部36仓全部分布。数据仅有扫描汇总、38模型/80配置混合统计及表格schema，缺逐仓联合画像、内部算法和真实标定。相同构造族、评分集中等限制继续公开。

## 每仓当前结果

| ID | 模块 / 业务 | 业务组件实例 | 展开子系统 | 根入/出 | 采样 | 业务属性 | 参考分 |
|---|---|---:|---:|---:|---:|---:|---:|
| NEP-01 | VcVcuInD：vehicle_input | 9 | 488 | 290/108 | 11948 | 4 | 42/61 |
| NEP-02 | VcVcuOutQM：actuator_output | 4 | 147 | 86/39 | 3562 | 5 | 40/61 |
| NEP-03 | VcVmcTrq：traction_torque | 4 | 114 | 62/26 | 2647 | 12 | 36/61 |
| NEP-04 | VcErcRgn：regeneration | 3 | 99 | 56/22 | 2251 | 6 | 34/61 |
| NEP-05 | VcDmcDrv：drive_mode | 1 | 82 | 50/22 | 1899 | 7 | 34/61 |
| NEP-06 | VcWrcWhl：wheel_traction | 3 | 109 | 62/27 | 2474 | 4 | 36/61 |
| NEP-07 | VcDeChg：charge_coordination | 2 | 114 | 68/28 | 2640 | 9 | 35/61 |
| NEP-08 | VcPvcThm：thermal_management | 3 | 190 | 110/47 | 4696 | 7 | 32/61 |
| NEP-09 | VcSfCPropR：propulsion_safety | 2 | 223 | 137/52 | 5493 | 12 | 40/61 |
| NEP-10 | VcSfDPropR：fault_supervision | 17 | 373 | 482/181 | 16433 | 25 | 43/61 |
| NEP-11 | VcScHv：high_voltage_sequence | 1 | 41 | 26/13 | 1270 | 7 | 37/61 |

NEP-01增加跨信号合理性；NEP-02分别控制驱动和辅助执行器；NEP-03分离驾驶需求、热保护、功率包络与仲裁；NEP-04协调再生与摩擦制动；NEP-05加入模式与换挡互锁；NEP-06按轴滑移和稳定性分配扭矩；NEP-07加入接入、电缆、电压/功率约束；NEP-08分离电池/电机PI与座舱执行器；NEP-09合理性和故障保持分离；NEP-10使用组件独立状态；NEP-11明确高压状态边界。可执行规则见各仓Documentation/BusinessBehavior.md。

## 执行与恢复

原源与全新恢复副本各完成R2023b MIL **55,313采样**；独立通道/诊断预期比较 **4,643,183**，输出范围检查 **5,227,373**，业务属性 **98**，均通过。两处原生运行的全部 **5,227,373输出值**逐项相同。
8仓真实生成C/H/A2L并用LCC-win64编译和执行host回放：**35,711采样、2,194,712输出比较，差异0**。LCC的fmodf兼容实现保留在scripts/lcc_float_compat.c；不是SIL/PIL/HIL。11仓均保留本轮模型Coverage；C语句覆盖未测。

4个故障变体全部被独立业务属性检出。通道、诊断、特定业务点及时间关系有独立预期，其余业务输出仅作为实测回放值；没有把生产业务函数原样复制成全输出gold。高模型覆盖率不能替代时间性质检查。
末次原生回放后仅修复14份review/tolerance表格的显示宽度与行高；逐单元格值相同，所有执行模型、标定、保护组件及C源码字节相同。最终源码另作全新完整历史恢复与143叶重放，不因格式变更冒称又运行了一轮MATLAB。

## 扫描对齐与限制

内部数字来自用户原文，不是本次重新扫描内部源码；本次实测分别列保存XML定义和原生展开实例。11个可执行模型加NEP-10一个真实库，不能把库误当主模型或第12个业务仓。

| 特征 | 原文汇总 | 本组当前 |
|---|---|---|
| 分组 | PROP33 / TVC3 | PROP10 / TVC1 |
| SLX、XLS | 36/36 | 11/11；XLS为OLE/BIFF8；另1库SLX |
| C/H/A2L | 约69% | 8/11；9仓有仓内测试报告，另2仓仅维护者准入测试 |
| MAT/LAB/P/MEX+TLC | 53%/56%/31%/22% | 6/6/3/2仓 |
| Inport/Outport/SubSystem中位 | 533/190/113 | 原生展开 568/210/114 |
| Inport/Outport/SubSystem最大 | 5262/3032/1012 | 原生展开 3317/1232/488 |

根输入类型：{'boolean': 717, 'uint16': 95, 'single': 486, 'int16': 111, 'uint32': 8, 'uint8': 12}；CAL参数类型：{'uint16': 190, 'single': 1196, 'int16': 222, 'uint32': 16, 'boolean': 226, 'uint8': 36}。候选仓.m文件0；业务函数真实存于SLX，维护者生成/验证脚本单独存放。
原文38模型/80配置不能当36仓的逐仓联合分布；不为贴合块数恢复无效复制。全部范围/比例为合成业务合同，不能称内部标定。single精度告警保留，数值比较和实际类型检查已覆盖。

## 参考裁决与评测边界

13叶×11仓，**409/671**，无failed，18叶值变化；Part 7及已批准构建补充逐字节不变。参考依据当前源码重新判定，不以修复必然提分为目标：NEP-01新增业务常量未外部化，参数管理5→1；NEP-10真实库使复用1→3、构建0→2；NEP-11新增仓内测试0→1；其余变化见score-revisions.json。
有观测档位21/52；按每叶固定众数猜测仍达 **123/143（86.0%）**，原值124/143。这只是同集合分布诊断，表明评分集中仍明显，不是模型成绩，也不证明泛化。
参考由知道构造和修复背景的维护者裁决，非盲gold。11仓和旧组存在共同构造知识，不能跨组假作独立holdout，正式候选运行0。候选仅获得单仓完整bundle与有效合同；运行器仍须负责真实文件/进程/网络隔离。

原116个标签保持旧基线，新增11个标签标识初始本地模型修复。9仓随后仅有表格排版提交，因此master为2或3提交。平台/auto分支仍保留旧快照；分支名代理评分不代表当前master已实现或验证多平台，不能称真实八个月生产发布历史。

原新能源联调组、APP、FW各自分母与合同保持；原evaluation_current.py和默认restore仍对应公开33仓，新组入口为verification/ne_reality.py。

## 公开入口与恢复

- NEP-01 [VcVcuInD](https://github.com/cockpit-bench/VcVcuInD) — `367b2ab786de8572c8b0d665de05b5b13983d4ae`
- NEP-02 [VcVcuOutQM](https://github.com/cockpit-bench/VcVcuOutQM) — `32d77f24db27d913aa0bfcdcc70dd15b463dfe00`
- NEP-03 [VcVmcTrq](https://github.com/cockpit-bench/VcVmcTrq) — `0902e6c52e3878edd5a1c7de4e2e2ea65ef73300`
- NEP-04 [VcErcRgn](https://github.com/cockpit-bench/VcErcRgn) — `c30baa42401b4086e57396213c07f7d0fd244099`
- NEP-05 [VcDmcDrv](https://github.com/cockpit-bench/VcDmcDrv) — `3a5f747d55331682a1ddadc49551f04236e3f958`
- NEP-06 [VcWrcWhl](https://github.com/cockpit-bench/VcWrcWhl) — `61084082b8d60f121303fef0a691b80916cd41dd`
- NEP-07 [VcDeChg](https://github.com/cockpit-bench/VcDeChg) — `e2fd73443c59459a560775405b486624b4b082cf`
- NEP-08 [VcPvcThm](https://github.com/cockpit-bench/VcPvcThm) — `a3946da6cca31d88979c55b6d18a64ea33225dbd`
- NEP-09 [VcSfCPropR](https://github.com/cockpit-bench/VcSfCPropR) — `3b60bb33258294e6b8c6d8ba531790af4c98617d`
- NEP-10 [VcSfDPropR](https://github.com/cockpit-bench/VcSfDPropR) — `dc1dd984ecc2152bb03c7aa8f13dd83f856f6e89`
- NEP-11 [VcScHv](https://github.com/cockpit-bench/VcScHv) — `27f0538f1d71375e12b02efd470b3e35586fda52`

```text
python verification/ne_reality.py restore --destination <全新目录> --output <回执.json>
python verification/ne_reality.py replay --source-root <恢复目录> --output <重放.json>
python verification/ne_reality.py candidate --source-root <恢复目录> --id NEP-01 --output <全新单仓目录>
```

重复restore对已完成仓重新验证，不重置用户修改。离线既有bundle可继续通过--bundle-root使用；在线恢复不依赖本机source-map。默认restore.ps1与evaluation_current.py继续对应原33仓。

原始执行附件：[下载](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.11.0/ne-reality-native-inputs-v0.11.0.zip)，2393479字节，SHA256 `c66e279b2e97e0e356a397b4d6622d814a538302ff93e35596f9be7b88aa49aa`。附件为维护者原始输入/记录，不向候选提供。EXECUTION.json绑定的记录可直接核对；发布本身没有新增MATLAB、host C或设备执行，沿用已绑定修复验证。

身份与逐叶参考见manifest.json、STANDARD_SCORES.json、OBSERVATIONS.json；分布见PROFILE_COMPARISON.json。无物理设备、BTC、ECU、SIL/PIL/HIL、C语句覆盖或ISO26262认证。
