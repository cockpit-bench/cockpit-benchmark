# v0.9.4 MAP仲裁与合同解释

FW-03 OCP 1→2；候选可见合同经用户同意升为v3.5.1。见[场景与源码依据](MAP_OCP_ARBITRATION_V094.md)。

Android259/828、MATLAB338/549；另170完整叶及27源码HEAD/refs不变。v0.9.3五项修复保持关闭。扩建由独立任务先规划，本轮无新样本或运行。

以下为历史版本记录；以当前标准分与同版本合同为准。

---

# v0.9.3 五项修复完成

三个SOLID边界已按统一尺度裁定，另修复当前基线与FW-15 LSP措辞。见[横向仲裁](HORIZONTAL_ARBITRATION_V093.md)。

Android258/828、MATLAB338/549；167个其他完整Android叶对象、27源码HEAD/refs及合同不变。本轮未新增Android/MATLAB执行或候选模型实验。扩展候选正式入库按用户决定单独推进。

以下为历史版本记录，其分数与措辞由当前标准分及本轮仲裁覆盖。

---

# Pro 审阅修复进度 — v0.9.2

剩余 20 个非 LSP SOLID 叶已按真实源码职责/消费者完成本轮校准；与此前 16 叶构成两批 36 叶记录，完整旧页保持历史。另复核 APP-14 编译独立性；本轮数值变化 12 叶，Android 255/828。见 [本轮裁决](SOLID_CALIBRATION_V092.md) 与 [编译证据](compilation-calibration-v092.json)。

ML-09 补充数值比较/失败分支源码锚点，分数与 MATLAB 原附件不变。此次标准答案校准没有重新构建 27 个冻结源码仓，也没有候选模型评测；独立扩展候选正在本地建设，不计入现有标准答案、档位覆盖或独立 holdout。合同业务决定仍待用户确认。

以下保留 v0.9.1 的当时进度，不能将其“另外 20 个未重审”解读为本轮当前状态。

---

# Pro 审阅修复进度 — v0.9.1

已完成本轮直接事实和工具修复：固定模式/可比集合/来源族切分的评测入口；逐组分布和同分母众数基线；单独的人工证据有效性统计；16 个非 LSP SOLID 叶的源码范围与相邻档校准，其中两项修分由第二 Agent 独立上下文复核；MATLAB 当前有效合同合成；FW-07 的中性外部 Git 原始输入包。

这不是全部审阅建议完成的声明。正式集 release、upgrade、FW 构建/CI/集成正向覆盖，以及 MATLAB 实际复用/外部业务依赖样本仍需后续源码建设和真实执行。这类工作会改变样本与取证 HEAD；本轮未以同源小例子或文本声明替代。36 个非 LSP 叶中另外 20 个未声称本轮重审。

模块命名、deprecated API 和平台实现者口径见 [待决定的具体对照](CONTRACT_DECISION.md)；未批准前保留 v3.5。现有公开 Dev/Regression 仍不作独立 holdout；不启用 22 pending，也不把两 suite 原始分相加。本轮未执行候选模型实验或新增 Android/MATLAB 构建、设备运行。

使用入口：[固定批次](EVALUATION_BATCH.md)、[SOLID 校准](SOLID_CALIBRATION.md)、[原始输入](EXTERNAL_GIT_INPUTS.md)、[MATLAB 有效合同](../suites/matlab-simulink/EFFECTIVE_CONTRACT.md)。
