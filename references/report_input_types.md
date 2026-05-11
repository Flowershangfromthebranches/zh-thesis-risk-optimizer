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
