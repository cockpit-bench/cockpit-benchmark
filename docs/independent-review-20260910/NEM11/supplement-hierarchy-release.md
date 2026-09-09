# NEM11 层次与发布策略补充复核

绑定HEAD：`d9cf0bae322d41e7d829c02636ce343d638797e1`。首稿review.json/review.md/static-inventory.json保持原字节，补充结论仅在本文件和同名JSON中给出。

层次最终仍为3；发布策略由首稿0修正为10，依据合同已接受的分支策略近似，未增加任何执行结论。

## 层次分母与粒度

直接块数包含端口/路由/容器，属于粒度事实，不作生产规模。根层按功能域；第二层按单个极值故障状态；第三层按单个等级的防抖适配；第四层是共享算法定义。顶层7至22块无巨型或失控粒度，BPC三输出属于同一电池状态估计职责。默认Subsystem系列确实损害名称自解释性，但通过父路径、Fault/DebouncedFlt接口及DMax/DMin消费者可以明确单一职责，不以命名缺陷直接否定职责存在。重复封装影响reuse，不自动使职责多重。

普通自建子系统21个，加实际被引用的同仓Debouncer定义去重1个，共22个。22个职责均明确且单一，22/22=100%。Stateflow Chart单独审阅；其system_27.xml中15个工具生成接口/适配块不作为手工生产层次或分母。库顶层容器、标准库内部和未实例化定义不加分母。

|层级|实际对象数|每对象直接块数|
|---|---|---|
|1 功能域|5|10、13、22、7、12|
|2 单极值故障状态|4，另有1个Chart逻辑单元|18、18、18、18；Chart表示的15块排除|
|3 单等级防抖适配|12|均7|
|4 共享Debouncer实例|12实例，去重1定义|均20（含接口/路由）|

直接块数含端口、路由与容器，用于审阅粒度；不是有效生产逻辑块规模。所有实例保留可追踪SID，但共享定义只进入分母一次。

## 逐定义完整清单

|层|SID/模型XML|路径|直接块数|明确且单一职责|
|---|---|---|---|---|
|1|8 / simulink/systems/system_8.xml|BatteryContactorController/BATTERY_FAULT_HANDLING - BFH|10|聚合四种监控故障和接触器故障，输出总故障等级|
|1|20 / simulink/systems/system_20.xml|BatteryContactorController/BATTERY_OPERATION_MODE - BM|13|依据观测/故障/SOC和连接等待参数执行电池接触器运行模式控制|
|1|35 / simulink/systems/system_35.xml|BatteryContactorController/BATTERY_PARAMETER_CALCULATION - BPC|22|由电池包电流和电压更新电荷、能量及SOC三个一致状态量|
|1|60 / simulink/systems/system_60.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM|7|提取单体电压极值并输出欠压/过压故障等级|
|2|62 / simulink/systems/system_62.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Max_Cell_Voltage_Fault_State|18|过压阈值比较、防抖后合成该物理量的故障等级|
|3|77 / simulink/systems/system_77.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Max_Cell_Voltage_Fault_State/Subsystem|7|针对CVM_DMaxVCellMaxCutoff_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|85 / simulink/systems/system_85.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Max_Cell_Voltage_Fault_State/Subsystem1|7|针对CVM_DMaxVCellMaxDrtd_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|93 / simulink/systems/system_93.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Max_Cell_Voltage_Fault_State/Subsystem2|7|针对CVM_DMaxVCellMaxWarn_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|2|105 / simulink/systems/system_105.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Min_Cell_Voltage_Fault_State|18|欠压阈值比较、防抖后合成该物理量的故障等级|
|3|120 / simulink/systems/system_120.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Min_Cell_Voltage_Fault_State/Subsystem|7|针对CVM_DMaxVCellMinCutoff_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|128 / simulink/systems/system_128.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Min_Cell_Voltage_Fault_State/Subsystem1|7|针对CVM_DMaxVCellMinDrtd_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|136 / simulink/systems/system_136.xml|BatteryContactorController/CELL_VOLTAGE_MONITORING - CVM/Min_Cell_Voltage_Fault_State/Subsystem2|7|针对CVM_DMaxVCellMinWarn_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|1|170 / simulink/systems/system_170.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM|12|提取模块温度极值、执行高低温故障检测并输出平均温度|
|2|175 / simulink/systems/system_175.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Max_Module_Temperature_Fault_State|18|高温阈值比较、防抖后合成该物理量的故障等级|
|3|190 / simulink/systems/system_190.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Max_Module_Temperature_Fault_State/Subsystem|7|针对MTM_DMaxTMdulMaxCutoff_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|198 / simulink/systems/system_198.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Max_Module_Temperature_Fault_State/Subsystem1|7|针对MTM_DMaxTMdulMaxDrtd_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|206 / simulink/systems/system_206.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Max_Module_Temperature_Fault_State/Subsystem2|7|针对MTM_DMaxTMdulMaxWarn_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|2|218 / simulink/systems/system_218.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Min_Module_Temperature_Fault_State|18|低温阈值比较、防抖后合成该物理量的故障等级|
|3|233 / simulink/systems/system_233.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Min_Module_Temperature_Fault_State/Subsystem|7|针对MTM_DMaxTMdulMinCutoff_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|241 / simulink/systems/system_241.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Min_Module_Temperature_Fault_State/Subsystem1|7|针对MTM_DMaxTMdulMinDrtd_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|3|249 / simulink/systems/system_249.xml|BatteryContactorController/MODULE_TEMPERATURE_MONITORING - MTM/Min_Module_Temperature_Fault_State/Subsystem2|7|针对MTM_DMaxTMdulMinWarn_P对应的单一故障等级，连接使能/复位/上限/下限并输出该通道防抖结果|
|4|49 / MiniBMS/BMSLib.slx!simulink/blockdiagram.xml|BMSLib/Debouncer|20|对一个布尔状态做上下计数防抖，支持使能/复位/Dmax/Dmin并输出锁存防抖状态|

12个共享库实例SID：83, 91, 99, 126, 134, 142, 196, 204, 212, 239, 247, 255。其完整父路径见JSON linked_instances。

默认Subsystem系列缺乏名称自解释性，应影响命名叶。其父路径、Fault/DebouncedFlt接口和独立DMax/DMin变量明确指定物理故障及等级，所以仍可判职责单一。此判断依据连线/消费者，未把默认名自动当有意义名称。

## 发布策略修正

撤回首稿0：README明确Release0.1.0和One mainline，不能称无计划。按合同允许的分支命名近似和统一主线/平台分支/车型分支/无计划策略分类，以唯一main、无车型/平台token及统一配置入口判统一主线10。

得10依据合同已经接受的策略近似；未证明两个指定车辆平台有独立配置画像或实际跨平台执行。普通校准脚本本身不能证明这些更强事实，但合同未要求新增跨平台执行门槛。缺实际执行不能降为无计划0。

将合同“跨平台”严格要求具名双平台配置时会出现信息缺口，但不能回填0；本次遵循合同明示允许的分支策略近似，精确结论为10。

- git show-ref唯一main且README策略一致
- README.md L9: Release 0.1.0, 2026-09-09. One mainline; no model/platform token in branch names.
- VERSION L1 0.1.0
- initialize_controller.m L2-10按统一参数脚本加载根模型工作区
- MiniBMSVariables.m为统一业务参数配置，run_acceptance.m L26-31对同一模型改变防抖配置

首稿错误在于将“未证明具名多平台配置”直接映射到“无计划0”，忽视了已声明统一主线及合同允许的近似。源码的统一校准入口能证明配置集中应用，但不会额外证明实际多平台应用。
