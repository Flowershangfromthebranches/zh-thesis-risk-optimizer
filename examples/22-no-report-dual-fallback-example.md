# Example 22: No Report Dual Fallback

## Situation

User has no similarity report or AIGC report and asks for dual optimization.

## Response Boundary

No-report mode can only provide heuristic optimization. It cannot promise actual detection changes.

## Diagnosis First

| Paragraph | AIGC Risk | Similarity Risk | Editability | Suggested Action |
|---|---|---|---|---|
| 绪论 P2 | 高 | 中 | 高 | 背景段结构重构 |
| 理论基础 P4 | 中 | 高 | 中 | 定义压缩并保留引用 |
| 实验 P3 | 低 | 低 | 低 | 不优先处理 |

## First Pass

Rebuild high-editability paragraphs: introduction background and theory definitions.

## Second Pass

Run AIGC self-audit. If 3 or more risks remain, rewrite again using the original facts.

## Remaining Advice

For precise localization, provide a similarity or AIGC report in the next pass.
