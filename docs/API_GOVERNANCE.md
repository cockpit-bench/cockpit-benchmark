Current v0.9.1: the v3.5 API decisions below remain unchanged. FW-07 frozen-external raw inputs are now supplied separately in EXTERNAL_GIT_INPUTS.md; its source-only eligibility is still unknown. Current Android total is 269/828 after two non-API SOLID corrections.

# v0.8.6 API governance scope B

Contract v3.5 implements the explicitly approved scope B. All 18 API leaves were source-reviewed against their unchanged final HEADs. The other 153 complete canonical leaf objects remain unchanged. Total: **271/828**. Historical releases retain their original contract and scores.

Three points require every critical production API/ABI responsibility to be covered; two points allow semantic version governance or real partial compatibility coverage. Unknown inventory/responsibility fails instead of becoming a low numeric score. Groups follow actual consumers and release boundaries, not every public symbol or LOC.

| Repository | API before → after | Covered / critical groups | Reason |
|---|---|---|---|
| APP-01 | 1 → 1 | 0 / 4 | SDK 使用日期/Git 生成的发布版本；Wear 协议只做整数版本匹配，未发现关键 API/ABI 的真实发布基线兼容 diff，仍为手工版本治理 1。 |
| APP-02 | 1 → 1 | 0 / 6 | 三个对外 Maven 库有手工版本和发布流程；explicit API 可见性约束、人工避免破坏 API 的说明不等于兼容 diff，安装 IPC 等关键边界也未覆盖，1。 |
| APP-03 | 1 → 1 | 0 / 0 | 单 APK 无自有关键跨应用 API/ABI；普通 MAIN/Activity 生命周期不人为纳入关键分母。仅手工 versionName 1.0.0，无语义化治理或真实兼容机制，1，不能以空分母获得 3。 |
| APP-11 | 1 → 1 | 0 / 4 | 仅应用手工版本；MediaBrowser、共享 URI、远端同步和播放依赖边界无真实发布基线兼容 diff；协议路径 /api/2 不是语义化 API 治理，1。 |
| APP-13 | 1 → 1 | 0 / 1 | 应用有手工版本；Camera2 核心消费与自有生产范围已核对，无真实 API/ABI 基线检查或完整外部固定责任，1。 |
| APP-14 | 1 → 1 | 0 / 4 | 插件接口有整数 VERSION 和运行时相等校验，但未提取并比较发布 API；共享跨进程 AIDL、系统组件和平台依赖也无完整治理，1。 |
| APP-15 | 0 → 0 | 0 / 3 | Settings 路由、Provider/Slice 与平台接口责任可建立；未发现产品/API 版本治理或真实兼容 diff，0。 |
| APP-16 | 1 → 1 | 0 / 4 | 应用与库有手工版本；Quickstep IPC、插件与搜索/权限控制的 Provider 边界无真实发布兼容 diff，外部 sysui_shared.jar 也未固定，1。 |
| APP-17 | 0 → 0 | 0 / 2 | Car HVAC 调用和受保护广播为真实关键接口；未发现版本治理或真实兼容机制，同 APK LocalBinder 不作为对外边界，0。 |
| FW-02 | 3 → 2 | 2 / 5 | 两套自有关键 Stable AIDL 有真实冻结/当前定义与版本化生产消费者；跨仓 Java client 暴露面、INetd/平台模块责任与其他外部 ABI 尚无完整兼容治理。方案 B 满足部分真实覆盖 2，不能将 AIDL 局部机制扩成全仓 3。 |
| FW-03 | 3 → 2 | 1 / 6 | 先清点 MAP、平台 Binder、Provider/intent、外部 native ABI 与同包 JNI：MAP 为真实关键生产边界且具发布基线提取/diff，其他关键受管边界无等价覆盖，故方案 B 为 2；没有因旧样例名称自动降档。 |
| FW-07 | 3 → 2 | 3 / 7 | 方案B审定2（repo_plus_external）：经固定官方Soong/default源码及extension7六份API/removed基线补证，public/system/module-lib存在实际当前→released兼容机制。关键cross-repo Binder、Parcelable与外部HAL/Mainline责任仍不全覆盖，因此不是3。未运行Soong/Metalava；签名字节一致不当执行通过。 |
| FW-08 | 3 → 2 | 1 / 8 | 已清点三套 Java SDK（含 Nearby）、native AIDL、两套导出 C ABI、外部 IPC/HAL/Cronet 及同 APEX 胶合。Stable native AIDL 有当前/冻结 V1 与真实服务/消费者，属于真实关键覆盖；其他关键面存在明确未闭合发布基线或外部责任，故 2 而非沿用单 Java 机制的 3。 |
| FW-10 | 1 → 1 | 0 / 5 | 服务回调、导出历史 Provider、跨仓共享常量和广播交付边界可完整建立；只有 Manifest 的 versionCode 300000000/versionName R-initial 手工版本，无任何关键边界真实发布基线提取/diff。SDK/platform 依赖声明不能抬到 2。 |
| FW-14 | 3 → 2 | 5 / 15 | 方案B为2：watchdog/telemetry/computepipe生产稳定AIDL有冻结dump/hash与真实机制，public/system droidstubs亦存在；builtin/module忽略missing latest、daemon unstable IPC、公开proto/vendor C++与外部责任未完整覆盖。 |
| FW-15 | 0 → 0 | 0 / 4 | 真实 Telecom Loader/ITelecomService、连接/通话插件 Binder、跨应用拨号入口和平台服务依赖清单可建立；无产品/API 版本治理、受控发布基线或真实兼容 diff。仅源码平台构建和测试 JNI，按方案 B 为 0，不把外部 Android 责任自动当已覆盖。 |
| FW-16 | 3 → 2 | 2 / 20 | 方案B为2：public/system/module-lib Metalava机制及OMAPI稳定AIDL、sysprop存在；graphics忽略missing latest、SYSTEM_SERVER只current+lint、跨仓security/media Binder、SystemUI Launcher/plugin及native提供/消费责任未全覆盖。 |
| FW-18 | 0 → 0 | 0 / 6 | 已清点自有导出 Java/IIccPhoneBook/ICC Provider、平台 Binder 实现、运营商/IMS服务与版本化 radio HAL 消费边界。HIDL 1.0–1.4 选择和运行时回退属真实消费适配，未发现关键自有边界的版本治理/提取 diff，也未建立可独立满足 2 的真实兼容机制；因此 0。 |

Group counts are descriptive and are not weighted coverage scores. The full per-boundary owner, consumer, release scope, version/baseline, mechanism and source anchors are in facts/<ID>.json and the matching maintainer data pack. Excluded same-release glue still records the external interfaces that remain in scope.

Mechanism presence and execution success are separate. Java signatures do not certify URI/permission behavior; JNI descriptors do not certify native ABI or Binder wire compatibility. No new full Android build/device integration execution is claimed. Rule replay checks disclosed judgments and source bindings, not independent semantic completeness.

The 18 sources and all source refs remain unchanged. Existing v0.8.1 18-main/25-submodule restore evidence applies to the unchanged restore behavior. Pending 22 and MATLAB remain outside this release. Eight non-API boundary regression leaves keep their exact source/reference scores and are separately rebound to the unchanged relevant v3.5 rules.

## Reviewed input and verification boundary

Each API observation supplies `evaluation_revision`, `semantic_api_versioning`,
`manual_api_version_exists`, and `api_governance`. The latter binds the same
revision, an explicit `inventory_complete` adjudication, `unresolved: []`, a
`scope_basis`, and a nonempty list of reviewed `boundaries`. Even repositories
with no critical external interface retain their explicitly excluded groups;
an empty critical denominator never earns three points.

Each group records its ID, type, provided/consumed/internal role, owner, consumer,
`owns_contract`, criticality and scope rationale, version/baseline, mechanism,
coverage rationale, and two distinct source anchors. `covered` requires version
control plus either a real compatibility mechanism or verified external fixed
interface responsibility. A repository-owned contract requires real extraction
and comparison; a dependency version or an external ownership assertion alone
does not qualify. A genuine partial mechanism can qualify for two while leaving
the group's full `covered` flag false.

The verifier validates this structure, source HEAD, anchor coordinates and Git
bytes. `binding_files`, when supplied, bind actual current/baseline files to Git
blob and SHA-256 values. A hashed `source_inventory` in the maintainer archive
binds the tracked path inventory and records the reviewed boundary catalog.
`current_binding` and `released_binding` descriptions, ownership, criticality,
scope completeness and mechanism semantics remain human-reviewed judgments;
the verifier does not prove these claims merely by checking strings or hashes.
Old version/check booleans without the reviewed scope cannot silently earn a
numeric API score. Synthetic regression fixtures exercise all/partial coverage,
unknown and empty scope, excluded groups, delegated responsibility, stale HEADs,
and modified source/inventory bytes; they are not production build execution.

## FW-07 external evidence and evaluator availability

The maintainer review resolves the actual `framework-wifi` public/system/module-lib
released baselines to SDK `extensions/7`, through fixed Android 14 release Soong
and module defaults. The six API/removed files match both their published Git
blob IDs and this repository's signature bytes. This establishes the disclosed
compatibility mechanism and its fixed inputs, without claiming a successful
Soong/Metalava execution. Other critical Binder, Parcelable and HAL responsibilities
remain uncovered, so the whole-repository score is two.

The archive's `api-inventories/FW-07.json` records immutable upstream commits,
URLs, SHA-256 values, baseline selection and byte comparisons. Raw external source
files are retained locally and are **not** in this archive. Public replay checks
the disclosed inventory binding but does not fetch or authenticate those external
bytes. Consequently FW-07 API stays `unknown` in `source_only` and the present
`frozen_external` profile. Maintainer observations are not candidate inputs.
The current common profile has 155 supported leaves, 15 unknown and one unavailable
historical APP-02 CI leaf; no candidate accuracy experiment is claimed.
