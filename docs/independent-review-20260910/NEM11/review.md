# NEM11 独立只读评分复核

HEAD：`d9cf0bae322d41e7d829c02636ce343d638797e1`。首次与末次git status均clean。

只读指定源码和合同；未读wrapper/标准分/维护者执行资料/其它结果。逻辑输入限制，非OS隔离。

## 13叶建议

|叶|分数/状态|理由|
|---|---|---|
|hierarchy|3|五个顶层分别承担故障聚合、运行模式、电池状态计算、电压监控、温度监控。22个自建子系统均有单一可识别职责；四个阈值组同为18块，十二个防抖包装同为7块，层级粒度一致。|
|reuse|1|防抖核心通过同仓库链接复用，但外围Fault/Ena/Rst/Dmax/Dmin及常量包装重复十二份；三级故障选择组合在四套高低压/温度监控中重复。不能以12个库引用直接判无重复。|
|interface|0|根端口显式且输入有类型单位；但影响公开输出的Goto/From/DataStore在同一合同范围内，符合隐式通信0档。|
|dataflow|0|大量未命名信号、跨子系统故障使能跳转和数据存储反馈。GotoTag语义清楚但不能替代所有信号命名及明确路由。|
|unit_test|unknown / failed|测试静态有效，但没有绑定HEAD的原生结果、通过率和decision coverage；按指令保持unknown。|
|naming|1|顶层、端口、状态有意义，但十二包装为Subsystem系列，大量Constant/Gain默认名且存在真实误名，未达基本准确统一。|
|directory|1|Demo和MiniBMS部分分类，根目录模型/创建/初始化/测试脚本平铺；MiniBMS混放生产库、参数、环境模型。|
|build_independence|3|依赖闭包为本仓根模型、BMSLib和参数脚本，库再引用Simulink标准库；未发现仓外业务依赖。未运行构建。|
|model_version|2|README含0.1.0/日期/相对上游主要变更与接口增量，Git有历史对比；未见完整连续逐项信号变更体系。|
|version_independence|3|独立版本0.1.0三段式，文件间一致。|
|release_branches|0|可见refs仅main；虽声明单主线，但无车型/平台分支及多平台配置差异化证据。单main本身不支持10。|
|device_specificity|10|按合同接受的分支名近似，main无车型/平台token，得10；不是实际跨平台验证。|
|parameter_management|unknown / failed|排除3/5：有未变量化业务阈值和初值及重复校准副本。不能选0：大量关键参数已变量化集中。不能无条件选1：合同要求多数散落，客观唯一业务量清点不支持多数；属于大部分集中、部分未集中中间情形空档。|

完整每叶证据位于 review.json。

## 参数管理精确裁决

排除3/5：有未变量化业务阈值和初值及重复校准副本。不能选0：大量关键参数已变量化集中。不能无条件选1：合同要求多数散落，客观唯一业务量清点不支持多数；属于大部分集中、部分未集中中间情形空档。

不支持现合同中的精确整数：3/5被具体反例排除，0与集中化事实不符，1的“多数”不能擅自解释为“只要部分”。建议明确中间情形规则后再评分；本报告不改合同。

按业务角色及独立校准变量识别，不按字面值或XML次数。24个Dmax/Dmin独立调节，保留24量；派生总能量算应管理量但非独立可调量。若排除派生量则42个集中独立量+6个未集中独立量=48。5个集中量有硬编码副本不重复增加分母。此数量说明多数散落不成立，不作评分比例公式。

出现次数与唯一量分开：列出的生产XML共22个数字出现、17个字段。Stateflow为13个阈值字面量/12个迁移标签；DataStore初值6个数字/2字段；根输入维度2个数字/2字段；active FixedStep1个数字/1字段。它们对应6个新增独立未集中业务量及5个既有中央业务量的未关联副本，不是22个独立参数。

## 未集中量与重复副本

|业务量|值|位置|性质及事实|
|---|---|---|---|
|最低放电SOC|3 %|chart_119.xml SSID44/58/71/73|新独立未集中量；44启用>3，58/71/73是同一跨层停止<3迁移的多个XML片段|
|充电SOC上限|98.5 %|chart_119.xml SSID44/57/68/74|新独立未集中量；44开始<98.5，57/68/74停止>=98.5，XML片段不作多个参数|
|连接失败电压比例|0.98|chart_119.xml SSID50|新独立未集中量；VBus<0.98*VBatPack，执行顺序1|
|连接成功电压比例|0.95|chart_119.xml SSID48/62/64|新独立未集中量；VBus>=0.95*VBatPack，同一跨层过渡SUB/SUPER片段，顺序2；与失败条件有重叠，优先级影响实际结果|
|断开成功电压比例|0.2|chart_119.xml SSID92|新独立未集中量；VBus<0.2*VBatPack|
|初始SOC|0.985|system_35.xml SID39/40|新独立未集中量；初始条件与充电停止阈值是不同业务角色；默认相等不能未经设计声明合并|
|总电荷容量|48 Ah|system_35.xml SID39/40|集中量的未关联副本；InitialValue=48*0.985与48*3*4.22*0.985未引用BPC_BattTotalCharge_P|
|电芯数|3|system_35.xml与system_root.xml SID40及根SID1|集中量的未关联副本；初始能量及PortDimensions不引用NrCells_C；属于结构配置，不是绘图几何|
|最高单体电压|4.22 V|system_35.xml SID40|集中量的未关联副本；初始能量不引用CVM_VCellMaxCutoffTh_P|
|计算步长|0.1 s|configSet0.xml FixedStep|集中量的未关联副本；configSetInfo明确active；create_controller.m L11也写0.1，不引用BMS_TiSample_C；inactive configSet1不计|
|温度传感器个数|3|system_root.xml SID4|集中量的未关联副本；PortDimensions=3与create_controller.m L15写死；温度平均分母用NrTMdulSnsr_C|

chart XML前缀为 BatteryContactorController.slx!simulink/stateflow/；system前缀为同模型的simulink/systems/；config前缀为simulink/。

## 全量脚本变量、类型及消费者

完整精确工作区值和数组位于static-inventory.json。本表逐一列出全部54个变量，不以脚本文件存在代替被使用。

|变量及源码行|表达式/type|生产消费者|分类|
|---|---|---|---|
|NrTMdulSnsr_C L7|uint8(3) / uint8|simulink/systems/system_170.xml SID173 Value|business_parameter|
|NrCells_C L10|uint8(3) / uint8|脚本间接：BPC_BattTotalEnergy_P|business_parameter|
|Em L13|完整数组见JSON/源码 / float64|无生产消费者|retained_environment_not_production|
|CapLUTBp L14|完整数组见JSON/源码 / float64|无生产消费者|retained_environment_not_production|
|RInt L15|完整数组见JSON/源码 / float64|无生产消费者|retained_environment_not_production|
|BattTempBp L16|[243.1 253.1 263.1 273.1 283.1 298.1 313.1]*0.1 / float64|无生产消费者|retained_environment_not_production|
|CapSOCBp L17|[0 0.2 0.4 0.6 0.8 1] / float64|无生产消费者|retained_environment_not_production|
|BMS_TiSample_C L22|single(0.1) / float32|simulink/systems/system_35.xml SID49 Gain; simulink/systems/system_35.xml SID50 Gain|business_parameter|
|BMS_ModeEnaFltChk L25|[0 100 110 111 115 120 130 140 200 211 220 230 255] / float64|simulink/systems/system_root.xml SID59 BreakpointsForDimension1|status_enumeration_or_mapping|
|BMS_EnaFltSts L26|[1 1 1 1 1 1 1 1 0 0 0 0 0] / float64|simulink/systems/system_root.xml SID59 Table|status_enumeration_or_mapping|
|CVM_VCellMinCutoffTh_P L30|single(3.26) / float32|simulink/systems/system_105.xml SID107 Value|business_parameter|
|CVM_VCellMinDrtdTh_P L31|single(3) / float32|simulink/systems/system_105.xml SID108 Value|business_parameter|
|CVM_VCellMinWarnTh_P L32|single(2.8) / float32|simulink/systems/system_105.xml SID109 Value|business_parameter|
|CVM_DMaxVCellMinCutoff_P L35|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_120.xml SID123 Value|business_parameter|
|CVM_DMinVCellMinCutoff_P L36|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_120.xml SID124 Value|business_parameter|
|CVM_DMaxVCellMinDrtd_P L37|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_128.xml SID131 Value|business_parameter|
|CVM_DMinVCellMinDrtd_P L38|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_128.xml SID132 Value|business_parameter|
|CVM_DMaxVCellMinWarn_P L39|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_136.xml SID139 Value|business_parameter|
|CVM_DMinVCellMinWarn_P L40|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_136.xml SID140 Value|business_parameter|
|CVM_VCellMaxCutoffTh_P L43|single(4.22) / float32|simulink/systems/system_62.xml SID64 Value|business_parameter|
|CVM_VCellMaxDrtdTh_P L44|single(4.15) / float32|simulink/systems/system_62.xml SID65 Value|business_parameter|
|CVM_VCellMaxWarnTh_P L45|single(4.1) / float32|simulink/systems/system_62.xml SID66 Value|business_parameter|
|CVM_DMaxVCellMaxCutoff_P L48|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_77.xml SID80 Value|business_parameter|
|CVM_DMinVCellMaxCutoff_P L49|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_77.xml SID81 Value|business_parameter|
|CVM_DMaxVCellMaxDrtd_P L50|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_85.xml SID88 Value|business_parameter|
|CVM_DMinVCellMaxDrtd_P L51|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_85.xml SID89 Value|business_parameter|
|CVM_DMaxVCellMaxWarn_P L52|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_93.xml SID96 Value|business_parameter|
|CVM_DMinVCellMaxWarn_P L53|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_93.xml SID97 Value|business_parameter|
|MTM_TMdulMinCutoffTh_P L58|single(-20) / float32|simulink/systems/system_218.xml SID220 Value|business_parameter|
|MTM_TMdulMinDrtdTh_P L59|single(0) / float32|simulink/systems/system_218.xml SID221 Value|business_parameter|
|MTM_TMdulMinWarnTh_P L60|single(5) / float32|simulink/systems/system_218.xml SID222 Value|business_parameter|
|MTM_DMaxTMdulMinCutoff_P L63|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_233.xml SID236 Value|business_parameter|
|MTM_DMinTMdulMinCutoff_P L64|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_233.xml SID237 Value|business_parameter|
|MTM_DMaxTMdulMinDrtd_P L65|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_241.xml SID244 Value|business_parameter|
|MTM_DMinTMdulMinDrtd_P L66|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_241.xml SID245 Value|business_parameter|
|MTM_DMaxTMdulMinWarn_P L67|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_249.xml SID252 Value|business_parameter|
|MTM_DMinTMdulMinWarn_P L68|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_249.xml SID253 Value|business_parameter|
|MTM_TMdulMaxCutoffTh_P L71|single(55) / float32|simulink/systems/system_175.xml SID177 Value|business_parameter|
|MTM_TMdulMaxDrtdTh_P L72|single(52.5) / float32|simulink/systems/system_175.xml SID178 Value|business_parameter|
|MTM_TMdulMaxWarnTh_P L73|single(50) / float32|simulink/systems/system_175.xml SID179 Value|business_parameter|
|MTM_DMaxTMdulMaxCutoff_P L76|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_190.xml SID193 Value|business_parameter|
|MTM_DMinTMdulMaxCutoff_P L77|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_190.xml SID194 Value|business_parameter|
|MTM_DMaxTMdulMaxDrtd_P L78|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_198.xml SID201 Value|business_parameter|
|MTM_DMinTMdulMaxDrtd_P L79|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_198.xml SID202 Value|business_parameter|
|MTM_DMaxTMdulMaxWarn_P L80|int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_206.xml SID209 Value|business_parameter|
|MTM_DMinTMdulMaxWarn_P L81|-int16(0.5/BMS_TiSample_C) / int16|simulink/systems/system_206.xml SID210 Value|business_parameter|
|BM_TiCtctrCnct_P L86|single(1)/BMS_TiSample_C / float32|simulink/systems/system_20.xml SID28 Value; simulink/stateflow/chart_119.xml SSID46 labelString|business_parameter|
|BM_TiCtctrDCnct_P L87|single(1)/BMS_TiSample_C / float32|simulink/systems/system_20.xml SID29 Value; simulink/stateflow/chart_119.xml SSID78 labelString|business_parameter|
|BPC_BattTotalCharge_P L92|single(48) / float32|simulink/systems/system_35.xml SID38 Value; simulink/systems/system_35.xml SID45 UpperSaturationLimit|business_parameter|
|BPC_BattTotalEnergy_P L95|BPC_BattTotalCharge_P * single(NrCells_C) * CVM_VCellMaxCutoffTh_P / float32|simulink/systems/system_35.xml SID46 UpperSaturationLimit|business_parameter|
|NrCutoff_C L99|uint8(3) / uint8|simulink/systems/system_root.xml SID149 Value; simulink/systems/system_62.xml SID67 Value; simulink/systems/system_105.xml SID110 Value; simulink/systems/system_175.xml SID180 Value; simulink/systems/system_218.xml SID223 Value|status_enumeration_or_mapping|
|NrDrtd_C L100|uint8(2) / uint8|simulink/systems/system_62.xml SID68 Value; simulink/systems/system_105.xml SID111 Value; simulink/systems/system_175.xml SID181 Value; simulink/systems/system_218.xml SID224 Value|status_enumeration_or_mapping|
|NrWarn_C L101|uint8(1) / uint8|simulink/systems/system_62.xml SID69 Value; simulink/systems/system_105.xml SID112 Value; simulink/systems/system_175.xml SID182 Value; simulink/systems/system_218.xml SID225 Value|status_enumeration_or_mapping|
|NrNoFlt_C L102|uint8(0) / uint8|simulink/systems/system_62.xml SID70 Value; simulink/systems/system_105.xml SID113 Value; simulink/systems/system_175.xml SID183 Value; simulink/systems/system_218.xml SID226 Value|status_enumeration_or_mapping|

## 算法常量、枚举和排除项

- 固定单位换算：3600秒每小时、100比例转百分比。数值算法常量完整清点；固定单位换算不是可调校准，不和电压比例阈值混为一类。 system_35.xml SID49/50=-BMS_TiSample_C/3600，SID51 Gain100
- 表示域不变量：SOC 0..100、电量/能量下界0。合法SOC表示域和非负不变量，不作为新增独立可调业务量。 system_35.xml Saturate54 [0,100]；Integrator45/46 LowerSaturationLimit0
- 算法结构及逻辑值：故障管线DelayLength1、UnitDelay一步、Debouncer计数±1、reset0、布尔0/1/true/false。计数单位/复位/布尔真值/离散结构；不把出现次数当业务参数。可调防抖时间由Dmax/Dmin管理。 system_8.xml SID15；root SID265；BMSLib blockdiagram.xml Constant39经bddefaults取1→Sum37/38；Constant42=0；UnitDelay44 IC默认0；S-R47 initial_condition0；12包装Rst=0
- 状态枚举及使能表：BM_OperMode=100/110/111/115/120/130/140/200/211/220/230/255、故障等级0/1/2/3、BMS_ModeEnaFltChk含0与状态号、BMS_EnaFltSts映射0/1。状态不是阈值。两个使能表+四个故障枚举已集中，有消费者；不纳入43个业务校准量。 chart_119 state labelString；MiniBMSVariables.m L25-26/99-102
- 排除绘图几何及标识：Position、labelPosition、intersection、dataLimits、fontSize、ZOrder、SSID、SID。排版/标识数字，不计业务参数。 
- 排除环境校准：Em、CapLUTBp、RInt、BattTempBp、CapSOCBp。生产根及库无直接/间接消费者；原值/shape/type保存在static-inventory.json，不虚增生产参数管理。 MiniBMSVariables.m L13-17
- 排除测试配置：run_acceptance.m的时间/温度/电压/预期状态号、StopTime10。测试场景/仿真停止配置，不算生产控制业务参数。 
- 排除泄漏工作区变量：k=58。创建脚本循环变量写入模型工作区，无生产消费者，非业务量。 

## 各叶证据

- hierarchy：system_root.xml SID8/20/35/60/170；system_62/105/175/218.xml；system_77/85/93/120/128/136/190/198/206/233/241/249.xml；BMSLib blockdiagram.xml SID49
- reuse：system_77.xml SID78-84与system_85.xml SID86-92；system_62与175同18块模式；BMSLib blockdiagram.xml SID49
- interface：system_root.xml SID150-169与输出266-273；system_35.xml SID39-44/48/52；INTERFACES.md L5-21
- dataflow：From22/Goto12/DataStoreMemory2/Read2/Write2；236个存储Line仅4个显式Name，含Stateflow生成接口表示，非有效生产块计数；system_35.xml read41/42→integrator46/45→write43/44
- unit_test：run_acceptance.m L6-31六场景12个断言；L32-43仅结果写出程序，不是实际报告
- naming：system_62.xml SID63 CVM_VCellMin实际输入max；system_60.xml SID104与system_170.xml SID217名称Min1但Function=max；system_35.xml SID38名BMS_TiProc_C2却为总电荷；chart_119 state89 DICCONNECT拼写
- directory：production-models.json L2-9；根三个m脚本；MiniBMS三文件
- build_independence：initialize_controller.m L2-10；全部Reference仅BMSLib/Debouncer、simulink_extras/Flip Flops/S-R Flip-Flop、simulink/Discontinuities/Saturation Dynamic
- model_version：README.md L3/9；INTERFACES.md L1/5-21；git log的三个提交
- version_independence：VERSION L1；README.md L9；INTERFACES.md L1
- release_branches：git show-ref仅refs/heads/main；README.md L9；未读取远端
- device_specificity：git show-ref仅refs/heads/main；README.md L9
- parameter_management：chart_119.xml SSID44/50/48/62/64/57/68/74/58/71/73/92；system_35.xml SID39/40；active configSet0 FixedStep0.1；MiniBMSVariables.m L7-102

## 验证边界

- 未执行MATLAB加载/update/MIL/coverage/codegen/编译/SIL/PIL/HIL。
- 分支评分基于指定本地可见refs和源码说明；当前远端状态unknown。
- 工作区通过scipy解读SLX内MAT-v5载荷，非MATLAB执行。
- 未声称阈值物理安全性；静态集中性不能代替业务准确性。
