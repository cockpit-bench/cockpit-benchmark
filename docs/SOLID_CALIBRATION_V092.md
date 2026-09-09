# v0.9.2 非 LSP SOLID 后续源码校准

本轮覆盖剩余五仓的 20 个 SRP/OCP/ISP/DIP 叶；此前 v0.9.1 的 16 叶记录保持历史。
两批合计覆盖 36 个非 LSP 叶，但不是盲评、独立模型实验或全仓缺陷比例估计。
本轮另复核 APP-14 编译独立性。数值变化共 12 叶；Android 255/828，由输入逐叶求和。
源码/refs 与合同不变；MATLAB 分数及 v0.9.0 附件不变，既有 ML-09 补锚保留。

[完整 SOLID 裁决](solid-calibration-v092.json)；[编译裁决](compilation-calibration-v092.json)；
[v0.9.1 历史记录](SOLID_CALIBRATION.md)。

## FW-03 solid_principle.single_responsibility: 2 → 2

基本按Profile和服务职责拆分；跨Profile适配器策略及OPP服务仍有集中职责混杂，尚不能判良好或优秀。
生命周期由ProfileService统一，音频/电话/消息等具有独立服务；GattService把扫描、广播、周期扫描交给不同Manager；AVRCP媒体列表、元数据和浏览回调由MediaPlayerList负责。反面并非单纯AdapterService体量大：适配器除启停还亲自枚举Profile并制定连接策略，PhonePolicy已有类似职责；OPP服务同时处理后台传输状态/数据库同步与设备选择UI的触发和全局发送状态。两处是独立职责面。它们仍有可识别的围绕适配器/传输的边界，不能把所有事件协调当上帝类。
为何不降：0要求严重、明显设计缺陷；1要求多处不合理职责分布。主要协议Profile并未揉成一个核心，GATT Manager、媒体列表、OBEX传输及持久化边界均真实被生产使用。当前最强残余是服务入口附近的两个集中热点，不把每个同类Binder方法重复记为独立违反。
为何不升：3/4要求更稳定的变更责任隔离；AdapterService连接策略与PhonePolicy部分重叠，OPP UI/存储协调仍在服务内，不能凭包名和Profile层级提升。
范围限制：JNI/native逐方法语义、底层蓝牙协议栈（仓外）；HFP/HFPClient、HID、PAN、LE Audio、SAP、HearingAid内部状态机仅在主要服务调用处覆盖；未声称逐个完成；lib/mapapi Provider全部抽象方法和外部应用消费者未逐个追踪；测试未执行；不评价LSP、CI/API/平台等其他叶

## FW-03 solid_principle.open_closed: 2 → 1

具有生命周期/回调扩展点，但Profile连接策略和MAP消息支持两条独立业务链仍要求修改核心条件，构成多处扩展传播。
Config+ProfileService使基础服务启停可以按配置扩展，ObexServerSockets对不同Profile的连接验证通过接口调用，均为正证。负面是扩展一个可自动连接Profile必须同时进入AdapterService及PhonePolicy的具体分支；支持一个新的MAP消息类别不能只加Provider：消息列表的Cursor/类型映射、会话列表和getMessage分派都显式枚举种类。Adapter/PhonePolicy是同一Profile连接族，不重复计成两个独立面；MAP消息适配是第二个独立面。类型枚举本身不是扣分依据，扣分来自上层业务链对新实现的修改传播。
为何不降：不能给0：ProfileService/Config和OBEX接口确实支持生产实现替换，未见全仓所有变化均被单一核心锁死；没有证明严重不可维护或无有效扩展机制。
为何不升：2要求基本遵循而残余少量；Profile连接与消息内容两条主要业务链都有重复核心修改点，不能仅用生命周期扩展点覆盖。3/4更缺少对这些变化原因的隔离。
范围限制：JNI/native逐方法语义、底层蓝牙协议栈（仓外）；HFP/HFPClient、HID、PAN、LE Audio、SAP、HearingAid内部状态机仅在主要服务调用处覆盖；未声称逐个完成；lib/mapapi Provider全部抽象方法和外部应用消费者未逐个追踪；测试未执行；不评价LSP、CI/API/平台等其他叶

## FW-03 solid_principle.interface_segregation: 3 → 2

媒体、OBEX和Profile生命周期契约多数按客户端拆分；OPP双向会话强加单向确认能力及扫描Manager对整个GattService的依赖仍有改进点。
MediaPlayerList分开更新/目录/根回调，AVRCP消费者各取所需；IObexConnectionHandler只负责连接接受/失败，MAP实际实现。反面最清楚的是BluetoothOppObexSession.unblock只在入站用户确认有意义，出站实现被迫空实现，Transfer消费者文档和控制路径明确是入站场景。这是ISP能力混合证据，本轮不重评LSP。另一个独立点是ScanManager为了扫描注销/统计直接依赖整个GattService并访问mScannerMap，可用窄扫描宿主接口。不是按Binder方法数量认定胖接口。
为何不降：主要接口没有普遍强制音频/消息/扫描消费者依赖其他Profile能力；媒体、连接接受与生命周期接口真实窄化。已证实的OPP会话能力错配与GATT内部宿主接口不足是集中边界缺口，不是全仓客户端普遍被迫实现无关业务。
为何不升：3/4不能忽略已证实的无关能力强制及扫描对完整服务/可变内部结构的依赖。
范围限制：JNI/native逐方法语义、底层蓝牙协议栈（仓外）；HFP/HFPClient、HID、PAN、LE Audio、SAP、HearingAid内部状态机仅在主要服务调用处覆盖；未声称逐个完成；lib/mapapi Provider全部抽象方法和外部应用消费者未逐个追踪；测试未执行；不评价LSP、CI/API/平台等其他叶

## FW-03 solid_principle.dependency_inversion: 1 → 1

若干窄回调和存储接口为正证，但Profile政策、音频启动、MAP服务及GATT宿主存在跨独立职责的具体实现/全局状态依赖。
ServiceFactory确实可作替换缝隙，但返回A2dpService/HeadsetService等具体类且内部查静态服务；PhonePolicy业务直接消费这些类型及AdapterService数据库。A2DP启动强制获取AdapterService和NativeInterface单例；MAP也通过AdapterService全局对象取得DatabaseManager。GATT扫描层向具体上层服务反向取共享可变状态。以上不是任意new对象扣分，而是高层策略与依赖实现/获取方式绑定，或下层与上层实现反向依赖。正面是OBEX接收连接由通用网络实现调用业务接口，媒体更新由回调反转到AVRCP；它们不能覆盖其他主要域。
为何不降：存在真实控制反转和可识别模块边界，不是全仓严重无抽象的紧耦合；OBEX和媒体跨层通知不需引用其业务消费者实现。
为何不升：2不能只依据存在Factory/Binder/Interface：策略、音频、消息以及扫描宿主等主要职责都能找到真实控制链中的具体依赖，超出单一局部边界。3/4更无依据。
范围限制：JNI/native逐方法语义、底层蓝牙协议栈（仓外）；HFP/HFPClient、HID、PAN、LE Audio、SAP、HearingAid内部状态机仅在主要服务调用处覆盖；未声称逐个完成；lib/mapapi Provider全部抽象方法和外部应用消费者未逐个追踪；测试未执行；不评价LSP、CI/API/平台等其他叶

## FW-08 solid_principle.single_responsibility: 2 → 2

主要职责真实拆为网络排序、Tethering、统计、Ethernet、mDNS及Nearby协作者；OEM偏好已有内部工厂分责，局部改进主要是Tethering政策协调与具体传输适配同居。
ConnectivityService把网络排序交给NetworkRanker，OEM偏好转换也由11975行OemNetworkRequestFactory内部类承担，不能把该内部工厂当不存在或声称尚无政策翻译器。NsdService分别组装发现/广告/socket组件，Tethering通过依赖对象取得offload、upstream、entitlement等组件，NetworkStats具有独立查询Session。更稳健的局部反例在Tethering：统一启停分派之外，同类直接实现WiFi热点操作与Bluetooth异步特例，协调政策和传输适配有不同变更原因。这个集中热点支持2分，不以服务体量或合法事件协调否定全仓职责结构。
为何不降：0/1不能由核心服务行数或方法数推出。网络排序、OEM偏好内部工厂、统计、mDNS发现/广告、Ethernet和offload均有实际分责。当前最强反例集中于Tethering协调/适配边界，不证明全仓多处职责分布失效。
为何不升：3/4尚受Tethering传输适配与协调政策同居限制；已有Dependencies和多个Manager不等于所有变化原因已隔离。
范围限制：netd/BPF内核侧、bpf_progs、JNI及Clat内部算法未逐函数重审；IpSec、全部网络统计归档/计费、完整FastPair/Presence流程未深入；Cronet源码实现/仓外NetworkStack、HAL服务端和设备环境未执行或核对完整闭包；测试目录只用于识别排除范围；没有新构建、Android/设备运行或LSP裁决

## FW-08 solid_principle.open_closed: 2 → 1

网络Agent、HAL和回调提供真实扩展能力，但OEM网络偏好、Tethering传输、Nearby发现后端三个独立主要业务面仍有核心扩展修改链。
正证包括NetworkAgent通用注册和Ethernet真实生产子类、IOffloadHal两个生产实现及工厂选择。负证不是任何switch都违规：OEM偏好新组合须改ConnectivityService请求翻译；新增共享网络传输须改Tethering.enableTetheringInternal及各特殊回调处理；Nearby新增发现后端须改DiscoveryProviderManager的固定字段/构造和BLE/CHRE选择。各问题在同一接口族内的多个分支只记一个机制，以上三种变化原因独立。BroadcastProviderManager固定协议版本序列化分派只作已查范围，不单凭它再加一个违规面。
为何不降：0不成立：Agent注册、HAL适配和回调是真实生产扩展边界，不能说所有业务扩展都要破坏核心；未验证严重功能设计缺陷。
为何不升：2的少量改进不能由未发现更多问题推断。当前已核实三个独立主要变化面都修改其高层控制核心，不能用单一HAL/Agent正证概括全仓基本闭合；3/4更无支持。
范围限制：netd/BPF内核侧、bpf_progs、JNI及Clat内部算法未逐函数重审；IpSec、全部网络统计归档/计费、完整FastPair/Presence流程未深入；Cronet源码实现/仓外NetworkStack、HAL服务端和设备环境未执行或核对完整闭包；测试目录只用于识别排除范围；没有新构建、Android/设备运行或LSP裁决

## FW-08 solid_principle.interface_segregation: 2 → 2

多个生产接口按职责充分收窄，但诊断客户端仍被迫依赖完整连接管理Binder能力，尚未达到全仓良好。
NetworkRanker.Scoreable只要评分和能力；EthernetNetworkAgent.Callbacks只通知网络不再需要；mDNS广告回调只负责成功/失败；NetworkStats通过独立INetworkStatsSession查询。正证分别来自排序、Ethernet、mDNS及统计，不是同一回调族的重复。最强反面是ConnectivityDiagnosticsManager只注册/注销诊断，但构造参数及成员要求整个IConnectivityManager，该契约还包含网络状态/代理/keepalive/OEM偏好/防火墙等无关能力。SocketKeepalive也消费同一宽Binder族，不重复算第二种根问题。
为何不降：不能给1/0：多个独立主职责的接口明确收窄、生产消费者可核对；现有强反例主要是共享连接Binder这一家族，而非接口普遍混合。未从方法数量推导普遍违反。
为何不升：3/4不能只看Manager外观：诊断客户端的依赖类型仍包含大量无关管理能力。HAL版本警告能力的显式检查只说明能力差异被管理，不抵消该宽IPC问题。
范围限制：netd/BPF内核侧、bpf_progs、JNI及Clat内部算法未逐函数重审；IpSec、全部网络统计归档/计费、完整FastPair/Presence流程未深入；Cronet源码实现/仓外NetworkStack、HAL服务端和设备环境未执行或核对完整闭包；测试目录只用于识别排除范围；没有新构建、Android/设备运行或LSP裁决

## FW-08 solid_principle.dependency_inversion: 2 → 2

主要跨边界依赖通过Binder、HAL契约、Scoreable和回调隔离，依赖创建也有明确替换缝隙；Nearby的Provider政策仍固定具体后端。
ConnectivityService构造接收IDnsResolver、INetd和Dependencies，核心依赖并非所有都自取全局实例；offload通过IOffloadHal调用AIDL/HIDL；排序依赖Scoreable；Ethernet/mDNS以窄回调反转事件。NearbyService也通过DiscoveryManager消费新旧发现实现。最强反面位于该抽象之下：DiscoveryProviderManager仍持有具体BLE/CHRE类型并在政策执行中调用具体后端可用性，测试构造器也接受具体类型。工厂创建普通协作者并不自动算违反；ConnectivityService直接创建NetworkRanker/DnsManager说明替换缝隙不完全，但其单一职责不等于严重依赖倒置。
为何不降：不能仅以new/具体类个数判1：主干网络系统服务通过稳定Binder抽象、硬件卸载通过真实多实现接口、排序输入/广告/Ethernet事件通过窄契约；最直接的不合理后端绑定集中在Nearby发现选择这一业务面。它的多处调用不是多个独立全仓违反。
为何不升：3/4不成立：Nearby关键Provider选择仍依赖具体后端；core的创建缝隙也不完全。存在Dependencies不自动证明依赖倒置优秀。
范围限制：netd/BPF内核侧、bpf_progs、JNI及Clat内部算法未逐函数重审；IpSec、全部网络统计归档/计费、完整FastPair/Presence流程未深入；Cronet源码实现/仓外NetworkStack、HAL服务端和设备环境未执行或核对完整闭包；测试目录只用于识别排除范围；没有新构建、Android/设备运行或LSP裁决

## FW-14 solid_principle.single_responsibility: 2 → 1

电源与用户两个独立业务面存在实质职责混合，符合“多处违反，设计不合理”；不依类长度计分。
先以实际职责划分：音频协调并委托 ducking/muting；属性 Binder 与 HAL 转换分离；乘员服务管理用户/座位/显示拓扑；电源协调 VHAL 状态转换。反向追踪发现电源服务还自行拥有网络状态持久化与进程筛选/强停政策；用户生命周期服务自行拥有具体 Picker 的可见任务识别/显示政策。电源的两种策略算一个主业务面，UserPicker 算另一面。网络存储格式或显示呈现规则变化会改变生命周期核心，超出仅调度已封装能力。
为何不降：不降0：音频、属性、乘员、用户、电源边界仍可识别，有专用辅助对象、HAL 转换和生命周期协议；未证明系统已为严重不可维护单体。
为何不升：不升2：网络存储/恢复政策与 Picker 呈现政策分别嵌入两个核心服务，并非单一便利函数；1分来自多个证实的修改原因冲突，不推断未审文件。3/4 更不成立。
范围限制：watchdog/telemetry全部内部策略；native cpp/JNI内部设计；experimental/package apps完整源码；service-builtin全部系统适配；蓝牙/EVS/VMS/诊断/媒体服务逐方法语义；所有AIDL/公开接口消费者穷举

## FW-14 solid_principle.open_closed: 3 → 2

主扩展面已有真实策略、配置和监听；新增 HAL 业务族/本地电源执行组件仍需修改处理核心的内部装配，基本遵循，尚不足良好。
按扩展类型核对：OEM ducking 由专用 AIDL 提供；属性 HAL 基于配置/抽象服务泛型路由；用户通过过滤监听扩展；乘员拓扑和电源策略支持数据扩展。覆盖四个主职责面且有真实消费者。缺口集中在“引入新底层本地实现种类”：VehicleHal 将路由与固定服务清单共置，PowerComponentHandler 的私有工厂固定 mediator 类型。这是不同业务面的同类限制。2分评价这一分层结构，不宣称全仓只有两处问题；不因任意 enum/schema switch 或装配 new 自动扣分。
为何不降：不降1/0：OEM、通用属性路由、过滤监听、乘员/电源配置是真实生产扩展；不能说每次常规扩展都改核心分支。
为何不升：不升3/4：跨 HAL 业务族与本地组件行为扩展仍进入核心处理类，主扩展轴尚未形成一致注册边界；未审面不能帮助抬分。
范围限制：watchdog/telemetry全部内部策略；native cpp/JNI内部设计；experimental/package apps完整源码；service-builtin全部系统适配；蓝牙/EVS/VMS/诊断/媒体服务逐方法语义；所有AIDL/公开接口消费者穷举

## FW-14 solid_principle.interface_segregation: 3 → 1

音频能力总接口与系统总 facade 在两个独立业务面造成无关能力依赖，符合多处违反；同时存在真实窄接口。
同时看契约/实现/客户端：AudioControlWrapper 汇集 focus/gain/fade/duck/mute，V1 被迫实现不支持能力的方法，muting 客户端仅使用 muting/能力检查。多个 HAL 版本只算一个音频面。独立的第二面：位置缓存仅需现有 IOInterface.getSystemCarDir，却依赖聚合显示/时钟/活动管理/系统状态的具体 SystemInterface。窄接口已存在，消费者未使用。反证是生命周期 onEvent、属性回调和 OEM ducking 保持窄接口，不能把全部接口判胖。
为何不降：不降0：有效窄回调和生命周期契约存在；能力保护使“不支持功能”不等于必然运行故障，未证明全面严重接口失配。
为何不升：不升2：两独立边界均证实客户端依赖不用能力，音频还强迫早期实现承担无此能力的方法；局部窄接口不能抹去多处违反。
范围限制：watchdog/telemetry全部内部策略；native cpp/JNI内部设计；experimental/package apps完整源码；service-builtin全部系统适配；蓝牙/EVS/VMS/诊断/媒体服务逐方法语义；所有AIDL/公开接口消费者穷举

## FW-14 solid_principle.dependency_inversion: 2 → 1

音频、用户乘员、属性多个高层链依赖具体服务/全局查找；抽象存在但未覆盖主要业务依赖，符合多处违反。
排除正常装配：ICarImpl 用 CarSystemService 调度，SystemInterface 持有窄系统接口，OEM proxy 依赖 AIDL，均为正向。业务内 CarDucking 全局查找具体 OEM proxy；CarUserService 构造接收具体 HAL/UX/包/乘员服务，Picker 再查具体 ActivityService；乘员 init 查具体属性/用户服务；属性 Binder 直接调用 PropertyHalService。至少音频、用户乘员、属性三个主链暴露实现类型，位置目录 lookup 是补充；不把所有 new/Android API 当违反。Builder/Deps 提供测试替换但不自动反转这些生产依赖。
为何不降：不降0：HAL/音频 AIDL、生命周期和系统接口提供有效隔离，未证明高层整体无法分离。
为何不升：不升2：证实的具体依赖跨音频、用户乘员、属性主链，超出孤立装配点；局部 mock/Builder/Deps 不改变这些生产依赖方向。
范围限制：watchdog/telemetry全部内部策略；native cpp/JNI内部设计；experimental/package apps完整源码；service-builtin全部系统适配；蓝牙/EVS/VMS/诊断/媒体服务逐方法语义；所有AIDL/公开接口消费者穷举

## FW-15 solid_principle.single_responsibility: 2 → 2

基本遵循。呼叫日志、音频、传感器、焦点和过滤执行都有独立生产责任。CallsManager的跨呼叫状态协调本身合法，不能因类长扣分；但核心还承担过滤图产品组装、音频对象装配和错误界面启动，PhoneAccountRegistrar合并账号选择、语音订阅同步与XML机制。问题以协调器和账号存储附近集中，尚不支持整个设计不合理。
基本遵循。呼叫日志、音频、传感器、焦点和过滤执行都有独立生产责任。CallsManager的跨呼叫状态协调本身合法，不能因类长扣分；但核心还承担过滤图产品组装、音频对象装配和错误界面启动，PhoneAccountRegistrar合并账号选择、语音订阅同步与XML机制。问题以协调器和账号存储附近集中，尚不支持整个设计不合理。
为何不降：日志规则在CallLogManager、传感器在ProximitySensorManager、过滤执行在独立图，核心有实质委派。账号存储和订阅同步也围绕账号一致性，不能自动当无关业务。
为何不升：可变产品组装、呈现和持久化机制尚未与核心隔离，不满足良好/优秀。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-15 solid_principle.open_closed: 3 → 1

音频路由中央映射和过滤图超时清理分别绑定具体端点/过滤实现，形成两个独立核心扩展传播面，OCP为多处违反的1；不是按switch数量或组合根new计分。
InCallService按协议发现，过滤器正常执行通过CallFilter多态调度，都是有效扩展边界。但performFiltering的超时清理按CallScreeningServiceFilter具体类型强转解绑，CallFilter缺少资源终止契约；新增需清理资源的过滤器需改通用图。独立音频路由的事件/状态映射仍中央列举端点。两条运行期责任的扩展限制不能仅归为装配代码的局部便利。
为何不降：正常过滤执行与InCallService发现有真实多态/协议扩展，不是全面严重封闭；不把固定设备状态机本身当运行缺陷。
为何不升：过滤生命周期和音频路由是两个独立生产责任，两处均须改核心控制；现有仅一种需解绑过滤器不能证明该生命周期开放。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-15 solid_principle.interface_segregation: 3 → 2

基本遵循。焦点以CallFocus窄视图工作，号码适配/过滤回调各有专门边界。CallsManagerListener和Call.Listener却混合音频、视频、会议、RTT和诊断；仅关心移除事件的传感器也依赖全集。两套监听属于同一通话事件族，不把大量默认空方法或多个观察者当成独立多业务面违反。
基本遵循。焦点以CallFocus窄视图工作，号码适配/过滤回调各有专门边界。CallsManagerListener和Call.Listener却混合音频、视频、会议、RTT和诊断；仅关心移除事件的传感器也依赖全集。两套监听属于同一通话事件族，不把大量默认空方法或多个观察者当成独立多业务面违反。
为何不降：焦点/号码/过滤有真实窄边界；可选默认回调是合法观察语义，不证明被迫执行无关操作。宽监听问题不能夸为全仓多种胖接口。
为何不升：关键事件订阅仍依赖全集，不能认定良好/优秀分隔。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-15 solid_principle.dependency_inversion: 2 → 2

基本遵循。CallsManager接收号码/时钟/通知抽象和工厂，焦点消费Requester/CallFocus，过滤调度消费CallFilter。未倒置处集中在高层接入与组装：核心选择具体过滤策略，CallIntentProcessor选具体广播器并解释其返回类型。普通Android API及组合根new不自动扣分；反例是可变实现选择进入生产政策路径。
基本遵循。CallsManager接收号码/时钟/通知抽象和工厂，焦点消费Requester/CallFocus，过滤调度消费CallFilter。未倒置处集中在高层接入与组装：核心选择具体过滤策略，CallIntentProcessor选具体广播器并解释其返回类型。普通Android API及组合根new不自动扣分；反例是可变实现选择进入生产政策路径。
为何不降：多个主链路真实消费抽象而非只有测试注入；焦点不依赖完整Call，号码匹配走适配器。没有把new数量当缺陷数。
为何不升：部分接入决策仍绑定具体实现，未统一隔离到组合边界。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-18 solid_principle.single_responsibility: 2 → 1

多处违反。GsmCdmaPhone除门面委派外亲自实现IMS/CS及紧急/WPS路由、语音信箱SIM/SharedPreferences/运营商回退；SubscriptionController同时直接映射/查询数据库并分配modem radio capability、刷新数据tracker和广播。电话政策与持久化、订阅仓储与radio政策是两个独立聚合，不靠类长判分。
多处违反。GsmCdmaPhone除门面委派外亲自实现IMS/CS及紧急/WPS路由、语音信箱SIM/SharedPreferences/运营商回退；SubscriptionController同时直接映射/查询数据库并分配modem radio capability、刷新数据tracker和广播。电话政策与持久化、订阅仓储与radio政策是两个独立聚合，不靠类长判分。
为何不降：CallTracker、DcTracker、UICC/电话本、SMS和NitzStateMachine已有独立所有者；没有全部主职责无法分开或严重失效证据，不给0。
为何不升：两个核心业务面均有可单独变化的机制/政策耦合，超过少量局部改进。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-18 solid_principle.open_closed: 2 → 1

多处违反。GsmCdmaPhone语音路由按GSM/CDMA/IMS及运营商条件选择，独立短信发送/重试又枚举IMS/GSM/CDMA并直接调用两种静态PDU编码。新增承载或制式政策需进入两个调度器；SMSDispatcher多态未封住重编码选择。配置工厂和IDataService是有效正向边界，阻止0分但不能覆盖核心反例。
多处违反。GsmCdmaPhone语音路由按GSM/CDMA/IMS及运营商条件选择，独立短信发送/重试又枚举IMS/GSM/CDMA并直接调用两种静态PDU编码。新增承载或制式政策需进入两个调度器；SMSDispatcher多态未封住重编码选择。配置工厂和IDataService是有效正向边界，阻止0分但不能覆盖核心反例。
为何不降：TelephonyComponentFactory.inject可选替换工厂，数据服务按包绑定IDataService；不是所有功能扩展都需改核心。
为何不升：语音与短信是独立主责任，均内嵌制式政策，不能压缩成一个局部工厂问题。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-18 solid_principle.interface_segregation: 1 → 1

多处违反。CommandsInterface合并SIM PIN、拨号和数据；SIM状态与数据服务消费者均依赖全集。独立上层Phone/PhoneInternalInterface再聚合通话、数据、身份及电话本，电话本为IccRecords/文件处理器依赖完整Phone。无线命令层与高层电话能力是两层契约，不把同一CommandsInterface的两个消费者重复算多种胖接口。NITZ/IDataService表明仍有专门边界。
多处违反。CommandsInterface合并SIM PIN、拨号和数据；SIM状态与数据服务消费者均依赖全集。独立上层Phone/PhoneInternalInterface再聚合通话、数据、身份及电话本，电话本为IccRecords/文件处理器依赖完整Phone。无线命令层与高层电话能力是两层契约，不把同一CommandsInterface的两个消费者重复算多种胖接口。NITZ/IDataService表明仍有专门边界。
为何不降：网络时间和数据提供者有窄契约；宽接口只证明依赖负担，不证明误调用、运行故障或所有边界严重失效。
为何不升：无线命令面和上层Phone面均有生产消费者持有无关能力，超过单一接口族局部问题。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

## FW-18 solid_principle.dependency_inversion: 1 → 1

多处违反。订阅高层查找ProxyController/MultiSimSettingController单例并操作静态Phone集合；独立数据高层DcTracker自行取UiccController，CellularDataService经PhoneFactory查找Phone再访问公开mCi。CommandsInterface、IDataService、NITZ和可注入工厂是真实正向证据，但未覆盖运行期全局旁路。配置工厂反射加载不是单独扣分原因。
多处违反。订阅高层查找ProxyController/MultiSimSettingController单例并操作静态Phone集合；独立数据高层DcTracker自行取UiccController，CellularDataService经PhoneFactory查找Phone再访问公开mCi。CommandsInterface、IDataService、NITZ和可注入工厂是真实正向证据，但未覆盖运行期全局旁路。配置工厂反射加载不是单独扣分原因。
为何不降：传入的CommandsInterface、实际IDataService调用和NitzStateMachine都是真实抽象，不能断言全面严重失败而给0。
为何不升：订阅radio和数据/SIM两个业务面均依赖全局具体状态；工厂返回具体tracker并未消除运行期旁路，不满足仅少量改进的2。
范围限制：定向核对已列主责任和消费者；未穷尽所有方法、历史和厂商实现，未执行构建或设备测试。

