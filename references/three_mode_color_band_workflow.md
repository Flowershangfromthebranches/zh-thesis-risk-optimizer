# Three-Mode Color-Band Workflow

## Purpose

This workflow defines the default user-facing operating model for thesis risk revision:

1. Similarity-only revision.
2. AIGC-only revision.
3. Dual revision.

It supports plain-text input and file input. It uses report color bands when the user provides a similarity or AIGC report. It does not promise any external detection result.

## Color Band Definitions

Use these defaults unless the user provides another report legend:

| color | risk meaning | default handling |
|---|---|---|
| red | AIGC or similarity suspicion above 70%, high risk | primary target |
| orange | AIGC or similarity suspicion from 60% to 70%, medium risk | primary target |
| purple | AIGC or similarity suspicion from 50% to 60%, light risk | optional light cleanup |
| black | AIGC or similarity suspicion below 50%, low risk | freeze / no edit |
| gray / white | low-risk, unmarked, or non-target area | ignore unless tied to red/orange context |

Red and orange are both main work areas. Do not wait for orange to become a later plateau.

## Global Character Control

All modes must apply `references/character_delta_guard.md`.

Default whole-thesis rule:

- `min_total_chars = original_chars * 0.90`.
- `max_total_chars = original_chars * 1.10`.
- If the original text has 10000 characters, the revised version must stay between 9000 and 11000 characters.

If the revised draft exceeds the allowed range, mark `CHARACTER_DELTA_FAIL` and run compression before completion.

## Mode 1: Similarity-Only

### With Similarity Report

Use report-driven similarity revision:

1. Parse report color legend.
2. Extract red and orange similarity fragments.
3. Map fragments back to source text.
4. Explain why each fragment may have been marked with that color.
5. Protect citations, source boundaries, formulas, code, data, table names, field names, and parameters.
6. Revise red and orange fragments first.
7. Aim heuristically to reduce red/orange fragments to purple or black style level when safe.
8. Leave gray/white/black text unchanged.
9. Apply character delta guard.

### Without Similarity Report

Use heuristic similarity revision:

1. Diagnose definitions, textbook-like background, literature-review stacking, source-close wording, and repeated common expressions.
2. Prioritize high-editability paragraphs.
3. State that a similarity report would provide better localization.
4. Do not claim precise report movement.

## Mode 2: AIGC-Only

### With AIGC Report

Use report-driven AIGC revision:

1. Parse report color legend.
2. Extract red and orange AIGC fragments.
3. Map fragments back to source text.
4. Explain why each fragment may have been marked with that color.
5. Run sentence-level localization for red/orange fragments.
6. Rewrite red and orange fragments with replacement-based reconstruction.
7. Internally self-audit whether revised text is closer to purple/black style level.
8. Leave gray/white/black text unchanged.
9. Apply character delta guard.

### Without AIGC Report

Use heuristic AIGC revision:

1. Scan for template openings, mechanical connectors, generic endings, abstract noun inflation, over-smooth rhythm, and repeated AI-like phrases.
2. Prioritize high-risk and high-editability paragraphs.
3. State that an AIGC report would provide better localization.
4. Do not claim precise report movement.

## Mode 3: Dual Revision

Dual revision combines the two modes above.

Default order:

1. Similarity-only pass.
2. AIGC-only pass.
3. Character delta check.
4. Citation, source-boundary, data, conclusion, and technical protection review.

If the user provides both reports:

- Process red/orange similarity fragments first.
- Then process red/orange AIGC fragments.
- If the same paragraph appears in both reports, treat it as a dual-risk priority task.

If the user provides only one report:

- Process the report-driven dimension first.
- Then run heuristic diagnosis for the other dimension.
- State that the missing report limits localization.

## Internal Iteration

For each red/orange fragment:

1. Diagnose color reason.
2. Select repair moves.
3. Revise.
4. Self-audit against color-band target.
5. If still red/orange-like, run a limited retry with a different repair move.
6. Stop when the text is heuristically purple/black-like, protected, evidence-limited, character-delta failed, or no-progress.

Default:

- `max_internal_passes = 2`.
- A third internal pass requires enough evidence and must remain within the character delta guard.
- Never recurse indefinitely.

## Output Requirements

Use these blocks when relevant:

```markdown
## Mode Decision

## Color Legend

## Red-Orange Task Table

## Color Reason Analysis

## Internal Iteration Log

## Candidate Revision

## Character Delta Table

## Integrity Review
```

## Safety

- Do not fabricate report color meanings, percentages, source names, or risk levels.
- Do not delete necessary citations.
- Do not turn source-dependent content into uncited original writing.
- Do not fabricate data, experiments, interviews, code, APIs, logs, screenshots, or running results.
- Do not damage formulas, code, paths, table names, field names, parameters, or reference entries.

## Relation To SKILL.md

Use this workflow as the high-level operating model before selecting specific prompts such as `SIMILARITY_ONLY`, `AIGC_ONLY`, `REPORT_AIGC_ONLY`, `REPORT_SIMILARITY_ONLY`, or `DUAL_OPTIMIZATION`.
