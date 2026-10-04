# FAQ

> Central answers for the audit method, boundaries, and artifact behavior. Kept short to avoid duplicating the main doc.
> 审计方法论、边界与产物行为的集中解答。每条尽量短，避免和主文档重复。

## 1. Will it edit my code for me?
No. This skill **audits read-only** and emits a report with fix-priority advice, but changes not a single character of the code under review. To apply fixes, open a separate pass, one PR at a time per the report's conclusion priority (see "Fix Priority: Incremental Cleanup").
不能。本 skill **只读审计**，产出报告与修复优先级建议，但不在被审计代码上改任何一个字。若要落地修复，另开一轮，按报告「结论」的优先级逐个 PR。

## 2. How is it different from code-review-assistant / clean-code / project-code-standard?
- `code-review-assistant` / `critical-code-reviewer`: generic PR/MR review with per-diff advice and annotations. This skill does not do diff review.
- `clean-code`: a style handbook (off-the-shelf SRP/DRY/KISS rules). This skill does not copy rules; it *derives* criteria from "code is written for humans".
- `project-code-standard`: lint/format execution (ruff/eslint/prettier). This skill does not run formatting.
区别：那些做 PR 审查 / 规范手册 / lint 执行。本 skill 只做第一性原理可读性-可维护性审计，并自行推导判据。

## 3. Where does the report go?
The **workspace root** of the current agent session, as `clean_code_audit_<target>.md`; it **never overwrites** an existing same-name report (avoids silently losing your earlier audit).
当前 agent 会话的**工作区根目录**，文件名 `clean_code_audit_<target>.md`；**不覆盖**已有同名报告。

## 4. How do I audit a huge file / a whole directory?
- Very large file (>2000 lines): scope to one function/module first to avoid a full-file sweep distorting severity; if the whole file is needed, audit in ~500-line chunks and combine.
- Whole skill directory: script by script, prioritizing the most-frequently-changed ones (high change risk by nature).
超大文件（>2000 行）：先聚焦函数/模块；确需整文件则按 ~500 行分段汇总。整目录：逐脚本审，优先最常改的。

## 5. Does a metric hit mean it's dirty?
No. The 5 lightweight signals (function >40 lines / params ≥4 / nesting ≥4 / boolean flag / dup ≥3) are only probes for "worth a closer look"; the criteria remain the A/B axes. If explained by comment + scoped and it truly lowers cost, it stays clean.
不。5 项轻量指标只是探针，判据永远是 A/B 两轴。能注释说清+范围可控且真降成本，仍干净。

## 6. Which languages are supported?
Python (.py) primarily; skill scripts often .py / .js / .ts; and any **human-readable source text**. Not binaries / images / data files / obfuscated code.
Python（.py）为主；Skill 脚本常含 .py / .js / .ts；及任何人类可读源码文本。不接受二进制/图片/数据/混淆代码。

## 7. Does it need network / an API key?
No. Pure local read-only audit — zero network, zero credentials, zero runtime dependencies. The optional `scripts/metric_probe.py` is also pure Python stdlib, offline, no credentials, read-only.
不需要。纯本地只读，零网络零凭据零依赖。可选 `scripts/metric_probe.py` 也是纯 stdlib、离线、无凭据、只读。
