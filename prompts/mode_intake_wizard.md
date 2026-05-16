# Prompt: INTAKE_WIZARD_PRECHECK

Use this prompt whenever a task is routed to `zh-thesis-risk-optimizer`.

Do not rewrite the thesis until the precheck determines whether required fields are present.

## Inputs

The user may provide any combination of:

- Thesis text, chapter, paragraph, or file path.
- AIGC report, similarity report, report screenshot transcription, color-marked text, or report fragments.
- Historical drafts and previous report metrics.
- Desired target, such as "继续降 AIGC" or "查重已经够了".
- Character budget or output preference.
- Protected terms, citations, technical identifiers, data, tables, fields, paths, formulas, or school format rules.

## Decision Rules

1. Always run intake precheck before selecting a revision mode.
2. If the user provided enough context, do not run a full wizard. Output `Intake Confirmation`, state the selected route, and proceed.
3. If one or two fields are missing, ask only those fields.
4. If the task is underspecified, show the copyable intake template from `workflow/intake_request_template.md`.
5. Always include selectable options plus "自动判断 / 其他补充".
6. Use defaults unless the user overrides them:
   - Whole-thesis character delta: `±10%`.
   - Report color legend: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
   - File input: create a copy and keep the original unchanged.
   - Protected items: citations, formulas, code, APIs, paths, table names, field names, parameters, experiment data, and reference entries.
7. Never ask the user to provide fabricated data, fake reports, fake citations, or invented case facts.

## Output Format

When context is incomplete, output:

```text
当前任务需要使用 zh-thesis-risk-optimizer，但关键信息还不完整。
请复制下面模板，替换参考值后发送；不知道的字段可以写“请自动判断”。

【任务目标】
只降 AIGC / 只降查重 / 双降 / 只诊断不改写 / 报告映射 / 文件副本处理 / 全文项目管理 / 请自动判断

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

【查重报告】可选
无 / 查重报告 DOCX 路径 / HTML 报告 / PDF 复制文本 / 手动复制标红片段

【论文专业和题目】强烈建议
例如：人力资源管理，《数智化时代A电商公司招聘管理优化研究》

补充说明：
- 如果没有报告，我可以先做启发式诊断，但不会声称能对应任何检测平台结果。
- 如果输入是文件，我会创建副本并只回写副本。
```

When only a few fields are missing, output:

```text
我已能判断大方向，还缺少这几项：

- [缺失项 1]：选项 A / 选项 B / 自动判断
- [缺失项 2]：选项 A / 选项 B / 其他补充

默认会保护引用、公式、代码、接口、路径、表名、字段、参数、实验数据和参考文献条目。
```

When enough information is present, output:

```text
## Intake Confirmation

| field | value | status |
|---|---|---|
| 任务目标 |  | OK |
| 论文输入 |  | OK |
| 报告输入 |  | OK / MISSING / NOT NEEDED |
| 处理范围 |  | OK |
| 输出形式 |  | OK |
| 字数约束 |  | DEFAULT / USER_SPECIFIED |
| 保护项 |  | DEFAULT / USER_SPECIFIED |

模式判断：
- 进入模式：
- 理由：
- 需要加载：
- 默认约束：
- 下一步输出：
```

## Routing Examples

| User Input | Mode Decision |
|---|---|
| Any thesis AIGC/similarity/report task | Run `INTAKE_WIZARD_PRECHECK` first. |
| "帮我降 AIGC" | Ask required intake template because input and report are missing. |
| "这是原文和原版 AIGC 报告，先处理红橙" | `FIRST_PASS_RED_ORANGE_ENGINE`; do not ask full wizard. |
| "查重够了，继续降 AIGC，别扩太多" | `AIGC_FOCUSED_LENGTH_CONTROLLED`; ask only budget if absent. |
| "这是 DOCX 和报告，改完给我文件" | `FILE_INPUT_COPY_WORKFLOW` plus report-driven mode. |
| "没有报告，帮我双降" | `NO_REPORT_FALLBACK_WORKFLOW`; state heuristic limitation. |
| "人力资源管理论文，报告降不动" | Ask for company/survey/interview/process evidence; route to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`. |

## Self-Check Before Asking

- Did the user already provide the missing field?
- Can the mode be selected safely without asking?
- Are you asking for only the minimum needed details?
- Did you avoid promising external detection results?
- Did you keep the file-copy and protection defaults visible?
