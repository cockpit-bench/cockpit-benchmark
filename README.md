本地准备完成，尚未发布。GitHub旧11仓删除已获用户批准，但实际请求因令牌缺少 delete_repo 返回403；设备授权正在等待用户完成。当前远端仍是v0.11.0。

# Benchmark — APP、FW、新能源 MATLAB

v0.11.1 将旧新能源联调 11 仓移出当前集合，并按用户指令删除对应 GitHub 源码仓。当前只有三类各 11 仓，共 33 仓、352 个参考叶；不跨类型合计健康度分数。

| 类型 | 仓数 / 参考叶 | 参考分 | 有效合同 |
|---|---:|---:|---|
| [APP](suites/app/SCORECARD.md) | 11 / 88 | 142/440 | [Android v3.5.1](SCORE_RULES.md) |
| [FW](suites/fw/SCORECARD.md) | 11 / 121 | 194/572 | [Android v3.5.1](SCORE_RULES.md) |
| [新能源现实代理](suites/new-energy-matlab/cohorts/reality-proxy-20260910/README.md) | 11 / 143 | 409/671 | [Part 7 及已批准补充](suites/new-energy-matlab/cohorts/reality-proxy-20260910/contract-index.json) |

[suites.json](suites.json) 是唯一当前注册入口。新能源仅 NEP-01..11；旧 ML-01..09、NEM-10、NEM-11 已退出，旧 ID 会被恢复入口拒绝。APP/FW 和现实代理源码、参考叶值及有效合同未改变。四个私有预留仓保持保密。

## 恢复

需要 Python 3.11+、Git、PowerShell。公开恢复无需 GitHub 凭据；验证完整主仓历史、HEAD/tree/refs、干净状态和零 remotes，不执行源码。

```powershell
./restore.ps1 -Destination C:/bench/restored
./restore.ps1 -Suite new-energy-matlab -Destination C:/bench/energy
./restore.ps1 -Suite app -RepositoryIds APP-21,APP-22 -Destination C:/bench/apps
```

默认 `all` 恢复当前 33 仓，按 app、fw、new-energy-matlab 分目录；单类型直接放入目的地。`-Resume` 复核已有仓，`-IncludeSubmodules` 检查固定子模块。别名 `matlab-simulink` 也只选择当前 NEP-01..11。

```sh
python verification/repository_types.py validate --wrapper . --require-publishable
python verification/ne_reality.py replay --source-root C:/bench/restored
python verification/ne_reality.py candidate --source-root C:/bench/restored --id NEP-01 --output C:/candidate/input
```

新组原独立恢复入口仍可用，产物与默认入口是相同 11 仓；replay/candidate 支持两种目录布局。候选只获得单仓源码、有效合同及明确允许的单仓原始输入，不能访问维护者参考分或其他仓。

## 评测与限制

[当前三类型评测](docs/CURRENT_EVALUATION.md)已统一覆盖这 33 仓。source_only 可评 APP 79/88、FW 109/121、新能源 143/143；frozen_external 为 81/88、113/121、143/143。旧新能源不再参与集合、分母、切分或统计。

参考分是维护者裁决，不是候选模型成绩。新组 6 个恒定叶，同集合众数 123/143；一个共同构造族，不是独立 holdout。NEP-10 构建优先级、证据语义与定位完整性仍需后续处理，见 [v0.11.0 Pro 评审核对及本轮范围](docs/REVIEW_V0111.md)。此次入口迁移没有新增 Android、MATLAB、C 或设备执行。

历史 wrapper tag 保留原内容；旧 11 源码仓被删除后，旧版相应下载链接将失效。当前主线已移除旧组合同、标准分、专用证据和工具。根 Android Validation-18 文件只保留冻结兼容，由 [legacy-v094.json](suites/legacy-v094.json) 绑定；它们不替代当前三类型入口。
