# Report Parsing Workflow

Use this workflow when the user provides a similarity report, AIGC report, report text copied from HTML/PDF/Word, or manually copied marked fragments.

## Workflow

1. Confirm report source and input type.
2. Extract report metadata:
   - Detection system name.
   - Report date.
   - Total similarity rate or AIGC risk value.
   - Chapter-level risk.
   - Fragment-level risk.
   - Similarity source.
   - Contribution rate.
   - Risk level.
   - Color-mark meaning.
3. Extract high-risk fragments.
4. Extract fragment context.
5. Extract similarity sources or risk explanations.
6. Map fragments back to the thesis source text.
7. Assign mapping confidence.
8. Classify risk type.
9. Identify protected or no-edit zones.
10. Generate priority queue.
11. Output report-driven task table.
12. Perform targeted revision only for confirmed or safe mappings.
13. Output human review checklist.

## Metadata Table

```markdown
| Field | Value | Provided by Report? | Notes |
| --- | --- | --- | --- |
| 检测系统名称 |  |  | 不得编造 |
| 报告日期 |  |  | 不得编造 |
| 总重复率/AIGC值 |  |  | 不得编造 |
| 颜色含义 |  |  | 如缺失则说明无法确认 |
```

## Fragment Extraction Table

```markdown
| 编号 | 报告片段 | 上下文 | 相似源/风险说明 | 贡献率/等级 | 颜色/标记 |
| --- | --- | --- | --- | --- | --- |
```

## Safety Notes

- Do not infer missing percentages.
- Do not invent source titles, authors, or URLs.
- Do not rewrite low-confidence mappings directly.
- Do not delete necessary citations just because a report marks a paragraph.
