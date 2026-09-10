# 新能源现实代理11仓：本地工程修复

当前NEP-01..11参考409/671，143个叶值保持；九个模型更新，NEP-11文档/测试更新，NEP-05不变。新HEAD未发布。具体四项修复与运行证据见[修复报告](../../../../docs/FIDELITY_REPAIR_20260910.md)。

`manifest.json`绑定完整Git历史/refs/298文件；`STANDARD_SCORES.json`绑定现行源码与未变Part7，构建独立性叶明确暂停。`OBSERVATIONS.json`区分静态定义与原生展开统计；`EXECUTION.json`保存当前原生/host结果及SHA绑定。`PROFILE_COMPARISON.json`只描述已实现范围，不代表内部联合分布或独立泛化。

恢复、重放和单仓导出使用wrapper根目录README的本地bundle命令；默认公开恢复拒绝本地新HEAD。保留原有分支和旧标签，其合成别名不代表多平台实现或真实发布史。
