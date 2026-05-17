# Intake Wizard And Precheck Example

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Scenario 1: Matching Task With Missing Required Fields

User:

```text
帮我给论文降 AIGC。
```

Assistant:

```text
当前任务需要使用 zh-thesis-risk-optimizer，但关键信息还不完整。
请复制 workflow/intake_request_template.md 中的模板，替换参考值后发送；不知道的字段可以写“请自动判断”。

必填项包括：
- 任务目标
- 论文输入
- 处理范围
- 输出形式
- 字数约束
- 保护项
```

## Scenario 2: User Provides Enough Information But No Completed Intake

User:

```text
这是原版论文和原版 AIGC 报告。红色是 70% 以上，橙色是 60%-70%。请首轮同时处理红色和橙色，全文字符变动控制在 ±10%。
```

Assistant:

```text
当前任务将使用 zh-thesis-risk-optimizer。正式处理前需要先完成 intake。
你已经提供了任务目标、原文/报告类型、颜色规则和字数约束，但还需要确认输出形式、保护项、论文专业和可选信息。
请补充下面模板；没有的项目可以写“无 / 跳过 / 请自动判断”。

【输出形式】
诊断表 / 修改后文本 / 报告驱动任务表 / 创建副本并回写 / 作者补充证据清单 / 全文项目总览

【保护项】
默认保护：引用、公式、代码、接口、路径、表名、字段名、参数、实验数据、参考文献条目、学校声明。
请补充其他必须保留内容：

【论文专业和题目】

【当前状态】

【历史版本】

【用户目标】

【可用证据】

【特殊要求】
```

## Scenario 3: User Provides Completed Intake

User:

```text
【任务目标】只降 AIGC
【论文输入】原文 DOCX：/path/original.docx
【处理范围】全文，只处理报告红橙片段
【输出形式】创建副本并回写，同时输出诊断表
【字数约束】全文 ±10%
【保护项】引用、问卷数据、图表编号、参考文献、学校声明
【AIGC 报告】/path/aigc.docx
【查重报告】无
【报告颜色规则】默认
【论文专业和题目】人力资源管理，《示例论文》
【当前状态】原文未改
【历史版本】无
【用户目标】请自动判断
【可用证据】无
【特殊要求】跳过
```

Assistant:

```text
## Intake Confirmation

| field | value | status |
|---|---|---|
| 任务目标 | 只降 AIGC | OK |
| 论文输入 | /path/original.docx | OK |
| 报告输入 | AIGC 报告 /path/aigc.docx；查重报告无 | OK |
| 处理范围 | 红色和橙色片段 | OK |
| 输出形式 | 创建副本并回写，同时输出诊断表 | OK |
| 字数约束 | 全文 ±10% | USER_SPECIFIED |
| 保护项 | 引用、问卷数据、图表编号、参考文献、学校声明 | USER_SPECIFIED |

模式判断：
- 进入模式：FILE_INPUT_COPY_WORKFLOW + REPORT_AIGC_ONLY
- 理由：用户提交了完整 intake，并提供了原文文件、AIGC 报告、输出形式、字数约束和保护项。
- 需要加载：prompts/mode_first_pass_red_orange.md；references/first_pass_red_orange_engine.md；references/character_delta_guard.md
- 下一步输出：红橙首轮任务表、颜色原因分析表、字符变动表和可安全修改段落。
```

## Scenario 4: File Input

User:

```text
这是 DOCX 文件和 AIGC 报告，改完给我文件。
```

Assistant:

```text
Intake Confirmation

| field | value | status |
|---|---|---|
| 任务目标 | AIGC 报告驱动修复 | OK |
| 论文输入 | DOCX 文件 | OK |
| 报告输入 | AIGC 报告 | OK |
| 处理范围 | 待确认 | MISSING |
| 输出形式 | 文件副本 | OK |
| 字数约束 | 全文 ±10% | DEFAULT |
| 保护项 | 引用、术语、代码、路径、表名、字段、参数、数据 | DEFAULT |

模式判断：
- 进入模式：FILE_INPUT_COPY_WORKFLOW + REPORT_AIGC_ONLY
- 理由：用户提供文件和 AIGC 报告，并要求文件交付。
- 默认约束：创建原文件副本，不直接修改原文件；只将 HIGH 或安全 MEDIUM 置信度映射写回副本；保护引用、代码、路径、表名、字段、参数和实验数据。
- 还需确认：颜色规则是否使用默认红>70%、橙60%-70%、紫50%-60%、黑<50%？
```

## Scenario 5: No Report

User:

```text
没有报告，帮我双降这章。
```

Assistant:

```text
Intake Confirmation

| field | value | status |
|---|---|---|
| 任务目标 | 双降 | OK |
| 论文输入 | 本章文本 | OK |
| 报告输入 | 无 | NOT NEEDED |
| 处理范围 | 单章 | OK |
| 输出形式 | 诊断表和修改建议 | DEFAULT |
| 字数约束 | 全文/章节 ±10% | DEFAULT |
| 保护项 | 引用、术语、公式、代码、数据 | DEFAULT |

模式判断：
- 进入模式：NO_REPORT_FALLBACK_WORKFLOW + AUTO_DIAGNOSIS
- 理由：用户没有提供检测报告，只能进行启发式风险诊断和保底优化。
- 说明：该流程不能对应任何检测平台结果；如需更精准定位，应补充 AIGC 或查重报告。
- 下一步输出：章节结构、保护清单、启发式风险表和高可改段落任务表。
```
