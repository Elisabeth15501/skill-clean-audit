---
name: skill-clean-audit
slug: skill-clean-audit
displayName: 第一性原理 Clean Code 审计
version: 1.1.0
license: MIT
description: >
  第一性原理 clean code 审计法。从单根前提「代码是写给人看的」推导出两根判据——
  A. 理解成本（读起来费不费劲）/ B. 修改风险（改起来怕不怕），用红/黄/绿三档给代码打分，
  并明确允许「有意的、注释了的、范围可控的技术债」暂时存在。专用于审计你自己的
  WorkBuddy Skill 脚本或其他 Python 代码，产出带证据(文件:行)的可勾选报告。
  触发词：「用第一性原理审代码」「理解成本/修改风险」「clean code 审计」「审计我的 Skill 脚本」
  「按红黄绿审代码」「clean code 审计样例」。注意：本 skill 只做可读性/可维护性的第一性原理审计，
  不做通用 PR/MR 审查（那用 code-review-assistant 或 critical-code-reviewer），
  不替代 clean-code 的写代码规范手册，也不做 lint/格式化（那用 project-code-standard）。
  ---
  First-Principles Clean Code Audit. Derives two criteria from one root premise — "code is written for humans":
  A. Comprehension cost (how hard to read) / B. Change risk (how scary to modify) — scored red/amber/green,
  explicitly permitting intentional, documented, scoped tech debt. Audits your own WorkBuddy skill scripts or
  Python code, emitting an evidence-backed (file:line) checklist report. Triggers: "audit code with first principles",
  "comprehension/change risk", "clean code audit", "audit my skill scripts". Read-only: emits findings, never edits.
  Note: this skill does first-principles readability/maintainability audit only — not generic PR/MR review
  (use code-review-assistant / critical-code-reviewer), not a style handbook (use clean-code),
  and not lint/format (use project-code-standard).
summary: 第一性原理 Clean Code 审计法——只读审计你自己的 WorkBuddy Skill 脚本 / Python 代码，用「理解成本 / 修改风险」两轴 + 红黄绿，产出带证据 (file:line) 的可勾选报告；方法论从单根前提推导，不依赖任何外部二进制或凭据。
tags:
  - clean-code
  - code-audit
  - readability
  - maintainability
  - static-analysis
  - skill-tooling
---

# 第一性原理 Clean Code 审计 / First-Principles Clean Code Audit

## 合规与边界声明（网络访问）/ Compliance & Boundary Statement (Network Access)

- 本 skill **不发起任何网络请求**，不调用任何第三方 / 海外 API，不读取任何凭据、密钥或环境变量，仅读取用户**显式指定**的本地代码文件做只读审计。
  This skill makes **no network requests**, calls no third-party / overseas API, reads no credentials, secrets, or env vars; it only reads user-**explicitly-specified** local code files for a read-only audit.
- **不提供、不指导、不支持任何规避网络管理措施的能力**；不使用非公开接口、不破解访问控制、不伪造身份绕过鉴权。
  Provides / instructs / supports **no means to circumvent network-management measures**; no private interfaces, no access-control bypass, no identity spoofing.
- 无「数据源 / 海外源」概念——全部输入来自本地文件，故「海外源不可达需降级」场景不适用（N/A）。
  No "data source / overseas source" concept — all input is local, so "overseas source unreachable → degrade" is N/A.
- 若运行环境禁止网络，本 skill 行为完全不受影响（它本就不联网）。
  If the runtime forbids network, this skill is unaffected (it never goes online).
- **Requirements（声明与行为一致 / declared == behaved）**：无需任何外部二进制（python/git/gh/node/npx/shell 均不调用）、无需任何环境变量、无需任何凭据。审计纯靠阅读+推理，无任何运行时依赖。
  **Requirements (declared == behaved)**: requires no external binaries (calls no python/git/gh/node/npx/shell), no env vars, no credentials. Audit is pure read+reason — zero runtime dependencies.

## 它是什么 / 不是什么 / What it is / is not

**是 / Is**：一个审计方法论 + 可落地产物。拿两根判据去戳代码，逐项打勾带证据，出报告。
An audit methodology + a concrete artifact. Pokes code with two criteria, ticks items with evidence, emits a report.

**不是 / Is not**（明确边界，避免和已有 skill 重叠 / explicit boundaries, to avoid overlap with existing skills）：

- ❌ 通用 PR/MR 审查 → 用 `code-review-assistant` / `critical-code-reviewer`
- ❌ 写代码的标准手册 → 用 `clean-code`（SRP/DRY/KISS 那套）
- ❌ lint/格式化执行 → 用 `project-code-standard`（ruff/eslint/prettier）
- ❌ SOLID / 干净架构 / TDD 原则库 → 用 `uncle-bob`（本 skill 只从第一性原理**推导**，不抄它的规则；见 `references/smells_crosswalk.md` 做等价桥接）

本 skill 的价值在三点，现有 skill 都没有：① 规则是**推导**出来的不是给定的；② 用**成本/风险**两轴而非类别桶；③ 允许**有意的债**。
Three things no existing skill does: ① rules are *derived*, not given; ② a cost/risk two-axis model, not category buckets; ③ permits *intentional debt*.

## 第一性原理推导 / First-Principles Derivation

1. **根前提 / Root premise**：代码是写给人看的。机器只认语法对不对，不在乎命名/长度/注释；代码真正的生命周期在「被另一个人（含未来的你）阅读、修改、维护」的那无数次里。
   Code is written for humans. Machines only care whether syntax is valid, not naming/length/comments; code's real life is in the countless times it is read, modified, maintained by another person (including future you).
2. 由此只推出两根判据 / From this, only two criteria follow:
   - **A. 理解成本 / Comprehension cost** —— 让人一眼读懂意图与边界 So intent and boundaries are obvious at a glance.
   - **B. 修改风险 / Change risk** —— 改动时不牵连出错 So a change doesn't quietly break something else.
3. 所有具体规则都是这两根的子树。检验不过「是否真的降低了理解和修改成本」的，就是噪音。
   Every concrete rule is a subtree of these two. Anything that fails "does it actually lower comprehension or change cost?" is noise.

> 关键反推 / Key reversal：为凑清单而清单（为短拆七层 tiny function、为 DRY 抽象没人用的接口）反而抬高成本，是脏的。
> Checklist-for-its-own-sake raises cost — that is dirty.

## 严重度（红黄绿）/ Severity (Red / Amber / Green)

- 🔴 **红 · 出现即脏，优先修 / Red · dirty on sight, fix first**：符号来源隐式（`import *`）、重复/矛盾的说明、注释退化成 changelog（满屏工单号）、模块级可变全局状态控行为、命名与行为不一致 / 隐藏副作用（CQS 违反：函数名像查询却偷偷改状态或打印）、重复逻辑（DRY 违反）、裸 `except` 静默吞错。
  Implicit symbol origin (`import *`), contradictory docs, comments degraded into a changelog, module-level mutable global controlling behavior, name≠behavior / hidden side effects (CQS violation), duplicated logic (DRY violation), bare `except` swallowing errors.
- 🟡 **黄 · 有意的债，需注释 + 范围可控 / Amber · intentional debt, needs comment + scope**：长函数（>40 行但确内聚难拆）、魔法数字/字符串未命名、有意的 best-effort `except`（单源失败不拖垮管线）。黄=暂时可接受，但必须写清「为什么」且范围可控。
  Long functions (>40 lines but cohesive), unnamed magic numbers/strings, intentional best-effort `except`. Amber = temporarily acceptable, but the "why" must be written and scope controlled.
- 🟢 **绿 · 出现即干净 / Green · clean on sight**：命名即文档、显式优于隐式、行为只由入参决定、有测试覆盖、所有 `except` 均精确。
  Naming is documentation, explicit beats implicit, behavior depends only on inputs, tested, every `except` precise.

完整可勾选清单见 **`assets/clean_code_checklist.html`**（打开即可逐项打勾，带实时计数）。
Full interactive checklist: **`assets/clean_code_checklist.html`** (open to tick items, with a live counter).

## 轻量指标信号（核查提示，非硬规则）/ Lightweight Metric Signals (hints, not hard rules)

以下数字只作「值得多看一眼」的探针，**不是自动判红**。第一性原理的判据永远是 A/B 两轴，指标只是帮你更快定位疑点：
The numbers below are only probes for "worth a closer look" — **not automatic red flags**. The first-principles criteria remain the A/B axes; metrics just help you locate suspects faster:

- 函数行数 > 40：可能是 **A** 信号，需看是否仍内聚；若内聚难拆，归黄。
  Function > 40 lines: possible **A** signal; check cohesion; if hard to split, amber.
- 参数数 ≥ 4：可能是 **A** 信号（调用处难读懂意图），优先抽 options 对象。
  Params ≥ 4: possible **A** signal (call site hard to read); prefer an options object.
- 嵌套深度 ≥ 4（if/for/try 层层套）：**A** 信号，读者需脑内维护多个上下文。
  Nesting ≥ 4: **A** signal, reader must hold multiple contexts in head.
- 布尔旗参数（`def f(..., dry_run=False)`）：**A** 信号，函数实际做两件相反的事，违反单一职责。
  Boolean flag params: **A** signal, the function does two opposite things (SRP violation).
- 单文件/单函数内同类逻辑重复 ≥ 3 次：**B** 信号（DRY 违反，改一处忘一处）。
  Same logic repeated ≥ 3× in a file/function: **B** signal (DRY violation, fix-one-forget-another).

> 重申 / Restated：指标命中 ≠ 脏。若它能用「注释说清 + 范围可控」解释，且真降低了理解/修改成本，仍是干净的。指标只为节省你逐行扫的时间。
> Metric hit ≠ dirty. If explained by "comment + scoped" and it truly lowers cost, it stays clean. Metrics only save you line-by-line scanning time.

## 审计流程 / Audit Flow

1. **读目标文件 / Read the target**：把要审的函数/模块完整读出来，不要凭印象。Read the whole function/module; don't audit from memory.
2. **逐项对照清单 / Check against the list**：对 `assets/clean_code_checklist.html` 每一项，判断在目标代码里是否命中。常见 smell 的标准命名（Rigidity/Fragility/Opacity…）对照见 **`references/smells_crosswalk.md`**，便于把发现标准化。
   For each item in `assets/clean_code_checklist.html`, judge whether it hits. Standard smell names (Rigidity/Fragility/Opacity…) crosswalk: **`references/smells_crosswalk.md`**.
3. **带证据打勾 / Tick with evidence**：每条命中必须给 `文件:行号` 和一句话「它抬高了 A 还是 B、怎么抬的」。无证据的直觉不打勾。
   Every hit needs `file:line` and one sentence on whether it raises A or B, and how. No evidence, no tick.
4. **数红黄绿 / Count red/amber/green**：用清单底部计数器或手算；指标信号（上节）可辅助定位，但不计入严重度。
   Use the checklist counter or count by hand; metric signals help locate but don't count toward severity.
5. **出报告 / Emit report**：格式见下方「输出格式」，完整范例见 **`references/clean_code_audit_sample.md`**（那是一份用合成示例脚本 `demo-skill/scripts/aggregate.py` 的 `main()` 真审出来的样例，照它的结构写；样例片段自带行号、可逐行核对，不对应任何真实项目）。
   Format below; full sample: **`references/clean_code_audit_sample.md`** (a real audit of synthetic `demo-skill/scripts/aggregate.py`; snippet is line-numbered, checkable, maps to no real project).

## 输出格式 / Output Format

落盘到**当前 agent 会话的工作区根目录**（即本对话打开的项目目录，例如 `~/WorkBuddy/<session>/`），文件名 `clean_code_audit_<target>.md`，结构：
Write to the **current agent session's workspace root** (the opened project dir, e.g. `~/WorkBuddy/<session>/`), filename `clean_code_audit_<target>.md`, structure:

- 表头：审计对象（路径 + 函数/行范围 + 行数） / Header: target (path + function/line range + line count)
- **A. 理解成本 / Comprehension cost** 表：# / 清单项 / 命中(✅红·✅黄·⬜未命中·❌未达标) / 证据(行) / 说明
- **B. 修改风险 / Change risk** 表：同上 / same as above
- **额外发现**（可选，不在清单内但同属理解成本的 smells，如嵌套条件难读）/ **Extra findings** (optional, smells outside the list but still comprehension cost, e.g. unreadable nested conditions)
- **审计评分 / Score**：红 N / 黄 N / 绿 N（+ 未命中/未核实项）
- **结论 / Conclusion**：按第一性原理说清「脏」偏在哪一侧、修改优先级建议（先消零行为风险的纯可读项，再排重复/拆函数，黄项随改顺手处理）
  Per first principles, state which side "dirty" leans toward and the fix priority (kill zero-behavior-risk pure-readability items first, then dedupe/split; handle amber along the way).

## 修复优先级：增量清理（Boy Scout）/ Fix Priority: Incremental Cleanup (Boy Scout)

本 skill 只读不改，但报告「结论」段的优先级建议按此原则给：
This skill reads only, but the report's "conclusion" priority follows this principle:

- 🔴 红项 / Red：你**本来就要改这个文件**时，顺手清掉；不要为清它而专门开 PR 动一个稳定、无人碰的文件。
  Clear it when you're *already* editing that file; don't open a PR just to clean a stable, untouched file.
- 🟡 黄项 / Amber：保持「注释说清 + 范围可控」即可，**不主动还债**；等下次自然触达时再评估。
  Keep "comment + scoped"; don't pay it down proactively; re-evaluate on next natural touch.
- 不带测试覆盖的 Skill 脚本 / Skill scripts without tests：测试「有则绿、无不算红」——Skill 脚本多为一次性工具，强求单测是过度工程，反而抬高理解成本。
  Tests "green if present, not red if absent" — skill scripts are mostly one-off tools; demanding unit tests is over-engineering that raises cost.

> 底层逻辑仍是第一性原理：重构也要花理解成本。只对「正在被修改、因而修改风险本就升高」的代码投资清理，才划算；对无人碰的代码提前重构，是净亏。
> Same first principle: refactoring also costs comprehension. Only invest cleanup in code *already being modified* (where change risk is already high); pre-refactoring untouched code is a net loss.

## 判据不是清单 / Criteria, not a checklist

收尾必须点明：红的全修；黄了只要「注释说清 + 范围可控」就先留着；绿的出现说明干净。同一处若「为清单而清单」反而是脏的。本 skill 只读不改——若要落地修复，另开一轮按优先级逐个 PR。
Closing note: fix all red; keep amber if "comment + scoped"; green means clean. Checklist-for-its-own-sake is itself dirty. This skill reads only — for fixes, open a separate prioritized pass.

## 交付物 / Deliverables

- 把 **`assets/clean_code_checklist.html`** 复制到**当前 agent 工作区根目录**（命名 `clean_code_checklist.html`），作为可反复使用的交互式清单；下次审计直接打开它打勾。
  Copy **`assets/clean_code_checklist.html`** to the **workspace root** (as `clean_code_checklist.html`) for reuse; open it next audit to tick.
- 把审计报告写到**当前 agent 工作区根目录** `clean_code_audit_<target>.md`，并调用 `present_files` 把该文件（及清单）呈现给用户预览。
  Write the audit report to the **workspace root** `clean_code_audit_<target>.md` and call `present_files` to preview it (and the checklist) for the user.
- 生成物（`clean_code_audit_*.md` / `clean_code_checklist*.html`）已被仓库 `.gitignore` 忽略，不进版本控制。
  Generated artifacts (`clean_code_audit_*.md` / `clean_code_checklist*.html`) are git-ignored, never version-controlled.

## 维护须知 / Maintenance Notes

- 若今后在 `references/` 新增会读环境变量或调用二进制的脚本，必须同步在 `metadata.openclaw.requires.env` / `requires.bins` 声明（ClawHub 的 mismatch 审核红线）。当前本 skill 无任何此类依赖。
  If you later add a script that reads env vars or calls binaries, declare it in `metadata.openclaw.requires.env` / `requires.bins` (ClawHub's mismatch-audit red line). This skill has none today.
- 多平台发布：源仓库 frontmatter 保留 `license: MIT` 供 SkillHub；ClawHub 导出副本由发布脚本剥离 `license` 字段并排除 LICENSE（见 `.clawhubignore`）。
  Multi-platform: the source keeps `license: MIT` for SkillHub; the ClawHub export strips the `license` field and excludes LICENSE (see `.clawhubignore`).
