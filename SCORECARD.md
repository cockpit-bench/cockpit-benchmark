# Validation-18 v0.8.2

| ID | Repository | Size | Quality | Score |
|---|---|---|---|---|
| APP-01 | navigation-map | large | high | 19/40 |
| APP-02 | market-distribution | medium | high | 20/40 |
| APP-03 | owner-handbook | small | high | 10/40 |
| APP-11 | podcast-player | medium | medium | 18/40 |
| APP-13 | camera-inspector | small | medium | 8/40 |
| APP-14 | system-ui-shell | large | medium | 12/40 |
| APP-15 | system-settings | large | low | 8/40 |
| APP-16 | launcher-workspace | medium | low | 14/40 |
| APP-17 | climate-panel | small | low | 7/40 |
| FW-02 | network-stack-service | small | high | 21/52 |
| FW-03 | bluetooth-service | medium | high | 19/52 |
| FW-07 | wifi-service | large | high | 21/52 |
| FW-08 | connectivity-service | medium | medium | 16/52 |
| FW-10 | cell-broadcast-service | small | medium | 19/52 |
| FW-14 | car-services | large | medium | 19/52 |
| FW-15 | telecom-service | small | low | 18/52 |
| FW-16 | platform-framework | large | low | 18/52 |
| FW-18 | telephony-service | medium | low | 11/52 |

## APP-01 navigation-map

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 5/5 | sdk与location:core等独立Gradle入口存在；GmsLocationProviderFactory有isProviderAvailable/getProvider行为方法，定位具体提供者通过工厂隔离，5。 |
| architecture.decoupling | 2/3 | 21模块49配置依赖无环；foss构建显式纳入google模块src/main/java，已确认源码侵入反例；app还直接调用Framework门面，因此维持2，不能沿用旧侵入0。 |
| architecture.modularization | 3/3 | 至少sdk/location:core/libs:utils等三个内聚构建模块和两个规范名称；7条api、42条implementation配置声明且5模块有测试源码，满足3。多ABI/native归属不被额外算作Gradle模块。 |
| compilation.api_version_management | 1/3 | SDK发布坐标使用日期型version.sh版本；有真实生产发布消费者，非语义化API策略，也无公开API兼容diff。 |
| compilation.ci_independence | 3/3 | 独立CI有真实Gradle编译、JUnit/设备测试和lint报告阶段。 |
| compilation.compilation_independence | 2/3 | Gradle仓内模块、NDK/CMake及已声明git子模块形成可复现入口，依赖SDK/Maven而非整棵Android树；无关键跨仓API兼容基线与hermetic证据，不到3。 |
| platform_reuse.platform_upgrade | 3/10 | ROMUtils与定位工厂仅覆盖局部差异；app通知权限及app/sdk的SDK分支未统一隔离。存在可行迁移路径，复杂权限规则封顶3；多ABI源码不构成架构独占。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-02 market-distribution

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 5/5 | download/index/database至少两个有独立Gradle入口的内聚公共组件；HttpManager经MirrorChooser和HttpClientEngineFactory构造参数承载可替换网络策略，满足5。 |
| architecture.decoupling | 3/3 | 完整生产声明图4模块6边无环；database向index/download下层依赖。RepoV2Fetcher通过构造参数接收TempFileProvider/DownloaderFactory/HttpManager，网络引擎在HttpManager内替换；没有因仅引用具体公共门面类型就虚构硬编码实现边。结合边界审阅，维持3。 |
| architecture.modularization | 3/3 | 改为3。4个真实内聚模块及4个含测试源码的模块成立；合同要求含关键词，database字面包含base，因此规范模块名为app、database共2。原人工裁决误漏database，与已提取事实2不一致，应修正而不是改变事实。 |
| compilation.api_version_management | 1/3 | 有 Git 派生版本名和手工 Android versionCode，但没有语义化策略或兼容基线保证。 |
| compilation.ci_independence | 3/3 | GitLab默认分支/MR触发，真实assemble/test、lint/pmd/checkstyle和报告任务齐备；非远程执行成功声明。 |
| compilation.compilation_independence | 2/3 | Gradle/KMP生产闭包完整，外部公开SDK/Maven接口；本地日志成功作为旁证，但无跨仓API兼容基线及hermetic保证。 |
| platform_reuse.platform_upgrade | 3/10 | 有compat封装及公共SDK迁移路径，但应用通知/安装运行时权限、业务SDK分支未统一；复杂权限风险封顶3，无单ABI闭源证据。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-03 owner-handbook

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 1/5 | ui/domain/data真实职责包存在；全部由同一app构建，包级分层满足1，不满足两个真实组件的3/5。 |
| architecture.decoupling | 2/3 | Catalog/Article领域与UI职责可辨且无模块环；HandbookActivity直接构造ReadingStore并调用AssetCatalog.load，具体数据实现未接口隔离，2。 |
| architecture.modularization | 1/3 | 职责包存在但只有单app构建边界，1。 |
| compilation.api_version_management | 1/3 | versionName 1.0.0 是手写发布号，没有 SemVer 变更策略或机制证据。 |
| compilation.ci_independence | 0/3 | 完整跟踪文件清单无有效 CI 入口。 |
| compilation.compilation_independence | 2/3 | 公开 SDK/AGP，生产闭包全在 app，无平台源码或 sibling 注入。 |
| platform_reuse.platform_upgrade | 3/10 | UI 直接调用废弃的 WindowInsets.getSystemWindowInset*；按合同属于未封装非兼容 API 风险，仍可直接迁移 Insets API。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-11 podcast-player

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 5/5 | model、parser:feed、playback:base等是独立Gradle组件；PlaybackServiceMediaPlayer提供实际播放状态/回调方法边界并支持本地与cast实现，公共能力下沉，5。 |
| architecture.decoupling | 2/3 | 14模块31生产依赖无环；ClientConfig虽然接收上层回调，却硬编码PodDBAdapter/UserPreferences等初始化，core还依赖cast实现；明确局部具体绑定足以封顶2，未证实循环或多处无稳定方向的1/0。 |
| architecture.modularization | 3/3 | 至少model/parser:feed/playback:base三个职责内聚真实模块，规范名app/core/base/common等至少2个，Gradle模块入口和implementation边界成立；实际含测试源码模块6个而非旧14，不改变3。 |
| compilation.api_version_management | 1/3 | versionName 2.5.2只是手工常量；makeRelease接受独立VERSION_NAME而不校验与APK版本匹配，缺少语义化控制策略/API基线。 |
| compilation.ci_independence | 2/3 | 独立CI有真实构建测试质量命令，但push只覆盖master/develop，code-style先fetch origin develop而当前候选无该ref；不满足当前仓完整可执行标准流水线。 |
| compilation.compilation_independence | 2/3 | 模块源码闭包在仓，SDK/Maven/JitPack明确；已有本地Java17 assembleFreeDebug成功日志旁证，无API兼容diff或完全锁定环境。 |
| platform_reuse.platform_upgrade | 3/10 | app与core两个业务模块有未统一的SDK分支；播放器抽象不覆盖通知、存储与UI差异，按两业务模块硬编码封顶3。未把单纯NotificationChannel当复杂权限，未发现单ABI闭源依赖。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-13 camera-inspector

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 0/5 | 单一app且生产代码位于com.android.devcamera根包。CameraInterface/MyCameraCallback/GyroListener是行为契约，但没有形成可独立构建组件或包级职责组织；组件化0。 |
| architecture.decoupling | 2/3 | CameraInterface提供相机调用边界且单模块图无环；DevCameraActivity直接new Api2Camera，存在可定位具体实现绑定，满足2而非完全隔离3。不能把该一处包内引用冒充跨模块引用数。 |
| architecture.modularization | 0/3 | 单app生产模块、根包集中；无包级职责模块结构，0。 |
| compilation.api_version_management | 1/3 | 版本仅为手写 versionCode 1 / versionName 1.0，无 API 基线控制。 |
| compilation.ci_independence | 0/3 | 完整跟踪文件清单无有效 CI 入口。 |
| compilation.compilation_independence | 2/3 | Gradle 生产源码闭包完整，仅需公开 SDK 和声明 AGP，存在可重复 app 构建入口。 |
| platform_reuse.platform_upgrade | 3/10 | 旧存储权限和直接 /sdcard 写入需要运行时行为迁移，未由相机接口覆盖，封顶 3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-14 system-ui-shell

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 5/5 | 完整生产图扩展为21个目标，SystemUIPluginLib、SystemUICommon、SystemUIAnimationLib等独立职责明确；ActivityStarter声明真实活动启动方法，公共能力下沉并由插件契约复用，5。 |
| architecture.decoupling | 2/3 | 21目标31内部依赖无环；SystemUI-core通过Compose defaults直接纳入compose/features源文件，存在明确条件源码侵入。局部DI/插件无法消除此边界事实，2。 |
| architecture.modularization | 2/3 | plugin/common/animation等至少三个内聚真实构建模块成立；包括Java库后仍没有两个小写加关键字模块名，21不能替代命名门槛，维持2。 |
| compilation.api_version_management | 1/3 | 插件使用手动整数版本并运行时精确匹配；不是语义化版本，也不是当前API对发布baseline兼容性diff。 |
| compilation.ci_independence | 1/3 | 真实PREUPLOAD/TEST_MAPPING受Android平台预提交系统调度；无仓库独立完整流水线。 |
| compilation.compilation_independence | 1/3 | animation/surfaceeffects有实际Gradle公共SDK局部单元；完整SystemUI需平台私有API和仓外SettingsLib/WindowManager-Shell，按1而非Soong自动0。 |
| platform_reuse.platform_upgrade | 0/10 | 插件/DI是局部扩展机制，不能覆盖状态栏、窗口/壁纸等核心平台内部接口依赖；多个核心通路绕过稳定接口且无迁移fallback，锁0。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-15 system-settings

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 3/5 | 12个生产构建目标包括Settings/Settings-core及协议/logtags/统计/ChangeIds库。业务实现仍集中Settings-core；BasePreferenceController是同核心包内可扩展契约。协议与常量生成辅助目标并不自动证明两个独立可替换业务/公共组件，维持3，不凭12抬至5。 |
| architecture.decoupling | 2/3 | 全仓生产声明图12模块11边无环，APK到core方向明确；BasePreferenceController直接关联SettingsSliceProvider/Utils等具体核心业务类，多个平台具体调用仍无统一隔离，2。Settings_srcs只有导出声明，不再作为已证明消费者侵入边扣分。 |
| architecture.modularization | 2/3 | 协议/日志/核心打包职责可辨，至少两个真实构建模块；完整清单仅app-usage-event-protos-lite一个名称符合小写含关键字，少于2，无法到3；维持2。 |
| compilation.api_version_management | 0/3 | 没有生产API版本控制机制；平台API选择、Android SDK与生成proto不算版本管理。 |
| compilation.ci_independence | 1/3 | 真实PREUPLOAD/TEST_MAPPING受Android平台预提交系统调度；无仓库独立完整流水线。 |
| compilation.compilation_independence | 0/3 | 全部有意义业务构建依赖SettingsLibDefaults、平台私有API和仓外telephony/ims源码模块；未找到自包含生产构建入口。 |
| platform_reuse.platform_upgrade | 0/10 | Settings核心在多个业务包直接访问平台隐藏Binder和系统API，Settings-core以platform_apis构建；不存在覆盖这些核心通路的统一兼容/降级边界，满足多处绕过稳定接口且无隔离的0档。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-16 launcher-workspace

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 5/5 | iconloader、LauncherPluginLib和SecondaryDisplayLauncherLib等有真实独立构建入口。BitmapRenderer声明draw行为并由图标组件复用；公共图标/插件边界满足至少两个组件，5。 |
| architecture.decoupling | 2/3 | Make/Soong归一化构建族加Gradle替代包装图无环；QuickStep直接使用ActivityManagerWrapper等具体SystemUI平台入口，主要边界存在但实现隔离不完全，2。 |
| architecture.modularization | 2/3 | 补入SecondaryDisplayLauncherLib后6个组件族，app/iconloader变体不重复计数；实际声明名没有两个合规名称，归一化临时标签launcher-app不能制造规范命名，仍2。 |
| compilation.api_version_management | 1/3 | versionName 1.0与versionCode为手工常量；无语义策略或API兼容diff。 |
| compilation.ci_independence | 0/3 | 当前tracked tree无有效CI配置；构建脚本及测试目录本身不等于流水线。 |
| compilation.compilation_independence | 1/3 | iconloader_base有SDK28局部生产边界；完整Launcher依赖仓外未版本化launcher_protos/plugin_core/sysui_shared平台预构建。 |
| platform_reuse.platform_upgrade | 3/10 | QuickStep核心任务/手势链依赖SystemUI私有平台接口且无统一独立契约，但withoutQuickstep变体及公开SDK图标单元保留迁移路径；无单ABI闭源依赖，total=3，裁3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## APP-17 climate-panel

| Leaf | Score | Reason |
|---|---|---|
| architecture.componentization | 1/5 | CarHvacApp仅一个构建模块；ui/controllers业务控制与控件分包属于包级结构，1。6个行为回调不等于6个独立组件。 |
| architecture.decoupling | 2/3 | 控制服务与控件边界可辨、模块无环；HvacUiService绑定HvacController.class并向具体LocalBinder强转，控制器传播平台具体类型，2。 |
| architecture.modularization | 1/3 | ui/controllers分包可辨，仍是单一Soong app边界，1。 |
| compilation.api_version_management | 0/3 | 没有产品/API 版本文件、语义策略或兼容基线。 |
| compilation.ci_independence | 0/3 | 完整跟踪文件清单无有效 CI 入口。 |
| compilation.compilation_independence | 0/3 | 完整目标依赖平台 APIs、android.car、平台签名和仓外 privapp 模块；仓内无有意义独立构建单元。 |
| platform_reuse.platform_upgrade | 3/10 | 平台专属覆盖窗、privateFlags 反射和旧 AsyncTask/CarHvacManager 未完全隔离，封顶 3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |

## FW-02 network-stack-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 3/3 | 仓内stable aidl_interface声明版本1–10、真实冻结签名/current和固定V10/V18生产链接，构成等价API/ABI兼容基线机制。 |
| compilation.ci_independence | 1/3 | 仅 Android 系统 TEST_MAPPING/平台构建 CI，未提供独立标准流水线。 |
| compilation.compilation_independence | 0/3 | 有声明 SDK 版本但依赖仓外 Connectivity/net-utils/AIDL/Soong 注入，未形成有意义独立生产构建闭包。 |
| platform_reuse.platform_upgrade | 3/10 | 兼容shim不能覆盖业务层SystemProperties及多业务版本分支，未封装风险上限3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | 有 Android JUnit 真实 DHCP 解码断言；无绑定 HEAD 的 Android 执行结果，最高1。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 3/4 | 至少两个生产 DHCP 实现保持序列化父合同；没有系统化 substitution 执行证明，不给4。 |
| solid_principle.open_closed | 3/4 | 良好遵循。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-03 bluetooth-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 3/3 | 版本由真实已发布API基线及来源提交控制，当前源码经过实际兼容性diff；按合同3.4满足版本控制与API baseline验证条件。范围仅本仓MAP库，不声称平台AIDL/JNI或全仓行为兼容。 |
| compilation.ci_independence | 1/3 | 只有平台PREUPLOAD checkstyle/clang-format/aosp hook；无仓库独立流水线。 |
| compilation.compilation_independence | 0/3 | 完整Bluetooth需平台签名/API、JNI system/bt和services.net；独立小型mapsapi实测公开SDK31编译仍因隐藏BLUETOOTH_MAP失败4处，无已证明独立生产目标。 |
| platform_reuse.platform_upgrade | 3/10 | 蓝牙系统权限、隐藏Binder、native平台链深度绑定；profile隔离不覆盖全部风险，但源码JNI和profile边界保留移植路径，total=3无单ABI闭源；3分。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | A2DP服务测试通过真实服务生命周期、native协作者调用与断言验证行为；无绑定HEAD执行证明，最高1。 |
| solid_principle.dependency_inversion | 1/4 | 多处违反，设计不合理。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 3/4 | 两个真实profile对合法生命周期均初始化/释放资源并返回成功；cleanup本来是可选钩子，重复start是生命周期防御条件而非任意收紧输入。调用者检查adapter与expected profile，不能将条件异常机械记为0；未证明系统化跨实现契约测试，裁3。 |
| solid_principle.open_closed | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-07 wifi-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 3/3 | framework-wifi 的 java_sdk_library 与受版本管理的 API 签名基线提供实际 API 差异检查机制。 |
| compilation.ci_independence | 1/3 | PREUPLOAD 和 TEST_MAPPING 构成真实平台 CI 声明；没有独立 CI。 |
| compilation.compilation_independence | 0/3 | 实际生产 Soong 模块依赖仓外平台 defaults、framework 和 connectivity 源码/生成工具，无独立闭合生产构建单元。 |
| platform_reuse.platform_upgrade | 3/10 | Android 版本分支和复杂权限适配未统一隔离；存在 HAL/模式迁移路径，封顶 3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | 存在真实组件交互测试与断言；缺少 final-HEAD Android 集成执行和覆盖证据，封顶 1。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 3/4 | 两个真实生产实现的连接 reset 契约已恢复，并通过可复用替换测试；未达到系统化异常/边界全覆盖的 4 档。 |
| solid_principle.open_closed | 3/4 | 良好遵循。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-08 connectivity-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 3/3 | framework-connectivity通过java_sdk_library与current/system/module API文本集成Soong标准API提取/兼容检查；不是仅普通版本字符串。当前仓不独立构建不抹掉真实平台API机制。 |
| compilation.ci_independence | 1/3 | 仅平台PREUPLOAD/TEST_MAPPING，工具与集成测试在Android树CI运行，无仓库独立流水线。 |
| compilation.compilation_independence | 0/3 | Java服务及库均依赖平台defaults、跨仓AIDL和modules-utils；无独立Gradle/CMake生产入口。Cronet/netd子目录仍由平台Soong组织，不能把同仓模块数量当外部闭包。 |
| platform_reuse.platform_upgrade | 3/10 | 平台SDK shim和mainline模块保留迁移路径；ConnectivityService仍有未封装SystemProperties及多个API层条件，局部抽象不能抹掉未覆盖风险，封顶3；JNI源码不是单ABI闭源SO。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | Android测试有真实Manager到Service交互及断言，缺少绑定HEAD的Android执行结果与覆盖代理，最高1。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.liskov_substitution | 0/4 | IPv6 no-op由父契约明确允许；但API30 IPv4删除无条件返回true，违反父契约true当且仅当map改变的后置条件，触发明确替换违反0档。 |
| solid_principle.open_closed | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-10 cell-broadcast-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 1/3 | versionCode300000000/versionName R-initial为手工平台发布号，无API基线。 |
| compilation.ci_independence | 1/3 | 仅 Android 系统 TEST_MAPPING/平台构建 CI，未提供独立标准流水线。 |
| compilation.compilation_independence | 0/3 | 完整生产目标依赖平台外部源码/工具；临时抽出的单类javac成功不构成仓内独立生产构建入口。 |
| platform_reuse.platform_upgrade | 3/10 | 定位权限处理与未覆盖的系统属性/旧电话监听风险存在，封顶3，有明确迁移路径。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | JUnit真实广播去重行为断言，但没有绑定HEAD的Android运行记录。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 3/4 | 两个生产处理器返回值符合父等待/空闲合同，未见明确收紧或无条件抛错。 |
| solid_principle.open_closed | 3/4 | 良好遵循。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-14 car-services

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 3/3 | droidstubs同时检查current与last_released public/system API真实签名/removed baseline，符合3档。 |
| compilation.ci_independence | 1/3 | 真实PREUPLOAD/TEST_MAPPING受Android平台预提交系统调度；无仓库独立完整流水线。 |
| compilation.compilation_independence | 1/3 | 3 分：完整源码闭包尚未成立，host依赖锁定不支持整仓3档。 2 分：完整Car平台依赖未通过独立版本化SDK/JAR接口封闭，2档不满足。 1 分：可局部构建具有真实消费者的生产单元；完整构建仍需平台环境/私有stub注入。 0 分：新入口与实际成功执行否定没有任何有意义独立生产单元的条件。 |
| platform_reuse.platform_upgrade | 3/10 | VehicleHal/Manager分层提供实际硬件迁移边界，但ICarImpl与Audio内部属性、系统服务耦合不由该边界完整覆盖；未发现单ABI闭源独占，按未封装内部API封顶3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | 旋钮输入与capture/occupant组件有真实交互断言，尚无当前HEAD执行结果和覆盖代理，最高1。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 0/4 | CarAudioService异步init允许返回时初始化未完成，弱化CarSystemService明示的functional后置。getCarService专门wait只能补偿该入口，通用生命周期调用者仍在init返回后调用onInitComplete。 |
| solid_principle.open_closed | 3/4 | 良好遵循。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-15 telecom-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 0/3 | 仓内无版本治理或API baseline，平台源码服务未声明本仓版本。 |
| compilation.ci_independence | 1/3 | 仅 Android 系统 TEST_MAPPING/平台构建 CI，未提供独立标准流水线。 |
| compilation.compilation_independence | 0/3 | 完整生产目标依赖平台外部源码/工具；临时抽出的单类javac成功不构成仓内独立生产构建入口。 |
| platform_reuse.platform_upgrade | 3/10 | 平台服务启动与分析直接引用hidden系统入口，存在迁移路径，按未封装风险3。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | 图执行测试有真实先后关系与结果断言，但无final-HEAD Android执行证明。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 3/4 | 两个生产过滤器均保持CompletionStage结果契约；没有系统化多实现契约执行记录，不能4。 |
| solid_principle.open_closed | 3/4 | 良好遵循。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-16 platform-framework

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 3/3 | api/StubLibraries.bp对当前公开API和last_released签名执行metalava兼容检查，含removed与兼容baseline。 |
| compilation.ci_independence | 1/3 | 真实PREUPLOAD/TEST_MAPPING受Android平台预提交系统调度；无仓库独立完整流水线。 |
| compilation.compilation_independence | 1/3 | SettingsLib/Spa真实生产AAR已在当前HEAD本机构建成功；完整framework依赖平台树。局部生产单元足以排除0，不代表整仓独立构建。 |
| platform_reuse.platform_upgrade | 0/10 | 这是平台框架本身，SystemServer启动、内部资源和Binder运行时为多个核心链路直接依赖；SystemService抽象仅隔离服务生命周期，不提供跨平台替换/fallback。按多核心非稳定接口依赖且缺乏覆盖隔离锁0，不按普通公开API使用扣分。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | UiMode服务夜间模式等行为有真实测试断言；Spa构建没有运行测试，其他当前HEAD执行/覆盖证明缺失，最高1。 |
| solid_principle.dependency_inversion | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.interface_segregation | 3/4 | 良好遵循。 |
| solid_principle.liskov_substitution | 3/4 | 两个真实SystemService子类均初始化并发布Binder，调用者不要求额外前置；boot hook父类允许默认空，不能机械扣分。未证明跨实现异常边界契约测试，不能4。 |
| solid_principle.open_closed | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |

## FW-18 telephony-service

| Leaf | Score | Reason |
|---|---|---|
| compilation.api_version_management | 0/3 | 未找到构建集成的API版本或兼容性基线；平台tag不替代API控制。 |
| compilation.ci_independence | 1/3 | 仅PREUPLOAD调用Android仓外checkstyle；无独立构建测试流水线。 |
| compilation.compilation_independence | 0/3 | telephony-common依赖services、ims/voip及多版本radio HAL生成库和framework-jarjar-rules，源码没有独立SDK模块入口。 |
| platform_reuse.platform_upgrade | 3/10 | 核心电话流程与平台内部服务/HAL绑定，CommandsInterface/RIL提供部分迁移边界但不覆盖全局服务访问；无单架构闭源SO证据，total=3且有迁移路径，3分。 |
| platform_reuse.release_branch_strategy | 0/10 | 本地 refs 未形成可验证的平台/车型 SOP 发布通道；main 和上游来源分支不等于跨平台统一发布。 |
| quality.integration_test | 1/3 | 真实GsmCdmaPhone交互测试有断言和Android配置；未有final HEAD设备执行证明，最高1。 |
| solid_principle.dependency_inversion | 1/4 | 多处违反，设计不合理。 |
| solid_principle.interface_segregation | 1/4 | 多处违反，设计不合理。 |
| solid_principle.liskov_substitution | 0/4 | SIP 生产实现破坏查询结果和异步完成合同：成功回调结果类型不符合父接口，另有请求不完成，触发明确替换违反档。 |
| solid_principle.open_closed | 2/4 | 基本遵循，仍有少量改进空间。 |
| solid_principle.single_responsibility | 2/4 | 基本遵循，仍有少量改进空间。 |
