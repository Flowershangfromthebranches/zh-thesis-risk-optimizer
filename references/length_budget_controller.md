# Length Budget Controller

## Purpose

This file controls whole-thesis length growth after revision. AIGC risk reduction must not rely on uncontrolled expansion.

## 1. Counting Rules

Default counting is an approximate Chinese character count:

- Count CJK characters as Chinese characters.
- English words, numbers, code, paths, formulas, and URLs may be listed separately as `protected_tokens`.
- This Skill does not implement a real counting program, but prompts must ask the agent to estimate before/after character changes.

## 2. Global Budget

Default:

- `max_global_added_chars = 2000`.
- `min_global_added_chars = 0`.
- `preferred_added_chars = 500-1500`.
- `allowed_total_delta_ratio = ±10%` for whole-thesis revision unless the user specifies another range.

If the user provides another range, use the user range.

When a fixed character-addition budget conflicts with the `±10%` whole-thesis delta guard, use the stricter user-stated constraint if one exists. Otherwise, use the stricter of the two default constraints.

## 3. Chapter Budget

Suggested chapter budgets:

| chapter | suggested_delta |
|---|---:|
| 摘要 | +0-150 |
| 绪论 | +0-300 |
| 研究现状 | +0-300 |
| 技术概述 | +0-250 |
| 可行性/需求分析 | +0-250 |
| 系统设计 | +0-250 |
| 系统实现 | +0-200 |
| 系统测试 | +0-250 |
| 结论 | +0-150 |

System design, implementation, and testing chapters usually already contain technical details and should not be expanded heavily. Introduction and technology-overview chapters are template-prone, but they must not be expanded by adding more background.

## 4. Paragraph Budget

Default paragraph rules:

- Low-risk paragraph: no change or `±5%`.
- Medium-risk paragraph: `-5%` to `+10%`.
- High-AIGC paragraph: `-10%` to `+20%`.
- Information-insufficient but necessary repair paragraph: at most `+25%`, consuming global budget.
- Single-paragraph addition above 120 Chinese characters must explain why.
- Single-paragraph addition above 200 Chinese characters is a default failure unless the user explicitly asks for expansion.

## 5. Budget Failure

If output exceeds `original_chars + 2000`, or falls outside the allowed `±10%` whole-thesis range, mark:

`LENGTH_BUDGET_FAIL`

or, when the ratio guard is the failing condition:

`CHARACTER_DELTA_FAIL`

Handling:

- Do not mark `COMPLETED`.
- Enter Compression Pass.
- Compress new background explanation, generic significance, repeated transitions, and empty summary sentences first.
- Do not compress technical facts, data, citations, parameters, or conclusions.

## 6. Budget Table

Every whole-thesis treatment must output:

| section | original_chars | revised_chars | delta | budget | status |
|---|---:|---:|---:|---:|---|

## Relation To SKILL.md

Use this file in `LENGTH_BUDGET_CONTROLLER` and any AIGC-focused full-thesis workflow.

For ratio-based whole-thesis control, also load `references/character_delta_guard.md`.
