# 六组66仓扩建与复核（v0.12.0）

新增架构中心、人工智能中心、智能驾驶中心各11仓，与原APP、FW、新能源MATLAB同级，技术只作为仓内元数据。新增33仓含10个MATLAB/Simulink工程、13个native C/C++工程、7个Android应用/库、1个Python构建工具和2个集成仓。

|报告组|仓库|参考分|叶数|
|---|---:|---:|---:|
|APP|11|142/440|88|
|FW|11|194/572|121|
|New Energy MATLAB|11|409/671|143|
|架构中心|11|205/436|142|
|人工智能中心|11|312/616|187|
|智能驾驶中心|11|329/596|182|

各组分别报告，不合并原始分数。新增511叶，整体863叶；均为知情维护者源码参考。候选模型正式执行0，不是盲gold或独立holdout。

## 真实扫描对照

六份所给扫描中有95个有效逐仓spec（架构40、AI12、智驾43）。本次按每仓联合结构选择33个原型，保留单模型/模型库、脚本/表格/字典标定、MDL/SLX、native生成代码/平台库、Android应用/组件库、Python构建和真实Git集成等差异。逐仓公开匿名对照在各中心profiles目录，保留原文SHA和spec行号；原始模块名与完整本地映射不随公开包上传。

修正了模型层次过平、Model Reference图文字重叠、工作区Git-clean但CRLF字节漂移、规则引擎缺少混合JNI外壳、集成包传递静态库不完整等具体问题。新增仓共跟踪1094个目标文件，不重复计算18个Gitlink子树。模型有68个生产根/组件模型及6个仓内UT harness；库链接和引用均实际加载。

实际规模明显小于内部生产仓；扫描文件总数可能含生成物、二进制和工具链，部分源码扫描有2500文件上限，模型统计也可能仅采样。零test_case_count与无效HTML百分比未当成无测试/真实覆盖。未补造扫描原仓的大量历史分支、tag、空默认HEAD、专有依赖或生产标定。交付是声明差异的可执行有界代理，不是完整生产分布复刻。

## 合同与评分复核

新增中心使用[软件17叶/56分、模型12叶/36分合同](../suites/center-contracts/README.md)。修正原提示重复维度、SOLID满分3与0..4档矛盾，以及不完整/错位的档位文本；模型不混用旧新能源13维合同。五个SOLID分别说明评审对象，无继承关系不自动满分。

主审纠正IDC-03：构建工具输入的外部源码不是工具自身实现依赖，构建0→3；IDC-03/IDC-10对依赖版本的校验不能替代自身API语义版本，API各3→1。模型重复项补充实际两份组件的文件、SLX成员及SID；数值不因补定位改变。仓外验证不计入仓内测试分，模型coverage不冒充C语句coverage。其余已确认的质量差异保留，未按目标分布补档。

终审修复AIC-09的重复技能补偿和逆序回滚：按每步独立上下文及实际成功顺序恢复；同一39项独立回放从旧版14项恢复断言失败变为全部通过，另79项新增仓内补偿检查通过。AIC-04/AIC-07/AIC-09/IDC-02已有的自身协议手工版本证据各补记API 0→1；文档标签、运行时检查及自动兼容机制分别说明，不混作同一能力。

原APP、FW、NEP的源码HEAD/tree/refs、有效合同和352叶数值保持。旧构建独立性争议仍保持暂停；本次新合同不回溯套用。四个私有预留仓没有加入公开集合。

## 实际执行与可恢复性

- 10个模型每仓640样本，共6400样本/27520输出比较，通过独立方程对照及编译类型检查。6仓自带UT、4仓两套实际参数配置均运行；ARC-10/IDC-09实际ERT输出再经GCC主机回放，各640样本，共5120比较零差异。
- 7个Android仓构建成功；14个仓内JVM单测、4个最终APK的45个UI检查、3个AAR的35个宿主检查通过。另AIC-07实际Windows JNI和Android API35/x86_64 JNI运行通过；arm64仅构建打包。
- 13个native仓在原源和全新完整恢复副本实际编译/执行通过；3个C仓的生成器与策略输入明确保留，未冒充Simulink生成。
- ARC-07三个场景连接8或9个组件模型，26次组件仿真/5226组件时间采样/22512输出通道采样；31项图/接口合同检查通过。IDC-03的12项仓内测试、城市/高速两配置实际构建及缓存/包成员SHA检查通过；IDC-10两产品8个场景56帧和14个业务/负例检查通过。
- 恢复检查完整Git历史、HEAD/tree/全部登记refs、全部目标文件SHA、18个真实Gitlink、clean、零remote与无alternates。恢复和参考重放只证明身份/绑定/算术，不替代上述实际执行和源码语义复核。

首次发布前，10仓的来源说明在完整可达历史中做了匿名化；原始构造历史完整留存本地。33仓的业务代码、模型、标定、测试和二进制blob逐提交保持，仅来源文档及由其身份变化派生的依赖锁定记录调整。原执行HEAD/tree与公开HEAD/tree之间的字节等价记录随单仓raw提供，不能把匿名化过程称作一次新原生执行。IDC-03和IDC-10另外在公开副本实际复验构建/运行。

本地准入190项回归全部通过、无跳过；新增33仓及18个子模块完整历史恢复通过，源码与恢复副本的511叶参考重放一致。33份单仓源码输入共165文件，33份单仓raw导出共791文件，全部清单/字节校验通过。原33仓核对现存完整恢复身份及公开refs，本轮没有重新匿名下载其全部历史。

本轮没有物理设备、ECU、SIL/PIL/HIL、BTC、C语句覆盖或认证结论。共同构造/依赖关系按传递闭包保守连接，新33仓不作为独立留出集。

## 新增逐仓参考

|ID|中心|源码仓|分数|合同|
|---|---|---|---:|---|
|ARC-01|架构中心|[arch-actuator-target](https://github.com/cockpit-bench/arch-actuator-target)|12/36|12叶|
|ARC-02|架构中心|[arch-brake-stability](https://github.com/cockpit-bench/arch-brake-stability)|22/36|12叶|
|ARC-03|架构中心|[arch-motion-coordinator](https://github.com/cockpit-bench/arch-motion-coordinator)|15/36|12叶|
|ARC-04|架构中心|[arch-signal-supervisor](https://github.com/cockpit-bench/arch-signal-supervisor)|14/36|12叶|
|ARC-05|架构中心|[arch-crosswind-control](https://github.com/cockpit-bench/arch-crosswind-control)|11/36|12叶|
|ARC-06|架构中心|[arch-vehicle-state](https://github.com/cockpit-bench/arch-vehicle-state)|13/36|12叶|
|ARC-07|架构中心|[arch-motion-integration](https://github.com/cockpit-bench/arch-motion-integration)|31/56|17叶|
|ARC-08|架构中心|[arch-steering-redundancy](https://github.com/cockpit-bench/arch-steering-redundancy)|22/36|12叶|
|ARC-09|架构中心|[arch-suspension-monitor](https://github.com/cockpit-bench/arch-suspension-monitor)|20/36|12叶|
|ARC-10|架构中心|[arch-vehicle-safety](https://github.com/cockpit-bench/arch-vehicle-safety)|15/36|12叶|
|ARC-11|架构中心|[arch-safety-runtime](https://github.com/cockpit-bench/arch-safety-runtime)|30/56|17叶|
|AIC-01|人工智能中心|[ai-service-hall](https://github.com/cockpit-bench/ai-service-hall)|34/56|17叶|
|AIC-02|人工智能中心|[ai-hall-data](https://github.com/cockpit-bench/ai-hall-data)|24/56|17叶|
|AIC-03|人工智能中心|[ai-compact-hall](https://github.com/cockpit-bench/ai-compact-hall)|14/56|17叶|
|AIC-04|人工智能中心|[ai-data-collector](https://github.com/cockpit-bench/ai-data-collector)|32/56|17叶|
|AIC-05|人工智能中心|[ai-data-exchange](https://github.com/cockpit-bench/ai-data-exchange)|30/56|17叶|
|AIC-06|人工智能中心|[ai-hall-widgets](https://github.com/cockpit-bench/ai-hall-widgets)|29/56|17叶|
|AIC-07|人工智能中心|[ai-rule-runtime](https://github.com/cockpit-bench/ai-rule-runtime)|40/56|17叶|
|AIC-08|人工智能中心|[ai-health-card](https://github.com/cockpit-bench/ai-health-card)|23/56|17叶|
|AIC-09|人工智能中心|[ai-agent-dispatch](https://github.com/cockpit-bench/ai-agent-dispatch)|38/56|17叶|
|AIC-10|人工智能中心|[ai-vehicle-agent](https://github.com/cockpit-bench/ai-vehicle-agent)|33/56|17叶|
|AIC-11|人工智能中心|[ai-personal-hall](https://github.com/cockpit-bench/ai-personal-hall)|15/56|17叶|
|IDC-01|智能驾驶中心|[drive-parking-arbitration](https://github.com/cockpit-bench/drive-parking-arbitration)|30/56|17叶|
|IDC-02|智能驾驶中心|[drive-mcu-platform](https://github.com/cockpit-bench/drive-mcu-platform)|23/56|17叶|
|IDC-03|智能驾驶中心|[drive-build-orchestrator](https://github.com/cockpit-bench/drive-build-orchestrator)|39/56|17叶|
|IDC-04|智能驾驶中心|[drive-calibration](https://github.com/cockpit-bench/drive-calibration)|29/56|17叶|
|IDC-05|智能驾驶中心|[drive-sensor-fusion](https://github.com/cockpit-bench/drive-sensor-fusion)|30/56|17叶|
|IDC-06|智能驾驶中心|[drive-route-planner](https://github.com/cockpit-bench/drive-route-planner)|34/56|17叶|
|IDC-07|智能驾驶中心|[drive-ultrasonic-perception](https://github.com/cockpit-bench/drive-ultrasonic-perception)|28/56|17叶|
|IDC-08|智能驾驶中心|[drive-world-model](https://github.com/cockpit-bench/drive-world-model)|37/56|17叶|
|IDC-09|智能驾驶中心|[drive-parking-state](https://github.com/cockpit-bench/drive-parking-state)|21/36|12叶|
|IDC-10|智能驾驶中心|[drive-algorithm-integration](https://github.com/cockpit-bench/drive-algorithm-integration)|27/56|17叶|
|IDC-11|智能驾驶中心|[drive-adaptive-platform](https://github.com/cockpit-bench/drive-adaptive-platform)|31/56|17叶|

各叶理由、限制、源码定位与SHA见相应中心STANDARD_SCORES.json及evidence目录。原始执行输入附件为center-native-inputs-v0.12.0.zip；候选单仓导出只含登记refs+HEAD，排除未登记stash/notes等对象。维护者完整材料不等同于候选输入。
