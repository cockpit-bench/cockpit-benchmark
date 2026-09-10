# Benchmark — APP、FW、新能源 MATLAB

当前是基于v0.11.2的本地工程修复分支，尚未发布。新新能源源码提交只能通过本地包恢复；GitHub仍对应原公开版本。APP/FW及其参考对象保持，四个私有预留仓继续保密。

| 类型 | 仓 / 参考叶 | 参考分 | 状态 |
|---|---:|---:|---|
| APP | 11 / 88 | 142/440 | 原公开快照保持 |
| FW | 11 / 121 | 194/572 | 原公开快照保持 |
| 新能源现实代理 | 11 / 143 | 409/671 | 本地修复，构建裁决暂停 |

修复了六份LAB标签、真实查表/数组标定组合、九仓类型化业务Bus，以及SWUT断言/容差。根接口和有效合同保持；详细实现、验证和限制见[工程修复报告](docs/FIDELITY_REPAIR_20260910.md)。

`suites.json`为当前三类型登记，新能源仅NEP-01..11。旧ML-01..09、NEM-10/11不参与当前评测。三类分别统计，不合计原始分。

## 本地恢复

需要Python 3.11+、Git、PowerShell。将本地交付目录作为`--bundle-root`；其中包含sources.json及bundles。

```sh
python verification/ne_reality.py restore --bundle-root C:/bench/delivery --destination C:/bench/sources --output C:/bench/restore.json
python verification/ne_reality.py replay --source-root C:/bench/sources
python verification/ne_reality.py candidate --bundle-root C:/bench/delivery --id NEP-01 --output C:/candidate/input
python verification/repository_types.py validate --wrapper .
```

PowerShell恢复入口可用`-SourceMap`将NEP ID映射到上一步恢复出的完整Git仓，再执行：

```powershell
./restore.ps1 -Suite new-energy-matlab -SourceMap C:/bench/source-map.json -Destination C:/bench/powershell-restored
./restore.ps1 -Suite new-energy-matlab -SourceMap C:/bench/source-map.json -Destination C:/bench/powershell-restored -Resume -IncludeSubmodules
```

不提供SourceMap的公开恢复以及`--require-publishable`会拒绝本地新源码。恢复只校验完整历史、HEAD/tree/refs/文件字节、干净状态及零remote，不执行模型。

## 评测

[当前评测说明](docs/CURRENT_EVALUATION.md)保留三类型、单仓输入和外部证据边界。各候选只获得一个源码bundle、有效合同与允许的单仓原始输入；不能访问维护者wrapper、参考分或其他仓。独立进程/网络隔离由运行器承担。

原合同逐字节保持。143个数值参考已重绑当前源码；构建独立性叶只是沿用暂停前的值，不表示争议已经解决。当前一个构造族，候选运行0；没有独立留出或内部真实分布完整复原证明。
