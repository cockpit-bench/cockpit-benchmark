# APP / Android Framework 现行评分合同（Benchmark 版）

版本：2026-09-04-v3.3  
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
8. 证据必须证明该叶的具体判断：结构化事实使用 JSON Pointer，代码使用真实行段与符号，Git 分支使用 ref 对应的真实 tip/tree。`file:1`、泛化的“reviewed code evidence”或同一锚点重复两次不算独立证据。
9. 本公开 Validation-18 定位为 Dev/Regression benchmark；它不等同于私有、谱系隔离的最终 Holdout。源码仓名称和描述不得直接暴露 high/medium/low 标签。

### 0.1 可复现体量分层

只统计 final HEAD 中的生产源码；排除 `.git`、构建产物、生成代码、vendored/third_party 依赖、二进制、测试和资源文件。`source_files` 与 `source_loc` 必须同时落入同一档：

- APP small：`source_files < 300` 且 `source_loc < 30,000`；medium：`300–999` 且 `30,000–79,999`；large：`source_files >= 1,000` 且 `source_loc >= 80,000`。
- FW small：`250–599` 且 `30,000–79,999`；medium：`600–1,499` 且 `80,000–199,999`；large：`source_files >= 1,500` 且 `source_loc >= 200,000`。
- 两个指标跨档或未达到 FW small 下限时标记 `size_band=unresolved`，不得按目标矩阵强贴标签。

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

三个架构叶必须使用同一组上述事实，但分别衡量不同构念，不能把同一“任意 N 条”结果换量程重复三次：组件化看可复用/可替换组件，解耦看依赖方向与修改传播，模块化看构建模块边界与内聚。

为避免只换术语不换测量，Gold 必须另外物化三组互不替代的决定性事实：

- componentization：`reusable_component_count`、`replaceable_component_count`、`shared_capability_owner_count`、`explicit_public_contract_count`；其中显式契约必须声明可调用方法或可替换属性，`@interface`、纯常量容器、枚举和无行为 marker interface 不计组件契约；
- decoupling：`reverse_dependency_edge_count`、`cross_module_source_intrusion_count`、`concrete_implementation_edge_count`、`dependency_cycle_count`、`platform_change_propagation_module_count`；
- modularization：`real_build_module_count`、`cohesive_module_count`、`module_test_entry_count`、`api_dependency_edge_count`、`implementation_dependency_edge_count`、`dependency_scc_count`。

Gradle Kotlin 构建脚本（`build.gradle.kts`、`settings.gradle.kts`）不是生产 Kotlin 源码，不得据此制造未归属源码或边界失败事实。

### 2.2 `architecture.componentization`（0/1/3/5）

- 5：存在至少两个有独立构建入口、职责边界明确的业务/公共组件，并且公共能力已下沉 base/core 或由显式接口边界复用；仅目录命名或模块数量不够。
- 3：存在至少两个真实构建模块且有业务分包，但复用、替换或公共能力边界不完整。
- 1：只有包级分层/文件类型分包，或代码虽不在根包但没有真实组件边界。
- 0：生产代码基本为单体根包，未形成可识别组件。

### 2.3 `architecture.decoupling`（0/1/2/3）

- 3：无模块环、无跨模块源码目录侵入，依赖方向稳定，公共能力下沉或通过接口/依赖注入隔离；修改一个平台/业务实现不要求修改多个无关模块。
- 2：无模块环且主要边界可识别，但存在跨模块源码侵入、反向依赖、硬编码具体实现或公共能力未下沉中的一类问题。
- 1：虽有包/模块划分，但多处直接跨边界引用、硬编码或修改传播明显。
- 0：存在模块环，或核心模块彼此强耦合到无法形成稳定依赖方向。

### 2.4 `architecture.modularization`（0/1/2/3）

- 3：无模块环，至少三个职责内聚的真实构建模块，至少两个规范命名模块，并具有模块级构建/测试入口或清晰 API/implementation 边界。
- 2：无模块环且至少两个真实构建模块，模块职责基本可辨，但独立测试/发布或 API 边界不完整。
- 1：只有包级分层，或名义模块缺少独立构建边界。
- 0：单体无模块结构，或存在模块循环依赖（一票否决）。

### 2.5 `compilation.ci_independence`（0–3）

检查 `.github/workflows/`、`.gitlab-ci.yml`、`Jenkinsfile`、`azure-pipelines.yml`、`APP_BUILD`、`PREUPLOAD.cfg`、`TEST_MAPPING`：

- 0：无有效 CI。
- 1：仅依赖 Android 系统层 CI。
- 2：有独立 CI，但不是完整标准流水线。
- 3：完整标准化流水线，至少有真实构建、测试和质量/报告阶段；步骤必须可执行，不能只有名称或空命令。

### 2.6 `compilation.compilation_independence`（0–3）

评分对象是“仓库外部构建闭包”，同仓 `implementation project(...)` 或 Soong 模块依赖属于正常模块化，不再自动扣到 0。按最强外部约束判定：

- 0：必须依赖完整 Android 平台源码树、未随仓声明的 sibling repository 或仓外源码，且当前仓不能独立构建任何有意义的生产单元。
- 1：可局部构建有意义单元，但完整构建依赖未版本化的 `framework.jar`、私有 stubs、平台环境注入或未锁定预编译物。
- 2：仓内源码模块闭包完整，仓外依赖均通过明确 SDK/AAR/JAR/stub/Maven 或预构建接口获得，并有可重复的模块级构建入口。
- 3：满足 2，且关键跨仓 SDK/API 全部版本锁定，具有真实兼容性检查/承诺，构建环境可重复或近似 hermetic。

`compileSdk`、`sdk_version` 或普通第三方依赖版本本身不能证明 2/3；必须结合完整依赖链和实际构建入口。

### 2.7 `compilation.api_version_management`（0–3）

- 0：无版本管理。
- 1：只有手动版本号，无控制机制或语义化策略。
- 2：使用语义化版本管理。
- 3：版本可控，并存在真实前后兼容保证/基线检查。

版本证据包括专用版本文件、构建集成、API baseline、兼容性任务和发布说明；Git tag 或 CHANGELOG 标题不能单独证明版本可控。

下列内容不得计为 API 兼容性证据：`sourceCompatibility`、`targetCompatibility`、`compileSdk`、`minSdk`、普通版本号文件、只检查 baseline 文件存在/包含固定字符串的任务。3 分必须能从当前公开 API 提取结果与已发布 baseline 做真实 diff，识别删除、签名或可见性变化，或使用等价的 metalava/checkapi/ABI 检查。

只把当前 descriptor 与一个固定哈希做全等比较、运行时版本协商或 `MIN_COMPATIBLE_MAJOR` 策略声明，也不能替代公开 API/ABI 的兼容性 diff。

### 2.8 `platform_reuse.platform_upgrade`（10/8/3/0）

只扫描生产 `src/main/java|kotlin|cpp|res`、生产 Manifest、模块 build.gradle/CMake；排除 test/androidTest/build/generated/third_party。先提取唯一七事实：

1. `has_non_compatible_api`：@hide、系统类反射、移除/废弃 API、厂商私有 API。
2. `has_arch_specific_deps`：只支持单一 ABI 的闭源 SO，且无 fallback/多 ABI。
3. `version_bound_status`：0 无业务绑定或仅标准注解；1 统一兼容层；2 两至三个业务模块硬编码 SDK 分支；3 核心链路深度绑定。
4. `arch_bound_status`：0 无绑定/多 ABI；1 单模块加载且有 fallback；2 两至三个模块无统一抽象；3 单架构闭源 SO 或核心强绑定。
5. `has_interface_abstraction`：平台差异由接口/抽象类/策略隔离；同时记录非兼容 API 是否全部被该抽象覆盖以及未覆盖数量。
6. `has_light_permission_adaptation`：只需 Manifest 轻量权限适配。
7. `has_complex_permission_adaptation`：高版本需修改蓝牙/存储/位置/通知等运行时逻辑。

兼容层/接口抽象只有在证据证明覆盖相应风险时，才能把对应 version/arch 绑定状态计为≤1；仓库里“存在某个 Adapter”不能抵消其他未封装风险。单纯创建或读取 `NotificationChannel` 不构成复杂权限适配，除非同时存在运行时请求/检查、版本化权限分支或等价行为变更。令 `total=version_bound_status+arch_bound_status`，采用风险单调的硬门槛：

- 10：无未封装非兼容 API、无单架构专属依赖、total≤1，并且存在明确接口隔离或至少两个 Android 平台版本的自动兼容验证。
- 8：风险集中在可定位 adapter/compat 层并有 fallback，或虽无非兼容/架构风险但缺少 10 分所需的接口隔离/跨版本自动验证；total≤3。
- 3：存在未封装 vendor/private/reflection API、两至三个业务模块的平台硬编码、复杂权限适配或无统一抽象，但仍有可行迁移路径；该类负向事实对分数封顶为 3。
- 0：单架构闭源依赖无 fallback、核心链路深度绑定（total≥5）、多处绕过稳定接口且无隔离，或权限/平台硬编码使核心功能无法迁移。

正常使用公开 Android Framework API 不属于非兼容 API；vendor private、`@hide`、系统类反射属于。已集中封装且有降级方案的非公开 API 最高 8，未封装则最高 3。

### 2.9 `platform_reuse.release_branch_strategy`（10/8/3/0）

读取真实本地 heads/tags、同版本 SOP 数量、分支实际差异和命名后判定：

- 0：无明确 release 分支策略。
- 3：存在可由 ref 名和真实差异共同证明的“单车型单 SOP”专用通道，车型拆分最细；ref 必须含车型身份（如 `model-a1`），仅有年份/版本型 `release/sop-2025` 或 `sop/2025` 不足以得到 3 分。
- 8：同平台同一分支，平台内车型共用。
- 10：跨平台统一主干/无后缀统一分支；现实中极少。

有 main 不自动等于 10；存在平台或车型分支时必须按更细粒度事实判定。通用 SOP 发布线可以与平台共用分支并存：当 SOP ref 不含车型身份、而真实 `platform/*` ref 存在时，按平台复用事实判 8，不得仅因 ref 名含 `sop` 降为 3。

## 3. Android Framework 评分规则

### 3.1 适用对象与类型门禁

FW 必须是座舱 Android Framework 层仓库，以 Java/Kotlin/AIDL/Soong 或 Gradle 为主，可含 JNI/native C/C++。典型职责包括 CarService、Manager/Service、VehicleProperty、HAL Java 适配、Binder/AIDL、系统权限、系统服务、平台兼容与 SDK 接口。

若仓库主要是 MCU、裸机、RTOS、QNX、寄存器/中断驱动，或只有 native 中间件而无 Android Framework 语义，则类型门禁失败，必须重做或替换后才能评分。不得使用 architecture 或 embedded platform_coupling 旧叶。

### 3.2 `compilation.ci_independence`（0–3）

事实与档位同 APP 2.5。3 分流水线应包含多阶段构建、测试、质量检查/报告；Android 系统 `PREUPLOAD.cfg`/`TEST_MAPPING` 单独存在只能得 1。

### 3.3 `compilation.compilation_independence`（0–3）

使用 APP 2.6 相同的“仓库外部构建闭包”定义。Android Soong 同仓模块依赖不自动判 0；只有确实需要仓外平台源码且无任何有意义独立构建单元才是 0。Framework 正常依赖公开 Android SDK/stub 与依赖私有 `framework.jar`/整棵平台树必须区分。

### 3.4 `compilation.api_version_management`（0–3）

- 0：无版本管理。
- 1：有手工版本，但不可控、非语义化或无精确匹配。
- 2：语义化版本管理。
- 3：完善的版本控制机制，同时存在真实向后兼容保证或 API baseline 验证。

检查 version.properties、构建集成、API/current.txt、兼容任务、CHANGELOG/RELEASE_NOTES；标签或说明文件不能单独抬分。

APP 2.7 的兼容性证据排除项同样适用。AOSP 源码中普通注释里的 `released`/`compatibility`、Java 语言级别和任意三段数字都不是 API 版本管理证据。

### 3.5 `quality.integration_test`（0–3）

先提取：JUnit4/5、androidx.test、Robolectric、Instrumentation、native gtest/gmock；测试目录和 Soong/Gradle/AndroidTest.xml 配置；真实断言；跨模块/跨组件交互；执行结果；覆盖率或覆盖代理事实。

- 0：没有集成测试，或只有空测试、无断言、恒过/恒跳过用例。
- 1：存在测试框架引用和有效真实断言，方法正确；至少能验证真实接口行为。
- 2：目标明确、预期合理、大部分通过，关键模块交互覆盖率或经定义的覆盖代理≥50%。
- 3：满足 2 分全部条件且绑定 final HEAD 的执行通过率为 100%。

不得仅凭测试文件或断言数量给 2/3；没有绑定 final HEAD 的可复现执行结果时，最高 1 分，不得声称“大部分通过”或“100% 通过”。

执行事实必须区分本地提取器执行与远程 CI 执行。CI 证明至少固化 provider、run ID/URL、final HEAD SHA、workflow path 及其 Git blob/SHA-256、job 结论、测试命令、通过/失败数、覆盖范围与门槛；若有 JUnit/coverage artifact，同时固化摘要和 digest。不能把 native 子目录覆盖率表述为整仓覆盖率。

2 分所用的“覆盖代理”必须可复算：显式记录代理名称、定义、范围、分子、分母、数值及被覆盖/全部关键跨模块交互边。空字段、测试文件数、断言数不是覆盖代理。

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

LSP 无可判断的父子/实现契约时为 `failed`；存在契约时按以下可观察门槛裁决：

- 0：子类/实现有空覆写、无条件抛错、收紧前置条件或破坏后置条件等明确替换违反。
- 1：可识别契约，但有多处未解释覆写/异常语义风险，替换可靠性差。
- 2：至少一个真实生产实现，关键 override 经核对且无明显违反，但没有第二个生产实现或可复用 contract/substitution test。
- 3：至少两个真实生产实现均保持父契约，或至少一个生产实现通过可复用 contract/substitution test。
- 4：多个生产实现均通过系统化 contract/substitution test，并显式覆盖异常、边界、前置和后置语义。

LSP 事实至少记录 `parent_symbol`、`child_symbols`、继承/实现关系、关键 `overridden_methods`、空覆写/无条件抛错/前后置风险计数、生产实现数与 substitution test 数。低质量样本仍须可构建/可解析，不能用语法错误制造低分。

### 3.7 `platform_reuse.platform_upgrade`（10/8/3/0）

使用 APP 2.8 完全相同的 Android 七事实和风险单调硬门槛。FW 重点检查系统服务启动链、Manager/Service、Binder/AIDL、HAL Java 适配、权限与 JNI/ABI；公开 Framework API 的正常使用不扣分，vendor private/reflection/hidden API 是否隔离和降级才决定封顶；不得出现 RTOS/BSP/寄存器评分语义。

### 3.8 `platform_reuse.release_branch_strategy`（10/8/3/0）

使用 APP 2.9 相同的真实 Git 分支通用性口径。分支名只是入口，必须验证分支 tip/树确有相应平台或车型差异。

## 4. 标准分输出与验收

每个叶必须输出：

- `name`、`score`、`max_score`、`status`
- `score_reasoning`
- `analysis`
- 至少一个可定位证据；需要判断的叶原则上至少两个独立锚点
- SOLID 额外输出 `issues`、`recommendations`

证据对象至少包含 `source`、`path`、`commit`、`claim`、`evidence_type`、`independent_group`，并按类型补充：

- 代码：`start_line`、`end_line`、真实 `symbol`；行段必须直接支持 claim。
- 结构化 facts：`json_pointer`，不得用第 1 行代表整份文件。
- Git ref：`ref`、`commit_oid`、`tree_oid`；`commit_oid` 必须等于该 ref 实际 tip，并与 manifest/facts 一致。

需要判断的叶至少两个不同 `independent_group`；纯粹的确定性缺失/计数事实允许一个结构化锚点。Schema、合同 hash 和字段必须在同一 release 的全部 18 个 oracle 中完全一致。

证据生成器必须校验 `symbol` 确实出现在给定行段，且该行段的语义直接支持 claim。集成测试的源码证据必须指向真实 `@Test`/`TEST(...)` 用例及其断言，helper、Binder wrapper、`@TestApi` 注解和类名含 `Test` 均不能代替测试方法证据。

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
