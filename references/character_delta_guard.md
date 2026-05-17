# Character Delta Guard

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Purpose

`CHARACTER_DELTA_GUARD` controls total thesis character change during AIGC-focused or report-driven revision. It prevents both uncontrolled expansion and excessive compression.

## Default Rule

Unless the user specifies a different range:

- `allowed_total_delta_ratio = 10%`.
- `min_total_chars = original_chars * 0.90`.
- `max_total_chars = original_chars * 1.10`.

This is a whole-thesis guard, not a promise of any report result.

## Counting Scope

Use approximate character counts:

- Count Chinese CJK characters as primary thesis characters.
- Track English terms, code, URLs, paths, parameters, formulas, and citations as `protected_tokens`.
- The Skill is not a real counting program, but every whole-thesis output must estimate before/after character counts.

## Priority

Character control outranks non-essential detail expansion. It does not outrank:

- citation integrity,
- data correctness,
- technical identifiers,
- formulas,
- code,
- parameters,
- table names and field names,
- conclusions supported by evidence.

## Per-Paragraph Guidance

| paragraph_type | suggested_delta |
|---|---:|
| black/white low-risk | 0% |
| purple/light risk | -5% to +5% |
| orange/medium risk | -10% to +10% |
| red/high risk | -15% to +15% |
| evidence-limited but repairable | up to +20%, only when global budget allows |
| protected paragraph | surrounding text only |

Single paragraph growth above 20% must be justified. Whole-thesis growth or shrinkage beyond 10% is `CHARACTER_DELTA_FAIL`.

## Compression Pass

If the revised draft exceeds the allowed range:

1. Remove newly added generic background.
2. Delete repeated value claims.
3. Merge duplicate transition sentences.
4. Compress list introductions.
5. Keep evidence, data, citations, and technical identifiers.
6. Recalculate the estimated delta.

## Output Table

Every whole-thesis or multi-chapter pass should output:

| scope | original_chars | revised_chars | delta_chars | delta_ratio | allowed_range | status |
|---|---:|---:|---:|---:|---|---|

## Failure State

Use:

`CHARACTER_DELTA_FAIL`

when the revised draft is outside the allowed range and compression has not yet fixed it.

## Relation To SKILL.md

Use this file with `FIRST_PASS_RED_ORANGE_ENGINE`, `AIGC_FOCUSED_LENGTH_CONTROLLED`, and `LENGTH_BUDGET_CONTROLLER`.
