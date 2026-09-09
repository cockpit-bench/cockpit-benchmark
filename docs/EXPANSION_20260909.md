# 首批六仓扩建：本地主线结果

2026-09-09。用户批准后在 wrapper `main` 正常前向实施。**APP、FW、新能源 MATLAB 各新增 2 仓，当前分别为 11 仓**。MATLAB 是技术，新能源是业务归属；以后其它中心的 MATLAB 不能并入本类型。新增源码仍为本地状态，未 push、未创建公开仓或 Release。

| 类型 | 新仓及画像 | 核心业务和真实工程组合 | 取证分数 | 生产规模 |
|---|---|---|---:|---:|
| APP | APP-21 `scene-coordinator`（A） | Touring/City 两变体；场景选择、能力查询、灯光/HVAC执行；跨仓固定 AAR；单 app 模块 | 13/40 | 122 LOC，small |
| APP | APP-22 `drive-event-recorder`（E） | 相机采集、完整视频确认、SQLite事件索引、回放和文档导出；app + video模块 | 13/40 | 387 LOC，small |
| FW | FW-21 `vehicle-capability-service`（B） | Manager/AIDL、独立服务进程、签名权限、两种实际单位映射、状态持久化和订阅 | 24/52 | 279 LOC，small |
| FW | FW-22 `vehicle-message-service`（F） | Binder调用者隔离、持久消息队列、离线重试、协议1/2、本地HTTP确认与幂等 | 25/52 | 321 LOC，small |
| 新能源 MATLAB | NEM-10 `battery-energy-calibration`（C） | 父模型/能量核算引用模型，接口/标定/用例表实际被执行入口读取，生成父子模型C/H | 55/61 | 362有效逻辑块，medium |
| 新能源 MATLAB | NEM-11 `battery-contactor-control`（D） | 从MiniBMS提取控制器；接触器状态机、12个Debouncer库实例、脚本参数、保留隐式通信 | 36/61 | 128有效逻辑块，small |

Android LOC按真实生产 Java/AIDL 去注释和空行计算，不含debug验收、示例客户端、Gradle、AAR或生成代码。MATLAB按同仓有效定义去重，接口/路由/容器不计；内置库作为依赖块，未展开凑规模。Stateflow状态/转移另外保留在模型库存中，不重复加到逻辑块规模。两个APP分数相同但各叶构成和业务不同；分数不是设计目标，也不证明样本独立性。

## 扫描依据与实际偏差

可访问依据是用户提供的 `Benchmark虚拟仓生成指导_原始Markdown.md` 与 `Matlab_Simulink虚拟仓生成指导_最新版_原文.md`，并非原始逐仓扫描包。以下行号对应保留原文。组合属于模拟设计假设，不能宣称内部某一真实仓就是此组合，也不能推断其出现频率。

| 画像 | 指导线索 | 已实现证据 | 边界或偏差 |
|---|---|---|---|
| A/B | Android 61–77业务线、247–328模块/SDK、478–529 API/IPC | A `app/build.gradle`消费校验SHA的AAR；B `VehicleManager`→AIDL→`CapabilityService`→两adapter；实际跨进程断言 | 自有Android业务实现，未复用COVESA领域代码；COVESA仅是取得Gradle wrapper的已有工程来源。公开SDK探索被独立小服务实现替代，避免把无关平台整体纳入 |
| A/B | Android 332–384分支/车型形态 | 同一主线的Touring/City真实能力和单位差异 | 没有伪造SOP历史或长期发布策略；两个模拟车型并不等于两个真实Android平台 |
| E | Android 71影像、267–285相机模块 | `CameraCapture`、`VideoStore`、`RecorderActivity`及两种原生验收入口 | Camera1旧API保留并影响平台评分；没有麦克风、停车录像、物理行车记录仪或云端上传 |
| F | Android 96–97消息/框架、279–281消息依赖 | `MessageManager`、`MessageService`、`MessageStore`、`LoopbackTransport` | 本地127.0.0.1接收端，绑定期间调度；不是真实云、开机常驻或车联网全链路 |
| C | MATLAB 101–155工程目录、617–633表字段、423–471模型引用、729–807生成/测试 | `Interfaces.xls`为真实BIFF8；`Calibration.xlsx` 201参数；`Cases.xlsx` 1128样本；加载函数检查消费者与端口；真实Model Reference | 全部68公开端口在同一范围审阅；引用子模型只有一个生产消费者；没有为了复用分数增加副本 |
| D | MATLAB 423–471库/路由、571–579类型、783–807测试 | 控制器根、`BMSLib/Debouncer`、Stateflow、`INTERFACES.md`和脚本参数 | Stateflow及紧凑治理是基于MiniBMS素材的额外设计假设；轻量接口表采用Markdown，未把C的工作簿治理机械复制给D |

四个Android新样本规模较小，说明它们补充的是可运行业务/依赖组合，并未重现内部总体规模分布。数据字典、保护模型、MEX、A2L符号链和长期车型维护仍未覆盖；本轮没有创建占位材料。

## 实际执行

- A/B：两个APP变体分别通过35项断言。覆盖跨进程Binder、permille/8bit灯光与decikelvin HVAC、能力缺失、越界/NaN、双订阅与注销、实际部分写入失败、服务进程死亡/重新绑定、持久状态恢复及不重放命令。另一无权限进程对两FW服务绑定均被拒绝。
- E：14项受控MediaCodec验收，真实MP4编码/解码、索引、逐字节导出、损坏/存储/未授权分支；9项模拟器相机验收，录制约3.2秒及中断丢弃。另在录制期间实际撤销CAMERA权限，Android终止进程；重启后未完成文件清理，两个已完成视频保留。UI文件与录制样片留在本地执行目录。
- F：一个原生Instrumentation业务场景通过19项断言，包括离线待发、真实服务进程kill/restart后的SQLite恢复、真实HTTP往返、两种协议、重复/冲突消息、过期、错误确认后的重试及接收端单次效果。五个定义的跨组件交互边覆盖5/5；这是交互边代理，不是分支、语句或decision覆盖。
- C：R2023b正常MIL比较1128×13个输出；标定扰动另外运行3×1128样本，131个输出发生预期变化，错误消费者映射被拒绝，恢复后逐位相同。父/引用模型生成13个C/H文件，生成字节包含在最终源码树中；未执行C编译或SIL。
- D：R2023b正常MIL运行6×101=606样本，12项行为断言通过。温度故障出现时间由3.9秒变为4.4秒，验证库参数实际影响；充/放电、接触器超时、故障恢复和短暂温升分别断言。上游Data Store读写顺序警告保留。

Android只在API 35模拟器运行；没有物理设备、VHAL或实车结论。两MATLAB新仓未收集decision coverage，故单元测试叶均只得1。D的低压cutoff/warning标定顺序、隐式通信和大量默认命名按实际来源保留，不能凭MIL通过称为生产标定验收。

FW-21本仓没有集成测试入口，所以该叶为0；外部APP的测试记录仍准确证明其被测业务。FW-22具有仓内测试和版本绑定代理证据，按合同得3。权限隔离测试、场景断言与服务实现来自相互绑定的源码版本，未把测试探针加入生产接口。

## 评分、谱系和恢复

每个类型的 `manifest.json`、`STANDARD_SCORES.json`、`SCORECARD.md` 和 `additions.json` 是当前入口；`evidence/`保存新仓的逐叶理由、具体源码行/模型元素、生产库存、原生记录SHA和独立规则输入。64个新叶完成维护者源码审阅和第二遍证据/相邻档位核对；规则使用另一套现有合同代码复算，未读取标准答案。源库存重复提取相同。**这些仍共享显式语义观察，不是盲审或第二独立评审者的语义结论。**

A/B依赖相同SDK，必须同family；四个新Android实现共享本轮构造来源。C继承ML-04来源并与原MATLAB构造族有关；D继承MiniBMS完整MIT历史。所有新仓同时带有本轮共同构造组。未来切分必须对来源族、依赖组和构造组取传递闭包，不能把相关仓划到训练和holdout两侧。此次没有候选模型实验，也没有独立holdout准入。

六仓从独立本地源经 `git clone --no-local` 恢复到全新目录，核验完整历史、final HEAD/tree、所有heads/tags、clean、无alternates及remote=0。恢复只证明Git材料完整，不替代构建或仿真。原27仓实物另作只读检查，HEAD/refs未变，47个原始标准/合同/oracle/MATLAB证据文件逐字节保留。

当前各类型结果：APP 140/440（88叶）、FW 194/572（121叶）、新能源MATLAB 429/671（143叶）；不相加。各类型9仓已公开、2仓仅本地。旧22 pending与全部已发布tag保持原样。正常发布须另获具体新源码目的地授权；在此之前 `--require-publishable` 应失败。
