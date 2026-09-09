# 非 LSP SOLID 定向源码校准

本次重新审查 FW-02、FW-07、FW-10、FW-16 四仓的 SRP/OCP/ISP/DIP，共 16/36 叶；14 保留、2 修正。其余 20 叶未声称本轮重审。16 叶由主任务执行新的源码通路审阅，已知旧答案；其中两项修分另由独立上下文的第二 Agent 只读复核合同和父接口—实现—消费者，均支持 2。第二审阅者已知待审结论，亦非盲评；没有声称 36 叶独立认证。
固定 v0.9.0 的源码 HEAD，按主职责、实际生产消费者及最强反例审查。未按类长度、方法数量或 no-op 关键词自动定档，也未从抽样推算全仓问题比例。

FW-07 OCP 3→2：评分扩展成立，但 ActiveModeWarden 的运行期恢复按具体 manager 类型分派。FW-16 ISP 3→2：通知提取器被统一接口强制提供不使用的配置/Zen 方法；接口未提供默认可选实现，所有插件必须声明这些方法；空 setter 不被进一步推断为运行行为契约失败。两项均说明局部设计边界，未证明现有车辆运行故障。
完整路径、行段、符号、HEAD、SHA 和相邻档理由见 [solid-calibration.json](solid-calibration.json)。Android 修正为 269/828；合同 v3.5、源码和 refs 不变。

## FW-02 solid_principle.dependency_inversion：2 → 2

主要职责：IP provisioning and reachability；network validation and carrier resource selection；DHCP packet extension/server dependencies；observer event delivery；IP memory persistence。
最强反例：IpMemoryStoreService 在运行时直调 IpMemoryStoreDatabase/RelevanceUtils 静态实现，并直接取系统时间。
为何不降：IpReachabilityMonitor 和 DhcpServer 实际接收 Dependencies/INetd 等边界，不能说全仓高层普遍只依赖具体实现；静态持久化主要集中在存储职责。
为何不升：持久化策略、时钟与具体实现耦合未隔离，已有注入入口不能抵消它而升 3。
未穷尽范围：未逐方法复核所有 APF、DHCP 状态转换、native/socket 边界与外部平台实现；不据此估计全仓问题比例。

## FW-02 solid_principle.interface_segregation：3 → 3

主要职责：IP provisioning and reachability；network validation and carrier resource selection；DHCP packet extension/server dependencies；observer event delivery；IP memory persistence。
最强反例：NetworkObserverRegistry 适配上游 Netd 全事件接口时，对 strict-cleartext 事件为空处理。
为何不降：该空处理被集中在边界适配器；下游 NetworkObserver 可选择默认事件，Reachability.Callback 只要求 notifyLost。没有证据显示每个业务观察者被强迫实现 cleartext 能力。
为何不升：已核对事件/可达性两类客户端，未获得全套汽车接口演进与一致性保障，故不升 4。
未穷尽范围：未逐方法复核所有 APF、DHCP 状态转换、native/socket 边界与外部平台实现；不据此估计全仓问题比例。

## FW-02 solid_principle.open_closed：3 → 3

主要职责：IP provisioning and reachability；network validation and carrier resource selection；DHCP packet extension/server dependencies；observer event delivery；IP memory persistence。
最强反例：DhcpPacket 对固定 DHCP 消息类型采用 switch；增加协议类型要修改解析表。
为何不降：该分支处理封闭协议枚举；实际 OEM TLV 业务通过数据列表及 finishPacket 模板消费，IP/DHCP 依赖有生产扩展入口，未发现要求每个 OEM 选项修改核心的反例。
为何不升：未建立系统化汽车扩展规范与跨扩展面验证；普通模板/数据扩展不自动是 4。
未穷尽范围：未逐方法复核所有 APF、DHCP 状态转换、native/socket 边界与外部平台实现；不据此估计全仓问题比例。

## FW-02 solid_principle.single_responsibility：2 → 2

主要职责：IP provisioning and reachability；network validation and carrier resource selection；DHCP packet extension/server dependencies；observer event delivery；IP memory persistence。
最强反例：NetworkMonitor 自行做定位权限、邻区 MCC 统计及 carrier 资源选择，把网络验证与配置选择政策放在同一类。
为何不降：IpClient 将 DHCP 会话交给 DhcpClient，监控、邻居可达性、持久化亦有独立协作者；本次主链未建立多业务子系统普遍无分工，不能仅按中心类长度降为 1。
为何不升：carrier/MCC 选择有自身变更原因，仍留在验证服务，尚不足以支持良好遵循的 3。
未穷尽范围：未逐方法复核所有 APF、DHCP 状态转换、native/socket 边界与外部平台实现；不据此估计全仓问题比例。

## FW-07 solid_principle.dependency_inversion：2 → 2

主要职责：Binder service policy；STA/SoftAP mode lifecycle and recovery；candidate and connected-network scoring；multicast filtering；wakeup persistence。
最强反例：WifiServiceImpl.resetNotificationManager 在业务执行中逐个向具体 WifiInjector 索取通知/唤醒实现；WifiScoreReport 构造固定具体评分器。
为何不降：Clock、Facade、评分与模式协作者有显式注入，构造装配本身不算普遍违反；主要反例是运行期具体 locator，未支撑全仓多处不合理设计的 1。
为何不升：运行期 locator 使具体通知实现的变化影响服务，未达到良好倒置的 3。
未穷尽范围：未穷尽全部 HAL、扫描、Passpoint、P2P 与配置迁移实现；主体范围是上述生产控制链而非整个 Wi-Fi 方法总体。

## FW-07 solid_principle.interface_segregation：3 → 3

主要职责：Binder service policy；STA/SoftAP mode lifecycle and recovery；candidate and connected-network scoring；multicast filtering；wakeup persistence。
最强反例：WifiMulticastLockManager 仍通过较大的 ActiveModeWarden 获取当前模式管理器。
为何不降：实际过滤能力被收窄为 start/stop 两方法并均有消费；WakeupConfigStoreData 分成四个类型化 DataSource 且 get/set 都在生产读写中使用。较宽 provider 的获取依赖不等于客户端被迫实现无关过滤方法。
为何不升：只证明已审能力拆分良好，未具备系统化汽车接口约束与演进证据，不升 4。
未穷尽范围：未穷尽全部 HAL、扫描、Passpoint、P2P 与配置迁移实现；主体范围是上述生产控制链而非整个 Wi-Fi 方法总体。

## FW-07 solid_principle.open_closed：3 → 2

主要职责：Binder service policy；STA/SoftAP mode lifecycle and recovery；candidate and connected-network scoring；multicast filtering；wakeup persistence。
最强反例：ActiveModeWarden 恢复路径按 ConcreteClientModeManager/SoftApManager 具体类型分支重启；新增不属于这两种具体类型、且需纳入用户可控模式恢复的实现时，现有核心分派不能自动覆盖；继承既有具体类而不改变恢复语义未必需要修改。
为何不降：WifiNetworkSelector 动态注册并统一消费 CandidateScorer，提名/评分存在真实扩展；没有严重设计失效或多个业务面完全封闭的证据，不能降 1/0。
为何不升：旧 3 分只核对评分扩展和装配，遗漏实际恢复类型分支；这属于运行期扩展边界不完整，修正为局部违反的 2。
未穷尽范围：未穷尽全部 HAL、扫描、Passpoint、P2P 与配置迁移实现；主体范围是上述生产控制链而非整个 Wi-Fi 方法总体。

## FW-07 solid_principle.single_responsibility：2 → 2

主要职责：Binder service policy；STA/SoftAP mode lifecycle and recovery；candidate and connected-network scoring；multicast filtering；wakeup persistence。
最强反例：WifiServiceImpl 内嵌 SIM 变化重置及版本权限策略，ActiveModeWarden 还内嵌飞行模式/紧急呼叫/用户限制政策。
为何不降：网络选择、评分、组播过滤与持久化已分配独立协作者；本轮审查体现少数协调中心的政策集中，不按服务职责多或类长直接给 1。
为何不升：两处中心拥有独立变更原因而非纯转发，故不能用已有协作者证明 3。
未穷尽范围：未穷尽全部 HAL、扫描、Passpoint、P2P 与配置迁移实现；主体范围是上述生产控制链而非整个 Wi-Fi 方法总体。

## FW-10 solid_principle.dependency_inversion：2 → 2

主要职责：GSM/CDMA service dispatch；wake-lock delivery lifecycle；message duplication policy；geofencing calculation；location session；provider persistence。
最强反例：高层 Handler 持有具体 LocationRequester/计算器；运行时通过 Context 取得配置与持久化服务，并使用静态 metrics 入口。
为何不降：计算器工厂和 HandlerHelper 可注入，定位状态封装在独立协作者；单纯 new 发生在构造期不能据此判全仓多处严重倒置，接口化程度并非零。
为何不升：定位实现及业务执行依赖仍未统一为显式抽象边界，不能只凭测试工厂升 3。
未穷尽范围：GSM/CDMA 位级解码器、数据库升级及平台 radio 的全部路径未穷尽；GsmCellBroadcastHandler/CdmaServiceCategoryProgramHandler 的职责入口另做符号搜索。

## FW-10 solid_principle.interface_segregation：3 → 3

主要职责：GSM/CDMA service dispatch；wake-lock delivery lifecycle；message duplication policy；geofencing calculation；location session；provider persistence。
最强反例：LocationUpdateCallback 同时要求位置更新、不可用及全部消息完成三个方法。
为何不降：三方法分别驱动同一定位会话的更新、超时/权限失败与结束；生产回调使用其完整生命周期，不是强制混入无关能力。状态机也只要求一项消息处理。
为何不升：当前会话能力划分合理，未证明跨接口体系的优秀实践，不升 4。
未穷尽范围：GSM/CDMA 位级解码器、数据库升级及平台 radio 的全部路径未穷尽；GsmCellBroadcastHandler/CdmaServiceCategoryProgramHandler 的职责入口另做符号搜索。

## FW-10 solid_principle.open_closed：3 → 3

主要职责：GSM/CDMA service dispatch；wake-lock delivery lifecycle；message duplication policy；geofencing calculation；location session；provider persistence。
最强反例：Handler 内有固定 GSM/CDMA 类别映射及消息动作分支，添加标准类型可能修改这些表。
为何不降：生命周期模板真正调用子类 handleSmsMessage；计算器工厂由生产构造保存并在地理围栏路径调用。固定协议映射不是每个接收器/计算器业务扩展都改状态机的证据。
为何不升：存在实际扩展入口，但未证明系统化汽车扩展/契约验证，普通模板不足以给 4。
未穷尽范围：GSM/CDMA 位级解码器、数据库升级及平台 radio 的全部路径未穷尽；GsmCellBroadcastHandler/CdmaServiceCategoryProgramHandler 的职责入口另做符号搜索。

## FW-10 solid_principle.single_responsibility：2 → 2

主要职责：GSM/CDMA service dispatch；wake-lock delivery lifecycle；message duplication policy；geofencing calculation；location session；provider persistence。
最强反例：CellBroadcastHandler 同时定义历史窗口/跨 SIM 去重政策及 Provider 查询、插入、状态列更新。
为何不降：Default 服务分派 GSM/CDMA，WakeLockStateMachine 管生命周期，LocationRequester 管定位，CbSendMessageCalculator 管围栏决策；不能把内部类定位职责误算成外层无分工。
为何不升：外层的去重政策与持久化具有独立变更原因，仍未完全隔离，不升 3。
未穷尽范围：GSM/CDMA 位级解码器、数据库升级及平台 radio 的全部路径未穷尽；GsmCellBroadcastHandler/CdmaServiceCategoryProgramHandler 的职责入口另做符号搜索。

## FW-16 solid_principle.dependency_inversion：2 → 2

主要职责：UI/night/projection mode policy；notification ranking and extraction；location provider substitution and dependencies；clipboard Binder boundary；system-service lifecycle。
最强反例：UiModeManagerService 运行时静态取得 ActivityTaskManager，通知删除政策通过 LocalServices 隐式取得 JobSchedulerInternal。
为何不降：JobSchedulerInternal 自身是抽象且 LocationProviderManager 使用 Injector 提供多个协作者；问题是隐式获取而非没有任何倒置，不据两个 locator 推断整个平台普遍不合理。
为何不升：运行期依赖未在这些政策入口显式注入，尚不能给 3。
未穷尽范围：WindowManager、ActivityManager、Power、全部 SystemUI 及其他大子系统未做本轮逐方法复核；该大仓不由几处局部样本获得全仓无缺陷认证。

## FW-16 solid_principle.interface_segregation：3 → 2

主要职责：UI/night/projection mode policy；notification ranking and extraction；location provider substitution and dependencies；clipboard Binder boundary；system-service lifecycle。
最强反例：NotificationSignalExtractor 强制 setConfig/setZenHelper；RankingHelper 对每个提取器调用它们。Channel/Intrusiveness 实现对无关配置或 Zen 能力提供空方法。
为何不降：问题集中在通知提取器这一接口族；SystemService 的可选 hook 与独立 IClipboard Binder 保持职责边界。不把同一接口的多个实现重复算成全仓多业务面违反而降 1。
为何不升：旧 3 分只看生命周期和剪贴板，未覆盖通知插件被迫依赖无关 helper 的反例；当前修正为局部违反的 2。
未穷尽范围：WindowManager、ActivityManager、Power、全部 SystemUI 及其他大子系统未做本轮逐方法复核；该大仓不由几处局部样本获得全仓无缺陷认证。

## FW-16 solid_principle.open_closed：2 → 2

主要职责：UI/night/projection mode policy；notification ranking and extraction；location provider substitution and dependencies；clipboard Binder boundary；system-service lifecycle。
最强反例：UiModeManagerService 在通用投影入口硬编码汽车独占条件，并在模式策略中集中枚举设备/夜间类型。
为何不降：MockableLocationProvider 可替换 AbstractLocationProvider；通知 RankingHelper 从配置加载并统一消费提取器，不是所有核心都必须随实现变化修改，不足以下降 1。
为何不升：UI 模式的实际政策分支未被这些其他扩展面覆盖，不能升 3。
未穷尽范围：WindowManager、ActivityManager、Power、全部 SystemUI 及其他大子系统未做本轮逐方法复核；该大仓不由几处局部样本获得全仓无缺陷认证。

## FW-16 solid_principle.single_responsibility：2 → 2

主要职责：UI/night/projection mode policy；notification ranking and extraction；location provider substitution and dependencies；clipboard Binder boundary；system-service lifecycle。
最强反例：UiModeManagerService 集中投影身份/独占策略、夜间模式存储、时间计算与 Alarm 调度。
为何不降：定位 provider/权限设置辅助与通知提取/排序有独立职责；本次没有跨所有大子系统的普遍混杂证据，2 为有范围限制的定性判断，不是已测得全仓少量问题比例。
为何不升：明确的政策、存储和调度变更原因仍集中，故不能升 3。
未穷尽范围：WindowManager、ActivityManager、Power、全部 SystemUI 及其他大子系统未做本轮逐方法复核；该大仓不由几处局部样本获得全仓无缺陷认证。
