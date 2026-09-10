# Benchmark — APP、FW、新能源 MATLAB

v0.11.3发布已验证的新能源工程修复：LAB真实标签、查表/数组标定、类型化业务Bus，以及SWUT断言容差。当前APP/FW/新能源各11仓，分别142/440、194/572、409/671，共352个参考叶；有效合同和叶值保持，构建独立性争议继续暂停。

十个新能源仓有前向提交，NEP-05保持。APP/FW源码及参考对象、四个私有预留仓和旧22pending保持。见[修复与验证](docs/FIDELITY_REPAIR_20260910.md)。

## 公开恢复

需要Python 3.11+、Git、PowerShell，无需GitHub凭据或本地SourceMap。

```powershell
./restore.ps1 -Destination C:/bench/restored
./restore.ps1 -Suite new-energy-matlab -Destination C:/bench/energy
./restore.ps1 -Suite new-energy-matlab -Destination C:/bench/energy -Resume -IncludeSubmodules
```

```sh
python verification/repository_types.py validate --wrapper . --require-publishable
python verification/ne_reality.py restore --destination C:/bench/native-sources --output C:/bench/restore.json
python verification/ne_reality.py replay --source-root C:/bench/native-sources
python verification/ne_reality.py candidate --source-root C:/bench/native-sources --id NEP-01 --output C:/candidate/input
```

默认all恢复33仓，单新能源恢复NEP-01..11。恢复验证完整历史、HEAD/tree/refs/文件字节、干净状态和零remote，不执行模型。旧ML-01..09、NEM-10/11不在当前集合。

## 评测与边界

[suites.json](suites.json)为三类型登记；[当前评测说明](docs/CURRENT_EVALUATION.md)解释单仓输入和外部证据。每个候选仅获得对应源码bundle、有效合同及允许的单仓raw；运行器负责实际进程/访问隔离。原始执行附件供维护者复核，不作为默认候选输入。

本次发布沿用已绑定的11模型55949采样/138条业务属性和8仓C host回放；没有新增设备或候选执行。当前一个知情构造族，非独立holdout；内部36仓完整联合画像及生产标定仍缺失。构建独立性叶沿用暂停前值，不表示争议已解决。
