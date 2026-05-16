# Intake Wizard And Precheck Example

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

## Scenario 2: User Provides Enough Information

User:

```text
这是原版论文和原版 AIGC 报告。红色是 70% 以上，橙色是 60%-70%。请首轮同时处理红色和橙色，全文字符变动控制在 ±10%。
```

Assistant:

```text
Intake Confirmation

| field | value | status |
|---|---|---|
| 任务目标 | 首轮降低 AIGC 风险 | OK |
| 论文输入 | 原版论文 | OK |
| 报告输入 | 原版 AIGC 报告 | OK |
| 处理范围 | 红色和橙色片段 | OK |
| 输出形式 | 任务表和可安全修改段落 | DEFAULT |
| 字数约束 | 全文 ±10% | USER_SPECIFIED |
| 保护项 | 引用、术语、公式、代码、路径、数据、参考文献 | DEFAULT |

模式判断：
- 进入模式：FIRST_PASS_RED_ORANGE_ENGINE
- 理由：用户提供了原版论文、原版 AIGC 报告、颜色规则和首轮红橙处理目标。
- 需要加载：prompts/mode_first_pass_red_orange.md；references/first_pass_red_orange_engine.md；references/character_delta_guard.md
- 下一步输出：红橙首轮任务表、颜色原因分析表、字符变动表和可安全修改段落。
```

## Scenario 3: File Input

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

## Scenario 4: No Report

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
