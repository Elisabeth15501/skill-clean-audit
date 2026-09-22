# skill-clean-audit

> 第一性原理 Clean Code 审计法 —— 一个**只读、可读、可复用**的 Agent Skill。

从单根前提「**代码是写给人看的**」推导出两根判据，用红/黄/绿三档给代码打分，
并明确允许「有意的、注释了的、范围可控的技术债」暂时存在。

专用于审计你自己的 **WorkBuddy / Claude / 任意 Agent 的 Skill 脚本**或其他 Python 代码，
产出带证据（`文件:行号`）的可勾选报告。**本 skill 只读不改**——修复交给下一轮。

---

## 为什么它不是「又一个 clean code skill」

市场上有三类相关 skill，本 skill 占的是它们都没做好的交叉缝：

| 红海 | 代表 | 本 skill 的差异 |
|---|---|---|
| 审应用 / PR 代码（正确·安全·性能） | code-review、review-pr、smart-code-review | 不审正确性，只审**可读性 / 可维护性**（理解成本与修改风险） |
| 列 clean code 规则手册 | clean-code（SRP/DRY/KISS） | 规则是**推导**出来的，不是给定的教条 |
| 审 skill 的安全性 | skill-vetting、agent-skills-audit | 只审**自身脚本的可读性**，零网络、零凭据、只读 |

**三个差异化**：① 规则由第一性原理推出；② 用「成本 vs 风险」两轴而非类别桶；③ 允许有意的债（黄档）。

---

## 第一性原理推导

1. **根前提**：代码是写给人看的。机器只认语法对不对，不在乎命名 / 长度 / 注释；代码真正的生命周期在「被另一个人（含未来的你）阅读、修改、维护」的那无数次里。
2. 由此只推出两根判据：
   - **A. 理解成本** —— 让人一眼读懂意图与边界。
   - **B. 修改风险** —— 改动时不牵连出错。
3. 所有具体规则都是这两根的子树。检验不过「是否真的降低了理解和修改成本」的，就是噪音。

> 关键反推：为凑清单而清单（为短拆七层 tiny function、为 DRY 抽象没人用的接口）反而抬高成本，是脏的。

---

## 严重度（红 / 黄 / 绿）

- 🔴 **红 · 出现即脏，优先修**：`import *` 来源隐式、重复/矛盾的说明、注释退化成 changelog（满屏工单号）、模块级可变全局状态控行为、重复逻辑（DRY 违反）、裸 `except` 静默吞错。
- 🟡 **黄 · 有意的债，需注释 + 范围可控**：长函数（>40 行但确内聚难拆）、魔法数字/字符串未命名、有意的 best-effort `except`（单源失败不拖垮管线）。黄 = 暂时可接受，但必须写清「为什么」且范围可控。
- 🟢 **绿 · 出现即干净**：命名即文档、显式优于隐式、行为只由入参决定、有测试覆盖、所有 `except` 均精确。

完整可勾选清单见 **[`assets/clean_code_checklist.html`](assets/clean_code_checklist.html)**（浏览器打开即可逐项打勾，带实时计数）。

---

## 目录结构

```
skill-clean-audit/
├── SKILL.md                       # 方法论 + 审计流程 + 输出格式 + 边界声明
├── LICENSE                        # MIT（开源用，不进 SkillHub 发布包）
├── README.md                      # 本文件
├── .gitignore
├── assets/
│   └── clean_code_checklist.html  # 交互式可勾清单（审计时复制到工作区复用）
└── references/
    └── clean_code_audit_sample.md # 完整范例：拿 agent-analytics-report 的 main() 真审出来
```

---

## 用法

### 在 WorkBuddy 里

把整个目录放进 `~/.workbuddy/skills/skill-clean-audit/`，对话中说：

> 「用第一性原理审一下 `~/.workbuddy/skills/ai-weekly/scripts/generate_site.py`」

或任一触发词：`理解成本/修改风险`、`clean code 审计`、`审计我的 Skill 脚本`、`按红黄绿审代码`。

它会把 `assets/clean_code_checklist.html` 复制到你的工作区，并把报告写成 `<workspace>/clean_code_audit_<target>.md`。

### 方法论迁移到其他平台

SKILL.md 里的「边界声明」写的是 WorkBuddy 的等价技能名（如 `code-review-assistant`）。
这份方法论本身与平台无关——把它里的两根判据 + 红黄绿 套到你平台的任意脚本即可，不必重写逻辑。

---

## 与其他工具的边界（避免重叠）

- ❌ 通用 PR/MR 审查 → 用你平台的等价 PR 审查工具
- ❌ 写代码的标准手册 → 用 clean-code（SRP/DRY/KISS 那套）
- ❌ lint / 格式化执行 → 用 project-code-standard（ruff/eslint/prettier）
- ✅ 本 skill 只做**可读性 / 可维护性的第一性原理审计**，且**只读不改**

---

## 许可证

[MIT](LICENSE) © 2026 Elisabeth15501 (Chen Yanting)
