# Three-Mode Color-Band Workflow

## Purpose

This workflow defines the default user-facing operating model for thesis risk revision:

1. Similarity-only revision.
2. AIGC-only revision.
3. Dual revision.

It supports plain-text input and file input. It uses report color bands when the user provides a similarity or AIGC report. It does not promise any external detection result.

## Forced Routing Priority

When the completed intake satisfies all of the following, this workflow is mandatory:

1. Mode is AIGC-only.
2. Input includes a DOCX AIGC color report or equivalent color-marked AIGC report.
3. The user provides or accepts red/orange/purple/black color rules.
4. The user requests character control, file-copy output, or no broad full-text rewrite.

Do not route this case to plain `AIGC_ONLY` or generic polishing.

Additional overlays:

- If the report is for the original thesis before any revision, use `FIRST_PASS_RED_ORANGE_ENGINE`.
- If the report is for a revised/current draft, use `CURRENT_REPORT_RED_ORANGE_ENGINE`.
- If the task includes a first/second/third-round report or orange accumulation after a prior revision, overlay `AIGC_PLATEAU_BREAKER`.
- If the discipline is human resource management, business administration, marketing, education management, or public administration, overlay `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`.

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

This is an internal color-band branch, not a separate entry mode. The old standalone AIGC-only and report-AIGC behavior is consolidated here and then handed to `FIRST_PASS_RED_ORANGE_ENGINE` or `CURRENT_REPORT_RED_ORANGE_ENGINE` when red/orange report bands exist.

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

If the AIGC report belongs to a revised/current draft, use `references/current_report_red_orange_engine.md` and `prompts/mode_current_report_red_orange.md`. Current-report mode must process all red and all orange fragments and output red-orange coverage acceptance.

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

Deep AIGC rewriting is no longer a standalone entry mode. Its usable parts are embedded in this internal iteration:

- diagnose why a red/orange fragment has its color;
- avoid synonym-only replacement;
- rebuild the fragment by changing information order, local evidence placement, sentence relationships, or template skeleton;
- run a finite self-audit before accepting the paragraph.

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

## Red-Orange Coverage Acceptance Table

## Unprocessed Red-Orange List

## Red-Orange Paragraph Processing Record
```

Completion is forbidden when current-report red/orange fragments exist without processing records.

## Safety

- Do not fabricate report color meanings, percentages, source names, or risk levels.
- Do not delete necessary citations.
- Do not turn source-dependent content into uncited original writing.
- Do not fabricate data, experiments, interviews, code, APIs, logs, screenshots, or running results.
- Do not damage formulas, code, paths, table names, field names, parameters, or reference entries.

## Relation To SKILL.md

Use this workflow as the high-level operating model for color-band tasks. Historical standalone similarity, AIGC, report-AIGC, report-similarity, dual, and deep-rewrite modes are internal branches only; they are not user-facing entry modes in the slim router.
