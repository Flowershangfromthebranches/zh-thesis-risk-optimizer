# Prompt: REPORT_SIMILARITY_ONLY

Use this prompt when the user provides a similarity report and wants targeted similarity-risk optimization.

## Boundaries

Do not invent report percentages, source titles, authors, URLs, or risk levels. Do not remove necessary citations.

## Workflow

1. Identify report type.
2. Extract marked fragments, repeated fragments, source notes, and contribution rates.
3. Map each report fragment back to the thesis source text.
4. Assign mapping confidence.
5. Classify similarity source type.
6. Determine whether similarity is caused by necessary citation.
7. Determine whether citations should be kept or supplemented.
8. Determine whether the fragment is a no-edit zone.
9. Revise by priority, only where mapping is safe enough.

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

## 映射说明

## 定点修改

## 引用复核
```
