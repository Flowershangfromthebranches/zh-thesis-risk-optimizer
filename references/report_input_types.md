# Report Input Types

This Skill is not a report parser program by itself. It provides an AI-agent workflow for understanding user-provided report text, extracting fragments, mapping them back to the thesis, and making safe revision decisions.

## Supported Inputs

1. HTML reports.
2. Copied text from PDF reports.
3. Word reports with color marks.
4. User-copied marked fragments.
5. Fragment lists from detection reports.
6. High-risk paragraphs without a complete report.
7. Structured manual input: original text + report fragment + source/risk note.
8. Plain thesis text without a file.
9. Thesis files such as DOCX, Markdown, plain text, or LaTeX.

## Default Color Legend

When the user provides the following legend, use it exactly:

| color | suspicion range |
|---|---|
| red | above 70%, high suspicion |
| orange | 60%-70%, medium suspicion |
| purple | 50%-60%, light suspicion |
| black | below 50% |

If the report uses colors but does not explain them, do not invent meanings. Ask the user or mark the color meaning as uncertain.

## File Input Rule

When the input is a file, load `references/file_input_copy_workflow.md`.

- Do not modify the original file directly.
- Create a copy.
- Extract target text from the copy.
- Rewrite mapped fragments.
- Write safe revisions back to the copy.
- Deliver the copied file.

## Word Color-Marked Report Rule

When a Word / DOCX report uses font colors to mark AIGC or similarity risk, also load `references/docx_color_report_extraction.md`.

Do not flatten the report directly into plain text before extracting color metadata. Plain-text conversion can lose the red/orange/purple/black markers and make report-driven processing fail.

Required steps:

1. Inspect DOCX run-level or style-level color metadata.
2. Record raw color hex values.
3. Map each color to the user's report legend when available.
4. Build the red/orange task table from colored runs, not from uncolored plain text.
5. If color metadata cannot be extracted, ask the user for copied red/orange fragments or a report export with explicit labels.

## Required Boundaries

- Do not fabricate report conclusions, percentages, source names, or risk levels.
- Do not simulate, crack, reverse engineer, or forge any commercial detection system.
- If the report format is incomplete, lower mapping confidence and request human confirmation.
- If only fragments are provided, report-driven output must say which fields are missing.
- If the user supplies screenshots, work only from text the user provides or OCR text explicitly supplied in the conversation.

## Recommended User Input Format

```markdown
## 原文
...

## 报告片段
- 片段：
- 风险等级：
- 相似源：
- 贡献率：
- 报告颜色：

## 用户要求
- 只处理 AIGC / 只处理查重 / 双降 / 只做映射
```

## Missing Report Data

If a required report field is absent, write:

```text
报告未提供该字段，不能据此生成检测结论；后续判断仅基于用户提供的片段和论文原文。
```
