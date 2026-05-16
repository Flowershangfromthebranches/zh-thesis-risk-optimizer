# Intake Wizard Example

## Scenario 1: User Only Says They Want To Use The Skill

User:

```text
我想用这个 Skill 帮我处理论文。
```

Assistant:

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

## Scenario 2: User Provides Enough Information

User:

```text
这是原版论文和原版 AIGC 报告。红色是 70% 以上，橙色是 60%-70%。请首轮同时处理红色和橙色，全文字符变动控制在 ±10%。
```

Assistant:

```text
模式判断：
- 进入模式：FIRST_PASS_RED_ORANGE_ENGINE
- 理由：用户提供了原版论文、原版 AIGC 报告、颜色规则和首轮红橙处理目标。
- 需要加载：prompts/mode_first_pass_red_orange.md；references/first_pass_red_orange_engine.md；references/character_delta_guard.md
- 默认约束：红色和橙色进入主处理区；黑色/低风险段落冻结；全文字符变动控制在 ±10%。
- 下一步输出：红橙首轮任务表、颜色原因分析表、字符变动表和可安全修改段落。
```

## Scenario 3: File Input

User:

```text
这是 DOCX 文件和 AIGC 报告，改完给我文件。
```

Assistant:

```text
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
模式判断：
- 进入模式：NO_REPORT_FALLBACK_WORKFLOW + AUTO_DIAGNOSIS
- 理由：用户没有提供检测报告，只能进行启发式风险诊断和保底优化。
- 说明：该流程不能对应任何检测平台结果；如需更精准定位，应补充 AIGC 或查重报告。
- 下一步输出：章节结构、保护清单、启发式风险表和高可改段落任务表。
```
