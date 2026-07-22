# Teece PFI — 从技术创新中获利 分析框架

[![SKILL](https://img.shields.io/badge/Claude--Code-SKILL-blue)](SKILL.md)

基于 David J. Teece 1986 年经典论文 *"Profiting from Technological Innovation"* 的**战略分析工具**。回答核心问题：**技术创新的利润流向何方——创新者、模仿者，还是互补资产所有者？**——并据此制定商业化策略。

## 目录结构

```
teece-pfi/
├── SKILL.md                              # 技能定义文件（核心）
├── assets/
│   ├── teece-pfi-terminology.json        # 术语映射（64 个术语 + 10 个案例，程序化消费）
│   └── teece-pfi-terminology.md          # 术语对照表（人可读）
├── references/
│   └── Profiting_from_technological_innovation.pdf  # 原始论文
└── tests/
    └── teece-pfi-analysis_report/        # 分析报告测试用例
```

## 适用场景

- 评估一项技术创新的商业化策略
- 判断创新利润的分配格局（谁能赚到钱）
- 决定**整合**（自建/收购）还是**契约**（合作/授权）获取互补资产
- 分析企业在特定竞争环境中的定位与风险

## 分析框架（6 步骤）

| 步骤 | 名称 | 核心问题 |
|------|------|----------|
| 1 | 独占性制度评估 | 技术容易模仿吗？法律保护有效吗？ |
| 2 | 互补资产识别与分类 | 商业化需要哪些资产？通用型/专用型/共用型？ |
| 3 | 主导设计阶段判断 | 行业处于前范式、范式还是后续阶段？ |
| 4 | 相对位置评估 | 创新者 vs 模仿者 vs 资产所有者，谁占优？ |
| 5 | 策略推导与决策矩阵 | 整合还是契约？钱够不够？时间够不够？ |
| 6 | 延伸分析（可选） | R&D 配置、大小企业对比、产业结构、制造能力等 |

## 内置案例库（10 个）

| 案例 | 结果 | 关键教训 |
|------|------|----------|
| EMI CAT 扫描仪 | 创新者失败 | 技术卓越 ≠ 商业成功，无互补资产则利润旁落 |
| IBM PC | 创新者大胜 | 品牌 + 开放生态 = 弱独占性下的制胜组合 |
| NutraSweet | 创新者持续获利 | 强独占性 + 前向整合制造与品牌 |
| RC Cola | 创新者失败 | 先发优势被可口可乐/百事的渠道+品牌碾压 |
| Bowmar 计算器 | 创新者失败 | 小企业被 TI / HP 的制造能力碾压 |
| 施乐办公电脑 | 创新者失败 | 有核心技术但缺乏目标市场的互补资产 |
| 彗星客机 | 创新者失败 | 前范式阶段选错设计 + 不可逆投入 = 致命 |
| Apple LaserWriter | 创新者成功 | 契约模式通过风险共担可以成功 |
| IBM + 微软 DOS | 双方获益 | IBM 品牌是微软的共用型资产 |
| 联合碳化物 | 创新者成功 | 强独占性 + 通用型资产 = 授权模式可行 |

## 运行模式

### 模式 A：一键全分析（默认）

直接提供一段创新描述即可获得完整报告：

> "帮我用 Teece PFI 框架分析 OpenAI 的 GPT 系列在商业化中的利润分配"

### 模式 B：交互式诊断

逐步完成每一步，适合需要深度讨论和验证的场景：

> "逐步指导我用这个框架分析我们的新产品"

## 术语规范

所有输出必须遵循统一的中文术语体系：

- **独占性制度**（强/弱）—— 不用"专有性""占有性"
- **互补资产三分类**：通用型 / 专用型 / 共用型
- **三阶段**：前范式阶段 → 范式阶段 → 后续阶段
- **整合 vs 契约** —— 不用"一体化"

完整术语对照表见 [assets/teece-pfi-terminology.md](assets/teece-pfi-terminology.md)。

## 输出格式

- **主输出**：结构化 Markdown 分析报告（6 步骤全覆盖）
- **可选导出**：DOCX 咨询报告 / PPTX 演示文稿

## 参考

- Teece, D.J. (1986) "Profiting from Technological Innovation: Implications for Integration, Collaboration, Licensing and Public Policy", *Research Policy* 15, pp. 285–305
- [原始论文 PDF](references/Profiting_from_technological_innovation.pdf)
