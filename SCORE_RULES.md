# APP / Android Framework 现行评分合同（Benchmark 版）

版本：2026-09-03-v2  
用途：为座舱 Android APP 与 Android Framework benchmark 生成逐叶标准分。  
纪律：本文件是唯一评分事实源；allowlist 之外的维度必须丢弃，不得从旧 rubric 换算或补零。

## 0. 通用规则

1. 每个分数必须绑定 final HEAD，并落到具体文件、行号、符号或真实 Git ref。
2. 先提取事实，后评分；同一维度共享同一份不可变事实，禁止为了目标档修改事实。
3. 不读取仓库名中的质量暗示、quality tier、目标矩阵或旧标准分来推导答案。
4. 无数据或无法评估时标记 `failed`，不得编造分数。
5. 分档按本文指定顺序判定；“任意 N 条”达到即锁档。
6. 注释、字符串、日志、测试 Mock、生成代码中的探针命中不算生产证据。
7. 被测 Agent 每次只能看到一个源码仓；wrapper、oracle、facts、SCORECARD 和标准分不得进入评测输入。

## 1. 维度总表

### 1.1 APP：8 叶，每仓 40 分

| canonical leaf | 满分 |
|---|---:|
| `architecture.componentization` | 5 |
| `architecture.decoupling` | 3 |
| `architecture.modularization` | 3 |
| `compilation.ci_independence` | 3 |
| `compilation.compilation_independence` | 3 |
| `compilation.api_version_management` | 3 |
| `platform_reuse.platform_upgrade` | 10 |
| `platform_reuse.release_branch_strategy` | 10 |

APP 的 `integration_test` 走 GBOP，不属于本 benchmark 的 LLM 标准分范围。

### 1.2 Android Framework：11 叶，每仓 52 分

| canonical leaf | 满分 |
|---|---:|
| `compilation.ci_independence` | 3 |
| `compilation.compilation_independence` | 3 |
| `compilation.api_version_management` | 3 |
| `quality.integration_test` | 3 |
| `solid_principle.single_responsibility` | 4 |
| `solid_principle.open_closed` | 4 |
| `solid_principle.liskov_substitution` | 4 |
| `solid_principle.interface_segregation` | 4 |
| `solid_principle.dependency_inversion` | 4 |
| `platform_reuse.platform_upgrade` | 10 |
| `platform_reuse.release_branch_strategy` | 10 |

FW 在评估引擎侧为 7 个 Agent；SOLID 一次调用产出 /20，但 benchmark 必须保留 5 个 /4 子叶。旧 architecture、embedded platform_coupling、RTOS/QNX/MCU integration-test 等叶全部作废。

## 2. APP 评分规则

### 2.1 架构共享事实

- `module_count`：业务/基础/app 模块数；排除 test、androidTest、buildSrc、build-logic。
- `standard_named_module_count`：小写加连字符/下划线，且含 base/core/common/util/widget/app/main/library/sdk/feature/biz/module 关键字的模块数。
- `has_layered_directory`：存在 UI（ui/view/presentation/page）、领域（domain/usecase/interactor/business/logic）或数据（data/repository/remote/local/network/database）职责目录。
- `has_file_type_packages`：仅 activity/fragment/adapter/utils/helper/constant/widget 等文件类型目录；不等于职责分层。
- `has_base_layered_architecture`：UI 与领域层同时存在。
- `layered_business_module_count`：包含职责分层目录的业务模块数。
- `has_business_packages`：存在业务分包结构。
- `code_not_in_root_package`：生产代码不直接堆在根包。
- `has_circular_dependency`：模块依赖图存在环。
- `is_component_friendly`：以下五项任意至少三项为真：无模块环、业务边界隔离且无跨模块源码侵入、公共能力下沉 base/core、模块可独立编译、无跨模块硬编码依赖。

三个架构叶必须使用同一组上述事实。

### 2.2 `architecture.componentization`（0/1/3/5）

- 5：以下任意两项：base layered；module_count≥2；standard_named_module_count≥2；至少两个业务模块有职责分层；component-friendly。
- 3：以下任意两项：base layered；module_count≥2；standard_named_module_count≥1；存在业务分包。
- 1：以下任意一项：有分层目录；仅文件类型分包；代码不在根包。
- 0：均不满足。

### 2.3 `architecture.decoupling`（0/1/2/3）

- 3：高级条件同 2.2 的 5 分档，任意两项。
- 2：中级条件同 2.2 的 3 分档，任意两项。
- 1：基础条件同 2.2 的 1 分档，任意一项。
- 0：均不满足。

### 2.4 `architecture.modularization`（0/1/2/3）

先判 `has_circular_dependency=true`，直接 0；否则档位与 2.3 相同。

### 2.5 `compilation.ci_independence`（0–3）

检查 `.github/workflows/`、`.gitlab-ci.yml`、`Jenkinsfile`、`azure-pipelines.yml`、`APP_BUILD`、`PREUPLOAD.cfg`、`TEST_MAPPING`：

- 0：无有效 CI。
- 1：仅依赖 Android 系统层 CI。
- 2：有独立 CI，但不是完整标准流水线。
- 3：完整标准化流水线，至少有真实构建、测试和质量/报告阶段；步骤必须可执行，不能只有名称或空命令。

### 2.6 `compilation.compilation_independence`（0–3）

从构建配置按最强约束优先判定：

- 0：模块通过 `implementation project(...)`、Soong 源码模块或其他方式直接编译依赖源码。
- 1：依赖 `framework.jar`。
- 2：依赖 SDK/AAR。
- 3：依赖带版本管理和稳定兼容承诺的 SDK。

源码依赖存在时优先锁 0，不能被同时存在的版本化第三方依赖抬分。

### 2.7 `compilation.api_version_management`（0–3）

- 0：无版本管理。
- 1：只有手动版本号，无控制机制或语义化策略。
- 2：使用语义化版本管理。
- 3：版本可控，并存在真实前后兼容保证/基线检查。

版本证据包括专用版本文件、构建集成、API baseline、兼容性任务和发布说明；Git tag 或 CHANGELOG 标题不能单独证明版本可控。

### 2.8 `platform_reuse.platform_upgrade`（10/8/3/0）

只扫描生产 `src/main/java|kotlin|cpp|res`、生产 Manifest、模块 build.gradle/CMake；排除 test/androidTest/build/generated/third_party。先提取唯一七事实：

1. `has_non_compatible_api`：@hide、系统类反射、移除/废弃 API、厂商私有 API。
2. `has_arch_specific_deps`：只支持单一 ABI 的闭源 SO，且无 fallback/多 ABI。
3. `version_bound_status`：0 无业务绑定或仅标准注解；1 统一兼容层；2 两至三个业务模块硬编码 SDK 分支；3 核心链路深度绑定。
4. `arch_bound_status`：0 无绑定/多 ABI；1 单模块加载且有 fallback；2 两至三个模块无统一抽象；3 单架构闭源 SO 或核心强绑定。
5. `has_interface_abstraction`：平台差异由接口/抽象类/策略隔离。
6. `has_light_permission_adaptation`：只需 Manifest 轻量权限适配。
7. `has_complex_permission_adaptation`：高版本需修改蓝牙/存储/位置/通知等运行时逻辑。

兼容层/接口抽象覆盖的 version/arch 绑定状态强制≤1。令 `total=version_bound_status+arch_bound_status`，严格按 10→8→3→0 判定并在首个满足档锁定：

- 10，以下任意两项：无非兼容 API 且无架构专属依赖；total≤1；有接口抽象；无复杂权限适配。
- 8，以下任意两项：无非兼容 API 且无架构专属依赖；total≤3；有轻量权限适配；有接口抽象。
- 3，以下任意一项：无非兼容 API 或无架构专属依赖；total≤4；有轻量权限适配；有接口抽象。
- 0，未命中更高档且出现非兼容 API、单架构闭源依赖、total≥5，或硬编码权限逻辑导致核心功能无法兼容。

### 2.9 `platform_reuse.release_branch_strategy`（10/8/3/0）

读取真实本地 heads/tags、同版本 SOP 数量、分支实际差异和命名后判定：

- 0：无明确 release 分支策略。
- 3：单车型单 SOP，车型拆分最细。
- 8：同平台同一分支，平台内车型共用。
- 10：跨平台统一主干/无后缀统一分支；现实中极少。

有 main 不自动等于 10；存在平台或车型分支时必须按更细粒度事实判定。

## 3. Android Framework 评分规则

### 3.1 适用对象与类型门禁

FW 必须是座舱 Android Framework 层仓库，以 Java/Kotlin/AIDL/Soong 或 Gradle 为主，可含 JNI/native C/C++。典型职责包括 CarService、Manager/Service、VehicleProperty、HAL Java 适配、Binder/AIDL、系统权限、系统服务、平台兼容与 SDK 接口。

若仓库主要是 MCU、裸机、RTOS、QNX、寄存器/中断驱动，或只有 native 中间件而无 Android Framework 语义，则类型门禁失败，必须重做或替换后才能评分。不得使用 architecture 或 embedded platform_coupling 旧叶。

### 3.2 `compilation.ci_independence`（0–3）

事实与档位同 APP 2.5。3 分流水线应包含多阶段构建、测试、质量检查/报告；Android 系统 `PREUPLOAD.cfg`/`TEST_MAPPING` 单独存在只能得 1。

### 3.3 `compilation.compilation_independence`（0–3）

检查 Gradle/POM/Soong 构建、模块依赖方式和 SDK 边界：

- 0：直接源码依赖，例如 `implementation project(...)` 或直接编译同仓/平台源码模块。
- 1：依赖 `framework.jar`。
- 2：依赖 SDK/AAR。
- 3：依赖带版本管理和兼容机制的稳定 SDK。

按实际依赖链的最强约束锁档；不能把 `compileSdk` 本身当成稳定 SDK。

### 3.4 `compilation.api_version_management`（0–3）

- 0：无版本管理。
- 1：有手工版本，但不可控、非语义化或无精确匹配。
- 2：语义化版本管理。
- 3：完善的版本控制机制，同时存在真实向后兼容保证或 API baseline 验证。

检查 version.properties、构建集成、API/current.txt、兼容任务、CHANGELOG/RELEASE_NOTES；标签或说明文件不能单独抬分。

### 3.5 `quality.integration_test`（0–3）

先提取：JUnit4/5、androidx.test、Robolectric、Instrumentation、native gtest/gmock；测试目录和 Soong/Gradle/AndroidTest.xml 配置；真实断言；跨模块/跨组件交互；执行结果；覆盖率或覆盖代理事实。

- 0：没有集成测试，或只有空测试、无断言、恒过/恒跳过用例。
- 1：存在测试框架引用和有效真实断言，方法正确；至少能验证真实接口行为。
- 2：目标明确、预期合理、大部分通过，关键模块交互覆盖率或经定义的覆盖代理≥50%。
- 3：满足 2 分全部条件且绑定 final HEAD 的执行通过率为 100%。

不得仅凭测试文件数量给 2/3；没有可复现执行结果时不能声称 100% 通过。

### 3.6 SOLID 五原则（各 0–4，共 20）

五个叶必须分别评分并分别给出 `score_reasoning`、`analysis`、具体代码证据、`issues`、`recommendations`：

- `solid_principle.single_responsibility`：上帝类、职责混杂、类/模块变更原因。
- `solid_principle.open_closed`：扩展点、策略/注册机制、是否每次扩展都修改核心分支。
- `solid_principle.liskov_substitution`：继承契约、替换正确性、空实现/抛异常/收紧前置条件。
- `solid_principle.interface_segregation`：胖接口、无关方法依赖、客户端是否被迫依赖不用的能力。
- `solid_principle.dependency_inversion`：高层是否依赖抽象；静态全局状态、反射加载具体类、硬编码实现属于违反信号。

每个原则独立采用同一档位：

- 0：严重违反，存在明显设计缺陷。
- 1：多处违反，设计不合理。
- 2：基本遵循，仍有少量改进空间。
- 3：良好遵循，符合汽车领域可靠性/可维护性规范。
- 4：优秀遵循，体现汽车领域优秀实践。

LSP 无继承/替换证据时不得凭空给高分；按 `failed` 处理，或在仓库设计中提供真实可判断的继承契约。低质量样本仍须可构建/可解析，不能用语法错误制造低分。

### 3.7 `platform_reuse.platform_upgrade`（10/8/3/0）

使用 APP 2.8 完全相同的 Android 七事实、负向过滤、豁免规则和 10→8→3→0 锁档流程。FW 重点检查系统服务启动链、Manager/Service、Binder/AIDL、HAL Java 适配、权限与 JNI/ABI；不得出现 RTOS/BSP/寄存器评分语义。

### 3.8 `platform_reuse.release_branch_strategy`（10/8/3/0）

使用 APP 2.9 相同的真实 Git 分支通用性口径。分支名只是入口，必须验证分支 tip/树确有相应平台或车型差异。

## 4. 标准分输出与验收

每个叶必须输出：

- `name`、`score`、`max_score`、`status`
- `score_reasoning`
- `analysis`
- 至少一个可定位证据；需要判断的叶原则上至少两个独立锚点
- SOLID 额外输出 `issues`、`recommendations`

计数：

- 9 APP：72 叶，满分 360。
- 9 FW：99 叶，满分 468。
- Validation-18：171 叶，满分 828。

发布前必须完成：

1. final HEAD 重新取证；
2. 第二遍逐叶证据复核；
3. 不读取 quality tier/目标矩阵的独立重算，与 canonical 逐叶零差异；
4. 相同 HEAD 重复提取事实，完整输出哈希一致；
5. wrapper/manifest/oracle/SCORECARD/refs/restore 相互一致。
