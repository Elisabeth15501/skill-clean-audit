# skill-clean-audit

> 第一性原理 Clean Code 审计法 —— 一个**只读、可读、可复用**的 Agent Skill。当前版本 **v1.1.0**。
> First-Principles Clean Code Auditor — a **read-only, readable, reusable** agent skill. Current version **v1.1.0**.

**合规 / Compliance**：纯本地只读审计，不联网、不读凭据、无第三方接口，不提供 / 不指导 / 不支持任何规避网络管理措施的能力。详见 SKILL.md《合规与边界声明》。
Purely local, read-only audit: no network, no credentials, no third-party APIs; provides / instructs / supports no means to circumvent network-management measures. See *Compliance & Boundary Statement* in SKILL.md.

从单根前提「**代码是写给人看的**」推导出两根判据，用红/黄/绿三档给代码打分，
并明确允许「有意的、注释了的、范围可控的技术债」暂时存在。
From one root premise — **"code is written for humans"** — it derives two criteria and scores code red / amber / green,
explicitly permitting *intentional, documented, scoped* tech debt to remain.

专用于审计你自己的 **WorkBuddy / Claude / 任意 Agent 的 Skill 脚本**或其他 Python 代码，
产出带证据（`文件:行号`）的可勾选报告。**本 skill 只读不改**——修复交给下一轮。
Built to audit your own **WorkBuddy / Claude / any-agent skill scripts** or other Python code,
emitting an evidence-backed (`file:line`) checklist report. **This skill reads only, never edits** — fixes go to the next pass.

---

## 为什么它不是「又一个 clean code skill」 / Why it is not "yet another clean-code skill"

市场上有三类相关 skill，本 skill 占的是它们都没做好的交叉缝：
Three families of related skills exist; this one occupies the gap none of them fills well:

| 红海 Red ocean | 代表 Representative | 本 skill 的差异 Our difference |
|---|---|---|
| 审应用 / PR 代码（正确·安全·性能） App / PR code (correctness·security·perf) | code-review、review-pr、smart-code-review | 不审正确性，只审**可读性 / 可维护性**（理解成本与修改风险） Audits readability / maintainability only (comprehension & change risk), not correctness |
| 列 clean code 规则手册 Rule handbooks | clean-code（SRP/DRY/KISS） | 规则是**推导**出来的，不是给定的教条 Rules are *derived*, not dogmatic givens |
| 审 skill 的安全性 Skill security | skill-vetting、agent-skills-audit | 只审**自身脚本的可读性**，零网络、零凭据、只读 Audits only its own scripts' readability — zero network, zero credentials, read-only |

**三个差异化 / Three differentiators**：① 规则由第一性原理推出 Rules derived from first principles；② 用「成本 vs 风险」两轴而非类别桶 Two axes (cost vs risk), not category buckets；③ 允许有意的债（黄档）Permits intentional debt (amber tier).

---

## 第一性原理推导 / First-Principles Derivation

1. **根前提 / Root premise**：代码是写给人看的。机器只认语法对不对，不在乎命名 / 长度 / 注释；代码真正的生命周期在「被另一个人（含未来的你）阅读、修改、维护」的那无数次里。
   Code is written for humans. Machines only care whether syntax is valid, not naming / length / comments; code's real life is in the countless times it is read, modified, and maintained by another person (including future you).
2. 由此只推出两根判据 / From this, only two criteria follow:
   - **A. 理解成本 / Comprehension cost** —— 让人一眼读懂意图与边界 So intent and boundaries are obvious at a glance.
   - **B. 修改风险 / Change risk** —— 改动时不牵连出错 So a change doesn't quietly break something else.
3. 所有具体规则都是这两根的子树。检验不过「是否真的降低了理解和修改成本」的，就是噪音。
   Every concrete rule is a subtree of these two. Anything that fails "does it actually lower comprehension or change cost?" is noise.

> 关键反推 / Key reversal：为凑清单而清单（为短拆七层 tiny function、为 DRY 抽象没人用的接口）反而抬高成本，是脏的。
> Checklist-for-its-own-sake (splitting into seven tiny functions to be short, abstracting unused interfaces for DRY) raises cost — that is dirty.

---

## 严重度（红 / 黄 / 绿）/ Severity (Red / Amber / Green)

- 🔴 **红 · 出现即脏，优先修 / Red · dirty on sight, fix first**：`import *` 来源隐式 implicit `import *`、重复/矛盾的说明 contradictory docs、注释退化成 changelog（满屏工单号）comments degraded into a changelog、模块级可变全局状态控行为 module-level mutable global controlling behavior、命名与行为不一致 / 隐藏副作用（CQS 违反）name≠behavior / hidden side effects (CQS violation)、重复逻辑（DRY 违反）duplicated logic (DRY violation)、裸 `except` 静默吞错 bare `except` swallowing errors.
- 🟡 **黄 · 有意的债，需注释 + 范围可控 / Amber · intentional debt, needs comment + scope**：长函数（>40 行但确内聚难拆）long functions (>40 lines but cohesive)、魔法数字/字符串未命名 unnamed magic numbers/strings、有意的 best-effort `except`（单源失败不拖垮管线）intentional best-effort `except`. Amber = temporarily acceptable, but the "why" must be written and the scope controlled.
- 🟢 **绿 · 出现即干净 / Green · clean on sight**：命名即文档 naming is documentation、显式优于隐式 explicit beats implicit、行为只由入参决定 behavior depends only on inputs、有测试覆盖 tested、所有 `except` 均精确 every `except` is precise.

完整可勾选清单见 **[`assets/clean_code_checklist.html`](assets/clean_code_checklist.html)**（浏览器打开即可逐项打勾，带实时计数）。
Full interactive checklist: **[`assets/clean_code_checklist.html`](assets/clean_code_checklist.html)** (open in a browser to tick items, with a live counter).

---

## 目录结构 / Directory Layout

```
skill-clean-audit/
├── SKILL.md                       # 方法论 + 审计流程 + 输出格式 + 边界声明 + 合规声明
│                                   # methodology + audit flow + output format + boundaries + compliance
├── LICENSE                        # MIT（开源用；不进 SkillHub / ClawHub 发布包）
│                                   # MIT (for open source; excluded from SkillHub / ClawHub publish packages)
├── README.md                      # 本文件（中英对照）。注意：ClawHub 发布包不含 README.md
│                                   # this file (bilingual). NOTE: ClawHub publish package omits README.md
├── CHANGELOG.md                   # 版本记录 version history
├── .gitignore                     # 忽略生成的审计报告/清单 ignores generated audit artifacts
├── .clawhubignore                 # ClawHub 排除清单（含 LICENSE）ClawHub exclusion manifest (incl. LICENSE)
├── assets/
│   └── clean_code_checklist.html  # 交互式可勾清单（审计时复制到工作区复用）
│                                   # interactive checklist (copied to workspace for reuse during audit)
└── references/
    ├── clean_code_audit_sample.md # 完整范例：用合成示例脚本 demo-skill 的 main() 真审出来
    │                               # full sample: a real audit of synthetic demo-skill's main()
    └── smells_crosswalk.md        # Uncle Bob 气味 → A/B 轴 + 红黄绿 桥接表
    │                               # Uncle Bob smells → A/B axes + red/amber/green crosswalk
```

---

## 用法 / Usage

### 在 WorkBuddy 里 / In WorkBuddy

把整个目录放进 `~/.workbuddy/skills/skill-clean-audit/`，对话中说：
Place the whole directory at `~/.workbuddy/skills/skill-clean-audit/`, then in chat say:

> 「用第一性原理审一下 `~/.workbuddy/skills/demo-skill/scripts/aggregate.py`」
> "Audit `~/.workbuddy/skills/demo-skill/scripts/aggregate.py` with first principles"

或任一触发词 / or any trigger：`理解成本/修改风险`、`clean code 审计`、`审计我的 Skill 脚本`、`按红黄绿审代码`
comprehension/change risk, clean code audit, audit my skill scripts, score code red/amber/green.

它会把 `assets/clean_code_checklist.html` 复制到你的工作区，并把报告写成 `<workspace>/clean_code_audit_<target>.md`。
It copies `assets/clean_code_checklist.html` into your workspace and writes the report to `<workspace>/clean_code_audit_<target>.md`.

### 方法论迁移到其他平台 / Porting the method to other platforms

SKILL.md 里的「边界声明」写的是 WorkBuddy 的等价技能名（如 `code-review-assistant`）。
The *Boundary Statement* in SKILL.md names WorkBuddy's equivalent skills (e.g. `code-review-assistant`).
这份方法论本身与平台无关——把它里的两根判据 + 红黄绿 套到你平台的任意脚本即可，不必重写逻辑。
The method is platform-agnostic — apply its two criteria + red/amber/green to any script on your platform; no rewrite needed.

---

## 与其他工具的边界（避免重叠）/ Boundaries vs Other Tools (avoid overlap)

- ❌ 通用 PR/MR 审查 / Generic PR/MR review → 用你平台的等价 PR 审查工具 use your platform's PR-review tool
- ❌ 写代码的标准手册 / Code-style handbook → 用 clean-code（SRP/DRY/KISS 那套 use clean-code (SRP/DRY/KISS)
- ❌ lint / 格式化执行 / Lint / format → 用 project-code-standard（ruff/eslint/prettier use project-code-standard (ruff/eslint/prettier)
- ✅ 本 skill 只做**可读性 / 可维护性的第一性原理审计**，且**只读不改**
  ✅ This skill only does **first-principles readability / maintainability audit**, and **reads only, never edits**

---

## 许可证 / License

MIT © 2026

> 多平台发布说明 / Multi-platform note: 本仓库（GitHub / SkillHub）以 MIT 分发；ClawHub 发布包按平台规则默认套用 **MIT-0**（由 `.clawhubignore` 排除 LICENSE 并剥离 frontmatter 的 `license` 字段）。
> This repo (GitHub / SkillHub) is distributed under MIT; the ClawHub package defaults to **MIT-0** per platform policy (LICENSE excluded via `.clawhubignore`, `license` field stripped from frontmatter).
