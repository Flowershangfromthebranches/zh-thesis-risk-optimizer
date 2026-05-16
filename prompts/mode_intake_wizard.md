# Prompt: INTAKE_WIZARD

Use this prompt when the user wants to use `zh-thesis-risk-optimizer` but has not provided enough information to choose a safe mode or output format.

Do not rewrite the thesis yet. First collect the missing context.

## Inputs

The user may provide any combination of:

- Thesis text, chapter, paragraph, or file path.
- AIGC report, similarity report, report screenshot transcription, color-marked text, or report fragments.
- Historical drafts and previous report metrics.
- Desired target, such as "继续降 AIGC" or "查重已经够了".
- Character budget or output preference.
- Protected terms, citations, technical identifiers, data, tables, fields, paths, formulas, or school format rules.

## Decision Rules

1. If the user provided enough context, do not run a full wizard. State the selected route and proceed.
2. If one or two fields are missing, ask only those fields.
3. If the task is underspecified, show the compact intake dialog.
4. Always include selectable options plus "自动判断 / 其他补充".
5. Use defaults unless the user overrides them:
   - Whole-thesis character delta: `±10%`.
   - Report color legend: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
   - File input: create a copy and keep the original unchanged.
   - Protected items: citations, formulas, code, APIs, paths, table names, field names, parameters, experiment data, and reference entries.
6. Never ask the user to provide fabricated data, fake reports, fake citations, or invented case facts.

## Output Format

When context is incomplete, output:

```text
为了正确选择模式，请先补充下面几项。可以直接选项作答，也可以写“自动判断”。

1. 目标：只降 AIGC / 只降查重 / 双降 / 只诊断 / 报告映射 / 文件副本处理 / 自动判断
2. 输入：粘贴文本 / DOCX 文件 / Markdown 或 TXT / LaTeX / 原文+报告 / 历史稿+新报告
3. 报告：AIGC 报告 / 查重报告 / 两者都有 / 没有报告 / 只有截图或复制片段
4. 范围：单段 / 单章 / 全文 / 只处理红橙 / 只输出任务表
5. 输出：诊断表 / 修改后文本 / 报告任务表 / 文件副本 / 作者补充清单
6. 字数约束：默认全文 ±10%，或请写你的范围
7. 保护项：引用、公式、代码、表名、字段、参数、路径、实验数据等，是否还有其他必须保留内容？

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
| "我要用这个 Skill" | Ask full intake dialog. |
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
