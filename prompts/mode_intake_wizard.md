# Prompt: INTAKE_WIZARD_PRECHECK

Use this prompt whenever a task is routed to `zh-thesis-risk-optimizer`.

Run `RISK_INTAKE_GATE` before rewrite routing. Do not rewrite until the user provides `current_similarity_rate` and `current_aigc_rate`.

## Inputs

The user may provide any combination of:

- Thesis text, chapter, paragraph, or file path.
- AIGC report, similarity report, report screenshot transcription, color-marked text, or report fragments.
- Historical drafts and previous report metrics.
- Desired target, such as "继续降 AIGC" or "查重已经够了".
- Current and target risk rates.
- Character budget or output preference.
- Protected terms, citations, technical identifiers, data, tables, fields, paths, formulas, or school format rules.

## Decision Rules

1. Always run `RISK_INTAKE_GATE` and intake precheck before selecting a revision mode.
2. On first contact for a new task, show the full copyable intake template from `workflow/intake_request_template.md`.
3. Required fields must be filled before processing.
3a. `current_similarity_rate` and `current_aigc_rate` are mandatory before rewriting. If either is missing, output `INTAKE_INCOMPLETE`; file reading and report parsing may continue only to complete intake.
3b. If AIGC color work is requested, red/orange/purple/black counts or ratios are mandatory. If the user uploaded a color report, parse it first; otherwise ask for the distribution.
4. Strongly recommended and optional fields must also be shown. The user may fill them, write `无`, write `跳过`, or write `请自动判断`.
5. If the user submits only required fields, do not proceed yet; ask them to fill or explicitly skip the strongly recommended and optional sections.
6. If the user submits a completed intake template, output `Intake Confirmation`, state the selected route, and proceed.
7. If the user submits conflicting fields, ask only the conflict question.
8. Always include selectable options plus "自动判断 / 其他补充".
9. Use defaults only after the user has accepted defaults or written `请自动判断`:
   - Whole-thesis character delta: `±10%`.
   - Report color legend: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
   - File input: create a copy and keep the original unchanged.
   - Protected items: citations, formulas, code, APIs, paths, table names, field names, parameters, experiment data, and reference entries.
10. Never ask the user to provide fabricated data, fake reports, fake citations, or invented case facts.

## Output Format

On first contact or incomplete intake, output:

```text
当前任务将使用 zh-thesis-risk-optimizer。正式处理前需要先完成 intake。
请复制下面模板，替换参考值后发送；不知道或不想提供的可选项可以写“无 / 跳过 / 请自动判断”。

【任务目标】
只降 AIGC / 只降查重 / 双降 / 只诊断不改写 / 报告映射 / 文件副本处理 / 全文项目管理 / 请自动判断

【当前查重率 current_similarity_rate】
例如：11% / 未检测

【当前 AIGC 疑似率 current_aigc_rate】
例如：68.6% / 未检测

【目标查重率 target_similarity_rate】
例如：15% / 10% / 请自动判断

【目标 AIGC 疑似率 target_aigc_rate】
例如：30% / 20% / 请自动判断

【任务类型 task_type】
aigc_only / similarity_only / dual_optimization

【论文输入】
粘贴正文 / 单章文本 / 原文 DOCX 路径 / Markdown 或 TXT 路径 / LaTeX 路径

【处理范围】
单段 / 单章 / 全文 / 只处理报告红橙片段 / 只输出任务表

【输出形式】
诊断表 / 修改后文本 / 报告驱动任务表 / 创建副本并回写 / 作者补充证据清单 / 全文项目总览

【字数约束】
默认全文总字符数浮动 ±10%，或写明你的范围

【保护项】
默认保护：引用、公式、代码、接口、路径、表名、字段名、参数、实验数据、参考文献条目、学校声明。
请补充其他必须保留内容：

【AIGC 报告】可选但强烈建议
无 / AIGC 报告 DOCX 路径 / PDF 复制文本 / 截图 OCR 文本 / 手动复制红橙片段

【是否有 AIGC 颜色报告 has_aigc_color_report】
true / false

【红段数量/比例 current_red_count/current_red_ratio】
红段数量 / 红色比例 / 有报告请自动解析

【橙段数量/比例 current_orange_count/current_orange_ratio】
橙段数量 / 橙色比例 / 有报告请自动解析

【紫段数量/比例 current_purple_count/current_purple_ratio】
紫段数量 / 紫色比例 / 有报告请自动解析

【黑段数量/比例 current_black_count/current_black_ratio】
黑段数量 / 黑色比例 / 有报告请自动解析

【查重报告】可选
无 / 查重报告 DOCX 路径 / HTML 报告 / PDF 复制文本 / 手动复制标红片段

【是否有查重报告 has_similarity_report】
true / false

【论文专业和题目】强烈建议
例如：人力资源管理，《数智化时代A电商公司招聘管理优化研究》

补充说明：
- 如果没有报告，我可以先做启发式诊断，但不会声称能对应任何检测平台结果。
- 如果输入是文件，我会创建副本并只回写副本。
```

When required fields are filled but strongly recommended or optional fields are not acknowledged, output:

```text
必填项已经足够判断大方向，但 intake 还没完成。
请补充下面可选信息；如果没有或不想提供，请写“无 / 跳过 / 请自动判断”。

【AIGC 报告】

【查重报告】

【报告颜色规则】

【论文专业和题目】

【当前状态】
stage = original / first_pass / second_pass / current_report_pass / first_pass_failure

【是否要求保持 DOCX 原格式 preserve_docx_format_required】
true / false

【历史版本】

【用户目标】

【可用证据】

【特殊要求】
```

When a few required fields are missing after the user has already submitted an intake reply, output:

```text
我已收到 intake，但还缺少以下必填项：

- [缺失项 1]：选项 A / 选项 B / 自动判断
- [缺失项 2]：选项 A / 选项 B / 其他补充

可选项也请填写，或写“无 / 跳过 / 请自动判断”。
```

If risk rates are missing, output:

```text
INTAKE_INCOMPLETE
还缺少当前风险率，不能进入改写链路。
请补充：
- current_similarity_rate：当前查重总体相似度
- current_aigc_rate：当前 AIGC 总体疑似率
- red/orange/purple/black counts or ratios：若没有报告且没有颜色分布，无法判断紫色策略

说明：可以继续读取文件或解析报告来补全 intake，但不能直接改写。
```

When enough information is present, output:

```text
## Intake Confirmation

| field | value | status |
|---|---|---|
| 任务目标 |  | OK |
| current_similarity_rate |  | OK / MISSING |
| current_aigc_rate |  | OK / MISSING |
| target_similarity_rate |  | OK / MISSING |
| target_aigc_rate |  | OK / MISSING |
| task_type |  | OK / MISSING |
| 论文输入 |  | OK |
| 报告输入 |  | OK / MISSING / NOT NEEDED |
| 处理范围 |  | OK |
| 输出形式 |  | OK |
| 字数约束 |  | DEFAULT / USER_SPECIFIED |
| 保护项 |  | DEFAULT / USER_SPECIFIED |

模式判断：
- 进入模式：
- risk_intake_strategy:
- max_humanization_level:
- level_4_allowed:
- 理由：
- 需要加载：
- 默认约束：
- 下一步输出：
```

## Routing Examples

| User Input | Mode Decision |
|---|---|
| Any thesis AIGC/similarity/report task | Run `INTAKE_WIZARD_PRECHECK` and show the full template unless a completed intake was already provided. |
| "使用 zh-thesis-risk-optimizer 给我的论文降 AIGC" | Show the full intake template and wait. |
| "帮我降 AIGC" | Show the full intake template and wait. |
| "这是原文和原版 AIGC 报告，先处理红橙" | If optional fields are not acknowledged, ask for optional fields or skip/auto-judge before routing. |
| "查重够了，继续降 AIGC，别扩太多" | Ask for the remaining intake fields unless the completed template is present. |
| Completed intake with current rates and AIGC 68.6%, similarity already below target | Run `RISK_INTAKE_GATE`, set `high_risk_controlled_humanization`, and allow local-only escalation where eligible. |
| "这是 DOCX 和报告，改完给我文件" | Ask for remaining intake fields before file reading or writeback. |
| Completed intake template with original thesis and original AIGC report | `FIRST_PASS_RED_ORANGE_ENGINE`; output `Intake Confirmation` and proceed. |
| Completed intake template with revised/current thesis and current AIGC report | `THREE_MODE_COLOR_BAND_WORKFLOW` plus `CURRENT_REPORT_RED_ORANGE_ENGINE`; output `Intake Confirmation` and proceed. |
| Completed intake template without report | `THREE_MODE_COLOR_BAND_WORKFLOW` with `fallback_heuristic: true`; state heuristic limitation. |
| Completed intake template for HR/management plateau | Route to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`; request evidence if missing. |

## Self-Check Before Asking

- Did the user already provide the missing field?
- Has the user completed the intake, including optional fields marked as filled, skipped, or auto-judge?
- Are you asking for only the minimum needed details?
- Did you avoid promising external detection results?
- Did you keep the file-copy and protection defaults visible?
