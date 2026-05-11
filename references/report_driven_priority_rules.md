# Report-Driven Priority Rules

Report-driven revision should process high-impact and safely editable fragments first.

## High Priority

Assign high priority when:

- Contribution rate is high.
- Paragraph is long.
- The same fragment has both similarity risk and AIGC risk.
- The fragment does not contain formulas, code, direct quotations, or protected citation text.
- The risk is background padding, definition repetition, generalized ending, or mechanical three-part structure.
- Revision is unlikely to affect experiment data, conclusions, or citation boundaries.

## Medium Priority

Assign medium priority when:

- Similarity risk exists but the paragraph contains many terms.
- AIGC risk exists but similarity risk is low.
- Only light structure adjustment is needed.
- Similarity-source boundary needs human confirmation.

## Low Priority

Assign low priority when:

- Formula, code, or parameter density is high.
- Necessary citation must be preserved.
- The fragment is legal text, standard text, or a classic definition.
- The report fragment cannot be accurately mapped.
- Revision may affect thesis conclusions.

## Priority Table

```markdown
| 编号 | 贡献率/等级 | 可安全改写 | 保护项 | 双风险 | 建议优先级 | 原因 |
| --- | --- | --- | --- | --- | --- | --- |
```

## Processing Order

1. Confirm mappings with HIGH confidence.
2. Process high-contribution and safely editable fragments.
3. Handle medium-confidence mappings with explicit notes.
4. Defer LOW or UNMAPPED items until the user confirms context.
5. Run citation and technical protection review before final output.

## Full-Thesis Integration

In `FULL_THESIS_PROJECT_MODE`, report-driven priority should update:

- `THESIS_MASTER_OVERVIEW` risk heatmap.
- Chapter task priority.
- Progress tracker report status.
- Iteration plan when a new report is uploaded.

Do not mark a chapter complete when it still has LOW or UNMAPPED report fragments.
