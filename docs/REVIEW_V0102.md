# v0.10.2 审阅修复

本次关闭 v0.10.1 审阅中的六项评分、证据、输入和工具问题。另两项数据集建设问题仍开放：新增独立来源留出集、按真实业务画像补充缺失机制和组合。诊断工具改进不等于这两项已完成。

| 项目 | 处理 | 当前结果 |
|---|---|---|
| NEM-10 复用 | 完整采集子图仍保留独立编写的资格判定/回退/IIR副本；参数和实例状态差异不足以否定重复；能量模型引用只是局部正例 | reuse 2→1 |
| 档位召回 | 基础合法数值校验后归一整数档位；3、3.0、-0.0语义一致 | 三类准确率、召回与混淆一致 |
| NEM-10 数据流 | 父子索引修正并绑定模型路径；审阅实际长距离向上/向左组合逻辑路由，保留完整Branch坐标 | dataflow 3→2 |
| APP-22 必要输入 | 绑定实际 compileSdk 34 的完整SDK公开定义，保留原始Gitiles、解码文件、目录响应与中性绑定 | 分数3不变；source_only unknown，frozen_external supported |
| APP-13 解耦 | 审阅13个生产Java文件、单模块构建、契约调用、组合位置、共享存储和陀螺仪边界 | decoupling 2→3 |
| FW-14 执行绑定 | 报告内实际执行HEAD与当前HEAD分别保存，验证4生产文件+1构建入口+4测试源的Git blob/SHA不变 | 分数1不变；历史25项host测试沿用，不称当前HEAD新运行 |

APP为142/440（88叶），FW为194/572（121叶），新能源MATLAB为427/671（143叶），各11仓，三类不相加。相对v0.10.1仅三叶分值改变，另349分值保持。33源码HEAD/tree/refs和两个合同保持；原冻结Android根目录和原MATLAB参考对象未改。当前APP-13/FW-14采用显式修订记录，校验前后完整对象、受影响叶、合同、源版本及规则输入，未静默改写兼容入口。

NEM-10采集子图的可复算材料为[块、连接与完整分支坐标](https://github.com/cockpit-bench/cockpit-benchmark/blob/ac6ffa46096993853dc7871413a9efe008bec2ec/docs/review-v0102/NEM-10-acquisition.json)和[与ML-04的拓扑对照](https://github.com/cockpit-bench/cockpit-benchmark/blob/ac6ffa46096993853dc7871413a9efe008bec2ec/docs/review-v0102/NEM-10-comparison.json)。`simulink/systems/system_1.xml` 内AmbientC有效性块SID214到Substitution SID216保留`[315,0;0,-2782;-162,0;0,-383]`折返，输入SID408到SID216上行3250布局单位；这些是组合逻辑资格判定路径。命名完整不自动满足最高档流向要求。实际使用R2023b加载/制图作辅助审阅，没有新增update、MIL、coverage、codegen或设备验证。

APP-13在`DevCameraActivity.java:83`保存`CameraInterface`，后续业务通过该契约调用；239行是构造接线。更换符合原契约的相机实现无需改无关UI、传感器或存储行为。`MediaSaver`承接共享存储，`GyroOperations/GyroListener`封装传感器行为，`CameraInfoCache`保留在Camera2后端内部。没有把`new`或具体类型单独当作扣分证据，也没有声称单模块已形成独立构建组件。明确修订见[APP-13](../suites/app/revisions/APP-13-v0102.json)。

FW-14原始报告位于冻结`facts/FW-14.json#/structured/0`，实际执行HEAD为`d6300ac2d7c433d574efd9dbf7f595457ba99ee7`，当前HEAD为`8b4badff6b9e3b96f6cb3d1c9ccf624e4ef6d784`。[重绑定记录](../suites/fw/revisions/FW-14-execution-rebinding.json)对嵌入原报告使用规范JSON摘要；对当前证据文件使用其自身摘要，不再混填原始execution.json的文件SHA。九个输入在两版本间完全相同，只沿用这些生产/测试输入的历史host结果，不推断完整Car平台或Android集成。

APP-22使用AOSP prebuilts/sdk commit `9736a6d287252a7e7e8feb2a709aa9e10a3caea7`的`34/public/api/android.txt`；第20352行声明`@Deprecated public class Camera`。完整API的Git blob为`ff242876fb37728684d25b487cd89f5eefa396ee`。原始响应解码、Git blob、目录返回、SHA、仓HEAD和compileSdk共同验证；候选仅导出该仓的四个SDK输入文件，不获得维护者结论或其他仓材料。

当前输入分母、导出命令和统计边界见[当前评测](CURRENT_EVALUATION.md)。无样本的合法档位输出`count=0, recall=null, measurement_status=unmeasured`，避免从表中消失或被误报为0%/100%。批次和评分结果携带来源闭包、常量叶、缺档及事后关联诊断。所有诊断仍是同一公开开发集的描述；不能代替候选实验或证据语义审查。

恢复兼容补修：旧恢复进度摘要包含可变证据元数据，导致源码未改也无法跨修订`-Resume`。现在只绑定恢复所需源身份、HEAD/tree/refs和目的地址；旧已完成标记必须先通过实际完整历史、HEAD/tree/refs、clean、remote=0和无alternates核验，才能重绑定。未知未完成克隆继续拒绝，用户源码修改不会被覆盖。PowerShell执行主体未改，只更新冻结文件表。

## 尚未关闭的建设项

当前来源总闭包仍18组，其中全部11个新能源样本位于同一组。其独立留出状态明确为`structurally_unavailable`；APP/FW各自存在10个来源组，但多组也不自动证明无构造暴露或独立裁决，状态为`not_certified`。

档位格覆盖仍为APP 23/32、FW 29/49、新能源40/52；当前逐叶众数为58/88、86/121、78/143。全部Android发布策略为0，全部新能源构建独立性为3；新能源发布分支、设备特有和版本独立三个变量仍样本内一一对应。完整缺档和关联可由[机器可读诊断](population-diagnostics.json)重算。

已核查现有独立素材MathWorks traction e-motor工程（`be4847eca805905bba4088bd9f334a2b1c0a8a5d`）：上游为R2026a，当前R2023b实际加载`CalculateTorqueLimits`和`TractionEmotorSoftwareArch_DataBus`均返回`Simulink:Commands:LoadingNewerModel`，未更新、仿真或准入。MiniBMS已参与NEM-11构造，不能重标为未见来源。现有内部材料仍只有指导汇总，缺逐仓原始扫描及预留来源。

完成这两项还需要未参与当前构造/调参且可运行的业务来源，以及其业务/依赖/接口/配置组合依据。可从兼容模型导出或具备对应工具链的独立来源开始；在实际行为、谱系、逐叶证据和独立预留条件验证前，不新增正式仓、不补造分值、不放松来源闭包。此版本未把公众已见素材包装为盲留出集，未触及旧22个pending槽位。

## 验证范围

本版本的自动检查覆盖数值等价、缺档输出、必要输入、单仓导出、SDK字节和Git blob、显式参考修订、源证据、旧执行重绑定、父子模型交换负例、完整路由以及诊断再生成；扩建64叶规则重算与源库存双遍保持一致。完整回执记录精确测试数、公开附件SHA和匿名恢复核验范围。

本轮没有新增Android构建/模拟器/物理设备执行，没有新增MATLAB仿真或覆盖。除上述加载/制图及独立素材加载失败外，原生执行仍只沿用已绑定记录；源码历史未改，不把重复hash检查称为独立盲语义评审。
