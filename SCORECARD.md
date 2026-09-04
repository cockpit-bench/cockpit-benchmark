# Validation-18 标准评分总表

- APP：9 仓 / 72 叶 / 223/360
- Android Framework：9 仓 / 99 叶 / 263/468
- 合计：18 仓 / 171 叶 / 486/828

> 分数只由绑定 HEAD 的代码与 refs 证据推导；质量/规模标签是矩阵角色，不是打分输入。
> APP 的三个 architecture 叶属于同一 Architecture Macro，但按组件复用、依赖传播、构建模块边界分别评分，不把命中数当作统计独立样本。

## APP 9 仓

| ID | 仓库 | 角色 | 规模 | architecture.componentization | architecture.decoupling | architecture.modularization | compilation.ci_independence | compilation.compilation_independence | compilation.api_version_management | platform_reuse.platform_upgrade | platform_reuse.release_branch_strategy | 总分 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| APP-03 | climatix-hvac | high | small | 5 | 2 | 3 | 3 | 1 | 2 | 8 | 8 | 32/40 |
| APP-02 | horizon-launcher | high | medium | 5 | 2 | 3 | 2 | 1 | 2 | 8 | 8 | 31/40 |
| APP-01 | aurora-settings | high | large | 5 | 3 | 3 | 1 | 0 | 3 | 8 | 8 | 31/40 |
| APP-13 | market-hub | medium | small | 5 | 3 | 3 | 1 | 2 | 1 | 8 | 8 | 31/40 |
| APP-11 | motion-control | medium | medium | 5 | 3 | 3 | 1 | 2 | 1 | 3 | 3 | 21/40 |
| APP-14 | cockpit-shell | medium | large | 5 | 2 | 2 | 1 | 0 | 2 | 3 | 8 | 23/40 |
| APP-17 | thermo-control | low | small | 3 | 2 | 2 | 0 | 0 | 1 | 3 | 8 | 19/40 |
| APP-16 | nova-launcher | low | medium | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 8 | 20/40 |
| APP-15 | atlas-settings | low | large | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 3 | 15/40 |

## Android Framework 9 仓

| ID | 仓库 | 角色 | 规模 | compilation.ci_independence | compilation.compilation_independence | compilation.api_version_management | quality.integration_test | solid_principle.single_responsibility | solid_principle.open_closed | solid_principle.liskov_substitution | solid_principle.interface_segregation | solid_principle.dependency_inversion | platform_reuse.platform_upgrade | platform_reuse.release_branch_strategy | 总分 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FW-02 | vehicle-property-service | high | small | 3 | 1 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 8 | 8 | 40/52 |
| FW-03 | vehicle-hal-adapter | high | medium | 3 | 1 | 3 | 3 | 3 | 4 | 3 | 3 | 4 | 8 | 8 | 43/52 |
| FW-07 | vehicle-diagnostics | high | large | 3 | 1 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 10 | 8 | 42/52 |
| FW-10 | cockpit-manager-kit | medium | small | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 8 | 8 | 31/52 |
| FW-08 | soa-gateway | medium | medium | 2 | 1 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 10 | 8 | 39/52 |
| FW-14 | update-manager-service | medium | large | 2 | 1 | 3 | 1 | 2 | 2 | 3 | 2 | 2 | 3 | 8 | 29/52 |
| FW-15 | car-runtime-service | low | small | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 8 | 12/52 |
| FW-18 | vehicle-platform-service | low | medium | 1 | 0 | 1 | 2 | 1 | 1 | 2 | 2 | 1 | 0 | 3 | 14/52 |
| FW-16 | platform-compat-service | low | large | 1 | 0 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 0 | 3 | 13/52 |

## 逐叶理由与证据

### APP-03 `climatix-hvac` — 32/40

- `architecture.componentization`：**5/5** — 共享事实 module_count=7、standard=3、boundary=False、common=True、cycle=False；按 componentization 独立构念锁定 5。
  - 证据：`facts/APP-03.json#/facts/architecture/facts`; `settings.gradle.kts:4`; `app/build.gradle.kts:3`
- `architecture.decoupling`：**2/3** — 共享事实 module_count=7、standard=3、boundary=False、common=True、cycle=False；按 decoupling 独立构念锁定 2。
  - 证据：`facts/APP-03.json#/facts/architecture/facts`; `settings.gradle.kts:4`; `app/build.gradle.kts:3`
- `architecture.modularization`：**3/3** — 共享事实 module_count=7、standard=3、boundary=False、common=True、cycle=False；按 modularization 独立构念锁定 3。
  - 证据：`facts/APP-03.json#/facts/architecture/facts`; `settings.gradle.kts:4`; `app/build.gradle.kts:3`
- `compilation.ci_independence`：**3/3** — CI 分类=independent_ci，锁定 3。
  - 证据：`facts/APP-03.json#/facts/ci`; `.github/workflows/android.yml:15`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 1。
  - 证据：`facts/APP-03.json#/facts/compilation/dependency_type_candidates`; `README.md:4`; `.github/workflows/android.yml:15`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-03.json#/facts/api_version`; `version.properties:1`; `version.properties:2`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-03.json#/facts/platform_upgrade/seven_fact_candidates`; `vehicle-api/src/main/java/com/cockpitbench/climatix/vehicle/ClimateServiceLocator.kt:29`; `domain/src/main/java/com/cockpitbench/climatix/domain/ObserveClimate.kt:20`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`b313db00f552`; `refs/heads/platform/8295`@`f6df3cc885c4`

### APP-02 `horizon-launcher` — 31/40

- `architecture.componentization`：**5/5** — 共享事实 module_count=3、standard=2、boundary=False、common=True、cycle=False；按 componentization 独立构念锁定 5。
  - 证据：`facts/APP-02.json#/facts/architecture/facts`; `settings.gradle:4`; `launcher-app/build.gradle:1`
- `architecture.decoupling`：**2/3** — 共享事实 module_count=3、standard=2、boundary=False、common=True、cycle=False；按 decoupling 独立构念锁定 2。
  - 证据：`facts/APP-02.json#/facts/architecture/facts`; `settings.gradle:4`; `launcher-app/build.gradle:1`
- `architecture.modularization`：**3/3** — 共享事实 module_count=3、standard=2、boundary=False、common=True、cycle=False；按 modularization 独立构念锁定 3。
  - 证据：`facts/APP-02.json#/facts/architecture/facts`; `settings.gradle:4`; `launcher-app/build.gradle:1`
- `compilation.ci_independence`：**2/3** — CI 分类=mixed，锁定 2。
  - 证据：`facts/APP-02.json#/facts/ci`; `.github/workflows/android.yml:1`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 1。
  - 证据：`facts/APP-02.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `.github/workflows/android.yml:1`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-02.json#/facts/api_version`; `version.properties:1`; `version.properties:2`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': False, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-02.json#/facts/platform_upgrade/seven_fact_candidates`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`29ce9d750e0b`; `refs/heads/platform/8295`@`30709ae25c06`

### APP-01 `aurora-settings` — 31/40

- `architecture.componentization`：**5/5** — 共享事实 module_count=4、standard=2、boundary=True、common=True、cycle=False；按 componentization 独立构念锁定 5。
  - 证据：`facts/APP-01.json#/facts/architecture/facts`; `settings.gradle:4`; `app/build.gradle:16`
- `architecture.decoupling`：**3/3** — 共享事实 module_count=4、standard=2、boundary=True、common=True、cycle=False；按 decoupling 独立构念锁定 3。
  - 证据：`facts/APP-01.json#/facts/architecture/facts`; `settings.gradle:4`; `app/build.gradle:16`
- `architecture.modularization`：**3/3** — 共享事实 module_count=4、standard=2、boundary=True、common=True、cycle=False；按 modularization 独立构念锁定 3。
  - 证据：`facts/APP-01.json#/facts/architecture/facts`; `settings.gradle:4`; `app/build.gradle:16`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-01.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-01.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `app/build.gradle:16`
- `compilation.api_version_management`：**3/3** — 语义版本=True、有效兼容检查=1、自动绑定=3；已排除 Java/SDK 级别和固定字符串检查，锁定 3。
  - 证据：`facts/APP-01.json#/facts/api_version`; `version.properties:1`; `version.properties:2`; `app/build.gradle:31`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': True, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-01.json#/facts/platform_upgrade/seven_fact_candidates`; `app/src/main/java/com/android/car/settings/accessibility/ScreenReaderUtils.java:29`; `app/src/main/java/com/android/car/settings/applications/ApplicationsUtils.java:31`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`769d29b8ea64`; `refs/heads/platform/8295`@`33e548d7b2fd`

### APP-13 `market-hub` — 31/40

- `architecture.componentization`：**5/5** — 共享事实 module_count=9、standard=3、boundary=True、common=True、cycle=False；按 componentization 独立构念锁定 5。
  - 证据：`facts/APP-13.json#/facts/architecture/facts`; `settings.gradle:2`; `foundation-api/build.gradle:1`
- `architecture.decoupling`：**3/3** — 共享事实 module_count=9、standard=3、boundary=True、common=True、cycle=False；按 decoupling 独立构念锁定 3。
  - 证据：`facts/APP-13.json#/facts/architecture/facts`; `settings.gradle:2`; `foundation-api/build.gradle:1`
- `architecture.modularization`：**3/3** — 共享事实 module_count=9、standard=3、boundary=True、common=True、cycle=False；按 modularization 独立构念锁定 3。
  - 证据：`facts/APP-13.json#/facts/architecture/facts`; `settings.gradle:2`; `foundation-api/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-13.json#/facts/ci`; `TEST_MAPPING:1`
- `compilation.compilation_independence`：**2/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': False}；同仓模块依赖不扣分，锁定 2。
  - 证据：`facts/APP-13.json#/facts/compilation/dependency_type_candidates`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-13.json#/facts/api_version`; `market-app/build.gradle:3`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': False, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-13.json#/facts/platform_upgrade/seven_fact_candidates`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`f8623eec7728`; `refs/heads/platform/8295`@`fad482ad315d`

### APP-11 `motion-control` — 21/40

- `architecture.componentization`：**5/5** — 共享事实 module_count=9、standard=3、boundary=True、common=True、cycle=False；按 componentization 独立构念锁定 5。
  - 证据：`facts/APP-11.json#/facts/architecture/facts`; `settings.gradle:2`; `foundation-api/build.gradle:1`
- `architecture.decoupling`：**3/3** — 共享事实 module_count=9、standard=3、boundary=True、common=True、cycle=False；按 decoupling 独立构念锁定 3。
  - 证据：`facts/APP-11.json#/facts/architecture/facts`; `settings.gradle:2`; `foundation-api/build.gradle:1`
- `architecture.modularization`：**3/3** — 共享事实 module_count=9、standard=3、boundary=True、common=True、cycle=False；按 modularization 独立构念锁定 3。
  - 证据：`facts/APP-11.json#/facts/architecture/facts`; `settings.gradle:2`; `foundation-api/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-11.json#/facts/ci`; `TEST_MAPPING:1`
- `compilation.compilation_independence`：**2/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': False}；同仓模块依赖不扣分，锁定 2。
  - 证据：`facts/APP-11.json#/facts/compilation/dependency_type_candidates`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-11.json#/facts/api_version`; `motion-app/build.gradle:3`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 0}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-11.json#/facts/platform_upgrade/seven_fact_candidates`; `motion-platform/src/main/java/com/cockpitbench/motion/platform/PlatformMotionAdapter.java:16`
- `platform_reuse.release_branch_strategy`：**3/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`f037ffc21b67`; `refs/heads/platform/8295`@`7dfbf90dc738`

### APP-14 `cockpit-shell` — 23/40

- `architecture.componentization`：**5/5** — 共享事实 module_count=2、standard=2、boundary=False、common=True、cycle=False；按 componentization 独立构念锁定 5。
  - 证据：`facts/APP-14.json#/facts/architecture/facts`; `settings.gradle:4`; `shell-app/build.gradle:1`
- `architecture.decoupling`：**2/3** — 共享事实 module_count=2、standard=2、boundary=False、common=True、cycle=False；按 decoupling 独立构念锁定 2。
  - 证据：`facts/APP-14.json#/facts/architecture/facts`; `settings.gradle:4`; `shell-app/build.gradle:1`
- `architecture.modularization`：**2/3** — 共享事实 module_count=2、standard=2、boundary=False、common=True、cycle=False；按 modularization 独立构念锁定 2。
  - 证据：`facts/APP-14.json#/facts/architecture/facts`; `settings.gradle:4`; `shell-app/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-14.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-14.json#/facts/compilation/dependency_type_candidates`; `README.md:4`; `build.gradle:1`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-14.json#/facts/api_version`; `version.properties:1`; `version.properties:2`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'version_bound_status': 1}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-14.json#/facts/platform_upgrade/seven_fact_candidates`; `shell-app/src/main/java/com/android/systemui/cockpit/presentation/CockpitShellController.java:12`; `shell-app/src/main/java/com/android/systemui/cockpit/presentation/CockpitShellController.java:11`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`e78cfb993351`; `refs/heads/platform/8295`@`d4afa6cac8e9`

### APP-17 `thermo-control` — 19/40

- `architecture.componentization`：**3/5** — 共享事实 module_count=2、standard=1、boundary=False、common=False、cycle=False；按 componentization 独立构念锁定 3。
  - 证据：`facts/APP-17.json#/facts/architecture/facts`; `settings.gradle.kts:4`; `app/build.gradle.kts:1`
- `architecture.decoupling`：**2/3** — 共享事实 module_count=2、standard=1、boundary=False、common=False、cycle=False；按 decoupling 独立构念锁定 2。
  - 证据：`facts/APP-17.json#/facts/architecture/facts`; `settings.gradle.kts:4`; `app/build.gradle.kts:1`
- `architecture.modularization`：**2/3** — 共享事实 module_count=2、standard=1、boundary=False、common=False、cycle=False；按 modularization 独立构念锁定 2。
  - 证据：`facts/APP-17.json#/facts/architecture/facts`; `settings.gradle.kts:4`; `app/build.gradle.kts:1`
- `compilation.ci_independence`：**0/3** — CI 分类=no_ci，锁定 0。
  - 证据：`facts/APP-17.json#/facts/ci`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-17.json#/facts/compilation/dependency_type_candidates`; `README.md:6`; `app/build.gradle.kts:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-17.json#/facts/api_version`; `app/build.gradle.kts:10`; `app/build.gradle.kts:9`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 1}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-17.json#/facts/platform_upgrade/seven_fact_candidates`; `app/src/main/java/com/cockpitbench/thermo/ThermalPlatformRuntime.java:9`; `vehicle/src/main/java/com/cockpitbench/thermo/vehicle/platform/Sa8155ClimateBridge.kt:29`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`483e416e1a9e`; `refs/heads/platform/8295`@`dc027394cbc9`

### APP-16 `nova-launcher` — 20/40

- `architecture.componentization`：**3/5** — 共享事实 module_count=4、standard=1、boundary=False、common=False、cycle=False；按 componentization 独立构念锁定 3。
  - 证据：`facts/APP-16.json#/facts/architecture/facts`; `settings.gradle:4`; `launcher-app/build.gradle:1`
- `architecture.decoupling`：**2/3** — 共享事实 module_count=4、standard=1、boundary=False、common=False、cycle=False；按 decoupling 独立构念锁定 2。
  - 证据：`facts/APP-16.json#/facts/architecture/facts`; `settings.gradle:4`; `launcher-app/build.gradle:1`
- `architecture.modularization`：**2/3** — 共享事实 module_count=4、standard=1、boundary=False、common=False、cycle=False；按 modularization 独立构念锁定 2。
  - 证据：`facts/APP-16.json#/facts/architecture/facts`; `settings.gradle:4`; `launcher-app/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-16.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-16.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-16.json#/facts/api_version`; `launcher-app/build.gradle:5`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'version_bound_status': 3}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-16.json#/facts/platform_upgrade/seven_fact_candidates`; `launcher-app/src/main/java/com/android/car/launcher/LauncherRuntime.java:13`; `legacy-platform/src/main/java/com/android/car/launcher/legacy/LegacyPlatformRuntime.java:9`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`12018f5c8629`; `refs/heads/platform/8295`@`8d942866a727`

### APP-15 `atlas-settings` — 15/40

- `architecture.componentization`：**3/5** — 共享事实 module_count=3、standard=1、boundary=False、common=False、cycle=False；按 componentization 独立构念锁定 3。
  - 证据：`facts/APP-15.json#/facts/architecture/facts`; `settings.gradle:4`; `app/build.gradle:1`
- `architecture.decoupling`：**2/3** — 共享事实 module_count=3、standard=1、boundary=False、common=False、cycle=False；按 decoupling 独立构念锁定 2。
  - 证据：`facts/APP-15.json#/facts/architecture/facts`; `settings.gradle:4`; `app/build.gradle:1`
- `architecture.modularization`：**2/3** — 共享事实 module_count=3、standard=1、boundary=False、common=False、cycle=False；按 modularization 独立构念锁定 2。
  - 证据：`facts/APP-15.json#/facts/architecture/facts`; `settings.gradle:4`; `app/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-15.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-15.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `app/build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-15.json#/facts/api_version`; `app/src/main/AndroidManifest.xml:1`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': True, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'version_bound_status': 0}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-15.json#/facts/platform_upgrade/seven_fact_candidates`; `app/src/main/java/com/android/car/settings/accounts/SyncPreference.java:51`; `app/src/main/java/com/android/car/settings/applications/ApplicationsUtils.java:28`
- `platform_reuse.release_branch_strategy`：**3/10** — 真实 refs 同时存在 main 与平台分支、无车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`2b04c1935fa5`; `refs/heads/platform/8295`@`035d15b75c11`

### FW-02 `vehicle-property-service` — 40/52

- `compilation.ci_independence`：**3/3** — 独立 GitHub Actions 包含真实构建、测试、覆盖率门禁和报告上传，且 final HEAD 运行成功。
  - 证据：`facts/FW-02.json#/ci`; `.github/workflows/native.yml:1`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': False, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'requires an AOSP'}], 'standalone_target_anchors': [{'path': '.github/workflows/native.yml', 'line': 2, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 5, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 12, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_executable('}, {'path': 'native/common/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/contract/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/hal/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/platform/CMakeLists.txt', 'line': 1, 'match': 'add_library('}]}；锁定 1。
  - 证据：`facts/FW-02.json#/compilation/external_build_closure`; `README.md:4`; `.github/workflows/native.yml:1`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=2、有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-02.json#/api_version`; `native/CMakeLists.txt:2`; `native/VERSION:1`
- `quality.integration_test`：**3/3** — 真实断言覆盖关键模块交互，覆盖代理达到 50%，且 final HEAD 独立流水线测试 100% 通过。
  - 证据：`facts/FW-02.json#/integration_test`; `native/tests/vehicle_property_integration_test.cpp:6`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**3/4** — 策略、平台访问、HAL 与 Binder 职责有边界；仍保留较大的命令处理类。 按独立 0–4 档位锁定 3。
  - 证据：`platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:22`; `runtime/src/com/android/car/VehicleStub.java:39`
- `solid_principle.open_closed`：**3/4** — VehicleStub 与策略对象提供扩展点。 按独立 0–4 档位锁定 3。
  - 证据：`runtime/src/com/android/car/VehicleStub.java:39`; `api/src/android/car/hardware/property/ICarProperty.aidl:26`
- `solid_principle.liskov_substitution`：**3/4** — AIDL/HIDL VehicleStub 实现遵守共同读写和订阅契约。 按独立 0–4 档位锁定 3。
  - 证据：`api/src/android/car/hardware/property/ICarProperty.aidl:26`; `platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:22`
- `solid_principle.interface_segregation`：**3/4** — 属性、回调和策略接口按客户端职责拆分。 按独立 0–4 档位锁定 3。
  - 证据：`platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:22`; `runtime/src/com/android/car/VehicleStub.java:39`
- `solid_principle.dependency_inversion`：**3/4** — 服务主要依赖 VehicleStub/HalClient 抽象，平台反射被收敛在边界内。 按独立 0–4 档位锁定 3。
  - 证据：`runtime/src/com/android/car/VehicleStub.java:39`; `api/src/android/car/hardware/property/ICarProperty.aidl:26`
- `platform_reuse.platform_upgrade`：**8/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 8。
  - 证据：`facts/FW-02.json#/platform_upgrade_review`; `platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:22`; `runtime/src/com/android/car/VehicleStub.java:39`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`fab2b54427e9`; `refs/heads/platform/8295`@`1c687eb3c852`

### FW-03 `vehicle-hal-adapter` — 43/52

- `compilation.ci_independence`：**3/3** — 独立 GitHub Actions 包含真实构建、测试、覆盖率门禁和报告上传，且 final HEAD 运行成功。
  - 证据：`facts/FW-03.json#/ci`; `.github/workflows/native-ci.yml:17`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [], 'standalone_target_anchors': [{'path': '.github/workflows/native-ci.yml', 'line': 17, 'match': 'build'}, {'path': '.github/workflows/native-ci.yml', 'line': 31, 'match': 'build'}, {'path': '.github/workflows/native-ci.yml', 'line': 32, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 3, 'match': 'project('}, {'path': 'native/CMakeLists.txt', 'line': 25, 'match': 'cmake'}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/application/CMakeLists.txt', 'line': 15, 'match': 'add_executable('}, {'path': 'native/common/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/contract/CMakeLists.txt', 'line': 24, 'match': 'build'}, {'path': 'native/contract/CMakeLists.txt', 'line': 25, 'match': 'CMake'}]}；锁定 1。
  - 证据：`facts/FW-03.json#/compilation/external_build_closure`; `.github/workflows/native-ci.yml:17`
- `compilation.api_version_management`：**3/3** — 专用语义版本证据=2、有效 API 检查=3；锁定 3。
  - 证据：`facts/FW-03.json#/api_version`; `native/CMakeLists.txt:5`; `native/VERSION:1`; `native/contract/include/fw03/api/vehicle_hal_api_version.h:11`
- `quality.integration_test`：**3/3** — 真实断言覆盖关键模块交互，覆盖代理达到 50%，且 final HEAD 独立流水线测试 100% 通过。
  - 证据：`facts/FW-03.json#/integration_test`; `native/tests/client_ipc_vertical_integration_test.cpp:170`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**3/4** — Vehicle HAL、传输、契约与生命周期分层清楚，但仍有若干大类。 按独立 0–4 档位锁定 3。
  - 证据：`service/src/com/android/car/VehicleStub.java:38`; `service/src/com/android/car/AidlVehicleStub.java:64`
- `solid_principle.open_closed`：**4/4** — AIDL/HIDL 适配及 native transport 可替换。 按独立 0–4 档位锁定 4。
  - 证据：`service/src/com/android/car/AidlVehicleStub.java:64`; `native/application/include/fw03/application/vehicle_service.h:18`
- `solid_principle.liskov_substitution`：**3/4** — AidlVehicleStub/HidlVehicleStub 保持 VehicleStub 合同。 按独立 0–4 档位锁定 3。
  - 证据：`native/application/include/fw03/application/vehicle_service.h:18`; `service/src/com/android/car/VehicleStub.java:38`
- `solid_principle.interface_segregation`：**3/4** — VehicleStub 子接口和细分 AIDL 隔离客户端职责。 按独立 0–4 档位锁定 3。
  - 证据：`service/src/com/android/car/VehicleStub.java:38`; `service/src/com/android/car/AidlVehicleStub.java:64`
- `solid_principle.dependency_inversion`：**4/4** — 高层 gateway 依赖 port/transport/clock 抽象。 按独立 0–4 档位锁定 4。
  - 证据：`service/src/com/android/car/AidlVehicleStub.java:64`; `native/application/include/fw03/application/vehicle_service.h:18`
- `platform_reuse.platform_upgrade`：**8/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 1, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 8。
  - 证据：`facts/FW-03.json#/platform_upgrade_review`; `service/src/com/android/car/VehicleStub.java:38`; `service/src/com/android/car/AidlVehicleStub.java:64`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`270b396861b0`; `refs/heads/platform/8295`@`4449839764f7`

### FW-07 `vehicle-diagnostics` — 42/52

- `compilation.ci_independence`：**3/3** — 独立 GitHub Actions 包含真实构建、测试、覆盖率门禁和报告上传，且 final HEAD 运行成功。
  - 证据：`facts/FW-07.json#/ci`; `.github/workflows/native.yml:1`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 5, 'match': 'complete build requires an AAOS'}], 'standalone_target_anchors': [{'path': '.github/workflows/native.yml', 'line': 2, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 5, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 12, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_executable('}, {'path': 'native/common/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/contract/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/hal/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/platform/CMakeLists.txt', 'line': 1, 'match': 'add_library('}]}；锁定 1。
  - 证据：`facts/FW-07.json#/compilation/external_build_closure`; `README.md:5`; `.github/workflows/native.yml:1`
- `compilation.api_version_management`：**3/3** — 专用语义版本证据=2、有效 API 检查=3；锁定 3。
  - 证据：`facts/FW-07.json#/api_version`; `native/CMakeLists.txt:2`; `native/VERSION:1`; `car-lib/Android.bp:105`
- `quality.integration_test`：**3/3** — 真实断言覆盖关键模块交互，覆盖代理达到 50%，且 final HEAD 独立流水线测试 100% 通过。
  - 证据：`facts/FW-07.json#/integration_test`; `car-lib/src/android/car/test/CarLocationTestHelper.java:29`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — 诊断、遥测、watchdog 边界明确，但 WatchdogPerfHandler 体量过大。 按独立 0–4 档位锁定 2。
  - 证据：`service/src/com/android/car/watchdog/WatchdogPerfHandler.java:164`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:23`
- `solid_principle.open_closed`：**3/4** — listener、watchdog AIDL 与 HAL service 提供扩展点。 按独立 0–4 档位锁定 3。
  - 证据：`car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:23`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:46`
- `solid_principle.liskov_substitution`：**3/4** — Manager/Service 与 Binder callback 保持父契约。 按独立 0–4 档位锁定 3。
  - 证据：`cpp/telemetry/cartelemetryd/src/TelemetryServer.h:46`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:164`
- `solid_principle.interface_segregation`：**3/4** — 诊断、遥测、资源过载接口按领域拆分。 按独立 0–4 档位锁定 3。
  - 证据：`service/src/com/android/car/watchdog/WatchdogPerfHandler.java:164`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:23`
- `solid_principle.dependency_inversion`：**3/4** — 服务通过 AIDL、HalServiceBase 与 listener 抽象协作。 按独立 0–4 档位锁定 3。
  - 证据：`car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:23`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:46`
- `platform_reuse.platform_upgrade`：**10/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': False, 'has_arch_specific_deps': False, 'version_bound_status': 0, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 10。
  - 证据：`facts/FW-07.json#/platform_upgrade_review`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:164`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:23`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`85f0ccfb542a`; `refs/heads/platform/8295`@`87130476985f`

### FW-10 `cockpit-manager-kit` — 31/52

- `compilation.ci_independence`：**2/3** — 存在可执行 APP_BUILD 独立构建/测试入口，但没有完整标准化流水线。
  - 证据：`facts/FW-10.json#/ci`; `APP_BUILD:1`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'requires an AOSP'}], 'standalone_target_anchors': [{'path': 'APP_BUILD', 'line': 1, 'match': 'cmake'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'build'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/service/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/tests/CMakeLists.txt', 'line': 6, 'match': 'add_executable('}]}；锁定 1。
  - 证据：`facts/FW-10.json#/compilation/external_build_closure`; `README.md:4`; `APP_BUILD:1`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=1、有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-10.json#/api_version`; `native/CMakeLists.txt:2`
- `quality.integration_test`：**1/3** — 存在真实断言并验证接口行为，但未证明关键跨组件覆盖代理达到 50%。
  - 证据：`facts/FW-10.json#/integration_test`; `native/tests/cockpit_manager_integration_test.cpp:4`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — ManagerGatewayService 混合权限、路由、fallback 与广播职责。 按独立 0–4 档位锁定 2。
  - 证据：`manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:20`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`
- `solid_principle.open_closed`：**2/4** — Backend 可注册，但平台 fallback 仍依赖字符串和反射表。 按独立 0–4 档位锁定 2。
  - 证据：`manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`; `manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:20`
- `solid_principle.liskov_substitution`：**2/4** — VehiclePropertyBackend 遵守 Backend 调用合同。 按独立 0–4 档位锁定 2。
  - 证据：`manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:20`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:20`
- `solid_principle.interface_segregation`：**2/4** — IManagerGateway 粒度尚可，但 Bundle 通用入口弱化类型隔离。 按独立 0–4 档位锁定 2。
  - 证据：`manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:20`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`
- `solid_principle.dependency_inversion`：**1/4** — Gateway 直接构造 Registry/Fallback/Backend，高层注入不完整。 按独立 0–4 档位锁定 1。
  - 证据：`manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`; `manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:20`
- `platform_reuse.platform_upgrade`：**8/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 1, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 8。
  - 证据：`facts/FW-10.json#/platform_upgrade_review`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:20`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`fcd9448a5bad`; `refs/heads/platform/8295`@`75655639921a`

### FW-08 `soa-gateway` — 39/52

- `compilation.ci_independence`：**2/3** — 存在可执行 APP_BUILD 独立构建/测试入口，但没有完整标准化流水线。
  - 证据：`facts/FW-08.json#/ci`; `APP_BUILD:7`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'complete build still requires AOSP'}], 'standalone_target_anchors': [{'path': 'APP_BUILD', 'line': 7, 'match': 'build'}, {'path': 'APP_BUILD', 'line': 9, 'match': 'cmake'}, {'path': 'APP_BUILD', 'line': 15, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 3, 'match': 'project('}, {'path': 'native/CMakeLists.txt', 'line': 28, 'match': 'cmake'}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/application/CMakeLists.txt', 'line': 7, 'match': 'add_library('}, {'path': 'native/application/CMakeLists.txt', 'line': 13, 'match': 'add_executable('}, {'path': 'native/broker/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/broker/CMakeLists.txt', 'line': 7, 'match': 'add_library('}]}；锁定 1。
  - 证据：`facts/FW-08.json#/compilation/external_build_closure`; `README.md:4`; `APP_BUILD:7`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=3、有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-08.json#/api_version`; `native/CMakeLists.txt:5`; `native/CMakeLists.txt:23`; `native/VERSION:1`
- `quality.integration_test`：**2/3** — 测试目标和断言有效，关键模块交互覆盖代理达到 50%；没有绑定 100% 执行结果，不能给 3。
  - 证据：`facts/FW-08.json#/integration_test`; `car-lib/src/android/car/test/CarLocationTestHelper.java:29`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — SOA service、broker、transport、contract 已分层，但完整闭包仍含大类。 按独立 0–4 档位锁定 2。
  - 证据：`native/application/include/fw08/application/soa_gateway_service.h:22`; `native/broker/include/fw08/broker/soa_broker.h:20`
- `solid_principle.open_closed`：**3/4** — ProviderRegistry、SubscriptionGraph 与 IpcTransport 支持扩展。 按独立 0–4 档位锁定 3。
  - 证据：`native/broker/include/fw08/broker/soa_broker.h:20`; `native/transport/include/fw08/transport/ipc_transport.h:17`
- `solid_principle.liskov_substitution`：**3/4** — fake/Unix transport 与 callback 保持同一生命周期契约。 按独立 0–4 档位锁定 3。
  - 证据：`native/transport/include/fw08/transport/ipc_transport.h:17`; `native/application/include/fw08/application/soa_gateway_service.h:22`
- `solid_principle.interface_segregation`：**3/4** — provider、subscription、packet 与 transport 接口按角色拆分。 按独立 0–4 档位锁定 3。
  - 证据：`native/application/include/fw08/application/soa_gateway_service.h:22`; `native/broker/include/fw08/broker/soa_broker.h:20`
- `solid_principle.dependency_inversion`：**3/4** — Service/Broker 依赖 transport 与 store 抽象并通过构造装配。 按独立 0–4 档位锁定 3。
  - 证据：`native/broker/include/fw08/broker/soa_broker.h:20`; `native/transport/include/fw08/transport/ipc_transport.h:17`
- `platform_reuse.platform_upgrade`：**10/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': False, 'has_arch_specific_deps': False, 'version_bound_status': 0, 'arch_bound_status': 0, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 10。
  - 证据：`facts/FW-08.json#/platform_upgrade_review`; `native/application/include/fw08/application/soa_gateway_service.h:22`; `native/broker/include/fw08/broker/soa_broker.h:20`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`c79cded97d4f`; `refs/heads/platform/8295`@`df09b062ef96`

### FW-14 `update-manager-service` — 29/52

- `compilation.ci_independence`：**2/3** — 存在可执行 APP_BUILD 独立构建/测试入口，但没有完整标准化流水线。
  - 证据：`facts/FW-14.json#/ci`; `APP_BUILD:1`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 3, 'match': 'Complete build requires an AOSP'}], 'standalone_target_anchors': [{'path': 'APP_BUILD', 'line': 1, 'match': 'cmake'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'build'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/service/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/tests/CMakeLists.txt', 'line': 6, 'match': 'add_executable('}]}；锁定 1。
  - 证据：`facts/FW-14.json#/compilation/external_build_closure`; `README.md:3`; `APP_BUILD:1`
- `compilation.api_version_management`：**3/3** — 专用语义版本证据=1、有效 API 检查=4；锁定 3。
  - 证据：`facts/FW-14.json#/api_version`; `native/CMakeLists.txt:2`; `car-builtin-lib/Android.bp:32`; `car-lib/Android.bp:105`
- `quality.integration_test`：**1/3** — 存在真实断言并验证接口行为，但未证明关键跨组件覆盖代理达到 50%。
  - 证据：`facts/FW-14.json#/integration_test`; `car-lib/src/android/car/test/CarLocationTestHelper.java:29`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — UpdateManagerService 混合权限、反射引擎、状态和 listener。 按独立 0–4 档位锁定 2。
  - 证据：`update-manager/src/com/cockpitbench/update/UpdateManagerService.java:9`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:3`
- `solid_principle.open_closed`：**2/4** — PermissionGate 可替换，但 UpdateEngine 扩展仍修改核心反射逻辑。 按独立 0–4 档位锁定 2。
  - 证据：`update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:3`; `update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:2`
- `solid_principle.liskov_substitution`：**3/4** — Binder Stub 与 callback 覆写基本保持父契约。 按独立 0–4 档位锁定 3。
  - 证据：`update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:2`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:9`
- `solid_principle.interface_segregation`：**2/4** — 控制与状态回调虽拆分，service 仍暴露完整生命周期。 按独立 0–4 档位锁定 2。
  - 证据：`update-manager/src/com/cockpitbench/update/UpdateManagerService.java:9`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:3`
- `solid_principle.dependency_inversion`：**2/4** — 权限依赖可注入，UpdateEngine 具体构造仍留在服务内。 按独立 0–4 档位锁定 2。
  - 证据：`update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:3`; `update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:2`
- `platform_reuse.platform_upgrade`：**3/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 2, 'arch_bound_status': 0, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 3。
  - 证据：`facts/FW-14.json#/platform_upgrade_review`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:9`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:3`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`a7bea930370a`; `refs/heads/platform/8295`@`f4b18929661f`

### FW-15 `car-runtime-service` — 12/52

- `compilation.ci_independence`：**1/3** — 仅有 PREUPLOAD.cfg/TEST_MAPPING 等 Android 系统层 CI 配置。
  - 证据：`facts/FW-15.json#/ci`; `TEST_MAPPING:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': False, 'external_dependencies_declared': False, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'Requires AAOS'}], 'standalone_target_anchors': []}；锁定 0。
  - 证据：`facts/FW-15.json#/compilation/external_build_closure`; `README.md:4`; `Android.bp:13`
- `compilation.api_version_management`：**0/3** — 专用语义版本证据=0、有效 API 检查=0；锁定 0。
  - 证据：`facts/FW-15.json#/api_version`
- `quality.integration_test`：**0/3** — 仅有类存在性检查和 assertTrue(true) 占位测试，按合同锁定 0。
  - 证据：`facts/FW-15.json#/integration_test`; `tests/integration/com/cockpitbench/carruntime/CarRuntimeServiceLaunchTest.java:19`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**0/4** — CarRuntimeService 集中多业务域、权限、反射和大量 Binder 方法。 按独立 0–4 档位锁定 0。
  - 证据：`runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:48`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:3`
- `solid_principle.open_closed`：**1/4** — 新增业务域需修改中心服务，核心对扩展不封闭。 按独立 0–4 档位锁定 1。
  - 证据：`runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:3`; `platform/src/com/cockpitbench/carruntime/product/AuroraBaseRuntimeProfile.java:24`
- `solid_principle.liskov_substitution`：**2/4** — profile 子类大体保持共同基类契约。 按独立 0–4 档位锁定 2。
  - 证据：`platform/src/com/cockpitbench/carruntime/product/AuroraBaseRuntimeProfile.java:24`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:48`
- `solid_principle.interface_segregation`：**0/4** — ICarRuntime 强制所有客户端依赖多业务域能力。 按独立 0–4 档位锁定 0。
  - 证据：`runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:48`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:3`
- `solid_principle.dependency_inversion`：**0/4** — 中心服务直接构造 facade 并保存全局实例。 按独立 0–4 档位锁定 0。
  - 证据：`runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:3`; `platform/src/com/cockpitbench/carruntime/product/AuroraBaseRuntimeProfile.java:24`
- `platform_reuse.platform_upgrade`：**0/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 3, 'arch_bound_status': 2, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 0。
  - 证据：`facts/FW-15.json#/platform_upgrade_review`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:48`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:3`
- `platform_reuse.release_branch_strategy`：**8/10** — 真实 refs 显示按平台共用分支，锁定 8。
  - 证据：`refs/heads/platform/8155`@`d2c21ebaf740`; `refs/heads/platform/8295`@`8ef2b0f2a5fb`

### FW-18 `vehicle-platform-service` — 14/52

- `compilation.ci_independence`：**1/3** — 仅有 PREUPLOAD.cfg/TEST_MAPPING 等 Android 系统层 CI 配置。
  - 证据：`facts/FW-18.json#/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': False, 'external_dependencies_declared': False, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [], 'standalone_target_anchors': []}；锁定 0。
  - 证据：`facts/FW-18.json#/compilation/external_build_closure`; `Android.bp:12`
- `compilation.api_version_management`：**1/3** — 专用语义版本证据=0、有效 API 检查=3；锁定 1。
  - 证据：`facts/FW-18.json#/api_version`; `apicheck.mk:147`; `apicheck.mk:155`
- `quality.integration_test`：**2/3** — 测试目标和断言有效，关键模块交互覆盖代理达到 50%；没有绑定 100% 执行结果，不能给 3。
  - 证据：`facts/FW-18.json#/integration_test`; `car-lib/src/android/car/test/CarTestManagerBinderWrapper.java:27`
- `solid_principle.single_responsibility`：**1/4** — PlatformSignalCoordinator 汇集连接、缓存、回调、profile 与 fallback。 按独立 0–4 档位锁定 1。
  - 证据：`platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:26`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:26`
- `solid_principle.open_closed`：**1/4** — 新增平台需要修改 router/profile 与 fallback 分支。 按独立 0–4 档位锁定 1。
  - 证据：`platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:26`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:3`
- `solid_principle.liskov_substitution`：**2/4** — vehicle profile 基本保持共同读取映射契约。 按独立 0–4 档位锁定 2。
  - 证据：`platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:3`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:26`
- `solid_principle.interface_segregation`：**2/4** — IVehiclePlatform 同时暴露信号和连接生命周期。 按独立 0–4 档位锁定 2。
  - 证据：`platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:26`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:26`
- `solid_principle.dependency_inversion`：**1/4** — Service 依赖全局 Coordinator，后者依赖具体 LegacyPlatformRouter。 按独立 0–4 档位锁定 1。
  - 证据：`platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:26`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:3`
- `platform_reuse.platform_upgrade`：**0/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 3, 'arch_bound_status': 2, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 0。
  - 证据：`facts/FW-18.json#/platform_upgrade_review`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:26`; `platform/src/com/cockpitbench/vehicleplatform/LegacyPlatformRouter.java:26`
- `platform_reuse.release_branch_strategy`：**3/10** — 真实 refs 同时存在平台分支和车型/SOP release 分支，车型拆分更细，锁定 3。
  - 证据：`refs/heads/platform/8155`@`1cd1c6a43839`; `refs/heads/platform/8295`@`bce6dc6fca9e`

### FW-16 `platform-compat-service` — 13/52

- `compilation.ci_independence`：**1/3** — 仅有 PREUPLOAD.cfg/TEST_MAPPING 等 Android 系统层 CI 配置。
  - 证据：`facts/FW-16.json#/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': False, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 5, 'match': 'requires an AAOS'}], 'standalone_target_anchors': []}；锁定 0。
  - 证据：`facts/FW-16.json#/compilation/external_build_closure`; `README.md:5`; `Android.bp:3`
- `compilation.api_version_management`：**1/3** — 专用语义版本证据=0、有效 API 检查=7；锁定 1。
  - 证据：`facts/FW-16.json#/api_version`; `car-builtin-lib/Android.bp:32`; `car-lib/Android.bp:105`
- `quality.integration_test`：**2/3** — 测试目标和断言有效，关键模块交互覆盖代理达到 50%；没有绑定 100% 执行结果，不能给 3。
  - 证据：`facts/FW-16.json#/integration_test`; `car-lib/src/android/car/test/CarLocationTestHelper.java:29`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**1/4** — PlatformCompatRuntime/Service 混合 registry、cache、polling 和兼容职责。 按独立 0–4 档位锁定 1。
  - 证据：`compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:19`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:19`
- `solid_principle.open_closed`：**1/4** — 平台规则与 vendor bridge 扩展需要修改多个核心类。 按独立 0–4 档位锁定 1。
  - 证据：`compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:19`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:3`
- `solid_principle.liskov_substitution`：**2/4** — Binder callback 基本维持声明契约但缺少跨版本替换测试。 按独立 0–4 档位锁定 2。
  - 证据：`compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:3`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:19`
- `solid_principle.interface_segregation`：**1/4** — IPlatformCompat 聚合命令、状态和 callback 多类能力。 按独立 0–4 档位锁定 1。
  - 证据：`compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:19`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:19`
- `solid_principle.dependency_inversion`：**1/4** — 运行时依赖静态 registry、具体 fallback 和反射 vendor 实现。 按独立 0–4 档位锁定 1。
  - 证据：`compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:19`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:3`
- `platform_reuse.platform_upgrade`：**0/10** — 区分正常 Framework API 后的 Android 七事实={'has_non_compatible_api': True, 'has_arch_specific_deps': False, 'version_bound_status': 3, 'arch_bound_status': 2, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_complex_permission_adaptation': False}；风险硬门槛锁定 0。
  - 证据：`facts/FW-16.json#/platform_upgrade_review`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatRuntime.java:19`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:19`
- `platform_reuse.release_branch_strategy`：**3/10** — 真实 refs 同时存在平台分支和车型/SOP release 分支，车型拆分更细，锁定 3。
  - 证据：`refs/heads/platform/8155`@`93ccc6f80839`; `refs/heads/platform/8295`@`068b6972dc4b`
