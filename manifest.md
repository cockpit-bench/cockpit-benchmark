# APP-9 transport manifest

本版本保留 40 仓库存元数据，只运输并评分 9 个 Android APP。全部 FW 与另外 11 个 APP 为 pending。

| ID | Repo | Role | Final HEAD | GitHub |
|---|---|---|---|---|
| APP-03 | climatix-hvac | high/small | c0a37f5985611ffe5b0dbb65bc4352729108d828 | https://github.com/cockpit-bench/climatix-hvac |
| APP-02 | horizon-launcher | high/medium | 82f129b9d9c1270ae2707032eee6b79c8dd072f2 | https://github.com/cockpit-bench/horizon-launcher |
| APP-01 | aurora-settings | high/large | 150289b5e0d67acf395aa5418e43347207e9c1b4 | https://github.com/cockpit-bench/aurora-settings |
| APP-13 | market-hub | medium/small | 3f421d00c591dc47b7de81f77292aa512eb34992 | https://github.com/cockpit-bench/market-hub |
| APP-11 | motion-control | medium/medium | 0ecc89a31ed4f6cecad8c6690f56862a07e78d57 | https://github.com/cockpit-bench/motion-control |
| APP-14 | cockpit-shell | medium/large | 83cc55774e720bc761e90e62ffb94bc61a33973b | https://github.com/cockpit-bench/cockpit-shell |
| APP-17 | thermo-control | low/small | ef1114ba61b39cf20eb5e66e160608bf8c4d8b9e | https://github.com/cockpit-bench/thermo-control |
| APP-16 | nova-launcher | low/medium | 730463f93a9bcdfdcdda176f62dbde5f47eeec9a | https://github.com/cockpit-bench/nova-launcher |
| APP-15 | atlas-settings | low/large | abe446eb843ce0b4ceb068b151ff4081b16ce832 | https://github.com/cockpit-bench/atlas-settings |

恢复脚本会校验每仓全部 heads/tags OID、final HEAD，并在恢复后移除 origin。
