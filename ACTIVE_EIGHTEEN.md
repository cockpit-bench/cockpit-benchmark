# Validation-18

| 类型/质量 | 小型 | 中型 | 大型 |
|---|---|---|---|
| APP 高 | APP-03 climatix-hvac | APP-02 horizon-launcher | APP-01 aurora-settings |
| APP 中 | APP-13 market-hub | APP-11 motion-control | APP-14 cockpit-shell |
| APP 低 | APP-17 thermo-control | APP-16 nova-launcher | APP-15 atlas-settings |
| Android FW 高 | FW-02 vehicle-property-service | FW-03 vehicle-hal-adapter | FW-07 vehicle-diagnostics |
| Android FW 中 | FW-10 cockpit-manager-kit | FW-08 soa-gateway | FW-14 update-manager-service |
| Android FW 低 | FW-15 car-runtime-service | FW-18 vehicle-platform-service | FW-16 platform-compat-service |

体量按 SCORE_RULES.md 的 final-HEAD 生产源码双阈值确定；两个指标跨档时标记 unresolved，不按矩阵角色强贴。

其余 22 仓 pending，不运输。`can-middleware` 仅保留为 v0.4 历史补充样例，不计入本版本。
