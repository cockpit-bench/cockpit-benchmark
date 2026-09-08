# Benchmark 虚拟仓生成指导（给 codex）

> 用途：让 codex 生成「拟真生产仓形态 + 满足 benchmark 评分口径」的虚拟仓，用于评分引擎 benchmark。 素材来源：生产环境 gerrit 真实仓 AI 扫描包（app/fw-repo-generator-pack，2026-09-07 用户提供）+ 正式 benchmark 18 仓本地全量画像。 本文档由 mini-benchmark session 整理，用户逐条 review 后定稿（保留 27 条 + 附录权威口径）。

---

## 0. 使用说明与口径权威

### 0.1 ⚠ 评分口径权威声明（铁律）

生产扫描包里 `prompts_standard.json` 的**提示词 / 维度 / 子维度 / 量程 / tiers / checks 全部是旧口径，已作废**。

**评分一律以 benchmark 新口径为准** ＝ `contract-20260903.json` + `benchmark-standard.json`(v0.7.x)：

- **APP 8 叶 / 满分 40**
- **FW 11 叶 / 满分 52**

详见 §9 附录：benchmark 权威评分口径。

生产包里**仍然有效、本文档采用的只有「仓库结构特征」**（synth\_spec 的体量/git/构建/系统API/语言/缺陷规则）——用来把仓「造得像生产」。但「按什么打分」必须走 benchmark，**禁止**从包内 prompts\_standard 取任何维度/量程/embedded rubric/`max:3`。

### 0.2 数据出处

| 数据来源文件    |                                                                                         |
| --------- | --------------------------------------------------------------------------------------- |
| 生产仓库特征    | `app-repo-generator-pack/synth_spec.json`、`fw-repo-generator-pack/synth_spec.json`      |
| 生产仓名清单/规模 | 两包 `structure_report.md`                                                                |
| 生产脱敏方法    | 两包 `generate_guide.md`（virtual-repo-spec skill 方法论）                                     |
| 正式 18 仓画像 | `official-profile.json`（profile\_official.py 逐仓扫描，本地 `.temp/v052-repos`）                |
| 正式仓元数据    | cockpit-benchmark wrapper `manifest.json` + `facts/` + `oracle/` + `ACTIVE_EIGHTEEN.md` |
| 权威评分口径    | `contract-20260903.json` + `benchmark-standard.json`(v0.7.x) + `standard-status.json`   |

### 0.3 状态标签图例

- 🟢 **可用**：生产有真实分布数据，可直接采样
- 🟡 **分歧**：生产口径 vs 正式 benchmark 口径不一致，**两侧都列出，等用户裁定取哪个**
- 🔴 **缺口**：生产未采集，需补/需决定
- 🔵 **权威**：评分口径，照 benchmark

### 0.4 脱敏标记说明（生产包 value\_shape 方法论）

生产扫描为脱敏，对原始值做了形式化替换，理解模式时需知：

- `<A>` ＝ 字母串（alphabetic）
- `<N>` ＝ 数字（number）
- `<M>` ＝ 模块名（module，匿名）
- `E1..` ＝ 枚举匿名标签
- 提交信息、分支名等敏感串均以 `<A>/<N>` 模板呈现，**结构保留、原值脱敏**。

### 0.5 用户裁定记录（2026-09-07）

- **丢弃条目**：原清单 #3 仓库数量规模、#4 APP 体量分布、#5 FW 体量分布、#18 提交历史深度。
  - 丢弃理由（推断）：#3 数量由生成时另行决定；#4/#5 生产规模列口径自相矛盾（synth\_spec 中位 3311 vs structure\_report 规模列中位 21K）且残缺（APP 缺 41%、FW 缺 12%），改用 #28 的正式 3×3 矩阵控制体量；#18 生产浅克隆提交深度=1 是采集 artifact、无拟真价值。
- **保留条目**：#1 #2 #6–#17 #19–#31（共 27 条）+ 附录 #32（权威口径，未点名但被多条依赖，保留）。
- **🟡 分歧条目**：用户本轮只给留/丢，未逐条裁定生产 vs 正式取哪个口径——本文档对每个 🟡 条目**两侧数据都完整保留**，并标「待裁定」，请用户后续逐条定夺。

---

## 1. 仓库群体与类型构成

### 1.1 APP 仓类型构成 🟢（原 #1）

**特征（生产扫描）**

- 来源 host：`icc-gerrit.geely.com:29418`，center：智能座舱分院。
- 生产 APP 全集 **100 仓**，跨 4 个产品线前缀：
  - `FlymeOS2__*`（35 仓）：FlymeOS2 App/Client/Cloud/Media/Net/Telecom/FlymeAuto 子族
  - `FlymeOS__App__*`（61 仓）：FlymeOS 一代 App 主力
  - `zeekos__app__*`（3 仓）：ZeekrBaseMap / internetVehicles / md\_zeekr\_coreservice
  - `ISD__BC__CAP_AVM_APP`（1 仓）：ISD 环视(AVM)
- 功能域多样（从仓名可提取）：账号/云鉴权(Account/CloudAuth)、应用商店(AppStore)、导航(Navi/Map/BaseMap)、音乐媒体(Music/Media/LinkMusic/OutCarMedia)、相机影像(Camera/XCCamera360/DVR/Rearview/ParkingPhoto/AVM)、语音(Aicy/VoiceInteract)、设置(Settings/AudioSettings/ConnectivitySettings)、桌面壁纸(WallpaperLauncher/WallpaperControl)、场景引擎(SceneEngine/SceneAssist/SceneDirector)、系统UI插件(SystemUIPlugin)、能耗(Energy)、数字钥匙(DigitalKey/KeyServer)、健康检测(HealthDetection)、TBox/车联(TBoxClient/MergeMobileConnect/internetVehicles)、VR/3D/矢量引擎(VRMiddleware/Auto3DEngine/VectorEngine)、推送(PushNotification)、权限(PermissionPlugin/PolicyAutoSDK)、说明书(UserManual/ManualApp)、销售助手(StaticSalesAssistant)、人流(PeopleCar)、智能按钮(SmartButton)、车控(ControlBoard)、云上传(CloudUpload)、天气/位置/数据(Cloud Weather/Location/Data)、车内通话(InCallUI/NetContact)、原子能力/设备共享/ caralive/appalive 等。

**多样性（分布/采样指导）**

- **不是单一形态**：多产品线（FlymeOS / FlymeOS2 / zeekos / ISD）× 多功能域（≥30 种车机 App 功能）。
- 生成虚拟 APP 仓时应覆盖不同功能域，避免全是 settings/launcher 一类。
- 产品线前缀可作为「代际/品牌」多样性维度（一代 FlymeOS、二代 FlymeOS2、Zeekr 系、ISD 系）。

**正式 benchmark 现状（对照）**

- 正式 9 个 active APP 仓全是 **AOSP Car 应用改编**：aurora-settings(Car/Settings)、horizon-launcher(Car/Launcher)、climatix-hvac(Car/Hvac)、cockpit-shell(Car/SystemUI)、atlas-settings(nxp Car/Settings)、nova-launcher(radiosound Car/Launcher) + 3 个纯合成(motion-control/market-hub/thermo-control)。
- 功能域偏窄：基本是 settings/launcher/hvac/systemui 四类 + 合成。

**分歧/裁定**

- 🟡 生产功能域极广（30+ 种）vs 正式仅 4–5 类。拟真生产应大幅扩展功能域覆盖。

### 1.2 FW 仓类型构成 🟢（原 #2）

**特征（生产扫描）**

- 来源 host：`zuocanggerrit-prod.geely.com:29418`，center：智能座舱分院。
- 生产 FW 全集标题 **119 仓**（synth\_spec `n_repos=105`、activity 分布按 `94` 计——**三处数字自相矛盾**，见 §6.4 备注）。构成：非AOSP 25 + external/packages 94。
- 三大类型（按仓名归类）：
  - *AOSP external/ OSS 上游（≈69 仓，58%）*\*：FXdiv、OpenCSD、adeb、androidplot、angle、apache-commons-compress、autotest、boringssl、bouncycastle、capstone、curl、deqp-deps(SPIRV-Headers/Tools)、dexmaker、drrickorang、dynamic\_depth、f2fs-tools、fdlibm、fec、flatbuffers、gemmlowp、google-breakpad、google-fonts、guice、icu、igt-gpu-tools、iproute2、ipsec-tools、iptables、iputils、iw、jarjar、javaparser、javasqlite、jcommander、jline、junit-params、kotlinx.coroutines、libcap、libdivsufsort、libdrm、libese、libevent、libgav1、libprotobuf-mutator、libunwind\_llvm、libvpx、libxaac、llvm、lzma、nanohttpd、neon\_2\_sse、oss-fuzz、python(cpython3/futures/ipaddress/pyasn1/six)、rust crates(byteorder/libc/unicode-xid)、scapy、skqp、smali、sonic、strace、unicode、vulkan-validation-layers、wayland-protocols、webp。
  - *AOSP packages/ 框架/应用/模块/provider（≈25 仓，21%）*\*：packages/apps(BasicSmsReceiver/Calendar/Car Messenger/Car Notification/Car Radio/Car SystemUpdater/CellBroadcastReceiver/DevCamera/Gallery/Music/Stk/StorageManager/TV/Traceur)、packages/modules(ArtPrebuilt/CellBroadcastService/NetworkPermissionConfig/NetworkStack/SdkExtensions)、packages/providers(CalendarProvider)、vendor/ecarx packages(MediaFocusTest/BluetoothEnhancement)。
  - **vendor 专有（≈25 仓，21%）**：Geely(GeelyFramework/GeelyFrameworkAPI/GeelyAdapter)、ICVSBG-CHUDC E04 SE1000\_SDK(deploy/android\_trusty\_tee/audio/m4firmware/siengine/toolchain)、E04 Security\_OS、JICA\_Dev E02\_ANDROID9(UpdateService/compatibility/development/kernel/libnativehelper/vendor jica interfaces: audiocontrol/diagbusiness/diagnostic/gnss/jicapower/system/tcam udsApp/vendor mediatek firmware)、vendor flyme frameworks/base、Android\_OEM ecarx adaptapi\_dev、Android\_Venus ecarx gnss\_release。

**多样性（分布/采样指导）**

- **三大类形态迥异，必须按比例配比**：
  - OSS external（58%）＝纯 C/C++ 上游库、巨型（百万行级）、make/cmake、零 Android IPC、无 AIDL、英文社区提交。
  - packages 框架（21%）＝Android Java/AIDL、中等体量、Soong/Make。
  - vendor 专有（21%）＝混合（C/Java）、平台/车型绑定、gerrit 工作流。
- 这是 FW 多样性的**主轴**：不配比就会全造成一类。

**正式 benchmark 现状（对照）**

- 正式 9 个 active FW 仓**全是一方 Car-service 改编**（vehicle-property-service、vehicle-hal-adapter、vehicle-diagnostics、soa-gateway、update-manager-service、car-runtime-service、platform-compat-service、vehicle-platform-service、cockpit-manager-kit），改编自 AOSP `packages/services/Car`。
- **缺 OSS external 类、缺 vendor 专有类**——只覆盖了生产 FW 的「packages 框架」一类的变体。
- type\_gate 实测：java\_kotlin 主导、aidl 丰富、native 少量、`forbidden_embedded_anchors []`（明确非嵌入式）。

**分歧/裁定**

- 🟡 生产 FW ＝ OSS+packages+vendor 三合一（C 为主）；正式 FW ＝ 纯一方 Java/AIDL 车服务。
- **拟真前必须先定：造哪一类？** 若目标是「像生产 FW 全集」→ 要按比例造三类（含纯 C OSS 巨仓）；若目标是「像正式 benchmark FW」→ 造 Android Java/AIDL 车服务。两者语言/构建/体量/IPC 全都不同（详见 §2.1、§3.1、§5.2、§5.4）。

---

## 2. 语言与接口构成

### 2.1 FW 语言/扩展概率 🟡（原 #6）

**特征（生产扫描）**

- `required_files` 每仓独立存在概率（FW synth\_spec）：
  - `.c` → **0.7**
  - `.h` → **0.7**
  - `.java` → **0.5**
  - `.cpp` → **0.3**
- synth\_spec note：「FW 仓多为 Android 平台/framework 仓（make/cmake 混合），**非纯 C 固件**」。即 C/C++ 与 Java 并存。
- 注：概率为「每仓是否含该扩展」的独立伯努利概率，非占比。

**多样性（分布/采样指导）**

- 按概率采样：约 70% 的 FW 仓含 .c/.h，50% 含 .java，30% 含 .cpp。
- 结合 §1.2 类型：OSS external 仓应几乎必含 .c/.h（纯 C），vendor/packages 仓更可能含 .java。

**正式 benchmark 现状（对照）**

- 正式 FW 语言构成（9 仓聚合）：**.java 5321 + .aidl 1136** 主导，.xml 2777、.h 316、.cpp 313、.bp 189、.mk 42、.cc 1。
- 即正式 FW 是 **Android Java/AIDL 框架服务**，C/C++ 仅少量（每仓 \~35 个 .h/.cpp）。

**分歧/裁定**

- 🟡 **语言重心相反**：生产 FW＝C/C++ 为主（.c/.h 0.7）；正式 FW＝Java/AIDL 为主。
- 待裁定：虚拟 FW 仓走 C 系（像生产 external/vendor）还是 Java/AIDL 系（像正式 Car 服务）。**这决定了 §3.1 构建、§5.2 IPC、§5.4 嵌入式特征的全部走向，是 FW 侧最大的范式开关。**

### 2.2 APP 语言构成 🔴（原 #7）

**特征（生产扫描）**

- 生产 APP synth\_spec **未给扩展名概率**（只有 gradle 模块 pattern，无 .java/.kt/.xml 语言占比）——**这是缺口**。
- generate\_guide 方法论层面声明 APP 核心产物＝`build.gradle + .java/.kt`。

**多样性（分布/采样指导）**

- 生产侧无量化分布，只能从正式仓反推（见下）或按经验补：Java 主、Kotlin 次、XML 资源大量。

**正式 benchmark 现状（对照，可作补位数据）**

- 正式 APP 语言构成（9 仓聚合）：**.java 3375 / .xml 4375 / .kt 481 / .aidl 49 / .bp 54 / .gradle 51 / .kts 14**。
- 逐仓差异大：
  - 纯 Java 系（AOSP 改编）：aurora-settings(.java 1098/.xml 594)、atlas-settings(.java 1100/.xml 394)、cockpit-shell(.java 614/.xml 1281/.kt 73/.aidl 29)。
  - Kotlin 系（合成/小仓）：climatix-hvac(.kt 118/.java 21)、thermo-control(.kt 152/.java 2)。
  - 资源重（launcher 类）：horizon-launcher(.xml 731/.java 187/.kt 68)、nova-launcher(.xml 740/.java 276/.kt 70)。
  - XML 主导（合成）：motion-control(.xml 351/.java 39)、market-hub(.xml 206/.java 38)。

**分歧/裁定**

- 🔴 **缺口**：生产未采 APP 语言分布。建议用正式 18 仓的实测构成作为补位分布（Java/Kotlin/XML 三档），或由用户给定目标比例。

### 2.3 AIDL 存在与密度 🟡（原 #8）

**特征（生产扫描）**

- 生产 FW `required_files` **不含 .aidl**（只列 .c/.h/.java/.cpp）——生产 FW 扫描**没把 AIDL 当采集轴**。
- 生产 FW synth\_spec system\_api 里也无 aidl 字段。
- 生产 APP synth\_spec：`aidl 572`（全 100 仓合计），即 **≈5.7 个 .aidl/仓**。

**多样性（分布/采样指导）**

- APP：约 5–6 个 .aidl/仓（生产均值）。
- FW：生产未采，但 AIDL 是 Android framework 仓的接口核心，若造 Java 系 FW（§2.1 裁定）则必须补 AIDL。

**正式 benchmark 现状（对照）**

- 正式 **FW .aidl 合计 1136 个 ＝ ≈126 个/仓**（vehicle-diagnostics 217、soa-gateway 136、platform-compat 278、vehicle-platform 121、vehicle-hal-adapter 101…）——AIDL 极丰富。
- 正式 APP .aidl 合计 49 ＝ ≈5.4 个/仓（cockpit-shell 29、motion-control 7、market-hub 7、climatix-hvac 5、thermo-control 1）——与生产 APP 5.7/仓**吻合**。

**分歧/裁定**

- 🟡 APP AIDL 密度生产(5.7)≈正式(5.4)，一致，可直接用。
- 🟡 FW AIDL：生产**漏采**（required\_files 不含），正式 126/仓。若虚拟 FW 走 Java 系，AIDL 密度应参照正式（百级/仓），不能照生产（生产根本没这轴）。**这是生产包的一个采集盲区。**

---

## 3. 构建体系

### 3.1 FW 构建体系比例 🟡（原 #9）

**特征（生产扫描）**

- FW synth\_spec `build_systems` 频率：**make 27 / cmake 27 / gradle 4**（合计 58 仓有构建信息）。
  - 换算比例：make ≈ 47%、cmake ≈ 47%、gradle ≈ 7%。
  - note：「make(Android.mk/Makefile) 是主流；cmake 次之；少量 gradle」。
- **生产包未建模 Soong / Android.bp**（build\_systems 只有 make/cmake/gradle 三类）。
- template 字段：「`cmake_template/`（CMakeLists.txt+mod.c 骨架）；**另需 make\_template(Android.mk) 因 make 是主流**」——但包内**只给了 cmake\_template，缺 make/Android.mk 模板**。

**多样性（分布/采样指导）**

- 按 make\:cmake\:gradle ≈ 47:47:7 采样构建体系。
- 结合 §1.2：OSS external 仓多 make/cmake（上游自带），vendor/packages 仓可能 Android.bp/mk。

**正式 benchmark 现状（对照）**

- 正式 FW 构建（9 仓聚合）：**Soong/Android.bp 主导（.bp 189 个）** + Android.mk 42 + CMakeLists.txt（多仓有 native/ 子构建）+ gradle 极少（soa-gateway/cockpit-manager-kit 有 settings.gradle）。
- 逐仓：vehicle-diagnostics(.bp 88)、platform-compat(.bp 45)、update-manager(.bp 42)、vehicle-hal-adapter(.bp 6 + 多 .cmake)、vehicle-platform(.bp 4 + .mk 26 + apicheck.mk)、car-runtime(.bp 1)、vehicle-property(.bp 3 + CMakeLists 8)、soa-gateway(build.gradle 4 + CMakeLists 7)、cockpit-manager-kit(settings.gradle + build.gradle 4 + CMakeLists 4)。

**分歧/裁定**

- 🟡 **生产 FW＝make/cmake（无 Soong）；正式 FW＝Soong/Android.bp 主导。** 构建体系不一致。
- 🟡 **生产包模板缺口**：缺 make/Android.mk 模板（自己声明需要却没给）、缺 Soong/Android.bp 模板。
- 待裁定：虚拟 FW 构建走 make/cmake（像生产）还是 Soong（像正式）。**与 §2.1 语言开关联动**：C 系→make/cmake；Java/AIDL 系→Soong/Android.bp。

### 3.2 APP 构建体系 🟡（原 #10）

**特征（生产扫描）**

- 生产 APP synth\_spec **只有 gradle**（gradle.modules\_per\_repo / module\_patterns / impl\_deps），**无 Soong/Android.bp 建模**。
- app 包模板 `gradle_template/`：settings.gradle + app/build.gradle + AndroidManifest.xml，namespace `com.geely.mod`、compileSdk 34、minSdk 29、targetSdk 34。

**多样性（分布/采样指导）**

- 生产 APP＝纯 gradle。多样性体现在模块数/模块名/依赖（见 §3.3–3.5），构建工具本身单一。

**正式 benchmark 现状（对照）**

- 正式 APP 9 仓：**Gradle 6 仓 + Soong/Android.bp 3 仓**。
  - Gradle：aurora-settings(settings.gradle+build.gradle 4)、atlas-settings(同)、climatix-hvac(build.gradle.kts 8)、motion-control(build.gradle 12)、market-hub(build.gradle 12)、thermo-control(build.gradle.kts 3)。
  - Soong：horizon-launcher(.bp 15 + gradle 5)、cockpit-shell(.bp 23 + gradle 3 + Android.mk + CMakeLists)、nova-launcher(.bp 16 + gradle 5 + CMakeLists)。

**分歧/裁定**

- 🟡 生产 APP 纯 gradle vs 正式 APP 1/3 带 Soong。待裁定虚拟 APP 是否引入 Soong（若引入则更贴近正式 benchmark 的 AOSP 改编形态；若纯 gradle 则更贴近生产 gerrit app 形态）。

### 3.3 Gradle 模块数分布 🟢（原 #11）

**特征（生产扫描）**

- APP synth\_spec `gradle.modules_per_repo`：**min 1 / median 1 / max 14**。

**多样性（分布/采样指导）**

- 多数 APP 仓单模块（median 1），少数多模块至 14。
- 采样建议：偏态分布，\~50% 仓 1 模块，长尾到 14。

**正式 benchmark 现状（对照）**

- 正式 APP manifest `module_count`：aurora 4、horizon 8、climatix 7、motion-control 11、market-hub 11、cockpit-shell 18、atlas 4、nova 9、thermo 2。
- 正式 APP 模块数中位 ≈ 8（远高于生产中位 1）。

**分歧/裁定**

- 🟢 生产分布可用（min1/med1/max14）。注意正式集模块数普遍偏高（中位 8），若拟真生产应让多数仓回到 1–2 模块。

### 3.4 Gradle 模块名频率 🟢（原 #12）

**特征（生产扫描）**

- APP synth\_spec `gradle.module_patterns`（模块名→出现仓数，全 100 仓）：
  - `:app` → **49**
  - `:base` → 6
  - `:common` → 6
  - `:core` → 5
  - `:camera_common` → 5
  - `:app-bridge` → 3
  - `:camera_sdk` → 3
  - `:org.eclipse.paho.android.service` → 2
  - `:lib-base` → 2
  - `:lib-mqtt` → 2

**多样性（分布/采样指导）**

- `:app` 主导（49/100 仓有），库型模块名 `:base`/`:common`/`:core`/`:lib-*` 次之，功能型 `:camera_*`/`:app-bridge`/`:*-mqtt`/`paho` 长尾。
- 命名风格：小写、连字符分词（app-bridge、lib-base、camera\_common 混用下划线/连字符）。
- guide 另声明 APP 包名规范 `com.geely.<module>`（正式仓未遵循，见 §1.1）。

**正式 benchmark 现状（对照）**

- 正式 APP gradle 模块名（settings include 实测）：aurora/atlas 用 AOSP 风格（settings-common/settings-connectivity/settings-security 等子目录），motion-control/market-hub 用 `com.cockpitbench.foundation.*`（foundationapi/foundationcore/foundationobservability），climatix/thermo 是 kts 单/双模块。
- 正式仓模块名**不复现生产的 \:app/\:base/\:common/\:basesdk 命名习惯**。

**分歧/裁定**

- 🟢 生产模块名频率表可直接用于采样「像生产」的模块命名。正式仓命名是另一套（AOSP/cockpitbench 风格）。

### 3.5 Gradle 依赖频率 🟢（原 #13）

**特征（生产扫描）**

- APP synth\_spec `gradle.impl_deps`（`implementation project(:x)` 依赖名→出现仓数，全 100 仓）：
  - `:basesdk` → **82**
  - `:base` → 27
  - `:eas-api-base-core` → 17
  - `:common` → 15
  - `:app-bridge` → 11
  - `:camera_common` → 10
  - `:eas-api-proxy` → 10
  - `:eas-api-ext` → 6
  - `:core` → 5
  - `:CommonLib` → 4

**多样性（分布/采样指导）**

- `:basesdk` 是**近乎全仓公共依赖**（82/100）——生产 APP 高度共享一个 base SDK。
- `:eas-api-*`（base-core/proxy/ext）是 EAS（企业应用服务？）API 族，成体系。
- 依赖结构反映「公共 SDK + API 分层 + 功能库」的真实组织。
- 对应评分：依赖解耦/组件化证据（architecture.decoupling、architecture.componentization）。

**正式 benchmark 现状（对照）**

- 正式 APP `implementation project()` 依赖数：motion-control 20、market-hub 20、horizon 3、nova 3、aurora 3、atlas 2、cockpit-shell 1、climatix 0、thermo 0。
- 正式仓依赖名是 cockpitbench/AOSP 内部模块，**无 \:basesdk 这种全仓公共依赖**。

**分歧/裁定**

- 🟢 生产依赖频率表可用。`:basesdk`(82%) 这种「全仓共享基础 SDK」是生产 APP 的强特征，正式集没有——拟真时应考虑加入。

---

## 4. Git 形态

### 4.1 分支数分布 🟡（原 #14）

**特征（生产扫描）**

- APP synth\_spec `git.branches_per_repo_med` = **77**（branch\_strategy.activity 同值）。
- FW synth\_spec `git.branches_per_repo_med` = **71**，note：「gerrit 多分支（均 71/仓）；master 空，代码在 bugfix/dev 分支」。
- FW `branch_strategy.auto_branch` note：「gerrit auto 分支由 CI 系统创建，格式 `auto/<base>/<id>`」。
- 采集方式 note：「git\_full 采集；shallow clone」。

**多样性（分布/采样指导）**

- 生产 gerrit 仓分支极多（中位 71–77），构成＝主干 + 多版本 release/sop 分支 + CI 自动分支（`auto/*`）+ gerrit review refs。
- ⚠ **可比性警告**：77/71 这个数包含 gerrit 特有的 `auto/*` CI 分支与 review refs，**与 GitHub/GitLab 式「人工分支数」不是一个口径**。直接照 77 造分支会造出一堆 CI 自动分支。
- 采样建议：若要拟真 gerrit 形态，需区分「人工分支（release/sop/dev，数个～数十个）」与「CI 自动分支（auto/\*，可大量）」。

**正式 benchmark 现状（对照）**

- 正式仓分支数：APP 中位 **5**（5–8），FW 中位 **6**（5–7）。
- 逐仓：aurora 5、horizon 6、climatix 5、motion-control 7、market-hub 5、cockpit-shell 5、atlas 8、nova 6、thermo 5；vehicle-property 5、hal-adapter 6、diagnostics 6、soa-gateway 6、manager-kit 5、update-manager 6、car-runtime 5、platform-compat 6、vehicle-platform 7。
- 正式仓**无 auto/\* CI 分支**，分支都是人工策划（develop/main/platform/release/sop）。

**分歧/裁定**

- 🟡 生产 71–77 分支/仓（含 CI 自动分支）vs 正式 5–8 分支/仓（纯人工）。差 13–15×。
- 待裁定：虚拟仓分支拓扑走生产 gerrit 富分支（需含 auto/\* 与多版本）还是正式精简分支。注意 benchmark 的 release\_branch\_strategy 叶（0–10）评分依赖分支形态——分支太少可能压不住该叶的区分度。

### 4.2 分支命名分类法 🟢（原 #15）

**特征（生产扫描）**

- 生产真实分支名（从 prompts\_standard checks 与 synth\_spec 提取，**属旧口径维度但分支「名称形态」是仓库特征，保留**）：
  - 平台主干：`origin/main`（=E06 平台）、`origin/main_8295`（8295 平台）、`origin/main_e04`（e04 平台）
  - SOP 车型分支：`origin/sop/flymeauto2.0.0.j1/q8295_p789`（8295 平台 p789 车型）、`origin/sop/flymeauto2.0.5.j1/e04_p171-a1`（e04 平台 p171-a1 车型）、`origin/sop/flymeauto2.0.0.j1/q8295`（8295 平台通用）、`origin/sop/flymeauto2.0.0.j1`（全平台通用，实际「现在看不到，没做到全平台通用」）
  - release 分支：`release/flymeauto2.3.0.e02`
  - CI 自动分支：`auto/<base>/<id>`
- 命名要素：平台代号（E06/8295/e04/e02）+ flymeauto 版本号（2.0.0/2.0.5/2.3.0）+ 车型代号（p789/p171-a1/q8295）+ 后缀（-a1/-a2/j1）。

**多样性（分布/采样指导）**

- 分支名携带「平台×版本×车型」三维信息，组合爆炸→每仓可有数十个 sop/release 分支。
- 平台后缀（\_8295/\_e04/\_e02）、车型后缀（\_p789/\_p171-a1）、版本号（X.Y.Z）是命名多样性的来源。

**正式 benchmark 现状（对照）**

- 正式仓分支名（虚构简化）：`main`、`develop`、`platform/8155`、`platform/8295`、`platform/xinqing`、`release/2026.1`、`release/1.0`、`release/2.0`、`release/0.8`、`release/0.9`、`release/sop-2024`、`release/sop-2025`、`release/sop-2019`、`sop/2026.1-model-a1`、`sop/2026.1-model-b2`、`sop/2024-model-a1`、`sop/2024-model-b2`、`presubmit/launcher-contracts`；FW 改编残留：`aosp-new/aosp-new/master`、`aosp/pie-release`。
- 正式用 `platform/8295`（≈生产 main\_8295）、`sop/YEAR-model-aN`（≈生产 sop/...q8295\_p789）、`release/YEAR.N`（≈生产 release/flymeauto2.3.0）——**概念对应但命名抽象化**，且**不含 flymeauto 版本号串**。

**分歧/裁定**

- 🟢 分支命名「形态」是有效仓库特征，生产真名（flymeauto 版本号 + 平台/车型后缀）可作拟真素材。
- ⚠ 注意：生产旧 prompts 里有 `single_platform_branch_template`/`cross_platform_branch_template` 两个维度**硬解析 flymeauto 版本号**做打分——但这两个维度在 benchmark 新契约里**已作废**（§9），新契约分支相关只有通用叶 `platform_reuse.release_branch_strategy`(0–10)。所以**虚拟仓分支名含不含 flymeauto 串，对新口径评分无影响**；是否复刻真名纯看「拟真度」诉求，不影响打分。

### 4.3 tag 分布 🟡（原 #16）

**特征（生产扫描）**

- APP synth\_spec `branch_strategy.activity.tag_count`：min 0 / median 0 / max 0 / **distribution {"0": 100}**（全 100 仓零 tag）。
- APP `tag_time_span`：earliest "?"、latest "?"、total\_tags\_with\_dates **0**。
- FW synth\_spec `tag_count`：min 0 / median 0 / max 0 / **distribution {"0": 94}**（全 94 仓零 tag）。
- FW `tag_time_span`：total\_tags\_with\_dates **0**。
- 即：**生产真实 gerrit 仓完全不用 tag**（退化分布，全 0）。

**多样性（分布/采样指导）**

- 生产侧 tag 无多样性（恒为 0）——这本身是一个强特征：**gerrit 工作流靠分支不靠 tag**。
- generate\_guide 方法论提示：「tag 数 = 活跃度指标（commit 数可能是快照=1）」——但生产实测 tag 恒 0，所以活跃度只能靠分支数/commit 体现，不能靠 tag。

**正式 benchmark 现状（对照）**

- 正式仓**每仓注入 tag**：APP 中位 1（atlas-settings 有 7 个：android-10.0.0\_r7\~r14 + local-sop-2024.4；motion-control/market-hub 各 2：app-foundation-1.0.0 + -2026.1），FW 中位 1（v2.0.0 / local-sop-2026.1 / -2026.1 等）。
- 正式仓 tag 命名：`v<X.Y.Z>`、`local-sop-<YEAR>.<N>`、`<repo>-<YEAR>.<N>`、`app-foundation-1.0.0`、AOSP 残留 `android-10.0.0_r*`。

**分歧/裁定**

- 🟡 **生产零 tag vs 正式每仓有 tag。** 直接冲突。
- 关键考量：benchmark 的 `compilation.api_version_management` 叶（0–3）评分**部分依赖版本证据**。facts 里 aurora 的 api\_version 证据用了 version.properties + RELEASE\_NOTES.md + build.gradle versionName，并明确注「**Git tags are not version records**」（tag 不算版本记录）。
- 待裁定：虚拟仓是否注入 tag。若拟真生产→零 tag（版本证据改走 version 文件/CHANGELOG/gradle versionName）；若对齐正式→注入 tag。**注意：即便注入 tag，新口径也不把它当版本管理证据**，所以零 tag + 版本文件 是更贴近生产且不影响评分的组合。

### 4.4 master 语义 🟢（原 #17）

**特征（生产扫描）**

- FW synth\_spec `branch_strategy.rules` **R1**（确定性规则）：
  - condition：「master is empty (Initial empty repository)」
  - action：「checkout first non-master branch (bugfix/dev/release) to get real code」
  - note：「gerrit 工作流：master 只是占位，真实代码在 feature 分支」
- FW synth\_spec note：「FW 仓为 gerrit 工作流（**master 空 + 代码在 feature/dev 分支**）；提取前需切到非 master 分支」。
- FW `master_commit_count`：min1/median1/max1/distribution {"1":94}（master 上只有 1 个占位 commit「Initial empty repository」）。
- APP `master_commit_count`：min0/median1/max1/distribution {"1":85, "0":15}（APP master 多为 1 commit 快照，15 仓 0 commit）。
- 采集 note：「shallow clone→commit\_count=1/branch」。

**多样性（分布/采样指导）**

- **FW 确定性规则**：master 必空（仅 Initial empty repository 占位 commit），真实代码在非 master 分支（bugfix/dev/release）。这是 gerrit FW 仓的硬形态，无随机性。
- APP：master 多为单 commit 快照（85% 有 1 commit，15% 空）。
- 缺陷关联：FW D05「master 保留代码（非空 master）＝违反 gerrit 工作流」→ 低分（见 §6.2）。

**正式 benchmark 现状（对照）**

- 正式仓 **main 为默认分支且承载全部代码**（GitHub main-default 模型），另有 develop 分支。
- 正式仓**不复现「空 master」**：master/main 上就是完整代码树。
- FW 改编仓有残留分支 `aosp-new/aosp-new/master`、`aosp/pie-release`（AOSP 镜像改编痕迹），但不是 gerrit 式空 master。

**分歧/裁定**

- 🟢 生产 FW「空 master + 代码在 feature 分支」是明确的确定性规则，可作拟真素材。
- 🟡 但与正式仓（main 承载代码）冲突，且与 benchmark 评分链路冲突——**评分引擎克隆仓后默认在 main/master 上跑评估**（平台 clone→checkout 默认分支→LangGraph DAG）。若虚拟仓照生产造「空 master」，引擎在默认分支上会看到空树→评估失败/全 0。
- ⚠ **重要约束**：除非评分引擎/克隆逻辑显式支持「checkout 非 master 分支」（生产 R1 规则），否则虚拟仓**不能造空 master**，必须让代码在默认分支。这是「拟真生产」与「可被引擎评分」的直接矛盾点，需用户/平台侧裁定（要么引擎支持切分支，要么放弃空 master 形态）。

### 4.5 提交信息语言/风格 🟢（原 #19）

**特征（生产扫描）**

- APP synth\_spec `branch_strategy.activity.commit_msg_patterns_top`（脱敏，`<A>`=字母串 `<N>`=数字）：
  1. `<A> <A> <A>`
  2. `[<A><N>][自研测试][<A><N>.<N>][实车][流媒体后视镜][必现]实车流媒体后视镜画面加载不出来`
  3. `<A>流水线切换`
  4. `<A> <A>-<N> 【<A><N>-<A>】【<A><N>】【云交互】【小<A>测试】【账号中心】【必现】<A>弹窗`
  5. `<A> <A>-<N> 副驾桌面应用建议卡片显示两个浏览器，点击打开后不显示腾讯视频图标`
- FW synth\_spec `commit_msg_patterns_top`：仅 `<A> <A> <A>`（1 条，脱敏后无结构信息）。
- 风格特征：APP＝**中文 + 缺陷单/工单格式**，多标签前缀 `[项目][测试类型][版本][环境][模块][复现性]` + 中文问题描述；含「流水线切换」这类 CI 操作提交。

**多样性（分布/采样指导）**

- APP 提交信息多样性高：缺陷单（多标签）、流水线操作、功能描述，全中文。
- 标签维度：测试类型（自研测试/小A测试）、环境（实车）、复现性（必现）、模块（流媒体后视镜/账号中心/云交互）、版本号。
- FW 提交信息：生产脱敏后无有效样本（仅 `<A><A><A>`），无法提取风格——**FW 提交风格是缺口**。

**正式 benchmark 现状（对照）**

- 正式仓**全英文 Conventional Commits**（CJK 提交数 = 0）：
  - 前缀分布：feat: / fix: / build: / ci: / docs: / refactor: / test:
  - 样例：`feat: govern settings API and isolate platform properties`、`build: standardize Android source roots`、`ci: verify standalone AAOS boundary`、`refactor: align native adapter with Android Framework scope`、`feat: add embedded vehicle property boundary`、`docs(platform): record peer credential portability path`。
  - conventional 前缀占比：APP 各仓 5–26 条不等（thermo 16/16 全 conventional、motion-control 26/26），FW 类似。

**分歧/裁定**

- 🟢 生产 APP 中文缺陷单风格是强特征，可作拟真素材（含标签结构）。
- 🟡 **语言相反**：生产 APP＝中文缺陷单；正式＝英文 Conventional Commits。
- 🔴 生产 FW 提交风格未采（缺口）。
- 待裁定：虚拟仓提交信息走中文缺陷单（像生产 APP）还是英文 conventional（像正式）。注意：若有依赖提交文本的判定（如分支识别曾解析提交时间戳），语言变化可能影响——但新口径下提交语言不直接进评分叶，纯拟真度考量。

---

## 5. 系统 API / IPC / 反射

### 5.1 系统 API 密度 🟡（原 #20）

**特征（生产扫描）**

- APP synth\_spec `system_api`：total **2190**、per\_repo\_med **0**、reflection 1240、ipc 12490、aidl 572。
  - `per_repo_med 0` ＝ **极端偏态**：超过半数 APP 仓系统 API 命中为 0，总量 2190 集中在少数 SDK/service 仓。
- FW synth\_spec `system_api`：total **492**、per\_repo\_med **0**、reflection 1949、ipc 5689。
  - 同样 per\_repo\_med 0（FW 系统 API 总量更低，492，因多数是 OSS external 纯 C 仓不碰 Android 系统 API）。
- 系统 API 采集口径（从模板 mod.c 注释）：`SystemProperties` / `__system_property_get` / `ServiceManager`。

**多样性（分布/采样指导）**

- **中位 0 是关键**：多数仓不碰系统 API，少数仓密集。不能用均值（APP 21.9/仓）造每个仓——要造偏态（大部分 0，少数高）。
- 结合 §1.2：OSS external 仓系统 API≈0；vendor/framework 仓才有 SystemProperties/ServiceManager。

**正式 benchmark 现状（对照）**

- 正式 APP（9 仓聚合）：sysprops **289**（≈32/仓）、servicemgr **132**（≈15/仓）——**每仓都有，分布均匀**，无「中位 0」偏态。
- 正式 FW（9 仓聚合）：sysprops **714**（≈79/仓）、servicemgr **356**（≈40/仓）、sdkint **243**——同样均匀且密度高。
- 逐仓 sysprops：thermo-control 205（异常高，热管理仓大量系统属性）、car-runtime 308、aurora 21、atlas 21、其余多为个位～几十。

**分歧/裁定**

- 🟡 **生产极端偏态（中位 0）vs 正式均匀铺开（每仓 32–79）。** 分布形态相反。
- 待裁定：虚拟仓系统 API 走生产偏态（多数仓 0，少数密集）还是正式均匀。拟真生产应造偏态。

### 5.2 IPC 密度 🟡（原 #21）

**特征（生产扫描）**

- APP synth\_spec：ipc total **12490**（≈125/仓），但 per\_repo\_med 0 暗示**高度集中**（少数仓扛大部分 IPC）。
- FW synth\_spec：ipc total **5689**（≈54/仓）。
- IPC 采集口径（模板 mod.c 注释）：`Parcel` / `BpBinder` / `IBinder` / `binder` / `someip` / `dbus`。

**多样性（分布/采样指导）**

- APP IPC 集中在含 AIDL/Binder 的 service 仓；OSS/纯 UI 仓 IPC≈0。
- FW IPC：OSS external 仓≈0（curl/boringssl 无 Binder），vendor/framework 仓才有。

**正式 benchmark 现状（对照）**

- 正式 APP（9 仓）：binder\_ipc **473**（≈53/仓）——比生产 APP 均值(125)低，但分布均匀（每仓都有）。
- 正式 FW（9 仓）：binder\_ipc **7557**（≈**840/仓**）、aidl\_kw 1515——**是生产 FW 均值(54)的 \~15×**。
- 逐仓 FW binder\_ipc：platform-compat 1995、update-manager 1304、diagnostics 1155、soa-gateway 971、vehicle-platform 780、hal-adapter 678、manager-kit 288、vehicle-property 289、car-runtime 97。

**分歧/裁定**

- 🟡 APP：生产均值 125（偏态）vs 正式 53（均匀）——量级相近但分布不同。
- 🟡 **FW：生产 54/仓 vs 正式 840/仓（15×差距）。** 因正式 FW 全是 Binder-heavy Car 服务，生产 FW 多为 OSS external（零 IPC）拉低均值。
- 待裁定：与 §2.1/§1.2 语言/类型开关联动——造 Java/AIDL 车服务则 IPC 高（像正式），造 OSS external 则 IPC≈0（像生产多数 FW 仓）。

### 5.3 反射密度 🟢（原 #22）

**特征（生产扫描）**

- APP synth\_spec：reflection **1240**（≈12.4/仓）。
- FW synth\_spec：reflection **1949**（≈18.6/仓）。
- 反射采集口径（模板 mod.c 注释）：`dlopen` / `dlsym` / `Class.forName` / `getDeclaredMethod`。
- 缺陷关联：APP D04「dlopen/dlsym 反射」detect\_rule `nonstd_api_count>20`；FW D02「添加 dlopen/dlsym」detect\_rule `nonstd_api_count>20`（见 §6）。

**多样性（分布/采样指导）**

- APP 反射 \~12/仓、FW \~18/仓（均值）；FW 反射密度高于 APP（因 C 仓 dlopen/dlsym + Java 仓 Class.forName 并存）。
- 与系统 API 同样可能偏态（OSS 仓 dlopen 多用于插件加载）。

**正式 benchmark 现状（对照）**

- 正式 APP（9 仓）：reflection **75**（≈8.3/仓）——略低于生产 12.4。
- 正式 FW（9 仓）：reflection **115**（≈12.8/仓）——低于生产 18.6。
- 逐仓：thermo-control 23、nova-launcher 23、diagnostics 19、update-manager 15、hal-adapter 13、vehicle-platform 12，其余个位。

**分歧/裁定**

- 🟢 量级相近（正式略低于生产），可直接用生产均值作采样目标。偏态/均匀之争同 §5.1。

### 5.4 FW 嵌入式特征 🟡（原 #23）

**特征（生产扫描）**

- FW synth\_spec defects 涉及的嵌入式/底层特征：
  - D02「添加 dlopen/dlsym」detect\_rule `nonstd_api_count>20`（applies\_to 平台升级影响）
  - D03「`#include <private/internal.h>`」detect\_rule `nonstd includes private/`（applies\_to 平台升级影响）
- 生产 FW prompts\_standard（**旧口径，已作废，但其期望的特征轴可参考**）期望：QNX(`MsgSend`/`MsgReceive`/`resmgr_*`/`pulse_*`/`ChannelCreate`/`ConnectAttach`)、RTOS(`xTaskCreate`/`vTaskDelay`/`rt_thread_*`/`osMutex*`)、BSP(`BSP_Init`/`Board_Init`/`SystemInit`/`HAL_Init`)。
- 但 FW synth\_spec note 自己说「**非纯 C 固件**，多为 Android 平台/framework 仓」——即嵌入式特征在生产 FW 里**不是主体**。

**多样性（分布/采样指导）**

- private/internal include（D03）：部分 vendor/framework 仓有。
- dlopen/dlsym（D02）：OSS 插件式库、vendor 仓有。
- QNX/RTOS/BSP：**生产 FW 主体是 Android 仓，这些嵌入式特征应稀少**（只在少数 m4firmware/trusty\_tee/Security\_OS 类仓出现）。

**正式 benchmark 现状（对照）**

- 正式 FW（9 仓聚合）：private\_inc **101**（全部集中在 vehicle-diagnostics 一仓）、rtos **22**、bsp\_init **0**、someip\_dbus **0**、abi **3**。
- type\_gate：`forbidden_embedded_anchors []`——正式 benchmark **明确禁止嵌入式锚点**，确保 FW 仓被识别为 Android 框架而非嵌入式。

**分歧/裁定**

- 🟡 生产 FW「非纯 C 固件」与正式 FW「明确非嵌入式（forbidden\_embedded\_anchors）」**方向一致**——两侧都不把 FW 当嵌入式固件。
- ⚠ 但生产包 prompts\_standard 仍带 QNX/RTOS/BSP 嵌入式 rubric（旧口径），与「非纯 C 固件」自相矛盾。**该矛盾因旧 prompts 作废而无需调和**——新 benchmark FW v3 用 android/通用 key，不评嵌入式（§9）。
- 裁定建议：虚拟 FW 仓**不造嵌入式特征**（QNX/RTOS/BSP=0 或极少），与正式 benchmark 的 type\_gate 约束一致；private include / dlopen 可少量存在于 vendor 类仓。

---

## 6. 缺陷注入

> 说明：缺陷规则的 `applies_to` 用的是生产旧维度名（中文）。下文每条都补了 **→ benchmark 新叶映射**（新口径权威），并标注量程。旧 prompts 的 `max:3` 一律作废。

### 6.1 APP 缺陷规则 D01–D06 🟡（原 #24）

**特征（生产扫描，APP synth\_spec ****`defects`****，逐条原样）**

| IDinject（注入手法）detect\_rule（判定规则）severityapplies\_to（旧维度）→ benchmark 新叶（量程） |                                |                                    |        |         |                                            |
| -------------------------------------------------------------------------- | ------------------------------ | ---------------------------------- | ------ | ------- | ------------------------------------------ |
| D01                                                                        | 删除 settings.gradle include     | `len(gradle.settings_modules)==0`  | high   | 组件化架构   | architecture.componentization (0–5)        |
| D02                                                                        | 删除 implementation project deps | `len(gradle.impl_project_deps)==0` | high   | 代码解耦    | architecture.decoupling (0–3)              |
| D03                                                                        | 大量 SystemProperties            | `system_api_count>50`              | high   | 平台升级影响  | platform\_reuse.platform\_upgrade (0–10)   |
| D04                                                                        | dlopen/dlsym 反射                | `nonstd_api_count>20`              | medium | 平台升级影响  | platform\_reuse.platform\_upgrade (0–10)   |
| D05                                                                        | 删除 AIDL                        | `n_aidl==0`                        | medium | API版本管理 | compilation.api\_version\_management (0–3) |
| D06                                                                        | 合并成单 app 无子模块                  | `len(settings_modules)<=1`         | medium | 组件化架构   | architecture.componentization (0–5)        |

**多样性（分布/采样指导）**

- 6 条缺陷覆盖 architecture（组件化/解耦）、platform\_upgrade、api\_version 三组叶。
- severity 分 high（D01/D02/D03）/ medium（D04/D05/D06）。
- detect\_rule 是确定性布尔/阈值判定，可直接用于「注入后自检」。

**正式 benchmark 现状（对照）**

- 正式 APP 仓的缺陷是**自然存在**（改编/合成时保留或制造），金标由 Validation-18 逐仓核定，无显式 D01–D06 注入。
- 例：aurora/atlas/cockpit-shell/nova 的 compilation\_independence=0（源码依赖，对应「编译独立性差」）；thermo ci\_independence=0（无 CI）；motion-control/atlas 的 release\_branch\_strategy=3（分支策略差）。

**分歧/裁定**

- 🟡 detect\_rule 要对齐 benchmark 新叶/量程（旧 max:3 作废）——上表已映射。
- 注意：D05「删除 AIDL→API版本管理」这个映射在新口径下需谨慎——benchmark 的 api\_version\_management 证据是 version 文件/CHANGELOG/versionName（facts 明确「tag 不算版本记录」），AIDL 缺失更多影响接口完整性而非版本管理。建议 codex 注入时按新叶证据链校准 detect\_rule。

### 6.2 FW 缺陷规则 D01–D06 🟡（原 #25）

**特征（生产扫描，FW synth\_spec ****`defects`****，逐条原样）**

| IDinject（注入手法）detect\_rule（判定规则）severityapplies\_to（旧维度）→ benchmark 新叶（量程） |                                 |                                   |        |        |                                                   |
| -------------------------------------------------------------------------- | ------------------------------- | --------------------------------- | ------ | ------ | ------------------------------------------------- |
| D01                                                                        | 删除 CMakeLists.txt/Makefile      | `not has cmake/make`              | high   | 编译独立性  | compilation.compilation\_independence (0–3)       |
| D02                                                                        | 添加 dlopen/dlsym                 | `nonstd_api_count>20`             | high   | 平台升级影响 | platform\_reuse.platform\_upgrade (0–10)          |
| D03                                                                        | `#include <private/internal.h>` | `nonstd includes private/`        | high   | 平台升级影响 | platform\_reuse.platform\_upgrade (0–10)          |
| D04                                                                        | 添加 Binder/Parcel IPC            | `ipc_usage_count>50`              | medium | 平台复用   | ⚠ 旧 platform\_coupling，**v3 已整维删除**（见下）           |
| D05                                                                        | master 分支保留代码（非空 master）        | `master has files`（违反 gerrit 工作流） | low    | 分支策略   | platform\_reuse.release\_branch\_strategy (0–10)  |
| D06                                                                        | 删除测试文件                          | `tests.test_files_n==0`           | low    | 质量     | quality.integration\_test (0–3, scoring\_android) |

**多样性（分布/采样指导）**

- 6 条覆盖 compilation\_independence、platform\_upgrade、release\_branch\_strategy、integration\_test。
- severity：high（D01/D02/D03）/ medium（D04）/ low（D05/D06）。

**正式 benchmark 现状（对照）**

- 正式 FW v3 契约**已整维删除 architecture 与 platform\_coupling**（§9）。
- 正式 FW 仓 private\_inc 仅 vehicle-diagnostics 有（101），其余 0；rtos/bsp/someip≈0。

**分歧/裁定**

- 🟡 **D04「添加 Binder/Parcel IPC → 平台复用(platform\_coupling)」的评分目标在 benchmark v3 里已不存在**（platform\_coupling 整维删除）。所以 D04 注入后**无对应叶可扣分**——要么弃用 D04，要么改挂到其它叶（但新契约 FW 无耦合叶）。**建议弃用 D04 或仅作形态多样性、不绑定评分。**
- 🟡 D05「非空 master＝违反 gerrit 工作流→分支策略低分」与 §4.4 冲突：正式仓 main 本就承载代码（非空），且引擎在默认分支评分。若按 D05 把「非空 master」当缺陷扣分，正式仓全会中招。**新口径下 release\_branch\_strategy 评的是分支命名/通用性，不是 master 空不空**——D05 的 detect\_rule 需重新对齐或弃用。
- detect\_rule 同样要对齐新叶量程（旧 max:3 作废）。

### 6.3 缺陷频率 prevalence 🔴（原 #26）

**特征（生产扫描）**

- 生产包**没给**任何缺陷的频率/流行度数据——即「多少 % 的仓该带 D01、多少 % 干净」完全未知。
- defects 列表只有 inject/detect\_rule/severity/applies\_to，无 prevalence 字段。

**多样性（分布/采样指导）**

- **缺口**：无法采样「缺陷在仓群里的分布」。若不给频率，codex 生成的仓要么全带缺陷、要么全不带，造不出「部分仓有缺陷、部分仓健康」的真实多样性。
- 建议补：给每条 D01–D06 一个 prevalence 概率（如 high severity 缺陷 20% 仓、medium 30%、low 40%，且互斥/共存关系），并与 §7.1 质量档分布联动（low 质量仓更可能带多缺陷）。

**正式 benchmark 现状（对照）**

- 正式 18 仓质量档（high/medium/low 各 6 仓）隐含了缺陷分布：low 档仓金标分低（如 car-runtime FW 多叶 0–1、atlas/thermo/nova APP 多叶低分），high 档仓金标分高。但这是「结果分布」非「缺陷注入频率」。

**分歧/裁定**

- 🔴 纯缺口，需用户/codex 补 prevalence 分布。这是「模拟多样性」的关键缺失之一。

### 6.4 包内计数自相矛盾（备注，非独立条目）

- FW synth\_spec `n_repos=105`、structure\_report 标题「119 FW仓(非AOSP 25+external/packages 94)」、activity 分布按 `94` 计——**三个数字不一致**（105 / 119 / 94）。
- APP synth\_spec `n_repos=100`、structure\_report 列 100 仓、activity 分布 {"1":85,"0":15}=100——APP 一致。
- 影响：FW 各聚合总量（system\_api/ipc/reflection）的分母不确定（105? 119? 94?），per-repo 均值有 ±20% 误差。codex 用 FW 聚合数据时注意这个不确定性。

---

## 7. 质量与联合分布【缺口重点区】

### 7.1 质量档分布 🔴（原 #27）

**特征（生产扫描）**

- 生产 structure\_report.md 的「分维度明细（打分方=双模型合议）」表**全空**：每仓总分 **0**、满分 **0**、得分率 **0%**，分维度列全空，附录 A「双模型一致性」＝「（无双模型数据）」。
- 即：**生产扫描没有产出任何质量分**——双模型合议打分没跑（或被剥离）。structure\_report 只有「规模」列有值（且 APP 缺 41%、FW 缺 12%）。
- 所以**生产仓的 high/medium/low 质量档占比完全未知**。

**多样性（分布/采样指导）**

- **缺口**：无法知道生产真实仓里高质量/中质量/低质量仓各占多少。
- 这是模拟多样性的核心缺失——真实仓群必然有质量梯度（有的仓架构好/CI 全/测试多，有的仓烂），但生产扫描没量化这个梯度。
- 建议补：要么对生产仓补跑双模型合议打分得到质量分布，要么由用户给定目标质量档配比。

**正式 benchmark 现状（对照）**

- 正式 18 仓有**显式 3×3 质量×体量矩阵**（ACTIVE\_EIGHTEEN.md），质量档 high/medium/low 各 6 仓（均匀设计）：
  - APP high：climatix-hvac、horizon-launcher、aurora-settings
  - APP medium：market-hub、motion-control、cockpit-shell
  - APP low：thermo-control、nova-launcher、atlas-settings
  - FW high：vehicle-property-service、vehicle-hal-adapter、vehicle-diagnostics
  - FW medium：cockpit-manager-kit、soa-gateway、update-manager-service
  - FW low：car-runtime-service、vehicle-platform-service、platform-compat-service
- 质量档由金标分体现（high 档金标总分高、low 档低）。

**分歧/裁定**

- 🔴 生产无质量分布（空壳）vs 正式有 3×3 均匀矩阵。
- 待裁定：虚拟仓质量档配比走正式 3×3 均匀（high/med/low 各 1/3），还是需补生产真实质量分布。当前**只能用正式的均匀矩阵**（生产侧无数据）。

### 7.2 体量×质量联合分布 🔴（原 #28）

**特征（生产扫描）**

- 生产**没给**体量与质量的联合/相关分布（质量分本身缺失，见 §7.1）。
- 生产体量数据：synth\_spec code\_stats 只有中位（APP source\_files\_med 29 / source\_lines\_med 3311；FW 81 / 17683），structure\_report 规模列有 per-repo 值但残缺。
- ⚠ 用户已**丢弃**原 #4/#5（生产 APP/FW 体量百分位分布），故本节体量口径**以正式 3×3 矩阵为准**，不引入生产规模列百分位。

**多样性（分布/采样指导）**

- 用正式 benchmark 的 **3×3 矩阵**作为体量×质量联合分布（small/medium/large × high/medium/low，9 格）。
- 正式矩阵体量分档依据：SCORE\_RULES.md「final-HEAD 生产源码双阈值」（source\_files + source\_loc 双指标），跨档标 unresolved。

**正式 benchmark 现状（对照，体量分档实测）**

- 正式仓 source\_files / source\_loc（manifest）与 size\_band：

| 仓族size\_bandsource\_filessource\_locquality\_tier |     |        |      |        |        |
| ------------------------------------------------- | --- | ------ | ---- | ------ | ------ |
| climatix-hvac                                     | APP | small  | 222  | 10787  | high   |
| thermo-control                                    | APP | small  | 169  | 12004  | low    |
| market-hub                                        | APP | small  | 264  | 21482  | medium |
| horizon-launcher                                  | APP | medium | 421  | 36320  | high   |
| nova-launcher                                     | APP | medium | 525  | 41051  | low    |
| motion-control                                    | APP | medium | 410  | 46142  | medium |
| aurora-settings                                   | APP | large  | 1445 | 106184 | high   |
| atlas-settings                                    | APP | large  | 1331 | 101805 | low    |
| cockpit-shell                                     | APP | large  | 1275 | 122044 | medium |
| vehicle-property-service                          | FW  | small  | 282  | 51854  | high   |
| cockpit-manager-kit                               | FW  | small  | 289  | 51751  | medium |
| car-runtime-service                               | FW  | small  | 342  | 41407  | low    |
| vehicle-hal-adapter                               | FW  | medium | 672  | 112910 | high   |
| soa-gateway                                       | FW  | medium | 660  | 103229 | medium |
| vehicle-platform-service                          | FW  | medium | 836  | 88725  | low    |
| vehicle-diagnostics                               | FW  | large  | 2030 | 231018 | high   |
| update-manager-service                            | FW  | large  | 1620 | 213319 | medium |
| platform-compat-service                           | FW  | large  | 1979 | 246978 | low    |

- 体量档边界（从实测反推，双阈值）：
  - APP：small ≈ 169–264 文件 / 10.8K–21.5K 行；medium ≈ 410–525 文件 / 36K–46K 行；large ≈ 1275–1445 文件 / 102K–122K 行。
  - FW：small ≈ 282–342 文件 / 41K–52K 行；medium ≈ 660–836 文件 / 89K–113K 行；large ≈ 1620–2030 文件 / 213K–247K 行。
- 质量×体量在正式集是**均匀 9 格**（每格 APP/FW 各 1 仓），无相关倾向（high 质量不偏向大仓或小仓）。

**分歧/裁定**

- 🔴 生产无联合分布；正式用均匀 3×3 矩阵。
- 待裁定：虚拟仓照正式 3×3 均匀配比（每格等量），还是仿生产自然长尾（小仓占多数、大仓少、质量未知）。**当前生产侧无质量数据，只能先用正式均匀矩阵。** 若要拟真生产的「小仓占多数」体量偏态，需用户单独给定体量配比（因 #4/#5 已丢弃，本文档不引入生产百分位）。

### 7.3 维度间关联规则 🔴（原 #29，多样性核心缺失）

**特征（生产扫描）**

- generate\_guide.md 方法论 **步骤 4「发现规律（规则优先，概率兜底）」** 明确声明要找确定性关联规则：
  - 「先找**确定性规则**：模块类型 → 分支类型？子系统数 → 层次档位？domain 前缀 → 文件族？」
  - 「概率只作无规律时的兜底。」
- 但**交付的 synth\_spec 里几乎没有这类关联规则**——只有 FW R1（master 空→切非 master 分支）一条确定性规则。其余全是**独立边际分布**（扩展概率、构建频率、模块频率、API 总量各自独立）。

**多样性（分布/采样指导）**

- **这是「模拟多样性」最核心的缺失。** 真实仓的多样性不是各维度独立随机，而是**维度间强相关**：
  - OSS external 仓 → C/C++ + 巨型（百万行）+ make/cmake + 零 Android IPC + 无 AIDL + 英文社区提交 + 无 gerrit 分支怪癖。
  - vendor 专有仓 → 混合语言 + 平台/车型绑定分支（sop/flymeauto）+ gerrit 空 master + 中文缺陷单提交 + 部分 dlopen/private include。
  - packages 框架仓 → Java/AIDL + Soong/Make + Binder-heavy + Android 系统 API。
  - APP 一方应用仓 → Java/Kotlin + gradle + \:basesdk 公共依赖 + 中文缺陷单提交 + 多 sop 分支。
- 若只按独立边际采样，会造出「C 语言 + gradle + 中文提交 + 百万行 + 全 AIDL」这种**现实中不存在的畸形组合**。
- 建议补：定义 3–5 个「仓型原型（archetype）」，每个原型绑定一组维度取值（语言/构建/体量/IPC/分支/提交/缺陷倾向），先采原型再在原型内扰动——这样才能造出真实多样性。

**正式 benchmark 现状（对照）**

- 正式 18 仓本身就是「原型化」的：APP＝AOSP Car 应用改编原型（Java/Kotlin + gradle/Soong + 英文 conventional + 5–8 分支 + 注入 tag）；FW＝Car-service 框架原型（Java/AIDL + Soong + Binder-heavy + 英文 conventional）。
- 正式集只有 **2 个原型**（APP 改编 / FW 车服务），多样性远不如生产（生产至少 OSS/vendor/packages/一方app 4+ 原型）。

**分歧/裁定**

- 🔴 生产包声称「规则优先」但没交付关联规则；正式集只有 2 个原型。
- **这是给 codex 最重要的补充建议**：要模拟生产多样性，必须先建「仓型原型库」（每原型一套绑定的维度取值），而非按独立边际采样。原型可从 §1.2 的 FW 三类型 + §1.1 的 APP 产品线/功能域提炼。

---

## 8. CI / 测试证据

### 8.1 CI 配置存在与形态 🔴（原 #30）

**特征（生产扫描）**

- 生产 synth\_spec **未聚合 CI 文件存在性**——没有 ci 字段、没有 CI 配置统计。
- 但生产 prompts\_standard（旧口径）有 `compilation.ci_independence` 维度（tiers 0–3：0=无CI / 1=依赖安卓系统层CI / 2=独立CI非标准流水线 / 3=标准流水线）——**说明 CI 是评分轴，但扫描没采对应证据**。

**多样性（分布/采样指导）**

- **缺口**：生产没采 CI 形态分布（多少仓无 CI、多少有系统层 CI、多少有标准流水线）。
- benchmark 新口径 `compilation.ci_independence`(0–3) 需要 CI 证据。codex 造仓时必须按目标分数档造对应 CI 形态：
  - 0 分：无任何 CI 配置文件
  - 1 分：依赖安卓系统层 CI（如 PREUPLOAD.cfg / TEST\_MAPPING 这类 AOSP 内置机制）
  - 2 分：独立 CI 配置但非标准流水线
  - 3 分：完整标准化 CI/CD 流水线（.github/workflows / .gitlab-ci.yml 多 stage build+test+quality）
- 建议补：给 CI 形态一个分布（如 low 质量仓多 0–1 分、high 质量仓多 2–3 分），与 §7.1 质量档联动。

**正式 benchmark 现状（对照）**

- 正式 APP **8/9 仓有 CI**（仅 thermo-control 无）：形态含 `.github/workflows/android.yml`、`PREUPLOAD.cfg`、`TEST_MAPPING`。
- 正式 FW **9/9 仓有 CI**：`.github/workflows/native.yml` / `native-ci.yml`、`PREUPLOAD.cfg`、`TEST_MAPPING`（含子目录 TEST\_MAPPING）。
- 金标 ci\_independence 分布：APP {0:1(thermo), 1:5, 2:1(horizon), 3:1(climatix)}；FW {1:3, 2:3, 3:3(vehicle-property/hal-adapter/diagnostics)}。
- facts（FW-03）记录 CI 证据：`.github/workflows/native-ci.yml` + stage\_counts {build:12, test:12, quality\_or\_report:14} + 逐 anchor 行号。

**分歧/裁定**

- 🔴 生产未采 CI（缺口）；正式 CI 齐全且金标已分档。
- 裁定建议：CI 形态分布**以正式 benchmark 金标分档为参照**（ci\_independence 0–3 各档对应的 CI 文件形态已在正式仓有实例），生产侧无数据可补。codex 按目标 ci\_independence 分档造对应 CI 证据。

### 8.2 测试框架与规模 🔴（原 #31）

**特征（生产扫描）**

- 生产 synth\_spec **未聚合测试框架/规模**——测试只作为缺陷轴出现：FW D06「删除测试文件」detect\_rule `tests.test_files_n==0`（applies\_to 质量）。
- 生产 prompts\_standard（旧口径）FW 有 `quality.integration_test_scoring_embedded`（**embedded 版，已作废**，期望 Unity/CppUTest/GTest/CMock）。

**多样性（分布/采样指导）**

- **缺口**：生产没采测试框架分布、测试文件数分布、覆盖率。
- benchmark 新口径 FW `quality.integration_test`(0–3, **scoring\_android** 非 embedded) 需要测试证据。codex 造仓时按目标分档造测试：
  - 参照新口径 scoring\_android（Android 集成测试）：0=无测试 / 1=少量或仅手工 / 2=有框架+部分覆盖 / 3=完整集成测试框架+高覆盖。
  - ⚠ **不要照生产旧 embedded rubric**（Unity/CppUTest/CMock 是嵌入式框架，新口径用 Android 测试栈：JUnit/Robolectric/androidx.test/TEST\_MAPPING）。
- APP 侧：benchmark 新契约 APP **不评 quality.integration\_test**（APP 该叶是 GBOP 数据源维度，非 LLM，排除在契约外）——所以 APP 虚拟仓的测试不影响 APP 契约分，但仍可按需造。

**正式 benchmark 现状（对照）**

- 正式仓**测试极丰富**（保留 AOSP 全套测试）：APP test 关键字命中 6517、FW 5650；测试文件命名计数 APP（aurora 380、atlas 338、cockpit-shell 172、horizon 67…）、FW（diagnostics 316、update-manager 316、hal-adapter 249、platform-compat 317…）。
- 测试框架：org.junit / robolectric / androidx.test / gtest（native）/ TEST\_MAPPING。
- 金标 integration\_test 分布（FW）：{0:1(car-runtime), 1:4(manager-kit/soa/update-manager/vehicle-platform/platform-compat), 3:3(vehicle-property/hal-adapter/diagnostics)}。

**分歧/裁定**

- 🔴 生产未采测试（缺口，仅作缺陷轴）；正式测试丰富且金标已分档。
- 裁定建议：测试形态分布**以正式 benchmark FW integration\_test 金标分档为参照**（0–3 各档对应测试规模/框架已在正式仓有实例），用 **Android 测试栈**（非生产旧 embedded 的 Unity/CppUTest）。生产侧无数据可补。

---

## 9. 附录：benchmark 权威评分口径 🔵（原 #32）

> 用户裁定说明：本条原清单未点名留/丢，但 §6（缺陷映射）、§7.1（质量档）、§8.1/8.2（CI/测试分档）均依赖此口径，且用户明确「评分以 benchmark 为准」，故作为附录锚点保留。如不需要可删。

### 9.1 契约总则（contract-20260903）

- **契约 ＝ 策略中带提示词的纯 LLM 叶子**；分析器/GBOP/DB 工具维度不入契约。
- 偏离度只在「契约叶子 ∩ 有效标准分」上计算。
- 金标来源：`benchmark-standard.json`(v0.7.x)，18 仓 valid（`standard-status.json` 2026-09-07 同步）。

### 9.2 APP 契约：8 叶 / 满分 40

| 叶 key量程(contract max)金标实测值域说明             |      |     |          |
| ----------------------------------------- | ---- | --- | -------- |
| architecture.componentization             | 0–5  | 3–5 | 组件化架构    |
| architecture.modularization               | 0–3  | 2–3 | 模块化      |
| architecture.decoupling                   | 0–3  | 2–3 | 代码解耦     |
| compilation.ci\_independence              | 0–3  | 0–3 | CI 独立性   |
| compilation.compilation\_independence     | 0–3  | 0–2 | 编译独立性    |
| compilation.api\_version\_management      | 0–3  | 1–2 | API 版本管理 |
| platform\_reuse.platform\_upgrade         | 0–10 | 3–8 | 平台升级适配   |
| platform\_reuse.release\_branch\_strategy | 0–10 | 3–8 | 发布分支策略   |

**APP 显式排除维度**（不评/不入契约）：

- `android_framework`：静态分析器维度（无 LLM 会话），9 分计总分但不入准确性契约。
- `quality.integration_test`：APP 占位 prompt → GBOP 数据源维度，非 LLM。
- `solid_principle`：APP 策略未配置该维度。
- （生产旧 prompts 里的 device\_specificity / single\_platform\_branch\_template / cross\_platform\_branch\_template / code\_duplication / platform\_coupling.scoring\_app / solid.scoring 均**非 APP 新契约叶**，作废。）

### 9.3 FW 契约：11 叶 / 满分 52

| 叶 key量程(contract max)金标实测值域说明             |      |     |                            |
| ----------------------------------------- | ---- | --- | -------------------------- |
| compilation.ci\_independence              | 0–3  | 1–3 | CI 独立性                     |
| compilation.compilation\_independence     | 0–3  | 0–1 | 编译独立性                      |
| compilation.api\_version\_management      | 0–3  | 0–3 | API 版本管理                   |
| quality.integration\_test                 | 0–3  | 0–3 | 集成测试（**scoring\_android**） |
| solid\_principle.single\_responsibility   | 0–4  | 0–3 | SOLID·单一职责                 |
| solid\_principle.open\_closed             | 0–4  | 1–3 | SOLID·开闭                   |
| solid\_principle.liskov\_substitution     | 0–4  | 2–3 | SOLID·里氏替换                 |
| solid\_principle.interface\_segregation   | 0–4  | 0–3 | SOLID·接口隔离                 |
| solid\_principle.dependency\_inversion    | 0–4  | 0–2 | SOLID·依赖倒置                 |
| platform\_reuse.platform\_upgrade         | 0–10 | 0–3 | 平台升级适配                     |
| platform\_reuse.release\_branch\_strategy | 0–10 | 8   | 发布分支策略                     |

**FW v3 关键变更（相对生产旧 prompts）**：

- **整维删除** `architecture`（v2 曾用 architecture.scoring\_embedded）。
- **整维删除** `platform_coupling`（v2 曾用 platform\_coupling.scoring\_embedded）。
- prompt\_key 换血：`quality.integration_test` scoring\_embedded → **scoring\_android**；`compilation.api_version_management` api\_version\_embedded → 通用 key；`compilation.compilation_independence` independence\_embedded → 通用 key；`platform_reuse.platform_upgrade` platform\_upgrade\_embedded → 通用 key。
- SOLID 对比粒度＝拆 5 原则（每原则 0–4），因引擎本就逐原则评分。

### 9.4 逐仓金标全表（benchmark-standard.json v0.7.x，18 valid 仓）

**APP（8 叶，满分 40）**

| 仓compmodudecoupcicompilapiverupgradebranch合计 |   |   |   |   |   |   |   |   |    |
| -------------------------------------------- | - | - | - | - | - | - | - | - | -- |
| climatix-hvac                                | 5 | 3 | 3 | 3 | 1 | 2 | 8 | 8 | 33 |
| horizon-launcher                             | 5 | 3 | 3 | 2 | 1 | 2 | 8 | 8 | 32 |
| aurora-settings                              | 5 | 3 | 2 | 1 | 0 | 2 | 3 | 8 | 24 |
| market-hub                                   | 5 | 3 | 3 | 1 | 2 | 1 | 8 | 8 | 31 |
| motion-control                               | 5 | 3 | 3 | 1 | 2 | 1 | 3 | 3 | 21 |
| cockpit-shell                                | 3 | 2 | 2 | 1 | 0 | 2 | 3 | 8 | 21 |
| thermo-control                               | 3 | 2 | 2 | 0 | 0 | 1 | 3 | 8 | 19 |
| nova-launcher                                | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 8 | 20 |
| atlas-settings                               | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 3 | 15 |

**FW（11 叶，满分 52）**

| 仓cicompilapiveritestSRPOCPLSPISPDIPupgradebranch合计 |   |   |   |   |   |   |   |   |   |   |   |         |
| -------------------------------------------------- | - | - | - | - | - | - | - | - | - | - | - | ------- |
| vehicle-property-service                           | 3 | 1 | 2 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 8 | 33→40\* |
| vehicle-hal-adapter                                | 3 | 1 | 2 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 8 | 42\*    |
| vehicle-diagnostics                                | 3 | 1 | 3 | 3 | 2 | 3 | 3 | 3 | 2 | 3 | 8 | 42\*    |
| cockpit-manager-kit                                | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 3 | 8 | 31      |
| soa-gateway                                        | 2 | 1 | 2 | 1 | 2 | 3 | 2 | 3 | 2 | 3 | 8 | 39\*    |
| update-manager-service                             | 2 | 1 | 3 | 1 | 2 | 2 | 3 | 2 | 2 | 3 | 8 | 29→\*   |
| car-runtime-service                                | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 8 | 12      |
| vehicle-platform-service                           | 1 | 0 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 3 | 8 | 14→\*   |
| platform-compat-service                            | 1 | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 1 | 3 | 8 | 13→\*   |

> \* 注：repos.json 记录的 std\_total（vehicle-property 40、hal-adapter 42、diagnostics 42、soa-gateway 39、update-manager 29、vehicle-platform 14、platform-compat 13）与逐叶求和略有出入，因 repos.json std\_total 含 SOLID 聚合口径(/20)换算；逐叶分值以 benchmark-standard.json 为准。codex 对标时用逐叶值。

### 9.5 缺陷 applies\_to → benchmark 新叶 映射总表

| 生产旧维度名（defects.applies\_to）benchmark 新叶量程族 |                                              |       |          |
| ------------------------------------------ | -------------------------------------------- | ----- | -------- |
| 组件化架构                                      | architecture.componentization                | 0–5   | APP      |
| 代码解耦                                       | architecture.decoupling                      | 0–3   | APP      |
| （架构-模块化）                                   | architecture.modularization                  | 0–3   | APP      |
| 平台升级影响                                     | platform\_reuse.platform\_upgrade            | 0–10  | APP+FW   |
| API版本管理                                    | compilation.api\_version\_management         | 0–3   | APP+FW   |
| 编译独立性                                      | compilation.compilation\_independence        | 0–3   | APP+FW   |
| CI独立性                                      | compilation.ci\_independence                 | 0–3   | APP+FW   |
| 分支策略                                       | platform\_reuse.release\_branch\_strategy    | 0–10  | APP+FW   |
| 质量（测试）                                     | quality.integration\_test (scoring\_android) | 0–3   | **仅 FW** |
| 平台复用 / 平台耦合                                | ⚠ **v3 已整维删除（platform\_coupling）**           | —     | 无对应叶     |
| SOLID（FW）                                  | solid\_principle.{SRP/OCP/LSP/ISP/DIP}       | 各 0–4 | **仅 FW** |

---

## 附录 A：生产 APP 100 仓全名单（类型多样性原料）

> 格式：仓名（规模列值＝structure\_report「规模」，单位约等于行数；`-`＝生产未采到）。按产品线分组。

**FlymeOS2 系（35 仓）**

1. FlymeOS2\_\_App\_\_AutoCloudAuthService (-)
2. FlymeOS2\_\_App\_\_AutoKeyServer (-)
3. FlymeOS2\_\_App\_\_AutoRADS (-)
4. FlymeOS2\_\_App\_\_AutoStreamRearview (4138)
5. FlymeOS2\_\_App\_\_FlymeAutoService (-)
6. FlymeOS2\_\_App\_\_PeopleCar (-)
7. FlymeOS2\_\_App\_\_SmartButton (-)
8. FlymeOS2\_\_App\_\_XCOutCarMedia (-)
9. FlymeOS2\_\_FlymeAuto\_\_AutoCarAlive (-)
10. FlymeOS2\_\_app\_\_Client\_\_AutoAicySuggestion (-)
11. FlymeOS2\_\_app\_\_Client\_\_AutoAppAlive (-)
12. FlymeOS2\_\_app\_\_Client\_\_AutoAppStore (-)
13. FlymeOS2\_\_app\_\_Client\_\_AutoAtomicAbility (-)
14. FlymeOS2\_\_app\_\_Client\_\_AutoAudioSettings (-)
15. FlymeOS2\_\_app\_\_Client\_\_AutoConnectivitySettings (-)
16. FlymeOS2\_\_app\_\_Client\_\_AutoCustomizeCenter (-)
17. FlymeOS2\_\_app\_\_Client\_\_AutoEnergy (-)
18. FlymeOS2\_\_app\_\_Client\_\_AutoHiCar (-)
19. FlymeOS2\_\_app\_\_Client\_\_AutoICCOACarLink (-)
20. FlymeOS2\_\_app\_\_Client\_\_AutoNaviService (-)
21. FlymeOS2\_\_app\_\_Client\_\_AutoSceneAssist (-)
22. FlymeOS2\_\_app\_\_Client\_\_AutoSentineMonitor (-)
23. FlymeOS2\_\_app\_\_Client\_\_AutoSettings (-)
24. FlymeOS2\_\_app\_\_Client\_\_AutoSystemUIPlugin (-)
25. FlymeOS2\_\_app\_\_Client\_\_AutoUserManual (-)
26. FlymeOS2\_\_app\_\_Client\_\_AutoVoiceInteract (-)
27. FlymeOS2\_\_app\_\_Client\_\_AutoWallpaperLauncher (-)
28. FlymeOS2\_\_app\_\_Cloud\_\_AutoData (-)
29. FlymeOS2\_\_app\_\_Cloud\_\_AutoLocationService (-)
30. FlymeOS2\_\_app\_\_Cloud\_\_AutoWeather (-)
31. FlymeOS2\_\_app\_\_Media\_\_AutoDeviceShare (-)
32. FlymeOS2\_\_app\_\_Media\_\_AutoLinkMusic (-)
33. FlymeOS2\_\_app\_\_Net\_\_AutoBrowser (-)
34. FlymeOS2\_\_app\_\_Telecom\_\_AutoInCallUI (-)
35. FlymeOS2\_\_app\_\_Telecom\_\_AutoNetContactService (-)

**FlymeOS 一代系（61 仓）** 36. FlymeOS\_\_App\_\_AnalysisSDK (647) 37. FlymeOS\_\_App\_\_Auto3DEngine (15483) 38. FlymeOS\_\_App\_\_AutoAccount (37205) 39. FlymeOS\_\_App\_\_AutoAicySuggestion (1776) 40. FlymeOS\_\_App\_\_AutoAppStore (37655) 41. FlymeOS\_\_App\_\_AutoBSV (5937) 42. FlymeOS\_\_App\_\_AutoCarExhibit (3271) 43. FlymeOS\_\_App\_\_AutoCloudAuthService (20980) 44. FlymeOS\_\_App\_\_AutoControlBoard (155630) 45. FlymeOS\_\_App\_\_AutoCustomizeCenter (31134) 46. FlymeOS\_\_App\_\_AutoDigitalKey (5803) 47. FlymeOS\_\_App\_\_AutoEnergy (120655) 48. FlymeOS\_\_App\_\_AutoGallery (342867) 49. FlymeOS\_\_App\_\_AutoHealthDetection (11547) 50. FlymeOS\_\_App\_\_AutoKeyServer (9499) 51. FlymeOS\_\_App\_\_AutoLocationService (2123) 52. FlymeOS\_\_App\_\_AutoMediaControl (30284) 53. FlymeOS\_\_App\_\_AutoMusic (74288) 54. FlymeOS\_\_App\_\_AutoParkingPhoto (4642) 55. FlymeOS\_\_App\_\_AutoPermissionPlugin (11572) 56. FlymeOS\_\_App\_\_AutoRADS (39563) 57. FlymeOS\_\_App\_\_AutoSceneAssist (6886) 58. FlymeOS\_\_App\_\_AutoSceneDirector (108640) 59. FlymeOS\_\_App\_\_AutoSetupWizard (9091) 60. FlymeOS\_\_App\_\_AutoStaticSalesAssistant (27669) 61. FlymeOS\_\_App\_\_AutoStringSDK (102) 62. FlymeOS\_\_App\_\_AutoSystemUIPlugin (183268) 63. FlymeOS\_\_App\_\_AutoVRMiddlewareService (169929) 64. FlymeOS\_\_App\_\_AutoVectorEngine (21275) 65. FlymeOS\_\_App\_\_AutoWallpaperControl (16993) 66. FlymeOS\_\_App\_\_AutoWallpaperLauncher (3352) 67. FlymeOS\_\_App\_\_AutoWirelessCharging (3243) 68. FlymeOS\_\_App\_\_Camera (11489) 69. FlymeOS\_\_App\_\_CloudAuthService (23422) 70. FlymeOS\_\_App\_\_CloudBusinessWidget (3147) 71. FlymeOS\_\_App\_\_DVR (19481) 72. FlymeOS\_\_App\_\_FlymeAutoService (1430) 73. FlymeOS\_\_App\_\_GeelyAutoMusic (67141) 74. FlymeOS\_\_App\_\_GeelyCloudUpload (1230) 75. FlymeOS\_\_App\_\_ManualApp (4951) 76. FlymeOS\_\_App\_\_MergeMobileConnect (59967) 77. FlymeOS\_\_App\_\_NaviMap (-) 78. FlymeOS\_\_App\_\_NeuAutoFactory (-) 79. FlymeOS\_\_App\_\_OpenAPISDK (358269) 80. FlymeOS\_\_App\_\_PeopleCar (100894) 81. FlymeOS\_\_App\_\_PolicyAutoSDK (8408) 82. FlymeOS\_\_App\_\_PushNotificationService (13594) 83. FlymeOS\_\_App\_\_RearSceneMode (41535) 84. FlymeOS\_\_App\_\_RearWallpaper (4852) 85. FlymeOS\_\_App\_\_SceneEngine (64475) 86. FlymeOS\_\_App\_\_SenseHourse (20311) 87. FlymeOS\_\_App\_\_SenseSpace (25293) 88. FlymeOS\_\_App\_\_SmartButton (92462) 89. FlymeOS\_\_App\_\_TBoxClient (-) 90. FlymeOS\_\_App\_\_VisualSenseService (13422) 91. FlymeOS\_\_App\_\_XCCamera360 (-) 92. FlymeOS\_\_App\_\_XCOutCarMedia (23688) 93. FlymeOS\_\_App\_\_XSFCarService (58513) 94. FlymeOS\_\_App\_\_XSFDeviceService (44567) 95. FlymeOS\_\_App\_\_XSFEASCoreService (29767) 96. FlymeOS\_\_App\_\_XSFNaviService (174296)

**ISD / zeekos 系（4 仓）** 97. ISD\_\_BC\_\_CAP\_AVM\_APP (37201) 98. zeekos\_\_app\_\_ZeekrBaseMap (-) 99. zeekos\_\_app\_\_internetVehicles (-) 100. zeekos\_\_app\_\_md\_zeekr\_coreservice (-)

> APP 规模列：59 仓有值、41 仓为 `-`（未采）。有值仓分布见 §0.5 丢弃说明（原 #4 已丢弃，此处仅留名单作类型多样性原料，不引入百分位口径）。

---

## 附录 B：生产 FW 119 仓全名单（类型多样性原料，按三类型分组）

> 格式：仓名（规模列值；`-`＝未采）。

**B-1. vendor 专有 / 平台 framework（≈25 仓，非 AOSP external/packages）**

1. E02\_Android9\_\_AOSP\_\_vendor\_\_geely\_\_packages\_\_services\_\_GeelyAdapter (3619)
2. Geely\_\_Android\_\_platform\_\_GeelyFramework (8003)
3. Geely\_\_Android\_\_platform\_\_GeelyFrameworkAPI (18081)
4. ICVSBG\_\_CHUDC\_\_AP\_\_Android\_OEM\_\_vendor\_\_ecarx\_\_oem\_\_adaptapi\_dev (-)
5. ICVSBG\_\_CHUDC\_\_AP\_\_Android\_Venus\_\_vendor\_\_ecarx\_\_venus\_\_gnss\_release (-)
6. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_SE1000\_SDK\_\_deploy (-)
7. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_SE1000\_SDK\_\_src\_\_android\_trusty\_tee (278790)
8. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_SE1000\_SDK\_\_src\_\_audio (344007)
9. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_SE1000\_SDK\_\_src\_\_m4firmware (-)
10. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_SE1000\_SDK\_\_src\_\_siengine\_android\_\_vendor\_\_siengine (1880446)
11. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_SE1000\_SDK\_\_toolchain (718326)
12. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_Security\_OS (22606)
13. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_aosp\_\_vendor\_\_ecarx\_\_packages\_\_app\_\_MediaFocusTest (700)
14. ICVSBG\_\_CHUDC\_\_AP\_\_E04\_\_aosp\_\_vendor\_\_ecarx\_\_packages\_\_service\_\_BluetoothEnhancement (-)
15. JICA\_Dev\_\_E02\_ANDROID9\_\_UpdateService (68519)
16. JICA\_Dev\_\_E02\_ANDROID9\_\_compatibility (246)
17. JICA\_Dev\_\_E02\_ANDROID9\_\_development (384171)
18. JICA\_Dev\_\_E02\_ANDROID9\_\_kernel (13248)
19. JICA\_Dev\_\_E02\_ANDROID9\_\_libnativehelper (6387)
20. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_interfaces\_\_audiocontrol (-)
21. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_interfaces\_\_diagbusiness (3759)
22. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_interfaces\_\_diagnostic (9387)
23. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_interfaces\_\_gnss (-)
24. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_interfaces\_\_jicapower (5355)
25. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_system (113901)
26. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_jica\_\_tcam\_\_udsApp (4236)
27. JICA\_Dev\_\_E02\_ANDROID9\_\_vendor\_\_mediatek\_\_proprietary\_\_hardware\_\_connectivity\_\_firmware (-)
28. vendor\_\_flyme\_\_frameworks\_\_base (46003)

*B-2. AOSP external/ OSS 上游（≈69 仓，纯 C/C++ 第三方库）*\*

- external\_\_FXdiv (929)、external\_\_OpenCSD (39072)、external\_\_adeb (481)、external\_\_androidplot (17683)、external\_\_angle (928504)、external\_\_apache-commons-compress (76008)、external\_\_autotest (463037)、external\_\_boringssl (261501)、external\_\_bouncycastle (290787)、external\_\_capstone (171224)、external\_\_curl (241013)、external\_\_deqp-deps\_\_SPIRV-Headers (26399)、external\_\_deqp-deps\_\_SPIRV-Tools (386628)、external\_\_dexmaker (17319)、external\_\_drrickorang (14802)、external\_\_dynamic\_depth (11804)、external\_\_f2fs-tools (47620)、external\_\_fdlibm (8856)、external\_\_fec (8490)、external\_\_flatbuffers (52843)、external\_\_gemmlowp (86592)、external\_\_google-breakpad (248284)、external\_\_google-fonts\_\_arbutus-slab (-)、external\_\_google-fonts\_\_karla (-)、external\_\_guice (96304)、external\_\_icu (1285927)、external\_\_igt-gpu-tools (254319)、external\_\_iproute2 (109147)、external\_\_ipsec-tools (67932)、external\_\_iptables (70887)、external\_\_iputils (15750)、external\_\_iw (15243)、external\_\_jarjar (3132)、external\_\_javaparser (233325)、external\_\_javasqlite (14730)、external\_\_jcommander (8550)、external\_\_jline (6530)、external\_\_junit-params (5095)、external\_\_kotlinx.coroutines (77995)、external\_\_libcap (4100)、external\_\_libdivsufsort (3790)、external\_\_libdrm (85915)、external\_\_libese (17886)、external\_\_libevent (87732)、external\_\_libgav1 (86980)、external\_\_libprotobuf-mutator (3914)、external\_\_libunwind\_llvm (14937)、external\_\_libvpx (455146)、external\_\_libxaac (115294)、external\_\_llvm (1073559)、external\_\_lzma (113847)、external\_\_nanohttpd (9608)、external\_\_neon\_2\_sse (16716)、external\_\_oss-fuzz (23698)、external\_\_python\_\_cpython3 (1330809)、external\_\_python\_\_futures (2390)、external\_\_python\_\_ipaddress (4695)、external\_\_python\_\_pyasn1 (20822)、external\_\_python\_\_six (2102)、external\_\_rust\_\_crates\_\_byteorder (-)、external\_\_rust\_\_crates\_\_libc (-)、external\_\_rust\_\_crates\_\_unicode-xid (-)、external\_\_scapy (100764)、external\_\_skqp (537700)、external\_\_smali (129594)、external\_\_sonic (2937)、external\_\_strace (281860)、external\_\_unicode (1527)、external\_\_vulkan-validation-layers (225032)、external\_\_wayland-protocols (-)、external\_\_webp (70122)

*B-3. AOSP packages/ 框架/应用/模块/provider（≈25 仓）*\*

- packages\_\_apps\_\_BasicSmsReceiver (556)、packages\_\_apps\_\_Calendar (19485)、packages\_\_apps\_\_Car\_\_Messenger (2039)、packages\_\_apps\_\_Car\_\_Notification (14533)、packages\_\_apps\_\_Car\_\_Radio (5697)、packages\_\_apps\_\_Car\_\_SystemUpdater (800)、packages\_\_apps\_\_CellBroadcastReceiver (13141)、packages\_\_apps\_\_DevCamera (3311)、packages\_\_apps\_\_Gallery (12569)、packages\_\_apps\_\_Music (749)、packages\_\_apps\_\_Stk (5043)、packages\_\_apps\_\_StorageManager (8491)、packages\_\_apps\_\_TV (160091)、packages\_\_apps\_\_Traceur (2811)、packages\_\_modules\_\_ArtPrebuilt (58)、packages\_\_modules\_\_CellBroadcastService (10697)、packages\_\_modules\_\_NetworkPermissionConfig (27)、packages\_\_modules\_\_NetworkStack (52972)、packages\_\_modules\_\_SdkExtensions (267)、packages\_\_providers\_\_CalendarProvider (17606)

> 注：B-1/B-2/B-3 分组数为按仓名归类的近似（生产标题口径「非AOSP 25 + external/packages 94 = 119」，与 synth\_spec n\_repos=105、activity 分布 94 矛盾，见 §6.4）。external 前缀均为 `ICVSBG__CHUDC__AP__E04__aosp__platform__` 路径下。

---

## 附录 C：正式 benchmark 18 仓画像总表（对照基线）

> 来源：official-profile.json（逐仓全量扫描）+ manifest.json。build/lang/patterns 为 HEAD（main 分支）工作区实测。

### C-1 APP 9 仓

| 仓role体量档构建src文件src行主语言(ext)aidlbindersyspropsreflCI文件分支tagcommits提交语言 |               |        |                        |      |        |                                 |    |     |     |    |                                   |   |   |       |         |
| --------------------------------------------------------------------- | ------------- | ------ | ---------------------- | ---- | ------ | ------------------------------- | -- | --- | --- | -- | --------------------------------- | - | - | ----- | ------- |
| aurora-settings                                                       | large/high    | large  | Gradle(4模块)            | 1099 | 142745 | .java1098/.xml594               | 0  | 49  | 21  | 1  | PREUPLOAD+TEST\_MAPPING           | 5 | 1 | 10669 | EN-conv |
| horizon-launcher                                                      | medium/high   | medium | Soong(.bp15)+gradle    | 256  | 46118  | .xml731/.java187/.kt68          | 0  | 23  | 0   | 8  | workflows+PREUPLOAD+TEST\_MAPPING | 6 | 1 | 3895  | EN-conv |
| climatix-hvac                                                         | small/high    | small  | Gradle-kts(8)          | 144  | 9086   | .kt118/.xml69/.java21           | 5  | 35  | 0   | 1  | workflows                         | 5 | 1 | 285   | EN-conv |
| motion-control                                                        | medium/medium | medium | Gradle(12)             | 46   | 4155   | .xml351/.java39                 | 7  | 15  | 1   | 1  | TEST\_MAPPING                     | 7 | 2 | 26    | EN-conv |
| market-hub                                                            | small/medium  | small  | Gradle(12)             | 45   | 4144   | .xml206/.java38                 | 7  | 15  | 0   | 0  | TEST\_MAPPING                     | 5 | 2 | 24    | EN-conv |
| cockpit-shell                                                         | large/medium  | large  | Soong(.bp23)+gradle+mk | 721  | 147769 | .xml1281/.java614/.kt73/.aidl29 | 29 | 273 | 38  | 13 | PREUPLOAD+TEST\_MAPPING           | 5 | 1 | 1803  | EN-conv |
| atlas-settings                                                        | large/low     | large  | Gradle(4模块)            | 1100 | 146439 | .java1100/.xml394               | 0  | 35  | 21  | 5  | PREUPLOAD                         | 8 | 7 | 2840  | EN-conv |
| nova-launcher                                                         | medium/low    | medium | Soong(.bp16)+gradle    | 349  | 53730  | .xml740/.java276/.kt70          | 0  | 23  | 3   | 23 | PREUPLOAD                         | 6 | 1 | 4035  | EN-conv |
| thermo-control                                                        | small/low     | small  | Gradle-kts(3)+cmake    | 156  | 15404  | .kt152/.xml9/.java2             | 1  | 5   | 205 | 23 | 无                                 | 5 | 1 | 16    | EN-conv |

### C-2 FW 9 仓

| 仓role体量档构建src文件src行主语言(ext)aidlbindersyspropsrtosprivIncCI文件分支tagcommits |               |        |                       |      |        |                                         |     |      |     |    |     |                                   |   |   |      |
| ------------------------------------------------------------------------ | ------------- | ------ | --------------------- | ---- | ------ | --------------------------------------- | --- | ---- | --- | -- | --- | --------------------------------- | - | - | ---- |
| vehicle-property-service                                                 | small/high    | small  | Soong(.bp3)+cmake8    | 276  | 77624  | .java216/.aidl50                        | 50  | 289  | 19  | 0  | 0   | workflows+TEST\_MAPPING           | 5 | 1 | 16   |
| vehicle-hal-adapter                                                      | medium/high   | medium | Soong(.bp6)+mk+cmake  | 609  | 159731 | .java469/.aidl101                       | 101 | 678  | 43  | 0  | 0   | workflows+PREUPLOAD+TEST\_MAPPING | 6 | 1 | 9    |
| vehicle-diagnostics                                                      | large/high    | large  | Soong(.bp88)+mk       | 1539 | 309137 | .java861/.xml721/.h232/.cpp227/.aidl217 | 217 | 1155 | 54  | 0  | 101 | workflows+PREUPLOAD+TEST\_MAPPING | 6 | 1 | 7    |
| soa-gateway                                                              | medium/medium | medium | gradle+cmake7+mk      | 635  | 149839 | .java431/.aidl136                       | 136 | 971  | 53  | 0  | 0   | PREUPLOAD+TEST\_MAPPING           | 6 | 1 | 8    |
| cockpit-manager-kit                                                      | small/medium  | small  | gradle+cmake4         | 281  | 77719  | .java223/.aidl52                        | 52  | 288  | 19  | 10 | 0   | TEST\_MAPPING                     | 5 | 2 | 14   |
| update-manager-service                                                   | large/medium  | large  | Soong(.bp42)+mk+cmake | 1209 | 281164 | .java1042/.xml866/.aidl144              | 144 | 1304 | 93  | 10 | 0   | PREUPLOAD+TEST\_MAPPING           | 6 | 1 | 6    |
| car-runtime-service                                                      | small/low     | small  | Soong(.bp1)           | 322  | 55119  | .java285/.aidl37                        | 37  | 97   | 308 | 0  | 0   | TEST\_MAPPING                     | 5 | 1 | 17   |
| platform-compat-service                                                  | large/low     | large  | Soong(.bp45)+mk2      | 1567 | 341662 | .java1266/.xml862/.aidl278              | 278 | 1995 | 108 | 0  | 0   | PREUPLOAD+TEST\_MAPPING           | 6 | 1 | 10   |
| vehicle-platform-service                                                 | medium/low    | medium | Soong(.bp4)+mk26      | 652  | 127380 | .java528/.xml154/.aidl121               | 121 | 780  | 17  | 2  | 0   | PREUPLOAD                         | 7 | 1 | 2802 |

### C-3 正式 18 仓分支名全集（命名分类法实例）

- 通用：`main`（默认，承载代码）、`develop`
- 平台分支：`platform/8155`、`platform/8295`、`platform/xinqing`
- release：`release/2026.1`、`release/1.0`、`release/2.0`、`release/0.8`、`release/0.9`、`release/sop-2024`、`release/sop-2025`、`release/sop-2019`
- sop 车型：`sop/2026.1-model-a1`、`sop/2026.1-model-b2`、`sop/2024-model-a1`、`sop/2024-model-b2`
- 特殊：`presubmit/launcher-contracts`(horizon)、`aosp-new/aosp-new/master`(hal-adapter/diagnostics/soa/update-manager)、`aosp/pie-release`(vehicle-platform)

### C-4 正式 18 仓 tag 全集

- v 系列：`v1.0.0`(climatix)、`v2.0.0`(vehicle-property/cockpit-manager-kit)、`v0.9.0`(thermo)、`v0.8.0`(car-runtime)
- local-sop 系列：`local-sop-2026.1`(aurora/horizon/hal-adapter)、`local-sop-2024.4`(atlas)、`local-sop-2025.4`(nova/platform-compat)、`local-sop-2019.4`(vehicle-platform)
- repo-年份系列：`motion-control-2026.1`、`market-hub-2026.1`、`cockpit-shell-2026.1`、`vehicle-diagnostics-2026.1`、`soa-gateway-2026.1`、`update-manager-2026.1`、`manager-kit-2026.1`
- foundation：`app-foundation-1.0.0`(motion-control/market-hub)
- AOSP 残留：`android-10.0.0_r7~r14`(atlas 6 个)

---

## 附录 D：给 codex 的执行清单（汇总裁定点）

**必须先裁定（🟡 范式开关，决定全局）**

1. FW 语言范式（§2.1）：C/C++ 系（像生产 external/vendor）还是 Java/AIDL 系（像正式 Car 服务）？→ 联动 §3.1 构建、§5.2 IPC、§5.4 嵌入式。
2. FW 类型配比（§1.2）：是否按生产 OSS 58%/packages 21%/vendor 21% 三类造，还是只造一方车服务？
3. 体量×质量分布（§7.2）：用正式 3×3 均匀矩阵，还是仿生产长尾（需另给体量配比，#4/#5 已丢弃）？

**缺口需补（🔴 生产未采）** 4. APP 语言构成分布（§2.2）——生产未采，用正式实测补位。 5. 缺陷频率 prevalence（§6.3）——生产未采，需给每条 D01–D06 注入概率。 6. 质量档分布（§7.1）——生产空壳，当前只能用正式均匀矩阵。 7. **维度间关联规则/仓型原型（§7.3）**——最关键缺失，建议建 archetype 库（OSS/vendor/packages/一方app 各一套绑定维度），避免独立边际采样造出畸形组合。 8. CI 形态分布（§8.1）——生产未采，按 benchmark ci\_independence 0–3 档造证据。 9. 测试形态分布（§8.2）——生产未采，按 benchmark integration\_test(scoring\_android) 0–3 档造证据（用 Android 测试栈，非 embedded）。

**与评分链路的硬冲突（⚠ 必须解决否则评估失败）** 10. master 语义（§4.4）：生产 FW「空 master + 代码在 feature 分支」与「引擎在默认分支评分」冲突——要么引擎支持 checkout 非 master（生产 R1 规则），要么虚拟仓代码必须放默认分支（放弃空 master 拟真）。 11. 缺陷 D04/D05（§6.2）：D04 评分目标 platform\_coupling 已被 v3 删除、D05「非空 master」在新口径不扣分且与正式仓冲突——建议弃用或重挂。

**可直接用（🟢 生产有真实分布）**

- APP 类型/功能域（§1.1）、FW 三类型（§1.2）、gradle 模块数/名/依赖频率（§3.3–3.5）、分支命名形态（§4.2）、master 空规则（§4.4，受 #10 约束）、提交信息中文缺陷单风格（§4.5）、反射密度（§5.3）、APP 缺陷 D01–D06（§6.1，按新叶量程）。

**评分口径（🔵 铁律）**

- 一律照 §9 benchmark 新契约（APP 8叶/40、FW 11叶/52），禁止用生产包 prompts\_standard 任何维度/量程/embedded/max:3。

---

*文档结束。来源：app/fw-repo-generator-pack（synth\_spec=仓库特征·有效 / prompts\_standard=旧口径·作废 / structure\_report=规模列+仓名）；正式 18 仓 official-profile.json + manifest.json + facts/oracle；权威口径 contract-20260903.json + benchmark-standard.json(v0.7.x)。整理 2026-09-07，mini-benchmark session。*