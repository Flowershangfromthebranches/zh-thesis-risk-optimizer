# Intake Wizard

The intake wizard is the startup guide for this Skill. It is used when the user wants to use the Skill but has not yet provided enough information to choose a safe mode, input workflow, report workflow, or output format.

It is not a separate detection or rewriting engine. It only collects the minimum missing context needed to route the task correctly.

## Purpose

- Help users provide the right materials before revision starts.
- Reduce weak results caused by missing reports, unclear goals, unknown color legends, or missing protection rules.
- Avoid starting full-thesis rewriting when the task only needs diagnosis, report mapping, or file-copy processing.
- Preserve academic integrity by asking for evidence instead of inventing facts.

## Use Cases

Use `INTAKE_WIZARD` when:

- The user says they want to use this Skill but provides no paper text, report, file, or goal.
- The requested mode is unclear: AIGC-only, similarity-only, dual revision, diagnosis-only, report mapping, or file-copy processing.
- The user provides a file but does not say whether to edit a copy, return text, or produce a task table.
- The user provides a report but the report type, color legend, or original-source mapping is unclear.
- The user provides a social-science or management thesis but does not provide organization, survey, interview, process, indicator, or case evidence.
- The user asks for full-thesis work but does not provide character budget, protected items, or desired output.

Do not use the wizard when the user has already provided enough information to route the task. In that case, proceed directly and state the selected mode.

## Intake Principles

- Ask only for missing information.
- Prefer 4 to 7 compact fields, not a long questionnaire.
- Always include selectable options and a free-form supplement.
- Allow the user to answer "不确定，自动判断".
- Do not ask for private or unnecessary information.
- Never pressure the user to provide fabricated evidence.
- If a required report, citation, data point, or technical fact is absent, mark it as missing instead of inventing it.

## Recommended Intake Fields

### 1. Task Goal

Options:

- 只降 AIGC
- 只降查重相似风险
- 双降
- 只诊断不改写
- 报告片段映射原文
- 文件副本处理
- 完整论文项目管理
- 不确定，自动判断

### 2. Input Type

Options:

- 直接粘贴文本
- DOCX / Word 文件
- Markdown / TXT 文件
- LaTeX 文件
- 原文 + AIGC 报告
- 原文 + 查重报告
- 原文 + 两类报告
- 原文 + 历史稿 + 新报告

### 3. Report Availability

Options:

- 有 AIGC 报告
- 有查重报告
- 两者都有
- 没有报告
- 只有截图转写或复制片段
- 只有颜色标记，没有完整报告

If no report is available, the Skill must state that processing is heuristic and report-driven localization would be stronger.

### 4. Report Color Legend

Default:

- 红色：AIGC 生成疑似度 70% 以上
- 橙色：60% 到 70%
- 紫色：50% 到 60%
- 黑色：50% 以下

Options:

- 使用默认颜色规则
- 报告颜色规则不同，我会补充
- 不知道颜色规则，请先按不确定处理

If the legend is unknown, do not infer exact thresholds. Use report labels as provided and mark uncertainty.

### 5. Scope

Options:

- 单段
- 单章
- 全文
- 只处理红色和橙色
- 只输出任务表，不改写
- 只处理报告命中的片段

### 6. Output Format

Options:

- 先输出诊断表
- 输出修改后文本
- 输出报告驱动任务表
- 创建文件副本并回写副本
- 输出作者补充证据清单
- 输出全文项目总览和章节任务

### 7. Constraints And Protection

Default constraints:

- 全文总字符变动控制在原文 `±10%`，除非用户指定其他范围。
- 文件输入时不修改原文件，只创建副本并在副本中回写。
- 保护引用、公式、代码、接口、表名、字段名、参数、路径、实验数据、参考文献条目。

Ask the user to add:

- 必须保留的术语
- 必须保留的引用
- 不能改动的数据或结论
- 学校模板或格式要求
- 专业、题目、研究对象或系统名称

## Routing After Intake

Use the collected answers to route:

| Intake Result | Route |
|---|---|
| User wants only AIGC revision with report | `REPORT_AIGC_ONLY` or `FIRST_PASS_RED_ORANGE_ENGINE` |
| User wants only AIGC revision without report | `AIGC_ONLY` plus `NO_REPORT_FALLBACK_WORKFLOW` if long text |
| User says similarity is enough and AIGC remains high | `AIGC_FOCUSED_LENGTH_CONTROLLED` |
| User provides original thesis and original AIGC report | `FIRST_PASS_RED_ORANGE_ENGINE` |
| User provides multiple drafts and reports | `TARGETED_MULTIPASS_ENGINE` or `AIGC_PLATEAU_BREAKER` |
| User provides file input | `FILE_INPUT_COPY_WORKFLOW` plus the selected revision mode |
| User asks for only mapping | `REPORT_TO_SOURCE_MAPPING` |
| User provides no report and no mode | `AUTO_DIAGNOSIS` |
| Social-science template plateau is likely | `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` |
| Full-thesis project is requested | `FULL_THESIS_PROJECT_MODE` |

## Minimal Dialog Template

Use this template when the user has not provided enough context:

```text
为了正确选择模式，请先补充下面几项。可以直接选项作答，也可以写“自动判断”。

1. 目标：只降 AIGC / 只降查重 / 双降 / 只诊断 / 报告映射 / 文件副本处理 / 自动判断
2. 输入：粘贴文本 / DOCX 文件 / Markdown 或 TXT / LaTeX / 原文+报告 / 历史稿+新报告
3. 报告：AIGC 报告 / 查重报告 / 两者都有 / 没有报告 / 只有截图或复制片段
4. 范围：单段 / 单章 / 全文 / 只处理红橙 / 只输出任务表
5. 输出：诊断表 / 修改后文本 / 报告任务表 / 文件副本 / 作者补充清单
6. 字数约束：默认全文 ±10%，或请写你的范围
7. 保护项：引用、公式、代码、表名、字段、参数、路径、实验数据等，是否还有其他必须保留内容？
```

## Compact User Reply Format

The user may reply in this format:

```text
目标：双降
输入：DOCX 文件
报告：AIGC + 查重
颜色规则：默认
范围：全文，只处理红橙
输出：文件副本 + 诊断表
字数约束：±10%
保护项：引用、表名、字段、参数、实验数据
其他：这是人力资源管理论文，问卷数据不能改。
```

## Safety Boundary

The intake wizard must not:

- Promise any external detection result.
- Ask the user to remove necessary citations.
- Ask for fabricated experiments, data, interviews, logs, or reports.
- Invent report colors, percentages, sources, or risk levels.
- Start file writeback before mapping confidence and protection checks are clear.
