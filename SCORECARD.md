# Validation-18 标准评分总表

- APP：9 仓 / 72 叶 / 242/360
- Android Framework：9 仓 / 99 叶 / 275/468
- 合计：18 仓 / 171 叶 / 517/828

> 分数只由绑定 HEAD 的代码与 refs 证据推导；质量/规模标签是矩阵角色，不是打分输入。

## APP 9 仓

| ID | 仓库 | 角色 | 规模 | architecture.componentization | architecture.decoupling | architecture.modularization | compilation.ci_independence | compilation.compilation_independence | compilation.api_version_management | platform_reuse.platform_upgrade | platform_reuse.release_branch_strategy | 总分 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| APP-03 | climatix-hvac | high |  | 5 | 3 | 3 | 3 | 0 | 3 | 10 | 8 | 35/40 |
| APP-02 | horizon-launcher | high |  | 5 | 3 | 3 | 2 | 0 | 2 | 10 | 8 | 33/40 |
| APP-01 | aurora-settings | high |  | 5 | 3 | 3 | 1 | 0 | 3 | 10 | 8 | 33/40 |
| APP-13 | market-hub | medium |  | 5 | 3 | 3 | 1 | 0 | 1 | 10 | 8 | 31/40 |
| APP-11 | motion-control | medium |  | 5 | 3 | 3 | 1 | 0 | 1 | 10 | 3 | 26/40 |
| APP-14 | cockpit-shell | medium |  | 5 | 3 | 3 | 1 | 0 | 2 | 8 | 8 | 30/40 |
| APP-17 | thermo-control | low |  | 3 | 2 | 2 | 0 | 0 | 1 | 3 | 8 | 19/40 |
| APP-16 | nova-launcher | low |  | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 8 | 20/40 |
| APP-15 | atlas-settings | low |  | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 3 | 15/40 |

## Android Framework 9 仓

| ID | 仓库 | 角色 | 规模 | compilation.ci_independence | compilation.compilation_independence | compilation.api_version_management | quality.integration_test | solid_principle.single_responsibility | solid_principle.open_closed | solid_principle.liskov_substitution | solid_principle.interface_segregation | solid_principle.dependency_inversion | platform_reuse.platform_upgrade | platform_reuse.release_branch_strategy | 总分 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FW-02 | vehicle-property-service | high | small | 3 | 0 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 10 | 8 | 41/52 |
| FW-03 | vehicle-hal-adapter | high | medium | 3 | 0 | 3 | 3 | 3 | 4 | 3 | 3 | 4 | 10 | 8 | 44/52 |
| FW-07 | vehicle-diagnostics | high | large | 3 | 0 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 10 | 8 | 41/52 |
| FW-10 | cockpit-manager-kit | medium | small | 2 | 0 | 0 | 1 | 2 | 2 | 2 | 2 | 1 | 10 | 8 | 30/52 |
| FW-08 | soa-gateway | medium | medium | 2 | 0 | 3 | 2 | 2 | 3 | 3 | 3 | 3 | 10 | 8 | 39/52 |
| FW-14 | update-manager-service | medium | large | 2 | 0 | 3 | 1 | 2 | 2 | 3 | 2 | 2 | 3 | 8 | 28/52 |
| FW-15 | car-runtime-service | low | small | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 3 | 8 | 15/52 |
| FW-18 | vehicle-platform-service | low | medium | 1 | 0 | 3 | 2 | 1 | 1 | 2 | 2 | 1 | 3 | 3 | 19/52 |
| FW-16 | platform-compat-service | low | large | 1 | 0 | 3 | 2 | 1 | 1 | 2 | 1 | 1 | 3 | 3 | 18/52 |

## 逐叶理由与证据

### APP-03 `climatix-hvac` — 35/40

- `architecture.componentization`：**5/5** — 唯一架构事实：module_count=7、standard_named_module_count=3、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 5 分。
  - 证据：`facts/APP-03.json:1`; `settings.gradle.kts:4`
- `architecture.decoupling`：**3/3** — 唯一架构事实：module_count=7、standard_named_module_count=3、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-03.json:1`; `settings.gradle.kts:4`
- `architecture.modularization`：**3/3** — 唯一架构事实：module_count=7、standard_named_module_count=3、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-03.json:1`; `settings.gradle.kts:4`
- `compilation.ci_independence`：**3/3** — 精确 HEAD 的 CI 分类为 independent_ci；结合流水线内容完整度锁定 3 分。
  - 证据：`facts/APP-03.json:1`; `.github/workflows/android.yml:1`
- `compilation.compilation_independence`：**0/3** — 依赖事实为 {'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True}；同仓 project 源码依赖优先判 0，不能被 compileSdk 或 framework 表象抬分，锁定 0 分。
  - 证据：`facts/APP-03.json:1`; `app/build.gradle.kts:1`
- `compilation.api_version_management`：**3/3** — 手动版本=True、语义化管理=True、兼容性证据=7、自动化证据=0，锁定 3 分。
  - 证据：`facts/APP-03.json:1`; `version.properties:1`
- `platform_reuse.platform_upgrade`：**10/10** — 唯一升级事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 0}；严格按 10→8→3→0 首个满足档锁定 10 分。
  - 证据：`facts/APP-03.json:1`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 含统一 main 及 8155/8295 平台分支，没有车型级一车一 SOP；按同平台同一分支锁定 8 分。
  - 证据：`facts/APP-03.json:1`; `refs/heads/platform/8155`@`5141af902414`; `refs/heads/platform/8295`@`5141af902414`

### APP-02 `horizon-launcher` — 33/40

- `architecture.componentization`：**5/5** — 唯一架构事实：module_count=3、standard_named_module_count=2、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 5 分。
  - 证据：`facts/APP-02.json:1`; `settings.gradle:4`
- `architecture.decoupling`：**3/3** — 唯一架构事实：module_count=3、standard_named_module_count=2、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-02.json:1`; `settings.gradle:4`
- `architecture.modularization`：**3/3** — 唯一架构事实：module_count=3、standard_named_module_count=2、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-02.json:1`; `settings.gradle:4`
- `compilation.ci_independence`：**2/3** — 精确 HEAD 的 CI 分类为 mixed；结合流水线内容完整度锁定 2 分。
  - 证据：`facts/APP-02.json:1`; `.github/workflows/android.yml:1`
- `compilation.compilation_independence`：**0/3** — 依赖事实为 {'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False}；同仓 project 源码依赖优先判 0，不能被 compileSdk 或 framework 表象抬分，锁定 0 分。
  - 证据：`facts/APP-02.json:1`; `build.gradle:1`
- `compilation.api_version_management`：**2/3** — 手动版本=True、语义化管理=True、兼容性证据=0、自动化证据=0，锁定 2 分。
  - 证据：`facts/APP-02.json:1`; `version.properties:1`
- `platform_reuse.platform_upgrade`：**10/10** — 唯一升级事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': False, 'version_bound_status': 0}；严格按 10→8→3→0 首个满足档锁定 10 分。
  - 证据：`facts/APP-02.json:1`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 含统一 main 及 8155/8295 平台分支，没有车型级一车一 SOP；按同平台同一分支锁定 8 分。
  - 证据：`facts/APP-02.json:1`; `refs/heads/platform/8155`@`82f129b9d9c1`; `refs/heads/platform/8295`@`82f129b9d9c1`

### APP-01 `aurora-settings` — 33/40

- `architecture.componentization`：**5/5** — 高级档命中 module_count≥2、standard_named_module_count≥2、is_component_friendly=true 三项，满足任意两项后锁定 5 分；UI+domain 基础分层为 false 不影响已满足档位。
  - 证据：`settings.gradle:4`; `app/build.gradle:49`
- `architecture.decoupling`：**3/3** — 优秀档命中 module_count≥2、standard_named_module_count≥2、is_component_friendly=true，满足任意两项。
  - 证据：`settings-common/src/main/java/com/android/car/settings/common/platform/PlatformPropertyAdapter.java:19`; `settings.gradle:4`
- `architecture.modularization`：**3/3** — 依赖图 app 单向指向三个无反向 project 依赖的库，has_circular_dependency=false；高级档又命中 module_count≥2、standard_named_module_count≥2、is_component_friendly=true。
  - 证据：`app/build.gradle:49`; `settings-common/build.gradle:1`
- `compilation.ci_independence`：**1/3** — 无 GitHub/GitLab/Jenkins/Azure/APP_BUILD 独立流水线；TEST_MAPPING 与 PREUPLOAD.cfg 明确依赖 Android repo 的 presubmit/prebuilts/packages 路径，属于依赖安卓系统层 CI。
  - 证据：`TEST_MAPPING:1`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — app 通过 implementation project(...) 直接编译同仓 settings-common/settings-connectivity/settings-security 源码模块；仓内没有以预构建 SDK/AAR 形态消费这些依赖。按合同“直接依赖源代码”归 0 分，compileSdkVersion 35 只说明 Android 编译目标，不能把同仓源码依赖升级为 SDK/AAR。
  - 证据：`settings.gradle:4`; `app/build.gradle:49`
- `compilation.api_version_management`：**3/3** — version.properties 提供 1.1.0 语义化版本；构建校验格式并以 api/current.txt 检查向后兼容，RELEASE_NOTES 明确 major 破坏性变更规则，满足版本可控+前后兼容。
  - 证据：`version.properties:1`; `app/build.gradle:9`; `RELEASE_NOTES.md:9`
- `platform_reuse.platform_upgrade`：**10/10** — 严格从 10 分档开始：total_bound_status=1 与 has_interface_abstraction=true 两项命中，达到任意两项即锁定 10；虽然存在 hidden/reflection API 且有复杂通知适配，也不得越过已锁定档位再用 0 分条件倒打。
  - 证据：`settings-common/src/main/java/com/android/car/settings/common/platform/PlatformPropertyAdapter.java:19`; `settings-common/src/main/java/com/android/car/settings/common/platform/AndroidPlatformPropertyAdapter.java:19`; `app/src/main/java/com/android/car/settings/applications/appinfo/HibernationSwitchPreferenceController.java:92`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在统一 main 和 release/2026.1，但仍按 8155/8295 拆成真实 platform 分支；没有同版本车型级 SOP 分支，最贴合“同平台同一分支”8 分，而非跨平台完全合一的 10 分。
  - 证据：`refs/heads/platform/8155`@`769d29b8ea64`; `refs/heads/platform/8295`@`33e548d7b2fd`; `refs/heads/release/2026.1`@`c4801bf2d3c4`

### APP-13 `market-hub` — 31/40

- `architecture.componentization`：**5/5** — 唯一架构事实：module_count=9、standard_named_module_count=3、base_layered=False、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 5 分。
  - 证据：`facts/APP-13.json:1`; `settings.gradle:2`
- `architecture.decoupling`：**3/3** — 唯一架构事实：module_count=9、standard_named_module_count=3、base_layered=False、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-13.json:1`; `settings.gradle:2`
- `architecture.modularization`：**3/3** — 唯一架构事实：module_count=9、standard_named_module_count=3、base_layered=False、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-13.json:1`; `settings.gradle:2`
- `compilation.ci_independence`：**1/3** — 精确 HEAD 的 CI 分类为 android_system_ci；结合流水线内容完整度锁定 1 分。
  - 证据：`facts/APP-13.json:1`; `TEST_MAPPING:1`
- `compilation.compilation_independence`：**0/3** — 依赖事实为 {'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True}；同仓 project 源码依赖优先判 0，不能被 compileSdk 或 framework 表象抬分，锁定 0 分。
  - 证据：`facts/APP-13.json:1`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 手动版本=True、语义化管理=False、兼容性证据=0、自动化证据=0，锁定 1 分。
  - 证据：`facts/APP-13.json:1`; `CHANGELOG.md:1`
- `platform_reuse.platform_upgrade`：**10/10** — 唯一升级事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': False, 'version_bound_status': 0}；严格按 10→8→3→0 首个满足档锁定 10 分。
  - 证据：`facts/APP-13.json:1`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 含统一 main 及 8155/8295 平台分支，没有车型级一车一 SOP；按同平台同一分支锁定 8 分。
  - 证据：`facts/APP-13.json:1`; `refs/heads/platform/8155`@`3f421d00c591`; `refs/heads/platform/8295`@`3f421d00c591`

### APP-11 `motion-control` — 26/40

- `architecture.componentization`：**5/5** — 排除 foundation-testkit 与 motion-tests 后 module_count=9；standard_named_module_count=3 且 is_component_friendly=true，已满足高级档任意两项。
  - 证据：`settings.gradle:1`; `foundation-core/build.gradle:1`
- `architecture.decoupling`：**3/3** — 优秀档命中 module_count≥2、standard_named_module_count≥2、is_component_friendly=true；虽然没有 UI/domain 目录标记，仍满足任意两项。
  - 证据：`motion-core/build.gradle:1`; `motion-platform/build.gradle:1`
- `architecture.modularization`：**3/3** — 完整 project 依赖图是从 app/platform/observability/storage 指向 api/core 的有向无环图，未触发循环依赖一票否决；高级档满足 module_count、standard_named_module_count、component_friendly。
  - 证据：`motion-app/build.gradle:1`; `foundation-observability/build.gradle:1`
- `compilation.ci_independence`：**1/3** — 无独立标准 CI 配置；TEST_MAPPING 仅声明 Android presubmit/postsubmit 测试名，属于依赖安卓系统层流水线。
  - 证据：`TEST_MAPPING:1`
- `compilation.compilation_independence`：**0/3** — 九个生产模块均作为同仓 Gradle project 源码构建，并通过 implementation project(...) 形成依赖图；未见业务依赖以预构建 SDK/AAR 输入。按 0 分“源码依赖”定档；AGP 8.7.3 和 compileSdkVersion 35 是构建工具/平台版本，不是稳定业务 SDK。
  - 证据：`settings.gradle:2`; `motion-app/build.gradle:5`
- `compilation.api_version_management`：**1/3** — 应用内手写 versionCode 1/versionName 1.0，CHANGELOG 标题为 1.0.0，但没有单一版本源、自动化、兼容性检查或向后兼容合同，属于手动版本不可控。
  - 证据：`motion-app/build.gradle:2`; `CHANGELOG.md:1`
- `platform_reuse.platform_upgrade`：**10/10** — 10 分档中 total_bound_status=0、has_interface_abstraction=true、has_complex_permission_adaptation=false 三项命中，立即锁定 10；反射 SystemProperties 使 non-compatible API=true，但锁档规则禁止继续向低档倒打。
  - 证据：`motion-platform/src/main/java/com/cockpitbench/motion/platform/PlatformMotionAdapter.java:16`; `motion-core/src/main/java/com/cockpitbench/motion/core/ActuatorSignalRouter.java:16`; `motion-app/src/main/AndroidManifest.xml:1`
- `platform_reuse.release_branch_strategy`：**3/10** — 同一 2026.1 版本存在 model-a1 与 model-b2 两条车型后缀 SOP 分支；二者 tree 不同，属性被 build.gradle 生成 BuildConfig 并由 PlatformMotionAdapter 消费，属于真实“单车型单 SOP”而不是空分支。
  - 证据：`refs/heads/sop/2026.1-model-a1`@`418aba900972`; `refs/heads/sop/2026.1-model-b2`@`dc7ac0a5e97e`; `refs/heads/sop/2026.1-model-a1`@`418aba900972`

### APP-14 `cockpit-shell` — 30/40

- `architecture.componentization`：**5/5** — 唯一架构事实：module_count=2、standard_named_module_count=2、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 5 分。
  - 证据：`facts/APP-14.json:1`; `settings.gradle:4`
- `architecture.decoupling`：**3/3** — 唯一架构事实：module_count=2、standard_named_module_count=2、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-14.json:1`; `settings.gradle:4`
- `architecture.modularization`：**3/3** — 唯一架构事实：module_count=2、standard_named_module_count=2、base_layered=True、component_friendly=True、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-14.json:1`; `settings.gradle:4`
- `compilation.ci_independence`：**1/3** — 精确 HEAD 的 CI 分类为 android_system_ci；结合流水线内容完整度锁定 1 分。
  - 证据：`facts/APP-14.json:1`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 依赖事实为 {'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False}；同仓 project 源码依赖优先判 0，不能被 compileSdk 或 framework 表象抬分，锁定 0 分。
  - 证据：`facts/APP-14.json:1`; `build.gradle:1`
- `compilation.api_version_management`：**2/3** — 手动版本=True、语义化管理=True、兼容性证据=0、自动化证据=0，锁定 2 分。
  - 证据：`facts/APP-14.json:1`; `version.properties:1`
- `platform_reuse.platform_upgrade`：**8/10** — 唯一升级事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'version_bound_status': 1}；严格按 10→8→3→0 首个满足档锁定 8 分。
  - 证据：`facts/APP-14.json:1`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 含统一 main 及 8155/8295 平台分支，没有车型级一车一 SOP；按同平台同一分支锁定 8 分。
  - 证据：`facts/APP-14.json:1`; `refs/heads/platform/8155`@`83cc55774e72`; `refs/heads/platform/8295`@`83cc55774e72`

### APP-17 `thermo-control` — 19/40

- `architecture.componentization`：**3/5** — 唯一架构事实：module_count=2、standard_named_module_count=1、base_layered=False、component_friendly=None、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-17.json:1`; `settings.gradle.kts:4`
- `architecture.decoupling`：**2/3** — 唯一架构事实：module_count=2、standard_named_module_count=1、base_layered=False、component_friendly=None、circular=False；按任意 N 条与循环依赖规则由高到低锁定 2 分。
  - 证据：`facts/APP-17.json:1`; `settings.gradle.kts:4`
- `architecture.modularization`：**2/3** — 唯一架构事实：module_count=2、standard_named_module_count=1、base_layered=False、component_friendly=None、circular=False；按任意 N 条与循环依赖规则由高到低锁定 2 分。
  - 证据：`facts/APP-17.json:1`; `settings.gradle.kts:4`
- `compilation.ci_independence`：**0/3** — 精确 HEAD 的 CI 分类为 no_ci；结合流水线内容完整度锁定 0 分。
  - 证据：`facts/APP-17.json:1`
- `compilation.compilation_independence`：**0/3** — 依赖事实为 {'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True}；同仓 project 源码依赖优先判 0，不能被 compileSdk 或 framework 表象抬分，锁定 0 分。
  - 证据：`facts/APP-17.json:1`; `app/build.gradle.kts:1`
- `compilation.api_version_management`：**1/3** — 手动版本=True、语义化管理=False、兼容性证据=0、自动化证据=0，锁定 1 分。
  - 证据：`facts/APP-17.json:1`; `app/build.gradle.kts:1`
- `platform_reuse.platform_upgrade`：**3/10** — 唯一升级事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 1}；严格按 10→8→3→0 首个满足档锁定 3 分。
  - 证据：`facts/APP-17.json:1`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 含统一 main 及 8155/8295 平台分支，没有车型级一车一 SOP；按同平台同一分支锁定 8 分。
  - 证据：`facts/APP-17.json:1`; `refs/heads/platform/8155`@`ef1114ba61b3`; `refs/heads/platform/8295`@`ef1114ba61b3`

### APP-16 `nova-launcher` — 20/40

- `architecture.componentization`：**3/5** — 唯一架构事实：module_count=4、standard_named_module_count=1、base_layered=False、component_friendly=None、circular=False；按任意 N 条与循环依赖规则由高到低锁定 3 分。
  - 证据：`facts/APP-16.json:1`; `settings.gradle:4`
- `architecture.decoupling`：**2/3** — 唯一架构事实：module_count=4、standard_named_module_count=1、base_layered=False、component_friendly=None、circular=False；按任意 N 条与循环依赖规则由高到低锁定 2 分。
  - 证据：`facts/APP-16.json:1`; `settings.gradle:4`
- `architecture.modularization`：**2/3** — 唯一架构事实：module_count=4、standard_named_module_count=1、base_layered=False、component_friendly=None、circular=False；按任意 N 条与循环依赖规则由高到低锁定 2 分。
  - 证据：`facts/APP-16.json:1`; `settings.gradle:4`
- `compilation.ci_independence`：**1/3** — 精确 HEAD 的 CI 分类为 android_system_ci；结合流水线内容完整度锁定 1 分。
  - 证据：`facts/APP-16.json:1`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 依赖事实为 {'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False}；同仓 project 源码依赖优先判 0，不能被 compileSdk 或 framework 表象抬分，锁定 0 分。
  - 证据：`facts/APP-16.json:1`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 手动版本=True、语义化管理=False、兼容性证据=0、自动化证据=0，锁定 1 分。
  - 证据：`facts/APP-16.json:1`; `build.gradle:1`
- `platform_reuse.platform_upgrade`：**3/10** — 唯一升级事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'version_bound_status': 3}；严格按 10→8→3→0 首个满足档锁定 3 分。
  - 证据：`facts/APP-16.json:1`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 含统一 main 及 8155/8295 平台分支，没有车型级一车一 SOP；按同平台同一分支锁定 8 分。
  - 证据：`facts/APP-16.json:1`; `refs/heads/platform/8155`@`730463f93a9b`; `refs/heads/platform/8295`@`730463f93a9b`

### APP-15 `atlas-settings` — 15/40

- `architecture.componentization`：**3/5** — 高级档仅命中 module_count≥2 一项：standard_named_module_count=1、无 base layered、没有两个分层业务模块，且跨 included-module main source root 侵入使 component_friendly=false。中档命中 module_count≥2、standard_named_module_count≥1、业务分包结构三项，锁定 3。
  - 证据：`settings.gradle:4`; `app/build.gradle:5`
- `architecture.decoupling`：**2/3** — 优秀档因 component_friendly=false、standard_named_module_count<2 且无 base layered，只命中 module_count 一项；良好档命中 module_count≥2、standard_named_module_count≥1、业务分包结构，锁定 2。
  - 证据：`app/build.gradle:6`; `platform-bridge/build.gradle:1`
- `architecture.modularization`：**2/3** — 声明的 project 依赖图无环，未触发 0 分否决；但高级档只命中 module_count≥2。中档命中 module_count≥2、standard_named_module_count≥1、业务分包结构，锁定 2。
  - 证据：`app/build.gradle:10`; `modern-tests/build.gradle:5`
- `compilation.ci_independence`：**1/3** — 无独立标准 CI 配置；PREUPLOAD.cfg 的 checkstyle/ktlint 明确依赖 Android repo 根下 prebuilts 工具，属于依赖安卓系统层 CI。
  - 证据：`PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — settings.gradle 已把 platform-bridge 声明为独立 included module，但 app 的 main java.srcDirs 直接指向该 sibling module 源码且未声明 project(':platform-bridge')；这是明确的直接源码依赖，按 0 分档。
  - 证据：`settings.gradle:4`; `app/build.gradle:6`
- `compilation.api_version_management`：**1/3** — manifest 中仅手写 versionCode=1/versionName=1.0，仓内无 version.properties/VERSION/CHANGELOG/RELEASE_NOTES、semver 自动校验或兼容性检查，属于手动版本不可控。
  - 证据：`app/src/main/AndroidManifest.xml:19`
- `platform_reuse.platform_upgrade`：**3/10** — 10 分档只命中 total≤1；8 分档只命中 total≤3，均不足两项。3 分档命中“无架构专属依赖”与 total≤4，按任意一项立即锁定 3；因此不再评估包含 non-compatible API 的 0 分档。
  - 证据：`platform-bridge/src/main/java/com/android/car/settings/platform/LegacySettingsRuntime.java:18`; `platform-bridge/src/main/java/com/android/car/settings/platform/SettingsPageCoordinator.java:19`; `modern-settings/src/main/java/com/android/car/settings/applications/appinfo/HibernationSwitchPreferenceController.java:92`; `app/src/main/java/com/android/car/settings/bluetooth/BluetoothPairingService.java:104`
- `platform_reuse.release_branch_strategy`：**3/10** — 同一 2024 版本有 model-a1 与 model-b2 两条车型后缀 SOP 分支；A1/B2 manifest 元数据不同，SettingsModelProfile 读取并由 PageCoordinator 消费，属于真实单车型单 SOP。旧 platform/release 分支的未消费 property 不改变该车型级 SOP 事实。
  - 证据：`refs/heads/sop/2024-model-a1`@`29e98aef4200`; `refs/heads/sop/2024-model-b2`@`676c405af0f6`; `refs/heads/sop/2024-model-a1`@`29e98aef4200`; `refs/heads/sop/2024-model-a1`@`29e98aef4200`

### FW-02 `vehicle-property-service` — 41/52

- `compilation.ci_independence`：**3/3** — 独立 GitHub Actions 包含真实构建、测试、覆盖率门禁和报告上传，且 final HEAD 运行成功。
  - 证据：`facts/FW-02.json:1`; `.github/workflows/native.yml:2`; `https://github.com/cockpit-bench/vehicle-property-service/actions/runs/33758455763:1`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-02.json:1`; `Android.bp:13`; `Android.bp:13`
- `compilation.api_version_management`：**2/3** — VERSION/CMake 使用三段语义化版本，但缺少覆盖完整 Android API 的兼容 baseline。
  - 证据：`facts/FW-02.json:1`; `native/VERSION:1`; `native/CMakeLists.txt:2`
- `quality.integration_test`：**3/3** — 真实断言覆盖关键模块交互，覆盖代理达到 50%，且 final HEAD 独立流水线测试 100% 通过。
  - 证据：`facts/FW-02.json:1`; `native/tests/vehicle_property_integration_test.cpp:7`; `TEST_MAPPING:1`; `https://github.com/cockpit-bench/vehicle-property-service/actions/runs/33758455763:1`
- `solid_principle.single_responsibility`：**3/4** — 策略、平台访问、HAL 与 Binder 职责有边界；仍保留 CarShellCommand 等大类，故为良好而非优秀。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-02.json:1`; `platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:1`; `runtime/src/com/android/car/VehicleStub.java:1`
- `solid_principle.open_closed`：**3/4** — VehicleStub 与策略对象提供扩展点，平台/HAL 变化无需集中改写属性策略。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-02.json:1`; `runtime/src/com/android/car/VehicleStub.java:1`; `api/src/android/car/hardware/property/ICarProperty.aidl:1`
- `solid_principle.liskov_substitution`：**3/4** — AIDL/HIDL VehicleStub 实现遵守共同读写、订阅和死亡通知契约，异常语义一致。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-02.json:1`; `api/src/android/car/hardware/property/ICarProperty.aidl:1`; `platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:1`
- `solid_principle.interface_segregation`：**3/4** — 属性、回调和策略接口按客户端职责拆分，未把所有车辆能力压入单一新接口。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-02.json:1`; `platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:1`; `runtime/src/com/android/car/VehicleStub.java:1`
- `solid_principle.dependency_inversion`：**3/4** — 服务主要依赖 VehicleStub/HalClient 等抽象；PlatformVehicleAccess 的反射仍是边界内具体机制。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-02.json:1`; `runtime/src/com/android/car/VehicleStub.java:1`; `api/src/android/car/hardware/property/ICarProperty.aidl:1`
- `platform_reuse.platform_upgrade`：**10/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 10。
  - 证据：`facts/FW-02.json:1`; `api/src/android/car/VehiclePropertyIds.java:2279`; `api/src/android/car/AoapService.java:58`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-02.json:1`; `refs/heads/platform/8155`@`fab2b54427e9`; `refs/heads/platform/8295`@`1c687eb3c852`

### FW-03 `vehicle-hal-adapter` — 44/52

- `compilation.ci_independence`：**3/3** — 独立 GitHub Actions 包含真实构建、测试、覆盖率门禁和报告上传，且 final HEAD 运行成功。
  - 证据：`facts/FW-03.json:1`; `.github/workflows/native-ci.yml:17`; `https://github.com/cockpit-bench/vehicle-hal-adapter/actions/runs/33757391217:1`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-03.json:1`; `Android.bp:14`; `Android.bp:14`
- `compilation.api_version_management`：**3/3** — 存在 current/released API baseline 与 check_api/checkapi 或等价兼容验证，版本可控并约束向后兼容。
  - 证据：`facts/FW-03.json:1`; `native/contract/include/fw03/api/vehicle_hal_api_version.h:11`; `native/CHANGELOG.md:11`
- `quality.integration_test`：**3/3** — 真实断言覆盖关键模块交互，覆盖代理达到 50%，且 final HEAD 独立流水线测试 100% 通过。
  - 证据：`facts/FW-03.json:1`; `native/tests/client_ipc_vertical_integration_test.cpp:170`; `TEST_MAPPING:1`; `https://github.com/cockpit-bench/vehicle-hal-adapter/actions/runs/33757391217:1`
- `solid_principle.single_responsibility`：**3/4** — Vehicle HAL、传输、契约、应用生命周期分层清楚，但上游服务仍存在若干大类。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-03.json:1`; `service/src/com/android/car/VehicleStub.java:1`; `service/src/com/android/car/AidlVehicleStub.java:1`
- `solid_principle.open_closed`：**4/4** — AIDL/HIDL 适配与 native transport/clock/session 均可替换，扩展通常新增实现而非改核心协议。 按 0–4 独立档位锁定 4 分。
  - 证据：`facts/FW-03.json:1`; `service/src/com/android/car/AidlVehicleStub.java:1`; `native/application/include/fw03/application/vehicle_service.h:1`
- `solid_principle.liskov_substitution`：**3/4** — AidlVehicleStub/HidlVehicleStub 完整实现 VehicleStub 合同，测试覆盖超时、死亡与订阅语义。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-03.json:1`; `native/application/include/fw03/application/vehicle_service.h:1`; `service/src/com/android/car/VehicleStub.java:1`
- `solid_principle.interface_segregation`：**3/4** — VehicleStub 的订阅子接口和细分 AIDL 将客户端职责隔离，少数 car-lib 公共接口仍较宽。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-03.json:1`; `service/src/com/android/car/VehicleStub.java:1`; `service/src/com/android/car/AidlVehicleStub.java:1`
- `solid_principle.dependency_inversion`：**4/4** — 高层 VehicleService/VehiclePropertyGateway 依赖 port/transport/clock 抽象并由构造装配。 按 0–4 独立档位锁定 4 分。
  - 证据：`facts/FW-03.json:1`; `service/src/com/android/car/AidlVehicleStub.java:1`; `native/application/include/fw03/application/vehicle_service.h:1`
- `platform_reuse.platform_upgrade`：**10/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 1, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 10。
  - 证据：`facts/FW-03.json:1`; `car-lib/src/android/car/hardware/CarPropertyConfig.java:419`; `car-lib/src/android/car/admin/CarDevicePolicyManager.java:52`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-03.json:1`; `refs/heads/platform/8155`@`270b396861b0`; `refs/heads/platform/8295`@`4449839764f7`

### FW-07 `vehicle-diagnostics` — 41/52

- `compilation.ci_independence`：**3/3** — 独立 GitHub Actions 包含真实构建、测试、覆盖率门禁和报告上传，且 final HEAD 运行成功。
  - 证据：`facts/FW-07.json:1`; `.github/workflows/native.yml:2`; `https://github.com/cockpit-bench/vehicle-diagnostics/actions/runs/33758464550:1`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-07.json:1`; `Android.bp:5`; `Android.bp:5`
- `compilation.api_version_management`：**3/3** — 存在 current/released API baseline 与 check_api/checkapi 或等价兼容验证，版本可控并约束向后兼容。
  - 证据：`facts/FW-07.json:1`; `car-lib/api/current.txt:1`; `car-lib/Android.bp:132`
- `quality.integration_test`：**3/3** — 真实断言覆盖关键模块交互，覆盖代理达到 50%，且 final HEAD 独立流水线测试 100% 通过。
  - 证据：`facts/FW-07.json:1`; `car-lib/src/android/car/test/CarLocationTestHelper.java:1`; `TEST_MAPPING:1`; `https://github.com/cockpit-bench/vehicle-diagnostics/actions/runs/33758464550:1`
- `solid_principle.single_responsibility`：**2/4** — 诊断、遥测、watchdog 边界明确，但 WatchdogPerfHandler 超过两千逻辑行，拉低 SRP。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-07.json:1`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:1`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:1`
- `solid_principle.open_closed`：**3/4** — 遥测 listener、watchdog AIDL 和 HAL service 可通过接口扩展，策略变化不集中在单个 switch。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-07.json:1`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:1`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:1`
- `solid_principle.liskov_substitution`：**3/4** — Manager/Service 与 Binder callback 的继承实现保留父契约，未发现空实现替代主路径。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-07.json:1`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:1`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:1`
- `solid_principle.interface_segregation`：**3/4** — 诊断、遥测、资源过载接口按领域拆分，客户端无需依赖全部车辆服务能力。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-07.json:1`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:1`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:1`
- `solid_principle.dependency_inversion`：**3/4** — 服务通过 AIDL、HalServiceBase 与 listener 抽象协作；少量具体服务构造仍限制到良好档。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-07.json:1`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:1`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:1`
- `platform_reuse.platform_upgrade`：**10/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 1, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 10。
  - 证据：`facts/FW-07.json:1`; `car-lib/src/android/car/VehiclePropertyIds.java:2279`; `car-lib/src/android/car/AoapService.java:58`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-07.json:1`; `refs/heads/platform/8155`@`85f0ccfb542a`; `refs/heads/platform/8295`@`87130476985f`

### FW-10 `cockpit-manager-kit` — 30/52

- `compilation.ci_independence`：**2/3** — 存在可执行 APP_BUILD 独立构建/测试入口，但没有完整标准化流水线。
  - 证据：`facts/FW-10.json:1`; `APP_BUILD:1`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-10.json:1`; `manager-runtime/build.gradle:3`; `manager-runtime/build.gradle:3`
- `compilation.api_version_management`：**0/3** — 没有专用版本文件、构建集成或 API baseline，锁定 0。
  - 证据：`facts/FW-10.json:1`; `manager-api/build.gradle:1`
- `quality.integration_test`：**1/3** — 存在真实断言并验证接口行为，但未证明关键跨组件覆盖代理达到 50%。
  - 证据：`facts/FW-10.json:1`; `native/tests/cockpit_manager_integration_test.cpp:5`; `TEST_MAPPING:1`
- `solid_principle.single_responsibility`：**2/4** — ManagerGatewayService 同时负责权限、路由、fallback 与广播，但 Registry/Backend 已拆出部分职责。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-10.json:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:1`
- `solid_principle.open_closed`：**2/4** — 新增 manager 可注册 Backend，然而平台 fallback 仍靠字符串和反射表修改。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-10.json:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:1`; `manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:1`
- `solid_principle.liskov_substitution`：**2/4** — VehiclePropertyBackend 遵守 Backend 调用合同；没有发现替代后收紧前置条件的证据。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-10.json:1`; `manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:1`
- `solid_principle.interface_segregation`：**2/4** — IManagerGateway 仅含调用与 listener 生命周期，粒度尚可，但 Bundle 通用入口弱化了类型隔离。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-10.json:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:1`
- `solid_principle.dependency_inversion`：**1/4** — Gateway 直接 new Registry/Fallback/VehiclePropertyBackend 并反射具体厂商类，高层未完全依赖注入抽象。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-10.json:1`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:1`; `manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:1`
- `platform_reuse.platform_upgrade`：**10/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 10。
  - 证据：`facts/FW-10.json:1`; `api/src/android/car/VehiclePropertyIds.java:2279`; `api/src/android/car/AoapService.java:58`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-10.json:1`; `refs/heads/platform/8155`@`fcd9448a5bad`; `refs/heads/platform/8295`@`75655639921a`

### FW-08 `soa-gateway` — 39/52

- `compilation.ci_independence`：**2/3** — 存在可执行 APP_BUILD 独立构建/测试入口，但没有完整标准化流水线。
  - 证据：`facts/FW-08.json:1`; `APP_BUILD:9`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-08.json:1`; `soa-service/build.gradle:11`; `soa-vms-tests/build.gradle:11`
- `compilation.api_version_management`：**3/3** — 存在 current/released API baseline 与 check_api/checkapi 或等价兼容验证，版本可控并约束向后兼容。
  - 证据：`facts/FW-08.json:1`; `native/contract/include/fw08/api/soa_api_version.h:1`; `native/CHANGELOG.md:1`
- `quality.integration_test`：**2/3** — 测试目标和断言有效，关键模块交互覆盖代理达到 50%；没有绑定 100% 执行结果，不能给 3。
  - 证据：`facts/FW-08.json:1`; `car-lib/src/android/car/test/CarLocationTestHelper.java:1`; `TEST_MAPPING:1`
- `solid_principle.single_responsibility`：**2/4** — SOA service、broker、transport、contract 已分层；完整 CarService 闭包仍包含大类。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-08.json:1`; `native/application/include/fw08/application/soa_gateway_service.h:1`; `native/broker/include/fw08/broker/soa_broker.h:1`
- `solid_principle.open_closed`：**3/4** — ProviderRegistry、SubscriptionGraph 与 IpcTransport 允许新增 provider/transport 而不改 broker 主协议。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-08.json:1`; `native/broker/include/fw08/broker/soa_broker.h:1`; `native/transport/include/fw08/transport/ipc_transport.h:1`
- `solid_principle.liskov_substitution`：**3/4** — fake/Unix transport 与 callback 实现遵守同一结果和生命周期契约，异常隔离有测试。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-08.json:1`; `native/transport/include/fw08/transport/ipc_transport.h:1`; `native/application/include/fw08/application/soa_gateway_service.h:1`
- `solid_principle.interface_segregation`：**3/4** — provider、subscription、packet 与 transport 接口按角色拆分，未形成单一万能 SOA 接口。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-08.json:1`; `native/application/include/fw08/application/soa_gateway_service.h:1`; `native/broker/include/fw08/broker/soa_broker.h:1`
- `solid_principle.dependency_inversion`：**3/4** — SoaGatewayService/Broker 依赖 IpcTransport、payload store 与 callback 抽象并通过构造装配。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-08.json:1`; `native/broker/include/fw08/broker/soa_broker.h:1`; `native/transport/include/fw08/transport/ipc_transport.h:1`
- `platform_reuse.platform_upgrade`：**10/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 10。
  - 证据：`facts/FW-08.json:1`; `car-lib/src/android/car/VehiclePropertyIds.java:2279`; `car-lib/src/android/car/AoapService.java:58`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-08.json:1`; `refs/heads/platform/8155`@`c79cded97d4f`; `refs/heads/platform/8295`@`df09b062ef96`

### FW-14 `update-manager-service` — 28/52

- `compilation.ci_independence`：**2/3** — 存在可执行 APP_BUILD 独立构建/测试入口，但没有完整标准化流水线。
  - 证据：`facts/FW-14.json:1`; `APP_BUILD:1`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-14.json:1`; `car-builtin-lib/Android.bp:22`; `car-builtin-lib/Android.bp:42`
- `compilation.api_version_management`：**3/3** — 存在 current/released API baseline 与 check_api/checkapi 或等价兼容验证，版本可控并约束向后兼容。
  - 证据：`facts/FW-14.json:1`; `car-lib/api/current.txt:1`; `car-lib/Android.bp:132`
- `quality.integration_test`：**1/3** — 存在真实断言并验证接口行为，但未证明关键跨组件覆盖代理达到 50%。
  - 证据：`facts/FW-14.json:1`; `car-lib/src/android/car/test/CarLocationTestHelper.java:1`; `TEST_MAPPING:1`
- `solid_principle.single_responsibility`：**2/4** — UpdateManagerService 同时管理权限、反射引擎、状态和 listener；系统 updater 也有 UI/执行混合。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-14.json:1`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:1`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:1`
- `solid_principle.open_closed`：**2/4** — PermissionGate 可替换，但 UpdateEngine 扩展仍需修改反射逻辑和状态分支。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-14.json:1`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:1`; `update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:1`
- `solid_principle.liskov_substitution`：**3/4** — Binder Stub 与 UpdateEngineCallback 的覆写总体符合父类契约，未发现主路径抛不支持。 按 0–4 独立档位锁定 3 分。
  - 证据：`facts/FW-14.json:1`; `update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:1`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:1`
- `solid_principle.interface_segregation`：**2/4** — 更新控制与状态回调分为两个 AIDL，但 service 对所有客户端暴露完整更新生命周期。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-14.json:1`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:1`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:1`
- `solid_principle.dependency_inversion`：**2/4** — 权限依赖使用接口注入；UpdateEngine 仍由服务内部反射构造，抽象不完整。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-14.json:1`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:1`; `update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:1`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 2, 'arch_bound_status': 0, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 3。
  - 证据：`facts/FW-14.json:1`; `car-lib/src/android/car/VehiclePropertyIds.java:2279`; `car-builtin-lib/src/android/car/builtin/os/BinderHelper.java:63`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-14.json:1`; `refs/heads/platform/8155`@`a7bea930370a`; `refs/heads/platform/8295`@`f4b18929661f`

### FW-15 `car-runtime-service` — 15/52

- `compilation.ci_independence`：**1/3** — 仅有 PREUPLOAD.cfg/TEST_MAPPING 等 Android 系统层 CI 配置。
  - 证据：`facts/FW-15.json:1`; `TEST_MAPPING:2`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-15.json:1`; `Android.bp:13`; `Android.bp:13`
- `compilation.api_version_management`：**0/3** — 没有专用版本文件、构建集成或 API baseline，锁定 0。
  - 证据：`facts/FW-15.json:1`; `Android.bp:1`
- `quality.integration_test`：**0/3** — 仅有类存在性检查和 assertTrue(true) 占位测试，按合同锁定 0。
  - 证据：`facts/FW-15.json:1`; `tests/integration/com/cockpitbench/carruntime/CarRuntimeServiceLaunchTest.java:19`; `TEST_MAPPING:1`
- `solid_principle.single_responsibility`：**0/4** — CarRuntimeService 集中 18 个业务域、权限、反射、审计和 54 个 Binder 方法，是明确上帝类。 按 0–4 独立档位锁定 0 分。
  - 证据：`facts/FW-15.json:1`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:1`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:1`
- `solid_principle.open_closed`：**1/4** — 新增车型/业务域需要复制 profile/coordinator 并修改中心服务，核心对扩展不封闭。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-15.json:1`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:1`; `platform/src/com/cockpitbench/carruntime/product/AuroraBaseRuntimeProfile.java:1`
- `solid_principle.liskov_substitution`：**2/4** — 大量 product profile 子类沿用共同基类，未见普遍收紧契约；但复制式继承可维护性一般。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-15.json:1`; `platform/src/com/cockpitbench/carruntime/product/AuroraBaseRuntimeProfile.java:1`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:1`
- `solid_principle.interface_segregation`：**0/4** — ICarRuntime 将 18 个域的读写重置共 54 个方法强制给所有客户端，严重违反接口隔离。 按 0–4 独立档位锁定 0 分。
  - 证据：`facts/FW-15.json:1`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:1`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:1`
- `solid_principle.dependency_inversion`：**0/4** — 中心服务直接构造全部 facade、保存静态 INSTANCE，并反射 ServiceManager，几乎没有依赖倒置。 按 0–4 独立档位锁定 0 分。
  - 证据：`facts/FW-15.json:1`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:1`; `platform/src/com/cockpitbench/carruntime/product/AuroraBaseRuntimeProfile.java:1`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 3, 'arch_bound_status': 2, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 3。
  - 证据：`facts/FW-15.json:1`; `api/src/android/car/VehiclePropertyIds.java:2279`; `api/src/android/car/AoapService.java:58`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`facts/FW-15.json:1`; `refs/heads/platform/8155`@`d2c21ebaf740`; `refs/heads/platform/8295`@`8ef2b0f2a5fb`

### FW-18 `vehicle-platform-service` — 19/52

- `compilation.ci_independence`：**1/3** — 仅有 PREUPLOAD.cfg/TEST_MAPPING 等 Android 系统层 CI 配置。
  - 证据：`facts/FW-18.json:1`; `PREUPLOAD.cfg:2`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-18.json:1`; `Android.bp:14`; `Android.bp:14`
- `compilation.api_version_management`：**3/3** — 存在 current/released API baseline 与 check_api/checkapi 或等价兼容验证，版本可控并约束向后兼容。
  - 证据：`facts/FW-18.json:1`; `car-lib/api/current.txt:1`; `apicheck.mk:159`
- `quality.integration_test`：**2/3** — 测试目标和断言有效，关键模块交互覆盖代理达到 50%；没有绑定 100% 执行结果，不能给 3。
  - 证据：`facts/FW-18.json:1`; `car-lib/src/android/car/test/CarTestManagerBinderWrapper.java:1`
- `solid_principle.single_responsibility`：**1/4** — PlatformSignalCoordinator 汇集连接、缓存、回调、profile、fallback 与 journal，职责明显混杂。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-18.json:1`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:1`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:1`
- `solid_principle.open_closed`：**1/4** — 新增平台依赖修改 router/profile 选择与 fallback 逻辑，扩展点有限。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-18.json:1`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:1`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:1`
- `solid_principle.liskov_substitution`：**2/4** — 三个 vehicle profile 保持相同读取映射契约，未发现替代时抛不支持的主路径。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-18.json:1`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:1`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:1`
- `solid_principle.interface_segregation`：**2/4** — IVehiclePlatform 六个方法覆盖信号与连接生命周期，尚未达到胖接口，但客户端仍耦合 reset/reconnect。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-18.json:1`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:1`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:1`
- `solid_principle.dependency_inversion`：**1/4** — Service 依赖全局 Coordinator.get()，Coordinator 又依赖具体 LegacyPlatformRouter，抽象和注入不足。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-18.json:1`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:1`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:1`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 3, 'arch_bound_status': 2, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 3。
  - 证据：`facts/FW-18.json:1`; `car-lib/src/android/car/hardware/CarPropertyConfig.java:205`; `car-lib/Android.mk:42`
- `platform_reuse.release_branch_strategy`：**3/10** — 真实 refs 同时存在平台分支和车型/SOP release 分支，车型拆分更细，锁定 3。
  - 证据：`facts/FW-18.json:1`; `refs/heads/platform/8155`@`1cd1c6a43839`; `refs/heads/platform/8295`@`bce6dc6fca9e`

### FW-16 `platform-compat-service` — 18/52

- `compilation.ci_independence`：**1/3** — 仅有 PREUPLOAD.cfg/TEST_MAPPING 等 Android 系统层 CI 配置。
  - 证据：`facts/FW-16.json:1`; `TEST_MAPPING:2`
- `compilation.compilation_independence`：**0/3** — 构建图直接编译同仓 Soong/Gradle 源码模块；源码依赖优先锁定 0，不能被 compileSdk/sdk_version 表象抬分。
  - 证据：`facts/FW-16.json:1`; `Android.bp:5`; `Android.bp:5`
- `compilation.api_version_management`：**3/3** — 存在 current/released API baseline 与 check_api/checkapi 或等价兼容验证，版本可控并约束向后兼容。
  - 证据：`facts/FW-16.json:1`; `car-lib/api/current.txt:1`; `car-lib/Android.bp:132`
- `quality.integration_test`：**2/3** — 测试目标和断言有效，关键模块交互覆盖代理达到 50%；没有绑定 100% 执行结果，不能给 3。
  - 证据：`facts/FW-16.json:1`; `car-lib/src/android/car/test/CarLocationTestHelper.java:1`; `TEST_MAPPING:1`
- `solid_principle.single_responsibility`：**1/4** — PlatformCompatRuntime/Service 与多个全局 registry/cache/polling 对象混合平台兼容职责，且复制整套 legacy car-lib。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-16.json:1`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:1`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:1`
- `solid_principle.open_closed`：**1/4** — 平台规则、hidden API 和 vendor bridge 通过集中分支扩展，新增平台需要修改多个核心类。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-16.json:1`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:1`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:1`
- `solid_principle.liskov_substitution`：**2/4** — Binder Stub 与 callback 基本维持声明契约，但兼容副本和 fallback 路径缺少替换性验证。 按 0–4 独立档位锁定 2 分。
  - 证据：`facts/FW-16.json:1`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:1`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:1`
- `solid_principle.interface_segregation`：**1/4** — IPlatformCompat 聚合兼容命令、状态、callback 等多类客户端能力，接口隔离较弱。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-16.json:1`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:1`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:1`
- `solid_principle.dependency_inversion`：**1/4** — 运行时依赖静态 registry、具体 fallback/cache/polling 与反射 vendor 实现，高层未依赖可注入抽象。 按 0–4 独立档位锁定 1 分。
  - 证据：`facts/FW-16.json:1`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:1`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:1`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实为 {'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 3, 'arch_bound_status': 2, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；严格按 10→8→3→0 首个满足档锁定 3。
  - 证据：`facts/FW-16.json:1`; `car-lib/src/android/car/VehiclePropertyIds.java:2279`; `car-builtin-lib/src/android/car/builtin/os/BinderHelper.java:63`
- `platform_reuse.release_branch_strategy`：**3/10** — 真实 refs 同时存在平台分支和车型/SOP release 分支，车型拆分更细，锁定 3。
  - 证据：`facts/FW-16.json:1`; `refs/heads/platform/8155`@`93ccc6f80839`; `refs/heads/platform/8295`@`068b6972dc4b`
