# Report Feedback Loop

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Purpose

Use this workflow whenever the user uploads a new similarity report, AIGC report, or revised draft after a previous pass.

## Inputs

Read user-provided:

- Original text.
- Current draft.
- Historical draft.
- Similarity report.
- AIGC report.

## Metrics Record

Record only values that the user provides:

```yaml
similarity_before:
aigc_before:
similarity_after:
aigc_after:
target_similarity:
target_aigc:
```

## Status Judgment

Classify the trend as one of:

- `both_improved`
- `similarity_improved_aigc_worse`
- `aigc_improved_similarity_worse`
- `both_worse`
- `no_clear_change`

## Next-Step Selection

- `both_improved` but not at target: continue targeted second pass.
- `similarity_improved_aigc_worse`: enter `AIGC_REGRESSION_GUARD`.
- `aigc_improved_similarity_worse`: enter Similarity Re-expansion Check.
- `both_worse`: discard the current strategy and return to the previous draft or original source.
- `no_clear_change`: review whether evidence density is too low or report mapping is inaccurate.

## Next-Round Task Table

| section | paragraph_id | original_risk | current_risk | target_gap | failure_reason | rewrite_mode | required_evidence | protected_items | next_action |
|---|---|---|---|---|---|---|---|---|---|

## Relation To SKILL.md

Use this file in `REPORT_FEEDBACK_LOOP` and `TARGETED_MULTIPASS_ENGINE`.
