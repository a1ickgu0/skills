# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

本目录是父级 `Skills` 集合仓库中的独立技能 `enterprise-network-product-research`，不是可运行的应用。用途是研究、复核和更新企业网络产品清单及字段级证据；默认支持交换机，但应保持跨厂商可复用。单参数查询不应自动扩展成产品全景研究。

父级 `../README.md` 说明集合仓库的技能目录约定和调用方式。本技能以 Markdown 指令为主，附带仅依赖 Python 3 标准库的数据校验器与 unittest 测试；没有应用构建或第三方依赖。

## 工作方式与验证

从本目录运行：

```sh
# 查看本技能的变更，避免混入父仓库其他技能的工作
git status --short -- .
git diff -- .

# 检查已跟踪变更的空白错误（不覆盖未跟踪文件或语义正确性）
git diff --check -- .
```

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s tests -p test_validate_research.py -k critical_unknown -v
python3 -B scripts/validate_research.py tests/fixtures/research.json
```

没有 build 或独立 lint 命令。`scripts/validate_research.py` 检查最小契约及引用，不证明事实正确；设计文档中的 `validate_inventory.py` 未实现。

行为验收见 `tests/scenarios.md`。测试夹具是合成数据，不能用作厂商规格证据；真实资料研究、图形渲染与飞书导入必须单独验证。场景包括：

- 新厂商研究、已有表更新、待核字段复核、系列筛选四类任务。
- 范围含糊时集中澄清关键缺项；范围已明确时复述后执行，不重复要求确认。
- Combo、多速率、breakout、可选模块、机框/线卡、PoE、官方来源冲突和生命周期未知等边界。

## 架构与修改边界

这是以 Markdown 指令为实现的技能，执行流程是：确定范围、发现产品与身份、采集证据、标准化与推导、交付与验证。

- `SKILL.md` 是运行入口：YAML frontmatter 定义技能名和触发描述，正文定义工作流及关键约束。保留它到参考文档的相对链接，以便按需加载细节。
- `references/schema-and-evidence.md` 定义主表字段语义、证据记录、未知与冲突状态，以及增量更新口径。
- `references/switch-port-model.md` 将物理接口、速率能力、复用、拆分、模块配置和电源条件映射到平面产品表，是交换机专属领域层。
- `references/research-and-quality.md` 定义目录覆盖、生命周期判定、交付校验及更新行为。
- `references/expert-review.md` 定义未知推进、专家计算与更新冲突处理。
- `references/reporting-and-feishu.md` 定义综合报告、SVG/PNG 及 manifest；JSON 是权威底稿，CSV/报告为派生交付。
- `scripts/validate_research.py` 实现契约的最小确定性检查；`tests/` 存放回归测试、合成夹具和行为场景。
- `references/panorama-example.json`、`panorama-example.md` 和 `scripts/render_panorama_example.py` 定义可公开的Aruba图形示例及重建方式；不能引入私有产品规划图或其脱敏衍生内容。`runs/`和本地中间表不属于发布包。

通用流程留在入口，字段约定和领域细节留在各自参考文档。Aruba 是初始需求及验收案例，不是技能的硬编码目标；不要将具体 SKU、实时在售状态或某厂商命名规律固化为通用规则。仅在确有复用价值时增加厂商资料或确定性校验脚本。

## 数据契约与易错边界

- 基础 SKU 主表、系列筛选视图和字段级溯源彼此关联；子 SKU 关系及变化清单按需生成。系列视图应从主表保持一致，不能成为独立维护的事实来源。
- 去除订货后缀只能产生归并候选。固定设备、机框、线卡、预配置套件、备件及硬件/认证/交付配置不同的型号须按真实身份区分。
- 官网列示、可订购和停售是不同事实，均受地区及截止日期约束；产品页存在不证明在售，搜索不到不证明停售。
- 字段证据需能定位到 SKU、来源 URL、版本、页码或章节、核查日期及配置/推导条件；一个字段允许多条证据。未知、不适用、证据支持的零、推测与官方冲突不可混同。
- 先构建真实接口及配置模型，再映射速率列。多速率列不可相加，breakout 逻辑口不等于物理口，可选模块不等于标配；连接器外形不能证明速率兼容性。PoE 端口数与依赖电源配置的 PSE 预算分开记录。
- ADCP 仅在用户定义为发布时间时采用该含义；SKU 日期、系列首发、最早存在证据和估计日期分开表达。交换芯片型号不是 MAC 地址表容量。
- 更新保留已有列、用户修正和历史证据，并记录旧值、新值与依据。默认 CSV 编码为 UTF-8 BOM，链接使用完整 URL。
