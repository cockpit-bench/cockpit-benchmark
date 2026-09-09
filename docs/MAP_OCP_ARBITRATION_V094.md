# v0.9.4：MAP 扩展场景仲裁与通用合同解释

Android 259/828；FW-03 OCP从1修为2，另170个完整叶对象保持。源码27仓HEAD/refs和MATLAB338/549不变。
本轮外部审阅提出反例后，维护者重新读取冻结源码；不是盲审，也没有安装新Provider、实现新协议或执行Android/MATLAB构建。

[完整场景、源码SHA与锚点](map-ocp-arbitration-v094.json)。

## 结论与边界

生命周期、OBEX回调及同契约MAP Provider有实际扩展机制；Profile连接控制仍直接依赖具体服务。MAP类别映射未证明超出必要协议适配的第二条不合理传播，按基本遵循、局部改进为2。

MAP新增同契约Provider经intent发现、authority账号、MAS和内容URI进入既有查询/读取链，不要求按Provider身份改核心。全新消息类别涉及TYPE、handle/过滤参数、SDP能力、投影与编码演进；getMessage及字段Cursor映射不能仅凭位置数锁低档。最强反例是单类型查询的排除掩码/分页推下优化和分页后按类型补字段：它们确实集中耦合类别，不能称全部通用控制已解耦；但最终消息/会话排序分页及时间比较已共享，没有具体新协议语义与MAS组合证据，尚不足以把这些映射认定为独立不合理扩展责任。保留Profile连接策略对具体实现的依赖，不改成良好遵循。

## 分开检验三个变化问题

### existing-provider

安装或替换一个符合既有EMAIL/IM接口、投影和查询约定的Provider；不改变协议类别。

必要修改：

- 新Provider自身实现、manifest接口/authority声明及账号数据；满足原权限、可见性、账号启用等条件。

保持的责任：

- parsePackages/createAppItem/parseAccounts
- createMasInstances
- BluetoothMapContent的账号URI查询及已有类别读取

有源码贯通的同契约扩展路径；不是新增Provider必须修改核心的负例。只读源码判断，不声称实际Provider接入测试。

### new-protocol-category

定义当前bMessage TYPE之外的新消息类别及其能力、过滤、handle与字段表示。

必要修改：

- 新类别的协议声明/解析与能力标记、handle编码、Provider契约或投影、字段与消息编解码适配。

保持的责任：

- 在保持时间排序/数量偏移语义的前提下，列表sort/segment与compareTo不依赖类别。

这些是协议/数据适配变化的真实位置；未定义新的实际协议，不把待实现变化实验当作已经运行的事实。

### strongest-extra-propagation-check

检验新类别是否额外迫使旧排序、分页或其他本应稳定控制重复修改。

已观察的反例：

- 最终sort/segment及比较按统一字段工作；分页后仍恢复类型Cursor并填充字段。
- 各类型单源查询优化显式枚举排除掩码；不能宣称整条分页控制完全类别无关。
- 当前过滤参数只接收0x1f既有类型位，生产MAS按账号单独构造；新协议位与混合组合需先定义。

可定位进一步抽象机会，但旧证据未建立超出新增协议边界的具体额外修改义务；不将该潜在建议与Profile问题凑成1分。

## 关键源码链

| 文件与行段 | 事实 |
|---|---|
| [BluetoothMapAccountLoader.java:61–88](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapAccountLoader.java#L61-L88) | 按既有EMAIL/IM契约发现Provider并遍历结果；类型判断不枚举Provider身份。 |
| [BluetoothMapAccountLoader.java:154–179](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapAccountLoader.java#L154-L179) | 按应用基础URI取得Provider并查询既有账号投影。 |
| [BluetoothMapEmailProvider.java:514–537](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/lib/mapapi/com/android/bluetooth/mapapi/BluetoothMapEmailProvider.java#L514-L537) | Provider基类将标准URI查询分发给数据实现钩子。 |
| [BluetoothMapEmailProvider.java:566–585](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/lib/mapapi/com/android/bluetooth/mapapi/BluetoothMapEmailProvider.java#L566-L585) | 既有Provider查询契约明确要求支持COUNT/OFFSET。 |
| [BluetoothMapService.java:848–867](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapService.java#L848-L867) | 生产服务遍历启用账号创建同类MAS实例；账号作为数据传入。 |
| [BluetoothMapContent.java:423–441](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapContent.java#L423-L441) | 内容消费者沿用账号URI，不按Provider包名选择实现。 |
| [BluetoothMapUtils.java:101–115](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapUtils.java#L101-L115) | 类型枚举对应bMessage type属性；新增类别涉及线协议表示。 |
| [BluetoothMapContent.java:2229–2255](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapContent.java#L2229-L2255) | 单类型查询推下分页优化显式比较排除掩码；不能把最终分页完全泛型化扩大到全部查询控制。 |
| [BluetoothMapContent.java:2411–2450](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapContent.java#L2411-L2450) | 共用排序分页之后按类别恢复Cursor并填充具体字段；映射仍集中但并非Provider身份分派。 |
| [BluetoothMapMessageListing.java:139–156](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapMessageListing.java#L139-L156) | 最终排序及截取实现只使用统一列表和数量/偏移。 |
| [BluetoothMapMessageListingElement.java:256–265](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapMessageListingElement.java#L256-L265) | 消息比较只依赖时间，不枚举消息类别。 |
| [BluetoothMapContent.java:2882–2927](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapContent.java#L2882-L2927) | 会话最终排序分页共享，随后按类别执行字段/联系人映射。 |
| [BluetoothMapConvoListingElement.java:247–256](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapConvoListingElement.java#L247-L256) | 会话比较只依赖最后活动时间。 |
| [BluetoothMapContent.java:3557–3578](https://github.com/cockpit-bench/bluetooth-service/blob/de95b814d40d093d26cd89e910299baee2b5dc31/src/com/android/bluetooth/map/BluetoothMapContent.java#L3557-L3578) | 读取入口从handle解出协议类别并选择相应格式读取。 |

## 档位与横向一致性

不降为1/0：原1分把Profile连接族与未充分界定的MAP新类别传播共同锁为多处不合理；动态Provider与共享排序分页反证了泛化表述。已证实的连接机制影响集中，连同现有扩展点不足以支持1或0。

不升为3/4：真实连接控制逐个调用具体服务，生命周期配置不能替代连接能力抽象；该缺口仍阻止3/4。

FW-02固定DHCP类别与FW-15固定路由类别均不因协议枚举本身扣分；FW-15另有通用超时清理对具体类型的真实依赖。FW-03保留Profile连接控制缺口，结合既有扩展机制评价为2；不是按“一个位置=2、两个位置=1”计数。比较仓分数与叶对象均保持。

## 候选可见合同 v3.5.1

用户明确同意将不带案例答案的通用解释合入SCORE_RULES.md §3.6：核对契约/合法前提、实际接口负担、具体OCP变化场景及严重度。合法叶、档位、满分、LSP执行证据门槛和MATLAB合同不变。
新合同SHA-256：`2bb21ed67c9e47c3cf7691bc2a526fa3e2c41b410017fa4faa41a02132da7b91`。候选只接收[同版本通用合同](../SCORE_RULES.md)，不能接收本页、机器可读仲裁、标准分或维护者facts。
除该解释与版本行外，合同原文逐字节保持；全部Android合同绑定及APP边界回归引用已更新。旧发布与旧输入包保持不可变。

本次仅对一个叶的MAP机制进行源码仲裁；其余170叶内容沿用原证据。合同hash和规则重放不等于重新完成所有语义审查，也未通过实验验证Prompt/模型稳定性改善。

## 后续边界

v0.9.3五项修复保持关闭。扩建由独立任务先规划、待用户批准，当前正式27仓与旧22pending集合均未改变。
旧/新Prompt比较仍需相同参考、输入模式及eligible集合；本轮没有候选模型预测。
