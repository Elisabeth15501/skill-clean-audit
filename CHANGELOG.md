# Changelog

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
