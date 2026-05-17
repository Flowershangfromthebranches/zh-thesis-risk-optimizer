# Dual Optimization Arbitration

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Purpose

`DUAL_OPTIMIZATION_ARBITRATION` prevents AIGC-risk reduction and similarity-risk reduction from weakening each other.

## Core Diagnosis

Poor dual optimization often happens because:

1. Revision is shallow polishing, not paragraph-logic rebuilding.
2. The model diagnoses labels but does not perform strong rewrite actions.
3. Similarity and AIGC goals pull in different directions, so the model becomes conservative.
4. No-report mode has no clear target and relies on generic diagnosis.
5. Report mode reduces similarity first but does not reshape AIGC style afterward.
6. There is no mandatory self-audit and second rewrite.
7. Protection rules are strong but editable-zone identification is weak, so the model avoids meaningful changes.

## Arbitration Rules

### Target Arbitration

- When the user target is similarity below 10%, prioritize high-contribution similarity fragments first.
- When the user target is AIGC below 20%, run `AIGC_REGRESSION_GUARD` after every substantial rewrite.
- When the two targets conflict, do not sacrifice facts, citations, data, code, formulas, or technical identifiers.
- Each round must end with one of: `COMPLETED`, `PARTIAL`, or `FAILED`.
- Similarity improvement alone must not be treated as dual-optimization success.
- If similarity improves but AIGC worsens, mark `PARTIAL_SUCCESS_SIMILARITY_ONLY_AIGC_FAILED`.
- When the similarity target is already met, downgrade similarity repair to stability check.
- When AIGC remains above the user target, continue through `THREE_MODE_COLOR_BAND_WORKFLOW` with `task_type = aigc_only`, then run `AIGC_REGRESSION_GUARD`.
- Do not continue reducing similarity if that pushes total length beyond budget.
- If similarity is acceptable but AIGC still needs work, mark `SIMILARITY_OK_AIGC_NEEDS_FOCUSED_REPAIR`.
- If AIGC improves but the draft exceeds the length budget, mark `AIGC_IMPROVED_LENGTH_BUDGET_FAILED`.

### Similarity High, AIGC Low

Use `task_type = similarity_only` inside `THREE_MODE_COLOR_BAND_WORKFLOW`. Focus on source expression, citation boundaries, and thesis-specific framing. Do not over-stylize.

### AIGC High, Similarity Low

Use `task_type = aigc_only` inside `THREE_MODE_COLOR_BAND_WORKFLOW`, then apply internal deep-rewrite actions. Rebuild rhythm, concrete objects, paragraph structure, and sentence relationships.

### Both High

Use three rounds:

1. First pass: handle similarity-risk and source-close expression.
2. Second pass: run AIGC deep rewrite.
3. Third pass: review terms, citations, data, formulas, and conclusions.

### Citation Involved

Citation integrity outranks risk reduction:

- Do not delete sources.
- Do not disguise cited views as original claims.

### Technical Entity Involved

For formulas, code, interfaces, fields, and data:

- Keep core entities unchanged.
- Rewrite only surrounding explanatory prose.

### No Report

- Do not claim precise similarity reduction.
- Run heuristic fallback only.
- Recommend using a report for further localization.

## Relation To SKILL.md

Used internally by `THREE_MODE_COLOR_BAND_WORKFLOW` when `task_type = dual_optimization` or `fallback_heuristic: true`.
