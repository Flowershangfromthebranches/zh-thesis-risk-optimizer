# Prompt: THREE_MODE_COLOR_BAND_WORKFLOW

Use this prompt as the default color-band workflow for similarity-only, AIGC-only, and dual revision. These are internal branches inside `THREE_MODE_COLOR_BAND_WORKFLOW`, not separate user-facing entry modes.

## Inputs

- User mode request: similarity-only, AIGC-only, or dual.
- Plain text or file path.
- Similarity report, if provided.
- AIGC report, if provided.
- Color legend, if provided.
- Original character count, if available.
- Protected list.

## 1. Mode Decision

```yaml
selected_mode:
input_type: plain_text_or_file
has_similarity_report:
has_aigc_report:
report_driven:
fallback_heuristic:
file_copy_required:
character_delta_guard: enabled
allowed_delta_ratio: 10%
forced_route_applied:
forbid_plain_aigc_only:
current_report_red_orange_engine:
overlay_aigc_plateau_breaker:
overlay_social_science_template_bottleneck:
```

Forced route:

- If mode is AIGC-only, input includes a DOCX AIGC color report, red/orange/purple/black rules are provided, and the user requests character control or no broad full-text rewrite, set `selected_mode: THREE_MODE_COLOR_BAND_WORKFLOW`.
- Do not route to an old standalone AIGC entry or generic polishing.
- If the report is for a revised/current draft, set `current_report_red_orange_engine: true`.
- If the report is after a first rewrite and orange remains concentrated, set `overlay_aigc_plateau_breaker: true`.
- If the discipline is HR, business administration, marketing, education management, or public administration, set `overlay_social_science_template_bottleneck: true`.

## 2. Color Legend

Use the default legend unless the report states otherwise:

| color | suspicion range | handling |
|---|---|---|
| red | above 70% | primary target |
| orange | 60%-70% | primary target |
| purple | 50%-60% | light cleanup |
| black | below 50% | freeze |
| gray/white | low-risk or non-target | ignore |

Do not invent color meanings when the report uses a different legend or does not explain colors.

## 3. File Handling

If input is a file, use `references/file_input_copy_workflow.md`:

```yaml
original_file:
copied_file:
original_untouched: true
format_preservation_plan:
```

Do not edit the original file directly.

## 4. Red-Orange Task Table

| id | mode | section | paragraph_id | report_band | color_reason | mapped_confidence | target_band | protected_items | action |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- Red and orange are primary targets.
- Purple is optional light cleanup.
- Black/gray/white text is frozen unless required for context.
- For current reports, every red and every orange paragraph must appear in the table.
- Do not process only red.
- Do not mark completion if any current-report red/orange paragraph is missing from the task table.

## 4.1 Red-Orange Coverage Acceptance Table

Required for current AIGC reports:

| current_report_red_total | current_report_orange_total | processed_red_count | processed_orange_count | unprocessed_red_orange_count | completion_status |
|---:|---:|---:|---:|---:|---|

If `unprocessed_red_orange_count > 0`, `completion_status` must not be `COMPLETED`.

## 4.2 Paragraph Processing Record

Required for every current-report red/orange paragraph:

| id | section | original_band | original_fragment | risk_reason | action_type | rewrite_strategy | evidence_used | char_delta | self_audit_result | passed |
|---|---|---|---|---|---|---|---|---:|---|---|

No record means the paragraph is unprocessed.

Allowed `action_type` values:

- `A_EVIDENCE_RECONSTRUCTION`
- `B_ARGUMENT_PATH_REWRITE`
- `C_TEMPLATE_SKELETON_BREAK`
- `D_AUTHOR_MATERIAL_REQUEST`

## 4.3 Unprocessed Red-Orange List

| id | section | paragraph_id | original_band | reason_not_processed | required_next_action |
|---|---|---|---|---|---|

## 5. Internal Iteration Log

| id | pass | diagnosis | repair_move | self_audit_result | next_action |
|---|---:|---|---|---|---|

Default:

- `max_internal_passes = 2`.
- Use a different repair move on retry.
- Stop for protected content, evidence limits, character-delta failure, or no progress.

## 6. Candidate Revision

Output only text that is safe to change.

Requirements:

- Preserve citations, source boundaries, formulas, code, paths, parameters, table names, field names, data, and conclusions.
- Do not fabricate facts.
- Prefer replacement-based rewriting.
- Use deep rewrite only as an internal action: change information order, evidence placement, sentence relationship, or template skeleton rather than swapping words.
- Keep whole-thesis character change within `±10%`.

## 7. Character Delta Table

| scope | original_chars | revised_chars | delta_chars | delta_ratio | allowed_range | status |
|---|---:|---:|---:|---:|---|---|

## 8. Writeback Table

Use only for file input.

| id | source_location | original_text | revised_text | mapping_confidence | writeback_status |
|---|---|---|---|---|---|

## 9. Integrity Review

- original_file_untouched:
- report_facts_not_fabricated:
- citations_preserved:
- technical_items_preserved:
- character_delta_status:
- red_orange_processed:
- red_orange_coverage_acceptance:
- unprocessed_red_orange_count:
- purple_black_target_self_audit:
- human_review_needed:

## Safety

This workflow is for writing-risk optimization only. It does not promise that any external detection platform will return a specific color, percentage, or result.
