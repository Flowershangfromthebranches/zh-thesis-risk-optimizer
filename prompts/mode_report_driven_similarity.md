**ARCHIVED_COMPATIBILITY_ONLY**

Do not call directly. Route through `SKILL.md` Minimal Mode Router.

# Prompt: REPORT_SIMILARITY_ONLY

Use this prompt when the user provides a similarity report and wants targeted similarity-risk optimization.

## Boundaries

Do not invent report percentages, source titles, authors, URLs, or risk levels. Do not remove necessary citations.

## Workflow

1. Identify report type.
2. Extract marked fragments, repeated fragments, source notes, and contribution rates.
3. If the report uses color bands, apply the default legend unless the report states otherwise: red `>=70%`, orange `>=60%` and `<70%`, purple `>=50%` and `<60%`, black `<50%`, gray non-scored/excluded.
4. Treat red and orange fragments as primary targets.
5. Analyze why each red/orange fragment has its color before rewriting.
6. Map each report fragment back to the thesis source text.
7. Assign mapping confidence.
8. Classify similarity source type.
9. Determine whether similarity is caused by necessary citation.
10. Determine whether citations should be kept or supplemented.
11. Determine whether the fragment is a no-edit zone.
12. Revise by priority, only where mapping is safe enough.
13. Apply whole-thesis character delta guard, default `±10%`.

If file input is provided, create a copy and write safe revisions back to the copy only.

## Source Types

- 引用导致重复。
- 定义导致重复。
- 教材式表述。
- 背景套话。
- 综述堆叠。
- 相似源表达过近。
- 自引过密。
- 不可改保护内容。

## Output

```markdown
## 报告驱动任务表

## 颜色原因分析

## 映射说明

## 定点修改

## 字符变动表

## 引用复核
```
