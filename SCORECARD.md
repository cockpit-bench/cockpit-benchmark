# Validation-18 标准评分总表

- APP：9 仓 / 72 叶 / 216/360
- Android Framework：9 仓 / 99 叶 / 239/468
- 合计：18 仓 / 171 叶 / 455/828

> 分数只由绑定 HEAD 的代码与 refs 证据推导；质量/规模标签是矩阵角色，不是打分输入。
> APP 的三个 architecture 叶属于同一 Architecture Macro，但按组件复用、依赖传播、构建模块边界分别评分，不把命中数当作统计独立样本。

## APP 9 仓

| ID | 仓库 | 角色 | 规模 | architecture.componentization | architecture.decoupling | architecture.modularization | compilation.ci_independence | compilation.compilation_independence | compilation.api_version_management | platform_reuse.platform_upgrade | platform_reuse.release_branch_strategy | 总分 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| APP-03 | climatix-hvac | high | small | 5 | 3 | 3 | 3 | 1 | 2 | 8 | 8 | 33/40 |
| APP-02 | horizon-launcher | high | medium | 5 | 3 | 3 | 2 | 1 | 2 | 8 | 8 | 32/40 |
| APP-01 | aurora-settings | high | large | 5 | 2 | 3 | 1 | 0 | 2 | 3 | 8 | 24/40 |
| APP-13 | market-hub | medium | small | 5 | 3 | 3 | 1 | 2 | 1 | 8 | 8 | 31/40 |
| APP-11 | motion-control | medium | medium | 5 | 3 | 3 | 1 | 2 | 1 | 3 | 3 | 21/40 |
| APP-14 | cockpit-shell | medium | large | 3 | 2 | 2 | 1 | 0 | 2 | 3 | 8 | 21/40 |
| APP-17 | thermo-control | low | small | 3 | 2 | 2 | 0 | 0 | 1 | 3 | 8 | 19/40 |
| APP-16 | nova-launcher | low | medium | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 8 | 20/40 |
| APP-15 | atlas-settings | low | large | 3 | 2 | 2 | 1 | 0 | 1 | 3 | 3 | 15/40 |

## Android Framework 9 仓

| ID | 仓库 | 角色 | 规模 | compilation.ci_independence | compilation.compilation_independence | compilation.api_version_management | quality.integration_test | solid_principle.single_responsibility | solid_principle.open_closed | solid_principle.liskov_substitution | solid_principle.interface_segregation | solid_principle.dependency_inversion | platform_reuse.platform_upgrade | platform_reuse.release_branch_strategy | 总分 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FW-02 | vehicle-property-service | high | small | 3 | 1 | 2 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 8 | 33/52 |
| FW-03 | vehicle-hal-adapter | high | medium | 3 | 1 | 2 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 8 | 33/52 |
| FW-07 | vehicle-diagnostics | high | large | 3 | 1 | 3 | 3 | 2 | 3 | 3 | 3 | 2 | 3 | 8 | 34/52 |
| FW-10 | cockpit-manager-kit | medium | small | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 3 | 8 | 26/52 |
| FW-08 | soa-gateway | medium | medium | 2 | 1 | 2 | 1 | 2 | 3 | 2 | 3 | 2 | 3 | 8 | 29/52 |
| FW-14 | update-manager-service | medium | large | 2 | 1 | 3 | 1 | 2 | 2 | 3 | 2 | 2 | 3 | 8 | 29/52 |
| FW-15 | car-runtime-service | low | small | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 8 | 12/52 |
| FW-18 | vehicle-platform-service | low | medium | 1 | 0 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 3 | 8 | 21/52 |
| FW-16 | platform-compat-service | low | large | 1 | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 1 | 3 | 8 | 22/52 |

## 逐叶理由与证据

### APP-03 `climatix-hvac` — 33/40

- `architecture.componentization`：**5/5** — 真实构建模块=7、可复用组件=6、可替换组件=6、显式公开契约=15、源码归属边界=True；按组件复用/替换构念锁定 5。
  - 证据：`facts/APP-03.json#/facts/architecture/componentization_metrics`; `comfort/src/main/java/com/cockpitbench/climatix/comfort/ComfortPolicy.kt:19`; `comfort/build.gradle.kts:1`
- `architecture.decoupling`：**3/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=1、Soong 已归属/仍未归属源码=0/0；按依赖方向/传播构念锁定 3。
  - 证据：`facts/APP-03.json#/facts/architecture/decoupling_metrics`; `vehicle-api/build.gradle.kts:1`
- `architecture.modularization`：**3/3** — 真实构建模块=7、内聚模块=7、规范命名模块=3、模块测试入口=6、API/implementation 依赖边=0/12；按构建模块边界构念锁定 3。
  - 证据：`facts/APP-03.json#/facts/architecture/modularization_metrics`; `settings.gradle.kts:4`; `app/build.gradle.kts:3`
- `compilation.ci_independence`：**3/3** — CI 分类=independent_ci，锁定 3。
  - 证据：`facts/APP-03.json#/facts/ci`; `.github/workflows/android.yml:15`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 1。
  - 证据：`facts/APP-03.json#/facts/compilation/dependency_type_candidates`; `README.md:4`; `.github/workflows/android.yml:15`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-03.json#/facts/api_version`; `version.properties:1`; `version.properties:2`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': True, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': True, 'uncovered_non_compatible_api_count': 0, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-03.json#/facts/platform_upgrade/seven_fact_candidates`; `vehicle-api/src/main/java/com/cockpitbench/climatix/vehicle/ClimateServiceLocator.kt:29`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`b313db00f552`; `refs/heads/platform/8295`@`f6df3cc885c4`

### APP-02 `horizon-launcher` — 32/40

- `architecture.componentization`：**5/5** — 真实构建模块=3、可复用组件=2、可替换组件=2、显式公开契约=41、源码归属边界=True；按组件复用/替换构念锁定 5。
  - 证据：`facts/APP-02.json#/facts/architecture/componentization_metrics`; `launcher-common/src/main/java/com/android/car/launcher/domain/LauncherCatalog.java:5`; `launcher-common/build.gradle:1`
- `architecture.decoupling`：**3/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=1、Soong 已归属/仍未归属源码=66/0；按依赖方向/传播构念锁定 3。
  - 证据：`facts/APP-02.json#/facts/architecture/decoupling_metrics`; `launcher-app/build.gradle:1`; `app/Android.bp:34`
- `architecture.modularization`：**3/3** — 真实构建模块=3、内聚模块=3、规范命名模块=2、模块测试入口=0、API/implementation 依赖边=0/3；按构建模块边界构念锁定 3。
  - 证据：`facts/APP-02.json#/facts/architecture/modularization_metrics`; `settings.gradle:5`; `launcher-app/build.gradle:1`
- `compilation.ci_independence`：**2/3** — CI 分类=mixed，锁定 2。
  - 证据：`facts/APP-02.json#/facts/ci`; `.github/workflows/android.yml:2`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 1。
  - 证据：`facts/APP-02.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `.github/workflows/android.yml:2`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-02.json#/facts/api_version`; `version.properties:1`; `version.properties:2`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': False, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 0, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-02.json#/facts/platform_upgrade/seven_fact_candidates`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295', 'release/2026.1']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`29ce9d750e0b`; `refs/heads/platform/8295`@`30709ae25c06`; `refs/heads/release/2026.1`@`af0cf348d8f9`

### APP-01 `aurora-settings` — 24/40

- `architecture.componentization`：**5/5** — 真实构建模块=4、可复用组件=3、可替换组件=3、显式公开契约=94、源码归属边界=True；按组件复用/替换构念锁定 5。
  - 证据：`facts/APP-01.json#/facts/architecture/componentization_metrics`; `settings-common/src/main/java/com/android/car/settings/common/ActionButtonInfo.java:245`; `settings-common/build.gradle:1`
- `architecture.decoupling`：**2/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=4、Soong 已归属/仍未归属源码=0/0；按依赖方向/传播构念锁定 2。
  - 证据：`facts/APP-01.json#/facts/architecture/decoupling_metrics`; `app/build.gradle:16`
- `architecture.modularization`：**3/3** — 真实构建模块=4、内聚模块=4、规范命名模块=2、模块测试入口=1、API/implementation 依赖边=0/3；按构建模块边界构念锁定 3。
  - 证据：`facts/APP-01.json#/facts/architecture/modularization_metrics`; `settings.gradle:4`; `app/build.gradle:16`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-01.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-01.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `app/build.gradle:16`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=2；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-01.json#/facts/api_version`; `version.properties:1`; `version.properties:2`; `app/build.gradle:31`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': True, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 54, 'version_bound_status': 0}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-01.json#/facts/platform_upgrade/seven_fact_candidates`; `settings-common/src/main/java/com/android/car/settings/common/PreferenceControllerListHelper.java:93`; `app/src/main/java/com/android/car/settings/accessibility/ScreenReaderUtils.java:29`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295', 'release/2026.1']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`769d29b8ea64`; `refs/heads/platform/8295`@`33e548d7b2fd`; `refs/heads/release/2026.1`@`c4801bf2d3c4`

### APP-13 `market-hub` — 31/40

- `architecture.componentization`：**5/5** — 真实构建模块=9、可复用组件=3、可替换组件=3、显式公开契约=14、源码归属边界=True；按组件复用/替换构念锁定 5。
  - 证据：`facts/APP-13.json#/facts/architecture/componentization_metrics`; `foundation-core/src/main/java/com/cockpitbench/foundation/core/CockpitClock.java:16`; `foundation-core/build.gradle:1`
- `architecture.decoupling`：**3/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=0、Soong 已归属/仍未归属源码=0/0；按依赖方向/传播构念锁定 3。
  - 证据：`facts/APP-13.json#/facts/architecture/decoupling_metrics`; `settings.gradle:2`
- `architecture.modularization`：**3/3** — 真实构建模块=9、内聚模块=8、规范命名模块=3、模块测试入口=0、API/implementation 依赖边=0/15；按构建模块边界构念锁定 3。
  - 证据：`facts/APP-13.json#/facts/architecture/modularization_metrics`; `settings.gradle:2`; `foundation-core/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-13.json#/facts/ci`; `TEST_MAPPING:1`
- `compilation.compilation_independence`：**2/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': False}；同仓模块依赖不扣分，锁定 2。
  - 证据：`facts/APP-13.json#/facts/compilation/dependency_type_candidates`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-13.json#/facts/api_version`; `market-app/build.gradle:3`
- `platform_reuse.platform_upgrade`：**8/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': False, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 0, 'version_bound_status': 0}；按风险单调硬门槛锁定 8。
  - 证据：`facts/APP-13.json#/facts/platform_upgrade/seven_fact_candidates`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295', 'release/2026.1']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`f8623eec7728`; `refs/heads/platform/8295`@`fad482ad315d`; `refs/heads/release/2026.1`@`7a3bcd1ea112`

### APP-11 `motion-control` — 21/40

- `architecture.componentization`：**5/5** — 真实构建模块=9、可复用组件=3、可替换组件=3、显式公开契约=13、源码归属边界=True；按组件复用/替换构念锁定 5。
  - 证据：`facts/APP-11.json#/facts/architecture/componentization_metrics`; `foundation-core/src/main/java/com/cockpitbench/foundation/core/CockpitClock.java:16`; `foundation-core/build.gradle:1`
- `architecture.decoupling`：**3/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=1、Soong 已归属/仍未归属源码=0/0；按依赖方向/传播构念锁定 3。
  - 证据：`facts/APP-11.json#/facts/architecture/decoupling_metrics`; `motion-platform/build.gradle:1`
- `architecture.modularization`：**3/3** — 真实构建模块=9、内聚模块=8、规范命名模块=3、模块测试入口=0、API/implementation 依赖边=0/15；按构建模块边界构念锁定 3。
  - 证据：`facts/APP-11.json#/facts/architecture/modularization_metrics`; `settings.gradle:2`; `foundation-core/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-11.json#/facts/ci`; `TEST_MAPPING:1`
- `compilation.compilation_independence`：**2/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': True, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': False}；同仓模块依赖不扣分，锁定 2。
  - 证据：`facts/APP-11.json#/facts/compilation/dependency_type_candidates`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-11.json#/facts/api_version`; `motion-app/build.gradle:3`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 1, 'version_bound_status': 0}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-11.json#/facts/platform_upgrade/seven_fact_candidates`; `motion-platform/src/main/java/com/cockpitbench/motion/platform/PlatformMotionAdapter.java:16`
- `platform_reuse.release_branch_strategy`：**3/10** — 存在含车型身份且有真实差异的单车型 SOP 分支 ['sop/2026.1-model-a1', 'sop/2026.1-model-b2']，按最细车型级策略锁定 3。
  - 证据：`refs/heads/sop/2026.1-model-a1`@`418aba900972`; `refs/heads/sop/2026.1-model-b2`@`dc7ac0a5e97e`

### APP-14 `cockpit-shell` — 21/40

- `architecture.componentization`：**3/5** — 真实构建模块=2、可复用组件=1、可替换组件=1、显式公开契约=55、源码归属边界=True；按组件复用/替换构念锁定 3。
  - 证据：`facts/APP-14.json#/facts/architecture/componentization_metrics`; `shell-core/build.gradle:1`; `Android.bp:20`
- `architecture.decoupling`：**2/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=2、Soong 已归属/仍未归属源码=304/0；按依赖方向/传播构念锁定 2。
  - 证据：`facts/APP-14.json#/facts/architecture/decoupling_metrics`; `shell-app/build.gradle:1`; `Android.bp:20`
- `architecture.modularization`：**2/3** — 真实构建模块=2、内聚模块=2、规范命名模块=2、模块测试入口=0、API/implementation 依赖边=0/1；按构建模块边界构念锁定 2。
  - 证据：`facts/APP-14.json#/facts/architecture/modularization_metrics`; `settings.gradle:5`; `shell-app/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-14.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-14.json#/facts/compilation/dependency_type_candidates`; `README.md:4`; `build.gradle:1`
- `compilation.api_version_management`：**2/3** — 语义版本=True、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 2。
  - 证据：`facts/APP-14.json#/facts/api_version`; `version.properties:1`; `version.properties:2`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 1, 'version_bound_status': 1}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-14.json#/facts/platform_upgrade/seven_fact_candidates`; `shell-app/src/main/java/com/android/systemui/cockpit/presentation/CockpitShellController.java:12`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295', 'release/2026.1']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`e78cfb993351`; `refs/heads/platform/8295`@`d4afa6cac8e9`; `refs/heads/release/2026.1`@`2883836c2dd7`

### APP-17 `thermo-control` — 19/40

- `architecture.componentization`：**3/5** — 真实构建模块=2、可复用组件=1、可替换组件=1、显式公开契约=1、源码归属边界=True；按组件复用/替换构念锁定 3。
  - 证据：`facts/APP-17.json#/facts/architecture/componentization_metrics`; `vehicle/build.gradle.kts:1`
- `architecture.decoupling`：**2/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=0、平台变更传播模块=2、Soong 已归属/仍未归属源码=0/0；按依赖方向/传播构念锁定 2。
  - 证据：`facts/APP-17.json#/facts/architecture/decoupling_metrics`; `app/build.gradle.kts:1`
- `architecture.modularization`：**2/3** — 真实构建模块=2、内聚模块=2、规范命名模块=1、模块测试入口=1、API/implementation 依赖边=0/1；按构建模块边界构念锁定 2。
  - 证据：`facts/APP-17.json#/facts/architecture/modularization_metrics`; `settings.gradle.kts:4`; `app/build.gradle.kts:1`
- `compilation.ci_independence`：**0/3** — CI 分类=no_ci，锁定 0。
  - 证据：`facts/APP-17.json#/facts/ci`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': True, 'external_dependencies_declared': True, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': True, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-17.json#/facts/compilation/dependency_type_candidates`; `README.md:6`; `app/build.gradle.kts:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-17.json#/facts/api_version`; `app/build.gradle.kts:10`; `app/build.gradle.kts:9`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': False, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 66, 'version_bound_status': 1}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-17.json#/facts/platform_upgrade/seven_fact_candidates`; `app/src/main/java/com/cockpitbench/thermo/ThermalPlatformRuntime.java:9`; `vehicle/src/main/java/com/cockpitbench/thermo/vehicle/platform/Sa8155ClimateBridge.kt:29`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`483e416e1a9e`; `refs/heads/platform/8295`@`dc027394cbc9`

### APP-16 `nova-launcher` — 20/40

- `architecture.componentization`：**3/5** — 真实构建模块=4、可复用组件=3、可替换组件=0、显式公开契约=66、源码归属边界=True；按组件复用/替换构念锁定 3。
  - 证据：`facts/APP-16.json#/facts/architecture/componentization_metrics`; `legacy-platform/build.gradle:1`; `app/Android.bp:34`
- `architecture.decoupling`：**2/3** — 环=0、反向依赖=0、跨模块源码侵入=0、具体实现依赖边=3、平台变更传播模块=4、Soong 已归属/仍未归属源码=73/0；按依赖方向/传播构念锁定 2。
  - 证据：`facts/APP-16.json#/facts/architecture/decoupling_metrics`; `launcher-app/build.gradle:16`; `app/Android.bp:34`
- `architecture.modularization`：**2/3** — 真实构建模块=4、内聚模块=4、规范命名模块=1、模块测试入口=0、API/implementation 依赖边=0/3；按构建模块边界构念锁定 2。
  - 证据：`facts/APP-16.json#/facts/architecture/modularization_metrics`; `settings.gradle:5`; `launcher-app/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-16.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': True, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-16.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-16.json#/facts/api_version`; `launcher-app/build.gradle:5`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 1, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 2, 'version_bound_status': 3}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-16.json#/facts/platform_upgrade/seven_fact_candidates`; `launcher-app/src/main/java/com/android/car/launcher/LauncherRuntime.java:13`; `legacy-platform/src/main/java/com/android/car/launcher/legacy/LegacyPlatformRuntime.java:9`
- `platform_reuse.release_branch_strategy`：**8/10** — 存在平台级分支 ['platform/8155', 'platform/8295', 'platform/xinqing', 'release/sop-2025']，且没有车型级一车一 SOP，锁定 8。
  - 证据：`refs/heads/platform/8155`@`12018f5c8629`; `refs/heads/platform/8295`@`8d942866a727`; `refs/heads/platform/xinqing`@`6c1af62ba519`

### APP-15 `atlas-settings` — 15/40

- `architecture.componentization`：**3/5** — 真实构建模块=3、可复用组件=1、可替换组件=1、显式公开契约=121、源码归属边界=False；按组件复用/替换构念锁定 3。
  - 证据：`facts/APP-15.json#/facts/architecture/componentization_metrics`; `modern-settings/build.gradle:1`
- `architecture.decoupling`：**2/3** — 环=0、反向依赖=0、跨模块源码侵入=1、具体实现依赖边=0、平台变更传播模块=3、Soong 已归属/仍未归属源码=0/0；按依赖方向/传播构念锁定 2。
  - 证据：`facts/APP-15.json#/facts/architecture/decoupling_metrics`; `app/build.gradle:1`
- `architecture.modularization`：**2/3** — 真实构建模块=3、内聚模块=2、规范命名模块=1、模块测试入口=1、API/implementation 依赖边=0/1；按构建模块边界构念锁定 2。
  - 证据：`facts/APP-15.json#/facts/architecture/modularization_metrics`; `settings.gradle:4`; `app/build.gradle:1`
- `compilation.ci_independence`：**1/3** — CI 分类=android_system_ci，锁定 1。
  - 证据：`facts/APP-15.json#/facts/ci`; `PREUPLOAD.cfg:1`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'critical_dependencies_version_pinned': False, 'external_dependencies_declared': False, 'has_framework_jar_dependency': False, 'has_internal_project_source_dependency': True, 'has_local_aar_dependency': False, 'has_meaningful_standalone_target': False, 'has_unversioned_external_artifact': False, 'has_versioned_external_artifact': False, 'requires_full_platform_source': True}；同仓模块依赖不扣分，锁定 0。
  - 证据：`facts/APP-15.json#/facts/compilation/dependency_type_candidates`; `README.md:5`; `app/build.gradle:1`
- `compilation.api_version_management`：**1/3** — 语义版本=False、有效兼容检查=0、自动绑定=0；已排除 Java/SDK 级别和固定字符串检查，锁定 1。
  - 证据：`facts/APP-15.json#/facts/api_version`; `app/src/main/AndroidManifest.xml:1`
- `platform_reuse.platform_upgrade`：**3/10** — Android 七事实={'arch_bound_status': 0, 'has_arch_specific_deps': False, 'has_complex_permission_adaptation': False, 'has_interface_abstraction': False, 'has_light_permission_adaptation': True, 'has_non_compatible_api': True, 'non_compatible_api_covered_by_abstraction': False, 'uncovered_non_compatible_api_count': 66, 'version_bound_status': 0}；按风险单调硬门槛锁定 3。
  - 证据：`facts/APP-15.json#/facts/platform_upgrade/seven_fact_candidates`; `app/src/main/java/com/android/car/settings/common/PreferenceControllerListHelper.java:93`; `modern-settings/src/main/java/com/android/car/settings/common/PreferenceControllerListHelper.java:93`
- `platform_reuse.release_branch_strategy`：**3/10** — 存在含车型身份且有真实差异的单车型 SOP 分支 ['sop/2024-model-a1', 'sop/2024-model-b2']，按最细车型级策略锁定 3。
  - 证据：`refs/heads/sop/2024-model-a1`@`29e98aef4200`; `refs/heads/sop/2024-model-b2`@`676c405af0f6`

### FW-02 `vehicle-property-service` — 33/52

- `compilation.ci_independence`：**3/3** — 实际构建/测试/质量命令数=[1, 1, 3]，系统 CI 文件数=1；阶段覆盖范围以实际构建目标为准，锁定 3。
  - 证据：`facts/FW-02.json#/current_review/ci`; `.github/workflows/native.yml:13`; `.github/workflows/native.yml:14`; `.github/workflows/native.yml:11`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': False, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'requires an AOSP'}], 'standalone_target_anchors': [{'path': '.github/workflows/native.yml', 'line': 2, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 5, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 12, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_executable('}, {'path': 'native/common/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/contract/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/hal/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/platform/CMakeLists.txt', 'line': 1, 'match': 'add_library('}]}；锁定 1。
  - 证据：`facts/FW-02.json#/compilation/external_build_closure`; `README.md:4`; `.github/workflows/native.yml:2`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=2，有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-02.json#/api_version`; `native/CMakeLists.txt:2`; `native/VERSION:1`
- `quality.integration_test`：**3/3** — final HEAD Actions run=33758455763，测试 5/5 通过，native/ only line coverage=0.8666667≥0.6；锁定 3。
  - 证据：`facts/FW-02.json#/integration_test/ci_execution_evidence`; `native/tests/vehicle_property_integration_test.cpp:7`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**3/4** — HAL 契约将属性写入职责集中在可替换接口。 写入白名单策略独立于 HAL 传输和 Binder 生命周期。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-02.json#/current_review/solid/single_responsibility`; `runtime/src/com/android/car/VehicleStub.java:193`; `platform/src/com/cockpitbench/vehicleproperty/VehiclePropertyPolicy.java:29`
- `solid_principle.open_closed`：**2/4** — AIDL/HIDL 的工厂选择集中在一个创建入口；增加后端需修改此入口。 订阅客户端通过抽象工厂返回，可扩展实现。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-02.json#/current_review/solid/open_closed`; `runtime/src/com/android/car/VehicleStub.java:79`; `runtime/src/com/android/car/VehicleStub.java:172`
- `solid_principle.liskov_substitution`：**3/4** — 生产实现=2，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 3。
  - 证据：`facts/FW-02.json#/lsp_review`; `runtime/src/com/android/car/VehicleStub.java:39`; `runtime/src/com/android/car/AidlVehicleStub.java:64`; `runtime/src/com/android/car/HidlVehicleStub.java:44`
- `solid_principle.interface_segregation`：**3/4** — 属性请求接口按读写与配置组织。 异步事件客户端只实现单独 oneway 回调。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-02.json#/current_review/solid/interface_segregation`; `api/src/android/car/hardware/property/ICarProperty.aidl:34`; `api/src/android/car/hardware/property/ICarPropertyEventListener.aidl:31`
- `solid_principle.dependency_inversion`：**2/4** — Binder 服务构造依赖具体 PropertyHalService，而非服务端口。 下层 HAL 保留 VehicleStub 抽象依赖。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-02.json#/current_review/solid/dependency_inversion`; `runtime/src/com/android/car/CarPropertyService.java:80`; `runtime/src/com/android/car/hal/VehicleHal.java:96`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=10；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-02.json#/current_review/platform`; `api/src/android/car/CarProjectionManager.java:50`; `runtime/src/com/android/car/CarProjectionService.java:79`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/2.0']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`fab2b54427e9`; `refs/heads/platform/8295`@`1c687eb3c852`

### FW-03 `vehicle-hal-adapter` — 33/52

- `compilation.ci_independence`：**3/3** — 实际构建/测试/质量命令数=[4, 3, 4]，系统 CI 文件数=2；阶段覆盖范围以实际构建目标为准，锁定 3。
  - 证据：`facts/FW-03.json#/current_review/ci`; `.github/workflows/native-ci.yml:36`; `.github/workflows/native-ci.yml:43`; `.github/workflows/native-ci.yml:46`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [], 'standalone_target_anchors': [{'path': '.github/workflows/native-ci.yml', 'line': 17, 'match': 'build'}, {'path': '.github/workflows/native-ci.yml', 'line': 31, 'match': 'build'}, {'path': '.github/workflows/native-ci.yml', 'line': 32, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 3, 'match': 'project('}, {'path': 'native/CMakeLists.txt', 'line': 25, 'match': 'cmake'}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/application/CMakeLists.txt', 'line': 15, 'match': 'add_executable('}, {'path': 'native/common/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/contract/CMakeLists.txt', 'line': 24, 'match': 'build'}, {'path': 'native/contract/CMakeLists.txt', 'line': 25, 'match': 'CMake'}]}；锁定 1。
  - 证据：`facts/FW-03.json#/compilation/external_build_closure`; `.github/workflows/native-ci.yml:17`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=2，有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-03.json#/api_version`; `native/CMakeLists.txt:5`; `native/VERSION:1`
- `quality.integration_test`：**3/3** — final HEAD Actions run=33757391217，测试 84/84 通过，native/ excluding native/tests/ line coverage=0.8318070818≥0.8；锁定 3。
  - 证据：`facts/FW-03.json#/integration_test/ci_execution_evidence`; `native/tests/client_ipc_vertical_integration_test.cpp:168`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**3/4** — HAL 契约将属性写入职责集中在可替换接口。 属性 Binder 的注册和读写均围绕同一属性领域。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-03.json#/current_review/solid/single_responsibility`; `service/src/com/android/car/VehicleStub.java:167`; `car-lib/src/android/car/hardware/property/ICarProperty.aidl:28`
- `solid_principle.open_closed`：**2/4** — AIDL/HIDL 的工厂选择集中在一个创建入口；增加后端需修改此入口。 订阅客户端通过抽象工厂返回，可扩展实现。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-03.json#/current_review/solid/open_closed`; `service/src/com/android/car/VehicleStub.java:76`; `service/src/com/android/car/VehicleStub.java:146`
- `solid_principle.liskov_substitution`：**3/4** — 生产实现=2，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 3。
  - 证据：`facts/FW-03.json#/lsp_review`; `service/src/com/android/car/VehicleStub.java:38`; `service/src/com/android/car/AidlVehicleStub.java:64`; `service/src/com/android/car/HidlVehicleStub.java:44`
- `solid_principle.interface_segregation`：**3/4** — 属性请求接口按读写与配置组织。 异步事件客户端只实现单独 oneway 回调。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-03.json#/current_review/solid/interface_segregation`; `car-lib/src/android/car/hardware/property/ICarProperty.aidl:34`; `car-lib/src/android/car/hardware/property/ICarPropertyEventListener.aidl:31`
- `solid_principle.dependency_inversion`：**2/4** — 应用服务构造依赖具体 VehiclePropertyGateway，而非独立应用端口。 Java HAL 保留 VehicleStub 抽象依赖。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-03.json#/current_review/solid/dependency_inversion`; `native/application/include/fw03/application/vehicle_service.h:31`; `service/src/com/android/car/hal/VehicleHal.java:96`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=14；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-03.json#/current_review/platform`; `car-lib/src/android/car/media/CarAudioPatchHandle.java:28`; `car-lib/src/android/car/user/CarUserManager.java:60`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/2026.1']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`270b396861b0`; `refs/heads/platform/8295`@`4449839764f7`

### FW-07 `vehicle-diagnostics` — 34/52

- `compilation.ci_independence`：**3/3** — 实际构建/测试/质量命令数=[1, 1, 3]，系统 CI 文件数=5；阶段覆盖范围以实际构建目标为准，锁定 3。
  - 证据：`facts/FW-07.json#/current_review/ci`; `.github/workflows/native.yml:13`; `.github/workflows/native.yml:14`; `.github/workflows/native.yml:11`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 5, 'match': 'complete build requires an AAOS'}], 'standalone_target_anchors': [{'path': '.github/workflows/native.yml', 'line': 2, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 5, 'match': 'build'}, {'path': '.github/workflows/native.yml', 'line': 12, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_executable('}, {'path': 'native/common/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/contract/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/hal/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/platform/CMakeLists.txt', 'line': 1, 'match': 'add_library('}]}；锁定 1。
  - 证据：`facts/FW-07.json#/compilation/external_build_closure`; `README.md:5`; `.github/workflows/native.yml:2`
- `compilation.api_version_management`：**3/3** — 专用语义版本证据=2，有效 API 检查=3；锁定 3。
  - 证据：`facts/FW-07.json#/api_version`; `native/CMakeLists.txt:2`; `native/VERSION:1`; `car-lib/Android.bp:105`
- `quality.integration_test`：**3/3** — final HEAD Actions run=33758464550，测试 5/5 通过，native/ only line coverage=0.8666667≥0.6；锁定 3。
  - 证据：`facts/FW-07.json#/integration_test/ci_execution_evidence`; `cpp/car_binder_lib/largeParcelable/tests/LargeParcelableTest.cpp:63`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — 性能处理类还负责组织持久化状态，存在职责集中。 同一性能处理类遍历并通知监听者；职责集中在 watchdog 域内。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-07.json#/current_review/solid/single_responsibility`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:1215`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:1326`
- `solid_principle.open_closed`：**3/4** — 资源通知经监听者集合分派，不依赖客户端类型分支。 遥测服务接收 ICarDataListener 接口扩展接收者。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-07.json#/current_review/solid/open_closed`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:1326`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:63`
- `solid_principle.liskov_substitution`：**3/4** — 生产实现=2，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 3。
  - 证据：`facts/FW-07.json#/lsp_review`; `service/src/com/android/car/CarDiagnosticService.java:556`; `service/src/com/android/car/CarDiagnosticService.java:571`; `service/src/com/android/car/CarDiagnosticService.java:596`
- `solid_principle.interface_segregation`：**3/4** — 诊断客户端通过独立诊断监听者订阅。 遥测监听契约与诊断接口分离。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-07.json#/current_review/solid/interface_segregation`; `car-lib/src/android/car/diagnostic/ICarDiagnostic.aidl:27`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:63`
- `solid_principle.dependency_inversion`：**2/4** — 时钟、存储和 daemon helper 从构造注入，但存储/helper 为具体类型。 遥测输出依赖 AIDL 监听抽象。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-07.json#/current_review/solid/dependency_inversion`; `service/src/com/android/car/watchdog/WatchdogPerfHandler.java:303`; `cpp/telemetry/cartelemetryd/src/TelemetryServer.h:63`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=32；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-07.json#/current_review/platform`; `car-lib/src/android/car/CarProjectionManager.java:50`; `car-lib/src/android/car/media/CarAudioPatchHandle.java:28`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/2026.1']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`85f0ccfb542a`; `refs/heads/platform/8295`@`87130476985f`

### FW-10 `cockpit-manager-kit` — 26/52

- `compilation.ci_independence`：**2/3** — 实际构建/测试/质量命令数=[1, 1, 0]，系统 CI 文件数=1；阶段覆盖范围以实际构建目标为准，锁定 2。
  - 证据：`facts/FW-10.json#/current_review/ci`; `APP_BUILD:2`; `APP_BUILD:3`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'requires an AOSP'}], 'standalone_target_anchors': [{'path': 'APP_BUILD', 'line': 1, 'match': 'cmake'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'build'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/service/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/tests/CMakeLists.txt', 'line': 6, 'match': 'add_executable('}]}；锁定 1。
  - 证据：`facts/FW-10.json#/compilation/external_build_closure`; `README.md:4`; `APP_BUILD:1`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=1，有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-10.json#/api_version`; `native/CMakeLists.txt:2`
- `quality.integration_test`：**1/3** — 有效测试源=46；无执行证明不推断通过率，锁定 1。
  - 证据：`facts/FW-10.json#/integration_test/executable_test_sources`; `native/tests/cockpit_manager_integration_test.cpp:5`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — 权限检查、路由、fallback 与输出转换集中于网关方法。 后端查找与调用仍被分离到 Registry。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-10.json#/current_review/solid/single_responsibility`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:29`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`
- `solid_principle.open_closed`：**2/4** — Backend 通过注册表扩展。 扩展芯片后端需修改具体类名映射。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-10.json#/current_review/solid/open_closed`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`; `manager-runtime/src/com/cockpitbench/managerkit/PlatformManagerFallback.java:22`
- `solid_principle.liskov_substitution`：**2/4** — 生产实现=1，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 2。
  - 证据：`facts/FW-10.json#/lsp_review`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerRegistry.java:17`; `manager-runtime/src/com/cockpitbench/managerkit/VehiclePropertyBackend.java:21`
- `solid_principle.interface_segregation`：**2/4** — 通用字符串/Bundle 网关让不同 manager 共享无类型入口。 事件回调独立于调用接口。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-10.json#/current_review/solid/interface_segregation`; `manager-runtime/src/com/cockpitbench/managerkit/IManagerGateway.aidl:5`; `manager-runtime/src/com/cockpitbench/managerkit/IManagerGatewayListener.aidl:4`
- `solid_principle.dependency_inversion`：**1/4** — 高层直接创建 Registry 和 Fallback。 高层还直接创建 VehiclePropertyBackend，多个依赖不可替换。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-10.json#/current_review/solid/dependency_inversion`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:23`; `manager-runtime/src/com/cockpitbench/managerkit/ManagerGatewayService.java:26`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=10；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-10.json#/current_review/platform`; `api/src/android/car/CarProjectionManager.java:50`; `runtime/src/com/android/car/CarProjectionService.java:79`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/2026.1']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`fcd9448a5bad`; `refs/heads/platform/8295`@`75655639921a`

### FW-08 `soa-gateway` — 29/52

- `compilation.ci_independence`：**2/3** — 实际构建/测试/质量命令数=[2, 1, 0]，系统 CI 文件数=4；阶段覆盖范围以实际构建目标为准，锁定 2。
  - 证据：`facts/FW-08.json#/current_review/ci`; `APP_BUILD:9`; `APP_BUILD:16`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'complete build still requires AOSP'}], 'standalone_target_anchors': [{'path': 'APP_BUILD', 'line': 7, 'match': 'build'}, {'path': 'APP_BUILD', 'line': 9, 'match': 'cmake'}, {'path': 'APP_BUILD', 'line': 15, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 3, 'match': 'project('}, {'path': 'native/CMakeLists.txt', 'line': 28, 'match': 'cmake'}, {'path': 'native/application/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/application/CMakeLists.txt', 'line': 7, 'match': 'add_library('}, {'path': 'native/application/CMakeLists.txt', 'line': 13, 'match': 'add_executable('}, {'path': 'native/broker/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/broker/CMakeLists.txt', 'line': 7, 'match': 'add_library('}]}；锁定 1。
  - 证据：`facts/FW-08.json#/compilation/external_build_closure`; `README.md:4`; `APP_BUILD:7`
- `compilation.api_version_management`：**2/3** — 专用语义版本证据=3，有效 API 检查=0；锁定 2。
  - 证据：`facts/FW-08.json#/api_version`; `native/CMakeLists.txt:5`; `native/CMakeLists.txt:23`; `native/VERSION:1`
- `quality.integration_test`：**1/3** — 有效测试源=13；无执行证明不推断通过率，锁定 1。
  - 证据：`facts/FW-08.json#/integration_test/executable_test_sources`; `native/tests/gateway_codec_test.cpp:11`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — 服务同时承担会话生命周期、路由策略重载和传输健康查询。 Provider、依赖图与包路由在 broker 中分为具体组件。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-08.json#/current_review/solid/single_responsibility`; `native/application/include/fw08/application/soa_gateway_service.h:72`; `native/broker/include/fw08/broker/soa_broker.h:60`
- `solid_principle.open_closed`：**3/4** — 通过 ProviderInfo/Offering 注册提供者，不以产品类分支新增业务。 传输接口可由构造注入替换。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-08.json#/current_review/solid/open_closed`; `native/broker/include/fw08/broker/soa_broker.h:33`; `native/broker/include/fw08/broker/soa_broker.h:23`
- `solid_principle.liskov_substitution`：**2/4** — 生产实现=1，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 2。
  - 证据：`facts/FW-08.json#/lsp_review`; `native/transport/include/fw08/transport/ipc_transport.h:25`; `native/transport/include/fw08/transport/unix_socket_transport.h:11`; `native/tests/support/fake_ipc_transport.h:11`
- `solid_principle.interface_segregation`：**3/4** — Broker 暴露消息订阅和发布契约。 传输合同与业务 provider/订阅接口分离。 根据明确标注的语义裁决按合同锁定 3。
  - 证据：`facts/FW-08.json#/current_review/solid/interface_segregation`; `native/broker/include/fw08/broker/soa_broker.h:42`; `native/transport/include/fw08/transport/ipc_transport.h:30`
- `solid_principle.dependency_inversion`：**2/4** — 顶层服务依赖具体 UnixSocketTransport，限制替换。 Broker 的主要传输依赖 IpcTransport 抽象。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-08.json#/current_review/solid/dependency_inversion`; `native/application/include/fw08/application/soa_gateway_service.h:42`; `native/broker/include/fw08/broker/soa_broker.h:23`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=57；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-08.json#/current_review/platform`; `car-lib/src/android/car/CarProjectionManager.java:50`; `car-lib/src/android/car/media/CarAudioPatchHandle.java:28`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/2026.1']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`c79cded97d4f`; `refs/heads/platform/8295`@`df09b062ef96`

### FW-14 `update-manager-service` — 29/52

- `compilation.ci_independence`：**2/3** — 实际构建/测试/质量命令数=[1, 1, 0]，系统 CI 文件数=5；阶段覆盖范围以实际构建目标为准，锁定 2。
  - 证据：`facts/FW-14.json#/current_review/ci`; `APP_BUILD:2`; `APP_BUILD:3`
- `compilation.compilation_independence`：**1/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': True, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 3, 'match': 'Complete build requires an AOSP'}], 'standalone_target_anchors': [{'path': 'APP_BUILD', 'line': 1, 'match': 'cmake'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'build'}, {'path': 'APP_BUILD', 'line': 2, 'match': 'cmake'}, {'path': 'native/CMakeLists.txt', 'line': 2, 'match': 'project('}, {'path': 'native/middleware/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/service/CMakeLists.txt', 'line': 1, 'match': 'add_library('}, {'path': 'native/tests/CMakeLists.txt', 'line': 6, 'match': 'add_executable('}]}；锁定 1。
  - 证据：`facts/FW-14.json#/compilation/external_build_closure`; `README.md:3`; `APP_BUILD:1`
- `compilation.api_version_management`：**3/3** — 专用语义版本证据=1，有效 API 检查=4；锁定 3。
  - 证据：`facts/FW-14.json#/api_version`; `native/CMakeLists.txt:2`; `car-builtin-lib/Android.bp:32`; `car-lib/Android.bp:105`
- `quality.integration_test`：**1/3** — 有效测试源=303；无执行证明不推断通过率，锁定 1。
  - 证据：`facts/FW-14.json#/integration_test/executable_test_sources`; `native/tests/update_manager_integration_test.cpp:5`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — 启动方法混合权限、参数验证、反射引擎、状态与通知。 监听者广播仍为同一服务内的独立方法。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-14.json#/current_review/solid/single_responsibility`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:19`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:55`
- `solid_principle.open_closed`：**2/4** — 权限策略允许通过构造扩展。 引擎类和无参构造在核心方法中硬编码。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-14.json#/current_review/solid/open_closed`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:18`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:51`
- `solid_principle.liskov_substitution`：**3/4** — 生产实现=2，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 3。
  - 证据：`facts/FW-14.json#/lsp_review`; `service/src/com/android/car/VehicleStub.java:38`; `service/src/com/android/car/AidlVehicleStub.java:64`; `service/src/com/android/car/HidlVehicleStub.java:44`
- `solid_principle.interface_segregation`：**2/4** — 更新控制、状态读取和监听注册仍汇聚于一个管理接口。 状态推送有独立 oneway 监听接口。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-14.json#/current_review/solid/interface_segregation`; `update-manager/src/com/cockpitbench/update/IUpdateManager.aidl:3`; `update-manager/src/com/cockpitbench/update/IUpdateStatusListener.aidl:2`
- `solid_principle.dependency_inversion`：**2/4** — PermissionGate 在构造函数注入。 服务自行反射构造具体 UpdateEngine。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-14.json#/current_review/solid/dependency_inversion`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:18`; `update-manager/src/com/cockpitbench/update/UpdateManagerService.java:51`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=69；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-14.json#/current_review/platform`; `car-builtin-lib/src/android/car/builtin/CarBuiltin.java:20`; `car-builtin-lib/src/android/car/builtin/app/VoiceInteractionHelper.java:24`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/2026.1']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`a7bea930370a`; `refs/heads/platform/8295`@`f4b18929661f`

### FW-15 `car-runtime-service` — 12/52

- `compilation.ci_independence`：**1/3** — 实际构建/测试/质量命令数=[0, 0, 0]，系统 CI 文件数=1；阶段覆盖范围以实际构建目标为准，锁定 1。
  - 证据：`facts/FW-15.json#/current_review/ci`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': False, 'external_dependencies_declared': False, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 4, 'match': 'Requires AAOS'}], 'standalone_target_anchors': []}；锁定 0。
  - 证据：`facts/FW-15.json#/compilation/external_build_closure`; `README.md:4`; `Android.bp:13`
- `compilation.api_version_management`：**0/3** — 专用语义版本证据=0，有效 API 检查=0；锁定 0。
  - 证据：`facts/FW-15.json#/api_version`
- `quality.integration_test`：**0/3** — 有效测试源=0；无执行证明不推断通过率，锁定 0。
  - 证据：`facts/FW-15.json#/integration_test/executable_test_sources`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**0/4** — 中央服务直接持有十八个互不相同业务域的 facade。 中央服务还混合系统属性权限判断和审计广播。 根据明确标注的语义裁决按合同锁定 0。
  - 证据：`facts/FW-15.json#/current_review/solid/single_responsibility`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:53`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:85`
- `solid_principle.open_closed`：**1/4** — 每增加业务域都需修改中央成员与具体构造。 业务调用按域逐个硬编码转发，不经通用注册/策略。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-15.json#/current_review/solid/open_closed`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:53`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:96`
- `solid_principle.liskov_substitution`：**2/4** — 生产实现=1，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 2。
  - 证据：`facts/FW-15.json#/lsp_review`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:3`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:48`
- `solid_principle.interface_segregation`：**0/4** — 单一 Binder 强迫气候和门窗等客户端依赖多个领域方法。 同一 Binder 又纳入车辆设置，客户端无窄接口选择。 根据明确标注的语义裁决按合同锁定 0。
  - 证据：`facts/FW-15.json#/current_review/solid/interface_segregation`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:4`; `runtime/src/com/cockpitbench/carruntime/ICarRuntime.aidl:55`
- `solid_principle.dependency_inversion`：**0/4** — 高层直接构造十八个具体业务依赖。 全局实例把使用者绑定到具体中央服务。 根据明确标注的语义裁决按合同锁定 0。
  - 证据：`facts/FW-15.json#/current_review/solid/dependency_inversion`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:53`; `runtime/src/com/cockpitbench/carruntime/CarRuntimeService.java:151`
- `platform_reuse.platform_upgrade`：**0/10** — 未隔离私有运行时导入=137；多处产品侧直接私有依赖=True；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 0。
  - 证据：`facts/FW-15.json#/current_review/platform`; `platform/src/com/cockpitbench/carruntime/platform/Sa8155VehicleBridge.java:19`; `platform/src/com/cockpitbench/carruntime/platform/Sa8295VehicleBridge.java:19`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/release/0.8']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`d2c21ebaf740`; `refs/heads/platform/8295`@`8ef2b0f2a5fb`

### FW-18 `vehicle-platform-service` — 21/52

- `compilation.ci_independence`：**1/3** — 实际构建/测试/质量命令数=[0, 0, 0]，系统 CI 文件数=1；阶段覆盖范围以实际构建目标为准，锁定 1。
  - 证据：`facts/FW-18.json#/current_review/ci`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': False, 'external_dependencies_declared': False, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [], 'standalone_target_anchors': []}；锁定 0。
  - 证据：`facts/FW-18.json#/compilation/external_build_closure`; `Android.bp:12`
- `compilation.api_version_management`：**1/3** — 专用语义版本证据=0，有效 API 检查=3；锁定 1。
  - 证据：`facts/FW-18.json#/api_version`; `apicheck.mk:147`; `apicheck.mk:155`
- `quality.integration_test`：**1/3** — 有效测试源=98；无执行证明不推断通过率，锁定 1。
  - 证据：`facts/FW-18.json#/integration_test/executable_test_sources`; `migration/aidl/tests/CarPropertyServiceUnitTest.java:96`
- `solid_principle.single_responsibility`：**1/4** — 协调器同时管理回调和审计集合。 同一协调器承担平台类型识别、创建和信号映射。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-18.json#/current_review/solid/single_responsibility`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:66`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:90`
- `solid_principle.open_closed`：**1/4** — 增加平台需修改 instanceof 分派。 还需同步修改 profile 创建分支。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-18.json#/current_review/solid/open_closed`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:90`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:96`
- `solid_principle.liskov_substitution`：**2/4** — 生产实现=1，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 2。
  - 证据：`facts/FW-18.json#/lsp_review`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:3`; `platform/src/com/cockpitbench/vehicleplatform/VehiclePlatformService.java:19`
- `solid_principle.interface_segregation`：**2/4** — 读取信号客户端同时依赖全局重连和清空等管理操作。 业务读取实现仅需要协调器读取能力。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-18.json#/current_review/solid/interface_segregation`; `platform/aidl/com/cockpitbench/vehicleplatform/IVehiclePlatform.aidl:4`; `platform/src/com/cockpitbench/vehicleplatform/VehiclePlatformService.java:22`
- `solid_principle.dependency_inversion`：**1/4** — Binder 服务取全局具体协调器。 协调器再取全局具体 Router 并创建 journal/fallback。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-18.json#/current_review/solid/dependency_inversion`; `platform/src/com/cockpitbench/vehicleplatform/VehiclePlatformService.java:20`; `platform/src/com/cockpitbench/vehicleplatform/PlatformSignalCoordinator.java:30`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=22；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-18.json#/current_review/platform`; `car-lib/src/android/car/media/CarAudioPatchHandle.java:24`; `car-lib/src/android/car/user/CarUserManagerHelper.java:29`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/platform/xinqing', 'refs/heads/release/sop-2019']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`1cd1c6a43839`; `refs/heads/platform/8295`@`bce6dc6fca9e`; `refs/heads/platform/xinqing`@`e4e968216af4`

### FW-16 `platform-compat-service` — 22/52

- `compilation.ci_independence`：**1/3** — 实际构建/测试/质量命令数=[0, 0, 0]，系统 CI 文件数=4；阶段覆盖范围以实际构建目标为准，锁定 1。
  - 证据：`facts/FW-16.json#/current_review/ci`
- `compilation.compilation_independence`：**0/3** — 仓外构建闭包={'requires_full_platform_source': True, 'has_meaningful_standalone_target': False, 'external_dependencies_declared': True, 'critical_dependencies_version_pinned': False, 'platform_requirement_anchors': [{'path': 'README.md', 'line': 5, 'match': 'requires an AAOS'}], 'standalone_target_anchors': []}；锁定 0。
  - 证据：`facts/FW-16.json#/compilation/external_build_closure`; `README.md:5`; `Android.bp:3`
- `compilation.api_version_management`：**1/3** — 专用语义版本证据=0，有效 API 检查=7；锁定 1。
  - 证据：`facts/FW-16.json#/api_version`; `car-builtin-lib/Android.bp:32`; `car-lib/Android.bp:105`
- `quality.integration_test`：**1/3** — 有效测试源=304；无执行证明不推断通过率，锁定 1。
  - 证据：`facts/FW-16.json#/integration_test/executable_test_sources`; `tests/BugReportApp/tests/src/com/android/car/bugreport/BugStorageUtilsTest.java:76`; `TEST_MAPPING:2`
- `solid_principle.single_responsibility`：**2/4** — 同一方法硬编码多个业务分派、写缓存和广播。 Binder 服务主要转发给 router/registry/callback 组件，已有职责拆分。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-16.json#/current_review/solid/single_responsibility`; `compat/src/com/cockpitbench/platformcompat/CompatibilityCommandRouter.java:22`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatService.java:23`
- `solid_principle.open_closed`：**1/4** — 新增业务域需修改 switch。 还需同步修改域枚举列表。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-16.json#/current_review/solid/open_closed`; `compat/src/com/cockpitbench/platformcompat/CompatibilityCommandRouter.java:22`; `compat/src/com/cockpitbench/platformcompat/CompatibilityCommandRouter.java:23`
- `solid_principle.liskov_substitution`：**2/4** — 生产实现=1，有效可复用替换测试=0；按父契约、实现关系和已核对的覆盖方法锁定 2。
  - 证据：`facts/FW-16.json#/lsp_review`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:3`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatService.java:19`
- `solid_principle.interface_segregation`：**2/4** — 通用调用、裸 Binder 查找和平台切换共享一接口。 裸服务查询和业务回调实现使用不同组件，说明可拆出窄接口。 根据明确标注的语义裁决按合同锁定 2。
  - 证据：`facts/FW-16.json#/current_review/solid/interface_segregation`; `compat/aidl/com/cockpitbench/platformcompat/IPlatformCompat.aidl:4`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatService.java:24`
- `solid_principle.dependency_inversion`：**1/4** — 高层集中获取全局 Registry 并创建具体 router/bridge/cache。 全局对象表加任意反射调用形成第二处不稳定依赖。 根据明确标注的语义裁决按合同锁定 1。
  - 证据：`facts/FW-16.json#/current_review/solid/dependency_inversion`; `compat/src/com/cockpitbench/platformcompat/PlatformCompatService.java:20`; `compat/src/com/cockpitbench/platformcompat/HiddenApiRegistry.java:20`
- `platform_reuse.platform_upgrade`：**3/10** — 未隔离私有运行时导入=78；多处产品侧直接私有依赖=False；SDK 分支集中于 API 兼容层，未发现闭源单 ABI 二进制，锁定 3。
  - 证据：`facts/FW-16.json#/current_review/platform`; `car-builtin-lib/src/android/car/builtin/CarBuiltin.java:20`; `car-builtin-lib/src/android/car/builtin/app/VoiceInteractionHelper.java:24`
- `platform_reuse.release_branch_strategy`：**8/10** — 实际配置/代码差异支持的分支=['refs/heads/platform/8155', 'refs/heads/platform/8295', 'refs/heads/platform/xinqing', 'refs/heads/release/sop-2025']；按车型/平台复用粒度锁定 8。
  - 证据：`refs/heads/platform/8155`@`93ccc6f80839`; `refs/heads/platform/8295`@`068b6972dc4b`; `refs/heads/platform/xinqing`@`a79b428ffc3e`
