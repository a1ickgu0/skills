# 数据与证据契约（1.0）

## 分层交付

JSON 是唯一权威数据底稿；CSV 是其派生视图，Markdown 是分析报告，SVG/PNG 是报告资源。不能分别修改三套事实。小任务可只输出相关对象和简要答复；全景研究与增量更新使用以下完整契约。已存在用户模板时保留列，通过字段映射导出，不要求用户迁移表头。

默认交付 `data/research.json`、`exports/products.csv`、`exports/open-issues.csv`、`report/report.md` 和 `manifest.json`；有图时增加 `figures/`。不要为满足文件清单生成无内容文件。JSON 使用 UTF-8，CSV 使用 UTF-8 BOM、标准引号和完整 URL。JSONL 只在大规模逐条处理确有必要时采用，并明确唯一权威版本，不能与 JSON 独立维护。

## research.json 最小契约

顶层必须有 `schema_version: "1.0"`、`dataset_id`、`revision`、`scope` 及以下数组。标识为非空稳定字符串；引用使用标识，不用数组位置。字段未定义时不猜测，新增字段保留语义说明。

- `scope`：`vendor`（单厂商默认值；跨厂商时填 `multiple`）、`category`、`region`、`as_of`（YYYY-MM-DD）、`lifecycle_target`、`defaults`（已采用默认值数组）。测试数据增加 `synthetic: true`。
- `products`：`id`（厂商命名空间）、`sku`、`name`、`kind`。SKU 在同一厂商内唯一；产品可用 `vendor` 覆盖 scope.vendor，跨厂商时每个产品必须显式填写 vendor，不能用 multiple 作为产品厂商。基础 SKU 与完整订货子 SKU 分开。可选 `relations` 记录套件、组件、区域子 SKU 及归并依据。
- `configurations`：`id`、`product_id`、`basis`（`standard` / `maximum` / `specified`）、`description`。电源、线卡、模块、软件条件写明；参数依赖不同配置时不能复用含糊的“最大配置”。
- `sources`：`id`、`url`、`kind`（`official` / `secondary` / `user` / `synthetic`）、`title`、`version`（未知用 null）、`accessed_at`。
- `evidence`：`id`、`source_id`、`locator`（页码/章节/表格/页面字段）、`excerpt`、`applicability`（适用 SKU、版本和配置）。不能只保留一个系列 URL。
- `claims`：见下文。一条记录只表达一个产品、一个字段、一个配置下的当前判断。
- `research_tasks`：见 [未知推进与专家复核](expert-review.md)。
- `coverage`：`id`、`segment`、`source_ids`、`candidate_product_ids`、`status`（`complete` / `partial` / `blocked`）、`gaps`。未收录或排除的候选另在 `exclusions` 中记录原标识、理由及证据，不能静默丢弃。
- `changes`：新研究可为空；更新时记录 `product_id`、`field`、`old_value`、`new_value`、`reason`、`evidence_ids`，涉及用户值时设置 `origin: "user"`，另记录 `user_resolution`（待决或明确决定），即使新旧采用值相同也记录新证据和冲突。

`revision` 标识一次一致的数据快照。报告、图表和导出在 manifest 中引用相同 `dataset_id` 与 `revision`，更新时重新生成受影响视图。

## claims 与状态

每项判断必须有：`id`、`product_id`、`configuration_id`、`field`、`value`、`unit`（无单位用 null）、`value_state`、`method`、`conflict`、`evidence_ids`、`importance`（`critical` / `normal`）、`rationale`。

| 维度 | 枚举与含义 |
| --- | --- |
| `value_state` | `known`、`unknown`、`not_applicable` |
| `method` | `official_direct`、`official_derived`、`name_inferred`、`secondary`、`user_asserted`、`unestablished` |
| `conflict` | `none`、`unresolved`、`explained` |

数值零是值，不是状态；只有支持不存在的证据或完整模型才能填零。`unknown` / `not_applicable` 的 `value` 为 null；后者在 rationale 中解释为何不适用。未知原因写在 task 中，不能用“0”“—”替代。`known` 不能为 null；数值字段使用数字，不把单位、最大值和待核字样塞入数值。未知、冲突和配置相关是不同维度，配置由 configuration 表达。

`known` 且非 `user_asserted` 的判断必须关联证据；官方方法必须有官方证据。`official_derived` 和 `name_inferred` 另有 `derivation`：`input_claim_ids`、`rule`、`calculation`、`conditions`、`limitations`。名称推测不得在正文写成官方确认。专家假设放入 task，不冒充已知值。

未解决的关键未知或任何未解决冲突必须关联 research task；冲突通常将当前值置为 unknown，双方原值保留在 evidence 中。若保留暂用值，应在 rationale 明确选择依据和风险，不能隐藏冲突。

## 字段语义与派生视图

主表有用户模板时严格保持原列名、列数和顺序，未经明确授权不扩列；没有模板时再定义字段。常见字段包括品牌、系列、类型、基础 SKU、产品名称、ADCP、CPU、内存、Flash、双向交换容量、ASIC、端口、PoE/PSE、电源条件、生命周期、规格页面、文档及核查日期。

- ADCP 仅在用户定义为发布时间时采用；SKU 发布时间、系列首发、最早存在证据、估计日期分别记录，注明日期精度。
- 交换容量、转发率、接口速率总和不能互换；交换芯片型号不是 MAC 表容量。GB/GiB、Gbps/Mpps、W 等单位不可静默混用。
- 端口字段明确 `connector_count`、`concurrent_port_count`、`breakout_logical_count` 或具体速率能力；不能用一个无口径“端口数”混合三者。见 [端口模型](switch-port-model.md)。
- 生命周期按地区与时点记录，目录列示不是在售证明；缺少证据时保留未知。

CSV 每个导出值应能通过SKU及独立字段映射关联product ID、field、configuration ID与claim。有模板时状态、配置和证据明细放claims.csv/sidecar，在模板已有说明和备注中提示条件，不增加_state/_claim等列；无模板时才可分列。表头逐项精确比较是交付门禁。系列产品CSV保持相同表头，从主表显式筛选。导入电子表格前检查以 `= + - @` 开头的自由文本，防止被解释为公式；文本转义只作用于 CSV 展示，不改变 JSON 原值和合法负数。

## 自动检查边界

`python3 scripts/validate_research.py data/research.json` 检查必需结构、枚举、标识引用、当前判断唯一性、推导依赖、关键未知任务与核查记录。它不是完整 JSON Schema 验证器，也不验证 URL 可访问性、官方真实性、计算正确性、目录完整性或报告内容；这些必须经过来源复核和场景验收。
