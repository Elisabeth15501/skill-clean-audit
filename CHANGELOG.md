# Changelog

## v1.1.0 (2026-09-25)

ClawHub 发布前优化 + 中英对照文档（能力不变）：

- **文档中英对照 / Bilingual docs**：`README.md` 全文改为中文 + 英文段落；`SKILL.md` 的 `description` 与各级 `##` 标题加英文副标题，便于国际平台（ClawHub / OpenClaw）发现与扫描。
- **ClawHub 合规前置 / ClawHub hardening**：
  - 新建 `.clawhubignore`，排除 `LICENSE`（与 ClawHub 强制 MIT-0 冲突，S1/S3/S5）与 `scripts/`（开发者构建脚本 `scripts/clean_code_clawhub_export.py` 只用于本地生成发布副本，不是技能可加载内容，不随包发布）；并把 `.clawhubignore` 加进 `.gitignore`，避免泄漏进 SkillHub 的 `git archive` 导出包。
  - `SKILL.md`《合规与边界声明》补一行可见的 `Requirements（声明与行为一致）`：无需外部二进制 / 环境变量 / 凭据（S4 扫描器读正文校验）。
  - 新增《维护须知》一节，写明「未来脚本若读 env / 调二进制须声明 `metadata.openclaw.requires`」红线（S1 mismatch 审核）。
  - 源仓库 frontmatter 仍保留 `license: MIT` / `slug` / `displayName`（供 SkillHub）；这些字段由 ClawHub 导出脚本剥离，不在发布包内。
- 多平台授权说明：GitHub / SkillHub 副本仍为 MIT（保留署名）；ClawHub 发布包按平台规则默认 MIT-0，源仓库**无需**改授 MIT-0。

## v1.0.1 (2026-09-25)

隐私脱敏 + 发布路径调整（能力不变）：

- 重写 `references/clean_code_audit_sample.md`：审计样例从真实项目 `agent-analytics-report` 的内部代码，改为自带行号、可逐行核对的**合成示例脚本** `demo-skill/scripts/aggregate.py`，不再泄露任何真实项目。
- `SKILL.md` / `README.md` 中的 `agent-analytics-report`、`ai-weekly` 命名引用改为合成示例；输出路径里的用户名绝对路径改为 `~/WorkBuddy/<session>/`。
- `assets/clean_code_checklist.html` 三处点名引用（`agent-analytics-report` 例1 / `ai-weekly` 例4 / `_PROXY_OVERRIDE` 例3）改为「审计范例」+ 通用占位 `_CONFIG_OVERRIDE`。
- skill 源目录从 `~/.workbuddy/skills/` 迁至 `C:\Users\elisa\dev\skill-clean-audit`（仅路径变更，方法/产出不变）。

## v1.0.0 (2026-09-23)

首个稳定版（stable）。整合 v0.1.0 第一性原理方法论与 v0.2.0 对标 Uncle Bob 的四项增强，并补齐发布就绪项：

- 版本号升至 **1.0.0**（SKILL.md frontmatter + 本 CHANGELOG）。
- **新增《合规与边界声明（网络访问）》小节**：本 skill 纯本地只读、零网络、零凭据、无第三方接口，不提供 / 不指导 / 不支持任何规避网络管理措施的能力；利于 SkillHub 内容审核的信任维度。
- 审计能力不变：A 理解成本 / B 修改风险两轴 + 红黄绿严重度 + 只读审计 + 交互式清单 + Uncle Bob 气味交叉对照 + CQS 红项 + 轻量指标信号 + 增量清理（Boy Scout）。
- 发布包剔除 LICENSE / .gitignore（SkillHub 封禁点文件），仅含 SKILL.md / README.md / CHANGELOG.md / assets / references。

## v0.2.0 (2026-09-23)

对标 Uncle Bob 原则库，补充 4 项不重叠、且重新接地到第一性原理的增强：

- **新增 `references/smells_crosswalk.md`**：把 Uncle Bob 的 canonical 代码气味（Rigidity/Fragility/Immobility/Opacity/Needless Repetition + 长函数/长参数/布尔旗/switch-on-type）映射到本 skill 的 A/B 两轴与红黄绿严重度，作为审计的标准命名桥接。
- **严重度红项补「命名与行为不一致 / 隐藏副作用（CQS 违反）」**：堵住函数级隐藏副作用的盲点（之前只覆盖模块级全局态）。
- **新增「轻量指标信号」小节**：函数行数 >40 / 参数 ≥4 / 嵌套 ≥4 / 布尔旗 / 重复 ≥3 次，明确框为「核查提示、非硬规则」，避免偏离第一性原理。
- **新增「修复优先级：增量清理（Boy Scout）」小节**：红项在你本来就要改该文件时顺手清，未碰代码不 gold-plate；Skill 脚本测试「有则绿、无不算红」。
- 审计流程第 2 步增加对照 `references/smells_crosswalk.md` 的指引。
- 交付物段补一句：生成物已被仓库 `.gitignore` 忽略。

## v0.1.0 (2026-09-22)

- 首个发布版：第一性原理 clean code 审计法（A 理解成本 / B 修改风险 两轴 + 红黄绿严重度 + 只读审计）。
- 交付 `SKILL.md`、`assets/clean_code_checklist.html`（交互式清单）、`references/clean_code_audit_sample.md`（完整审计范例）。
- MIT 开源，仓库 github.com/Elisabeth15501/skill-clean-audit。
