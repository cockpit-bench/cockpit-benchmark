# v0.8.3 evidence and accuracy corrections

All 171 canonical leaves were re-reviewed against their frozen source contracts, actual behavior and counterevidence. 149 conclusions were supported; 22 needed facts, reasons or evidence repairs. This is complete leaf coverage, not exhaustive inspection of every source path or a new Android execution.

APP-02 CI changes from 3 to 2, so the total is **277/828**. The independent GitLab configuration contains real build/test/quality jobs, but the inspected buildserver-bullseye image and .base setup use an unavailable bullseye-backports Release. The 2026-09-08 10:12 UTC snapshot records image digest, layer configuration and 404/200 mirror responses under [APP-02 facts](../facts/APP-02.json). This is dated external dependency evidence; no container or GitLab job was executed.

| Repository | Leaf | Before → after | Repair |
|---|---|---|---|
| APP-01 | platform_reuse.platform_upgrade | 3 → 3 | ROMUtils把SystemProperties反射及失败返回false集中在工具内，不能单凭它说反射未隔离；但MwmActivity真实按TIRAMISU检查/请求POST_NOTIFICATIONS，业务仍需通知权限逻辑。另有路由UI直接使用废弃Resources.getColor(int)，不受ROMUtils覆盖。SDK声明四种ABI，未发现生产单ABI闭源门槛；3分由实际未封装废弃API及复杂权限封顶成立。 |
| APP-02 | compilation.ci_independence | 3 → 2 | 独立 GitLab CI 有真实构建、测试、质量/报告任务，但 2026-09-08 核查的 buildserver-bullseye 镜像及 .base 补源仍使用已返回 404 的 bullseye-backports；前置 apt update 无法完成，不能满足完整可执行流水线，2。 |
| APP-02 | platform_reuse.platform_upgrade | 3 → 3 | FileCompat对libcore反射有捕获，不将这个局部封装当全部风险已隔离；NotificationHelper实际检查POST_NOTIFICATIONS，安装器还直接调用废弃Intent.getParcelableExtra(String)。独立业务调用没有统一API迁移边界。无生产单ABI闭源物，3分有独立负面事实支持。 |
| APP-11 | architecture.componentization | 5 → 5 | model、parser:feed、playback:base 有独立 Gradle 配置和真实业务行为；playMediaObject/resume、PSMPCallback 契约由 LocalPSMP 与 CastPsmp 实现并被 core/cast 消费，支持组件复用与替换，5。 |
| APP-11 | platform_reuse.platform_upgrade | 3 → 3 | PlaybackService和PreferenceActivity分别在core/app中处理SDK31 PendingIntent及SDK26设置跳转；播放器接口不封装这两条路径。另有PlaybackService直接调用废弃getParcelableExtra(String)。通知通道创建本身未算复杂权限；公开SDK迁移可行且无单ABI闭源物，评3。 |
| APP-14 | compilation.ci_independence | 1 → 1 | 当前仓有 5 个 TEST_MAPPING，映射到真实 Soong 测试目标；没有 PREUPLOAD.cfg 或独立 provider 配置，仅有 Android 系统层 CI，1。 |
| APP-14 | platform_reuse.platform_upgrade | 0 → 0 | 状态栏启动直接向IStatusBarService注册，锁屏状态通过ActivityTaskManager私有Binder更新；这是两条真实核心平台通路，现有插件/DI未提供它们的跨版本替代实现。SystemUI以platform_apis/privileged方式构建，按多核心未隔离内部接口依赖评0。wallpaper ambient 调用有明确非关键/异常忽略，不作为核心阻断证据。 |
| APP-16 | architecture.componentization | 5 → 5 | LauncherPluginLib、SecondaryDisplayLauncherLib 和图标公共库等 6 个组件族具有实际职责、构建边界和行为契约；BitmapRenderer.draw 被生产代码消费，组件复用成立，5。 |
| APP-16 | architecture.decoupling | 2 → 2 | 6 个归并组件族的 9 条配置边无环，图标/插件/次屏依赖方向清楚；QuickStep 仍直接依赖 ActivityManagerWrapper 具体平台入口，基本解耦但不满足 3 档，2。 |
| APP-16 | architecture.modularization | 2 → 2 | 11 个 Make/Soong 声明按重叠源码和替代变体归并为 6 个组件族，主要职责可辨且无环；仅 iconloader_base 族符合规范命名，1 个少于 3 档要求的 2 个，2。 |
| FW-02 | solid_principle.dependency_inversion | 2 → 2 | 基本遵循，仍有少量具体或隐式全局依赖。 |
| FW-02 | solid_principle.open_closed | 3 → 3 | 生产封包模板与OEM自定义TLV有真实扩展面；固定DHCP解码枚举不等于每次业务扩展改核心，良好遵循。 |
| FW-03 | compilation.api_version_management | 3 → 3 | 版本由真实已发布API基线及来源提交控制，当前源码经过实际兼容性diff；按合同3.4满足版本控制与API baseline验证条件。范围仅本仓MAP库，不声称平台AIDL/JNI或全仓行为兼容。 |
| FW-07 | platform_reuse.release_branch_strategy | 0 → 0 | 本地head为refs/heads/main。没有其他本地head提供车型/平台分流证据。全部17个tag解引用为1个提交；标签名字没有被当成已证明的车型或跨平台复用。结合生产构建/来源说明，未形成合同要求的同版本车型SOP、同平台车型共用或跨平台合格工件证据，按显式审查缺失评0；不是根据main/master名称判0，也不推断上游组织没有发布流程。 |
| FW-10 | compilation.compilation_independence | 0 → 0 | CellBroadcastServiceCommon 依赖平台 statsd、modules-utils 和生成工具；BitwiseInputStream 的单类临时 javac 不构成仓内独立生产目标，完整产品仍需平台树，0。 |
| FW-10 | platform_reuse.platform_upgrade | 3 → 3 | 实际两处SDK差异集中在CellBroadcastHandler共同兼容入口：T前RECEIVER_EXPORTED=0，U前getSubIdForPhone回退getSubscriptionIds/INVALID_SUBSCRIPTION_ID，Gsm与DefaultService等复用它们，版本适配状态为 1。位置代码fine/coarse检查带onLocationUnavailable，未发现高版本专属复杂权限路径；复杂权限适配为 false。GsmCellBroadcastHandler仍直接实现废弃PhoneStateListener，LocationRequester调用非公开旧LocationRequest.create，未封装风险维持3。 |
| FW-10 | solid_principle.single_responsibility | 2 → 2 | 已有定位/计算器/状态机分工，但外层历史去重政策与Provider持久化仍集中，基本遵循且有有限改进空间。 |
| FW-14 | platform_reuse.platform_upgrade | 3 → 3 | CarPackageManagerService.init直接读取系统驾驶安全区域属性并更新安全策略，CarAudioService直接读私有开关；这些是实际运行行为而非只用dump/log证明风险。VehicleStub真实按有效性由AIDL回退HIDL，说明有硬件迁移通路但不覆盖上述平台消费。未发现单ABI闭源核心链，保持3；ICarImpl.dumpRROs 不作为核心风险主证。 |
| FW-15 | compilation.compilation_independence | 0 → 0 | Telecom 的生产服务及资源/生成物依赖 services 与平台 API；RingerAttributes 为决策结果值载体，临时单类 javac 不提供独立业务构建闭包，0。 |
| FW-15 | platform_reuse.platform_upgrade | 3 → 3 | CallAudioRouteStateMachine.setMuteOn通过工厂取得IAudioService后直接调用带当前用户的setMicrophoneMute，源码说明普通AudioManager不具等价跨用户语义。工厂封装服务获取，不消除业务对私有接口的消费。属于可局部迁移的未封装风险，3成立；Analytics 硬件版本 dump 不作为核心风险主证。 |
| FW-15 | solid_principle.dependency_inversion | 2 → 2 | 基本遵循，仍有少量具体或隐式全局依赖。 |
| FW-16 | platform_reuse.platform_upgrade | 0 → 0 | SystemServer启动实际调用ART VMRuntime、BinderInternal调度/线程原语并加载android_servers；ServiceManager的发现链继续调用BinderInternal原生上下文。JNI链接libandroid_runtime/libbinder等平台内部运行时，服务生命周期抽象不能替代启动/IPC底座。按这些真实多核心内部运行时绑定保留0；普通同仓内部资源以及启动统计不单独作0档证明，也不把有源码的native误称单ABI闭源物。 |

The Kotlin counter now handles nested block comments by language. All selected blobs in all 18 repositories were recounted. Two Kotlin files, present in both APP-14 and FW-16, account for 21 fewer LOC in each repository. APP-14 is 361,419 LOC; FW-16 is 2,905,419 LOC. Both remain large. Source scope selection and source refs are unchanged.

The verifier compares the complete oracle and standard leaf objects, decisive facts, evidence indices, HEAD/tree/contract/refs, counts and Markdown/CSV scorecards. It rejects stale evidence or reasons even when scores are equal. JSON metadata uses hash-bound JSON Pointers instead of a brace placeholder. The exporter preserves the reviewed counter source.

APP-14 and FW-16 share family_id `aosp-frameworks-base`: all 2,812 selected APP-14 production files are byte-identical to the corresponding FW-16 packages/SystemUI files. The 18 repositories therefore contain 17 recorded families. Use [check_split.py](../verification/check_split.py) to reject splitting a recorded family across evaluation sets. Boundary candidates inherit their originating family and remain outside the 18-repository denominator.

The dataset remains public development/regression material. [Band coverage](COVERAGE.md), absent final-HEAD Android integration executions, static ownership selection and the limits of semantic sampling remain disclosed. The 22 pending repositories and published historical refs are unchanged.
