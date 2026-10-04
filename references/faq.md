# 常见问题 / FAQ

> 审计方法论、边界与产物行为的集中解答。每条尽量短，避免和主文档重复。
> Central FAQ for the audit method, boundaries, and artifact behavior. Kept short to avoid duplicating the main doc.

## 1. 能帮我改代码吗？
不能。本 skill **只读审计**，产出报告与修复优先级建议，但不在被审计代码上改任何一个字。若要落地修复，另开一轮，按报告「结论」的优先级逐个 PR（见《修复优先级：增量清理》）。
No. This skill **audits read-only** and emits a report with fix-priority advice, but changes not a single character of the code under review. To apply fixes, open a separate pass, one PR at a time per the report's conclusion priority.

## 2. 和 code-review-assistant / clean-code / project-code-standard 区别？
- `code-review-assistant` / `critical-code-reviewer`：通用 PR/MR 审查，会逐 diff 给建议、可批注。本 skill 不做 diff 审查。
- `clean-code`：写代码的规范手册（SRP/DRY/KISS 那套现成规则）。本 skill 不抄规则，而是从「代码是写给人看的」**推导**判据。
- `project-code-standard`：lint/格式化执行（ruff/eslint/prettier）。本 skill 不执行格式化。
Difference: those do PR review / style handbook / lint execution. This skill only does first-principles readability-maintainability audit and derives its own criteria.

## 3. 报告写到哪？
当前 agent 会话的**工作区根目录**，文件名 `clean_code_audit_<target>.md`；**不覆盖**已有同名报告（避免静默丢失你之前的审计）。
Workspace root of the current session, as `clean_code_audit_<target>.md`; never overwrites an existing same-name report.

## 4. 大文件 / 整目录怎么审？
- 超大文件（>2000 行）：先聚焦某个函数/模块，避免一次性扫全文件导致严重度失真；若确需整文件，按 ~500 行分段逐段审后汇总。
- 整 Skill 目录：逐个脚本审，优先挑最常被修改的那几个（修改风险本就高）。
Large file (>2000 lines): scope to one function/module first; if the whole file is needed, audit in ~500-line chunks and combine. Whole skill dir: script by script, prioritize the most-frequently-changed ones.

## 5. 指标命中就代表脏吗？
不。5 项轻量指标（函数>40行 / 参数≥4 / 嵌套≥4 / 布尔旗 / 重复≥3）只是「值得多看一眼」的探针，**判据永远是 A/B 两轴**。若能用「注释说清 + 范围可控」解释且真降成本，仍是干净的。
No. The 5 lightweight metric signals are only probes for "worth a closer look"; the criteria remain the A/B axes. If explained by comment + scoped and it truly lowers cost, it stays clean.

## 6. 支持哪些语言？
Python（.py）为主；WorkBuddy Skill 脚本常含 .py / .js / .ts；以及任何**人类可读的源代码文本**。不接受二进制 / 图片 / 数据文件 / 加密或混淆代码。
Python (.py) primarily; skill scripts often .py / .js / .ts; any human-readable source text. Not binaries / images / data / obfuscated code.

## 7. 需要联网 / API key 吗？
不需要。纯本地只读审计，零网络、零凭据、零运行时依赖。可选 `scripts/metric_probe.py` 也是纯 Python 标准库、零网络、零凭据、只读。
No. Pure local read-only audit — zero network, zero credentials, zero runtime dependencies. The optional `scripts/metric_probe.py` is also pure Python stdlib, offline, no credentials, read-only.
