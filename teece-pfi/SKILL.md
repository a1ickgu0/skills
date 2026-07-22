---
name: teece-pfi
description: Apply Teece's "Profiting from Technological Innovation" framework to analyze who captures innovation profits and prescribe strategy. Use when evaluating an innovation's commercialization strategy, profit distribution, integration vs. contract decisions, or competitive positioning around complementary assets.
---

# Teece PFI Framework — SKILL

## Purpose

This SKILL operationalizes David J. Teece's 1986 framework "Profiting from Technological Innovation" into a structured analytical tool. It answers the core question: **Who captures the profits from an innovation — the innovator, imitators, or owners of complementary assets?** — and prescribes actionable strategy.

## Terminology

All outputs MUST use the organization-standard Chinese terminology defined in the companion files:
- `teece-pfi-terminology.json` — programmatic mapping (64 terms + 10 cases)
- `teece-pfi-terminology.md` — human-readable alignment table

**Mandatory usage rules:**
1. 独占性制度 — use 独占性(强/弱), NOT 专有性/占有性
2. 互补资产三分类 — 通用型/专用型/共用型, NOT 共专用/共同专有
3. 共用型 emphasizes bilateral dependence, NOT "共专用"
4. Three-stage model — 前范式阶段 → 范式阶段 → 后续阶段
5. 整合 vs 契约 — 整合=ownership control; 契约=contractual access; NOT 一体化
6. 创新者 = first to commercialize, NOT mere inventor

**Language:** SKILL instructions are in English. Output language AUTO-ADAPTS to match the user's input language (Chinese → Chinese output; English → English output; mixed → follow dominant language).

## Mode Selection

### Mode A: One-Click Full Analysis

Trigger: User provides a description of an innovation, firm, or industry scenario (even a single sentence). The SKILL runs the complete analysis pipeline in one pass and delivers a full Markdown report.

Workflow:
1. Parse user input → identify the innovation/firm/industry
2. If input is underspecified, use WebSearch to gather context (industry landscape, competitive dynamics, IP protection environment, complementary asset structure)
3. Run all 6 analytical steps sequentially
4. Generate complete Markdown report
5. Offer optional DOCX/PPTX export

### Mode B: Interactive Diagnostic

Trigger: User explicitly requests step-by-step analysis, or the input is too ambiguous for one-click mode.

Workflow: Execute Steps 1–6 one at a time, presenting each step's findings to the user for validation and deepening before proceeding. The user may skip, revisit, or drill into any step.

### Mode Detection Logic

- User says "analyze this", "帮我分析", "run the framework on X" → Mode A
- User says "walk me through", "step by step", "逐步分析" → Mode B
- Input is a single vague sentence with no concrete scenario → Mode B (need clarification)
- If unsure → default to Mode A, but offer to switch to Mode B at any step

## Data Gathering

The SKILL MUST proactively search for data when user input is insufficient to make confident assessments on any analytical dimension. Search triggers include:

- **Industry landscape unknown** → search for market structure, key players, competitive dynamics
- **Appropriability unclear** → search for patent landscape, trade secret practices, reverse engineering risk in the industry
- **Complementary assets unidentified** → search for supply chain structure, distribution channels, manufacturing requirements, service infrastructure
- **Dominant design stage ambiguous** → search for technology standards, design convergence signals, product evolution history
- **Relative positioning uncertain** → search for specific competitors' asset portfolios, partnership patterns, market share data

Search strategy:
1. Use WebSearch with targeted queries (industry name + specific dimension keywords)
2. Cross-reference multiple sources when possible
3. Flag any assessment that relies on incomplete data with a confidence level (high/medium/low)
4. Present findings with source citations

## Analytical Pipeline (6 Steps)

### Step 1: Appropriability Regime Assessment (独占性制度评估)

Objective: Determine whether the innovation operates under a strong (强) or weak (弱) appropriability regime.

Assessment dimensions:

**A. Nature of Technology (技术的性质)**
- Knowledge type: Is the core knowledge tacit (隐性) or codified (显性)?
  - Tacit → favors strong appropriability (hard to copy even if disclosed)
  - Codified → favors weak appropriability (easy to transmit and replicate)
- Innovation type: Product innovation (产品创新) vs. Process innovation (工艺创新)?
  - Product → more visible, easier to reverse engineer
  - Process → can sometimes be kept as trade secret even while product is public
- Technological complexity: How difficult is reverse engineering (逆向工程)?
  - High complexity → favors strong appropriability
  - Low complexity → favors weak appropriability

**B. Legal Protection Efficacy (法律保护效力)**
- Patent protection: Are patents available, enforceable, and difficult to invent around?
  - Pharmaceutical/chemical → often strong patent protection
  - Software/mechanical → patents often easy to design around
- Trade secret viability: Can the innovation be commercially exploited while keeping core knowledge secret?
- Copyright/trademark: Any supplementary protection?
- Regulatory barriers: Do approval processes (e.g., FDA, telecom standards) create de facto barriers to imitation?

**Scoring:** Rate each dimension on a 1-5 scale (1=very weak protection, 5=very strong protection). Aggregate to classify:
- Total ≥ 15 → **强独占性** (Tight)
- Total < 15 → **弱独占性** (Weak)
- Note: Teece emphasizes that weak appropriability is the norm in practice

**Output for this step:**
- Appropriability regime classification (强/弱)
- Confidence level
- Key evidence supporting the classification
- Reference to comparable cases from the built-in case library

### Step 2: Complementary Asset Identification & Classification (互补资产识别与分类)

Objective: Identify all complementary assets required for successful commercialization and classify each as generic (通用型), specialized (专用型), or cospecialized (共用型).

Process:
1. List all assets/capabilities needed to bring the innovation to market:
   - Manufacturing / production
   - Distribution / sales channels
   - Marketing / brand
   - After-sales service / support
   - Regulatory compliance / certification
   - Software / ecosystem (for systemic innovations)
   - Supply chain components
   - Customer relationships / user base
   - Any other industry-specific requirements
2. For each asset, determine the dependency relationship:
   - **Generic (通用型)**: Unilateral independence — asset is widely available, not tailored to the innovation, easily accessible through contract. Example: general-purpose manufacturing equipment.
   - **Specialized (专用型)**: Unilateral dependence — asset depends on the innovation for value, but the innovation does not equally depend on the asset. Example: specialized production tooling that is worthless without the product.
   - **Cospecialized (共用型/双向专用)**: Bilateral dependence — both the innovation and the asset depend on each other. Example: dedicated repair facilities for a novel engine type; distribution channels that only make sense for this product category, and the product only sells through these channels.
3. Identify bottlenecks (瓶颈): Which assets are in fixed supply, controlled by few players, or structurally difficult to access?
4. Assess current ownership: Does the innovator already control any of these assets? Which ones are controlled by competitors or independent parties?

**Output for this step:**
- Complete asset inventory table with classification
- Bottleneck identification
- Ownership map (innovator vs. competitors vs. independents)
- Reference to case analogies (EMI lacked service/marketing; IBM had brand+distribution)

### Step 3: Dominant Design Stage Assessment (主导设计阶段判断)

Objective: Determine whether the industry is in the preparadigmatic (前范式), paradigmatic (范式), or post-paradigmatic (后续) stage.

Assessment criteria:

**前范式阶段 (Preparadigmatic):**
- Multiple distinct designs compete in the market
- Manufacturing processes are loose and adaptive
- General-purpose capital is used in production
- Competition is design-centric, not price-centric
- Production volumes are low
- Complementary assets are relatively unimportant
- Innovator must "closely couple to the market" (紧密耦合市场)
- Design "floats" until market acceptance validates a direction

**范式阶段 (Paradigmatic):**
- A dominant design or narrow class of designs has emerged
- Product design uncertainty has decreased
- Competition shifts to price, scale, and learning curves
- Specialized capital begins to appear
- Complementary assets become critically important
- Process innovation accelerates (cost reduction focus)
- Scale economies become available

**后续阶段 (Post-paradigmatic):**
- Product design is fully stabilized
- Production is highly automated / standardized
- Competition is based on cost-performance ratio (性价比)
- Innovation is primarily incremental (微创新/渐进式改进)
- Major innovation is rare
- Complementary assets are fully integrated into incumbents' boundaries

**Key strategic implications by stage:**
- Pre-paradigmatic: Focus on design selection; stay closely coupled to market; don't over-invest in specialized assets yet
- Paradigmatic: Rush to secure specialized/cospecialized complementary assets; if weak appropriability, integration is essential
- Post-paradigmatic: New entrants face high barriers; must form alliances with incumbents who control cospecialized assets

**Output for this step:**
- Stage classification with evidence
- Implications for timing of complementary asset investment
- Warning if the innovator is in the wrong stage for its strategy

### Step 4: Relative Positioning Assessment (相对位置评估)

Objective: Map the relative positioning of three player classes — innovator (创新者), imitators/followers (模仿者/跟随者), and owners of complementary assets (互补资产所有者) — with respect to each other and the required assets.

Assessment dimensions:
- **Innovator's asset position**: Does the innovator already possess relevant specialized/cospecialized assets? Or is it asset-poor?
- **Imitators' asset position**: Do potential imitators already possess the relevant complementary assets? Are they better positioned?
- **Independent asset owners**: Are there firms that control bottleneck complementary assets but are neither the innovator nor obvious imitators?
- **Lead time / speed**: How quickly can the innovator build/buy complementary assets compared to how quickly imitators can enter?
- **Cash constraints**: Is the innovator financially constrained, limiting its ability to integrate?

**Output for this step:**
- Three-player positioning map
- Lead time and cash constraint assessment
- Identification of whether the innovator is "advantageously positioned" or "disadvantageously positioned" vis-à-vis independent asset owners (this directly feeds the Figure 11 matrix)

### Step 5: Strategy Derivation & Decision Matrix Placement (策略推导与决策矩阵定位)

Objective: Place the innovation scenario into Teece's decision matrix and prescribe the optimal strategy.

**Decision logic (from paper Figures 10 & 11):**

IF appropriability is TIGHT:
  IF complementary assets are GENERIC → **Contract/License** (契约/授权)
    Outcome: Innovator wins; asset owners won't benefit significantly
  IF complementary assets are SPECIALIZED → **Contract possible, but integration prudent** (契约可行，整合更稳健)
    Risk: Relationship breakdown leaves irreversible investments worthless
  IF complementary assets are COSPECIALIZED → **Integrate** (整合)
    Reason: Bilateral dependence creates contractual hazards
    Outcome: Innovator can afford time to build/buy assets (imitation is muted)

IF appropriability is WEAK:
  IF complementary assets are GENERIC → **Contract** (契约)
    Outcome: Innovator can still profit; generic assets are easily sourced
  IF complementary assets are SPECIALIZED → **Must integrate** (必须整合)
    Reason: Without ownership, innovator will lose profits to imitators
    Outcome depends on relative positioning:
      - Innovator advantageously positioned → can win
      - Innovator disadvantageously positioned → will probably lose to imitators and/or asset holders
  IF complementary assets are COSPECIALIZED → **Must integrate; urgency extreme** (必须整合，紧迫性极高)
    Reason: Bottleneck cospecialized assets determine profit distribution
    IF asset is completely "locked up" by a monopoly → innovator loses even with optimal strategy
    IF innovator is cash-constrained → minority position (少数股权) as pragmatic compromise

**Timing and cash constraints (Figure 9 integration calculus):**

| Time to Position | Investment Required | Criticality | Strategy |
|---|---|---|---|
| Long | Major | Not Critical | Forget it (放弃) |
| Long | Major | Critical | Internalize ownership if possible |
| Short | Major | Critical | Full steam ahead (全力整合) |
| Short | Tolerable | Critical | Internalize ownership |
| Short | Minor | Not Critical | Don't internalize; contract out (契约外包) |
| Short | Minor | Critical | Internalize (but if cash-constrained, take minority position) |

**Output for this step:**
- Decision matrix cell placement (which cell in Figure 11)
- Prescribed strategy with reasoning
- Alternative strategies considered and why rejected
- Timing and cash constraint assessment
- Risk warnings

### Step 6: Extended Analysis (延伸分析) — Optional, expand as needed

These modules are activated by user request or when the core analysis reveals significant implications in these areas.

**6A: R&D Resource Allocation (研发资源配置)**
- Should the firm redirect R&D toward innovations that:
  - Are easy to protect with existing IP law?
  - Require complementary assets already within the firm's repertoire?
- Is the current R&D portfolio aligned with the firm's asset position?

**6B: Small vs. Large Firm Implications (大小企业对比)**
- Large firms: likely already possess relevant specialized/cospecialized assets → can milk even modest technology
- Small firms: likely lack relevant assets → must build, buy, or ally → higher risk
- Implications for the specific innovator's size and position

**6C: Industry Structure & Maturity (产业结构与成熟度)**
- Is the industry consolidating cospecialized assets under incumbents?
- Are new entry barriers rising?
- Should the innovator pursue alliances with incumbents as entry mechanism?

**6D: Manufacturing & International Competitiveness (制造能力与国际竞争力)**
- Is manufacturing a critical complementary asset for this innovation?
- If weak appropriability: is the innovator competitive at manufacturing?
- If not: can low-cost imitator-manufacturers capture all profits?
- Implications for "designer role" strategy (is it viable?)

**6E: Trade & Investment Barriers (贸易与投资壁垒)**
- Are there host government restrictions that block access to complementary assets abroad?
- Can host governments force licensing/JV structures that redistribute profits?
- Is market access itself a complementary asset controlled by government policy?

**6F: Organizational Implications (组织启示)**
- Public platform perspective: How to allocate R&D; which innovations to pursue
- Technology innovation perspective:
  - Active attack (主动进攻): Build innovation channels with lead users; profit from joint innovation using own complementary assets
  - Passive defense (被动防御): When core tech is easy to imitate, focus on complementary assets to prevent imitators from profiting

**Output for each activated module:**
- Specific findings and recommendations
- Connection back to the core framework assessment

## Built-In Case Library

The SKILL maintains 10 reference cases from the paper (and the organizational reading notes). Each case is used as an analogy benchmark during analysis.

| Case | Appropriability | Key Complementary Assets | Stage | Outcome | Key Lesson |
|---|---|---|---|---|---|
| EMI CAT Scanner | 弱 | Needed: marketing, service, manufacturing; had: none | 范式 | Innovator LOSES | Tech excellence without complementary assets = failure |
| IBM PC | 弱 | Had: brand (cospecialized), induced ecosystem (cospecialized) | 茓式 | Innovator WINS | Complementary assets beat technological advantage |
| NutraSweet | 强 | Built: manufacturing, brand, trade secrets | 茓式 | Innovator WINS | Tight appropriability + strategic asset building = sustained profits |
| RC Cola | 弱 | Needed: distribution, brand; had: none | 茓式 | Innovator LOSES | First-to-market advantage erased without complementary assets |
| Bowmar Calculator | 弱 | Needed: manufacturing, distribution | 茓式 | Innovator LOSES | Small innovator crushed by large imitators |
| Xerox Office PC | 弱 | Had: PARC tech; lacked: PC market assets | 茓式 | Innovator LOSES | Wrong complementary assets for the target market |
| de Havilland Comet | 弱 | Sunk into wrong design (irreversible) | 前范式 | Innovator LOSES | Wrong design choice in preparadigmatic phase = fatal |
| Apple LaserWriter | Mixed | Contracted with Canon (shared risk) | 茓式 | Innovator WINS (with risk) | Contractual mode with risk-sharing can work |
| IBM + Microsoft DOS | 弱 | IBM brand = cospecialized asset for Microsoft | 茓式 | Both benefit (short: IBM; long: MS) | Brand credibility as cospecialized asset |
| Union Carbide | 强 | Generic manufacturing assets | 茓式 | Innovator WINS | Tight appropriability + generic assets = licensing viable |

**Usage in analysis:** When assessing any dimension, reference the most analogous case(s) to ground the assessment in empirical evidence.

## Output Format

### Primary Output: Markdown Report

Structure:

```markdown
# Teece PFI 框架分析报告

## 1. 独占性制度评估
- [Classification: 强/弱]
- [Confidence: 高/中/低]
- [Evidence summary]
- [Case analogy]

## 2. 互补资产识别与分类
- [Asset inventory table]
- [Bottleneck identification]
- [Ownership map]

## 3. 主导设计阶段判断
- [Stage classification]
- [Evidence]
- [Strategic timing implications]

## 4. 相对位置评估
- [Three-player positioning map]
- [Lead time & cash constraints]

## 5. 策略推导与决策矩阵定位
- [Matrix cell placement]
- [Prescribed strategy]
- [Risk warnings]

## 6. 延伸分析 [if activated]
- [Module-specific findings]

## 核心结论
- [One-paragraph synthesis: who wins, why, what the innovator must do]

## 风险提示
- [Key uncertainties and failure modes]
```

### Optional Export

If user requests:
- **DOCX**: Generate a formatted consulting report using the docx skill
- **PPTX**: Generate a presentation deck using the pptx skill
- Offer these at the end of every analysis: "是否需要导出为 Word 咨询报告或 PowerPoint 演示文稿？"

## Execution Checklist

Before delivering the final report, verify:
1. All 6 steps have been executed (or explicitly skipped by user in Mode B)
2. Appropriability classification is supported by evidence, not just assertion
3. Every complementary asset is classified (通用型/专用型/共用型), not left vague
4. Dominant design stage has concrete evidence, not assumed
5. Strategy prescription matches the decision matrix logic (trace the IF-THEN chain)
6. At least one case analogy is referenced for each key assessment
7. Uncertain assessments are flagged with confidence levels
8. Output uses organization-standard terminology per the JSON mapping
9. Output language matches user input language
10. Optional export offer is included at the end
