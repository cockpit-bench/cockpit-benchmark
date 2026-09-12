# Benchmark — 六组66仓

v0.12.0新增架构中心、人工智能中心、智能驾驶中心各11仓。六组各11仓，分别评分；新中心内部不按技术再拆报告组。

|报告组|仓库|参考分|叶数|
|---|---:|---:|---:|
|APP|11|142/440|88|
|FW|11|194/572|121|
|New Energy MATLAB|11|409/671|143|
|架构中心|11|205/436|142|
|人工智能中心|11|312/616|187|
|智能驾驶中心|11|329/596|182|

新增33仓511叶，整体863叶。原三组源码、合同和352叶分值保持。完整构造对照、修正、逐仓分数及执行边界见[本版报告](docs/SIX_GROUPS_20260912.md)，新合同见[评分定义](suites/center-contracts/README.md)。这些是有界代理工程的维护者参考，正式候选运行0；不声明完整内部生产分布、盲gold或独立留出验证。

## 公开恢复

需要Python 3.11+、Git、PowerShell，无需GitHub凭据或本地SourceMap。恢复不运行源码。

```powershell
./restore.ps1 -Destination C:/bench/restored -IncludeSubmodules
./restore.ps1 -Suite architecture-center -Destination C:/bench/architecture -IncludeSubmodules
./restore.ps1 -Suite architecture-center -Destination C:/bench/architecture -Resume -IncludeSubmodules
```

```sh
python verification/repository_types.py validate --wrapper . --require-publishable
python verification/centers.py replay --source-root C:/bench/restored --output C:/bench/center-replay.json
python verification/centers.py candidate --source-root C:/bench/restored --id ARC-01 --output C:/candidate/input
```

默认all包含当前66仓。IncludeSubmodules恢复两个集成仓的18个实际Gitlink，并核对全部登记历史/refs/文件字节、clean、零remote和无alternates。旧matlab-simulink别名仍仅对应NEP-01..11；旧ML-01..09、NEM-10/11已退役，不映射到新ID。

## 评测

[suites.json](suites.json)是当前六组登记；[当前评测说明](docs/CURRENT_EVALUATION.md)定义单仓输入和外部证据。每个候选只获得对应源码bundle、有效合同及允许的单仓raw。集成仓依赖由运行器按登记gitlink在独立只读区域提供；运行器负责实际访问隔离。

原始执行记录与源码复核分开报告。主机编译、模型仿真、模拟器与物理设备互不替代；没有ECU/SIL/PIL/HIL/BTC或认证结论。根目录旧Android标准文件及旧验证工具保留冻结兼容，不代表全部66仓。
