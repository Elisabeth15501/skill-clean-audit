# Clean Code 审计样例 · collect_usage_data.py → `main()`

> 审计对象：`agent-analytics-report/scripts/collect_usage_data.py` 的 `main()`（行 71–539，约 468 行）
> 判据：A. 理解成本 / B. 修改风险。红=出现即脏优先修，黄=有意的债(注释+可控)，绿=出现即干净。
> 注：`import *` 与重复 docstring 在模块层（非 main 体内），但 main 直接调用被灌入的符号，故一并计入。

## A. 理解成本

| # | 清单项 | 命中 | 证据（行） | 说明 |
|---|--------|------|-----------|------|
| A1 | 🔴 符号来源隐式（`import *`） | ✅ 红 | 40–43, 调用点 119/133/196/198/228/234/373–383/406/503 等 | `resolve_date_range`/`collect_db_data`/`aggregate_*`/`DB_PATH`/`TZ`/`PERIOD_DAYS`/`DISPLAY_MERGE`/`_PRICING_LOCAL_LOADED`/`MODE_RATES_META` 全从 `import *` 进来。看到调用无法判断定义在哪个文件，要全局搜。 |
| A2 | 🔴 同一说明多处重复且矛盾 | ✅ 红 | 2–17 vs 51–69 | 顶部 docstring 与第 51 行起的裸字符串字面量重复同一段；后者是死字符串（运行时丢弃）。且 15–16 行说"本文件仅为 facade"，65–68 行又补"功能增强"，定位自相矛盾。 |
| A3 | 🔴 注释像 changelog（满屏工单号） | ✅ 红 | 145/161/233/258/290/364/378–383/402/500，版本标 v1.3.0/v1.5.2/v1.6.0/v1.7.0 | `P2-1`/`P2-3`/`F17`/`C7`/`D5`/`§3.1`/`§3.4` 之类 issue-tracker 标签散落 main 体内。新读者要先在脑子里解码这套内部编号体系才懂"这段代码现在归谁管"。 |
| A4 | 🟡 长函数 >40 行但内聚难拆 | ✅ 黄 | 71–539（约 468 行） | 确实长。但"难拆"辩护弱：它本质是顺序编排（解析参数→按源采集→聚合→挂定价元信息→输出），可拆成 `parse_args`/`collect_by_source`/`build_summary`/`attach_pricing_meta`/`write_output`。标黄=暂时可接受，但应排期拆。 |
| A5 | 🟡 魔法数字/字符串未命名 | ✅ 黄 | 260/419（`"estimate"`/`"official"`）、293/315/334/361（`gap_min=15`）、73/128/129（`"week"` 默认） | `"estimate"`/`"official"` 成本口径字符串出现 2 处；`gap_min=15` 在注释+默认+调用+写入共 4 处。命名常量（`COST_SOURCE_ESTIMATE` 等）即可消除。注：`PERIOD_DAYS` 已命名，算及格。 |
| A6 | 🟢 命名即文档 | ✅ 绿（多数） | `explicit_params`(123)/`sid_to_rawmodel`(166)/`unconfigured`(444)/`daily_tokens`(506) | 多数局部变量名一眼知意图，这一项达标。 |
| A7 | 🟢 显式优于隐式 | ❌ 未达标 | 见 A1/B1 | 行为混入导入的模块级全局（DB_PATH/TZ/_PRICING_LOCAL_LOADED…），前提与边界不清，故本项不算绿。 |

## B. 修改风险

| # | 清单项 | 命中 | 证据（行） | 说明 |
|---|--------|------|-----------|------|
| B1 | 🔴 模块级可变全局状态控行为 | ✅ 红 | 40–43 + 206/255/461/464–468 | main 一路读 `import *` 灌入的模块全局（`DB_PATH`/`TZ`/`_PRICING_LOCAL_LOADED`/`MODE_RATES_META` 等）。这些在 import 时由 ca_* 设定，非运行中改，风险比 ai-weekly 的 `_PROXY_OVERRIDE` 低一档，但按清单定义仍属"依赖非局部状态"，标红。 |
| B2 | 🔴 重复逻辑（违反 DRY） | ✅ 红 | 160–176 vs 177–193 | `claude-code` 与 `codex` 两个分支结构几乎逐行相同（collect→建 sid_to_rawmodel→skill_usage→outputs/memory_logs→task_types→print INFO），仅适配器名与打印标签不同。约 30 行重复，改一处要同步两处。 |
| B3 | 🔴 裸 `except` 静默吞错 | ⬜ 未命中（好评） | 全文 | 所有 `except` 均精确：`(sqlite3.Error, OSError)`(220)、`(ValueError, ImportError)`(155)、`(ValueError, TypeError)`(243)、`(OfficialUsageError, ImportError)`(398)、`(requests.RequestException, ValueError, KeyError)`(493)。无裸 `except`。本项达标。 |
| B4 | 🟡 有意的 best-effort `except` | ✅ 黄 | 201–221（补全会话查询）、147–156（LLM 分类器回退） | 补全会话查询失败只 `[WARN]` 不中断整条管线（注释 220 说明）；LLM 分类器不可用回退启发式。均有注释+范围可控，属"暂时可接受的债"。 |
| B5 | 🟡 过早抽象出没人复用的接口 | ⬜ 未命中 | — | facade 拆 ca_* 属 deliberate 重构，非过早抽象，本项不算。 |
| B6 | 🟢 行为只由入参决定 | ⚠️ 部分达标 | 解析自 `sys.argv`(109) | CLI 工具必然读 argv，但混入导入全局（见 B1），非纯入参驱动，故仅部分达标，不记满绿。 |
| B7 | 🟢 测试覆盖 | ❓ 未核实 | — | 未在本次审计中确认测试存在，留空。 |

## 额外发现（不在清单内，但同属理解成本）

**行 128–130 的 `explicit_params` 嵌套条件难读：**
```python
if args.period != "week" or explicit_params:
    if args.period != "week" and not (args.days or args.start):
        explicit_params.append(f"--period {args.period}")
```
外层与内层条件交叠，意图（"到底什么算显式生效参数"）要反复读才能还原。可提取为 `def _effective_params(args) -> list[str]` 显式表达，理解成本立刻下降。

## 审计评分

- 🔴 红（必须修）：**5** —— A1 import* / A2 重复 docstring / A3 changelog 注释 / B1 全局状态 / B2 DRY 重复分支
- 🟡 黄（可控债）：**3** —— A4 长函数 / A5 魔法量 / B4 best-effort except
- 🟢 绿（已达标）：**1**（A6 命名）+ B3 裸 except 未命中（好评）
- 未核实/未命中：A7、B5、B6、B7

## 结论（按第一性原理）

`main()` 的"脏"集中在**理解成本**一侧：来源隐式（A1）、说明自相矛盾（A2）、注释退化成工单追踪器（A3）、函数过长（A4）。
**修改风险**一侧反而较克制——没有裸 except（B3 好评），重复只在 claude-code/codex 两分支（B2），全局依赖是 import-time 而非运行中变异（B1）。
优先级建议：先消 A1/A2/A3（几乎零行为风险，纯可读性），再排 B2 合并双分支、A4 拆函数；A5/B4 这类黄项可随改顺手处理。

> 本样例只读不改。若要落地修复，建议另开一轮，按上面优先级逐个 PR。
