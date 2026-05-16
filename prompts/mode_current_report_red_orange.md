# Prompt: CURRENT_REPORT_RED_ORANGE_ENGINE

Use this prompt when the user provides a revised/current thesis draft plus its current AIGC color report.

Do not use this prompt for `original thesis + original report`; that case uses `FIRST_PASS_RED_ORANGE_ENGINE`.

## Inputs

- Current or revised thesis text or file path.
- Current AIGC color report, preferably DOCX when color metadata exists.
- Red/orange/purple/black color legend.
- User mode, usually AIGC-only.
- Character constraint, usually whole-thesis `±10%`.
- Protected list.
- Discipline or thesis type.

## 1. Forced Mode Decision

```yaml
selected_mode: THREE_MODE_COLOR_BAND_WORKFLOW
sub_engine: CURRENT_REPORT_RED_ORANGE_ENGINE
plain_aigc_only_forbidden: true
generic_polish_forbidden: true
current_report_not_original_report:
docx_color_report:
color_legend_confirmed:
character_delta_guard: enabled
overlay_aigc_plateau_breaker:
overlay_social_science_template_bottleneck:
```

If the input is a current report after one or more rewrites, do not route to `FIRST_PASS_RED_ORANGE_ENGINE`.

## 2. Frozen Zones

Freeze by default:

- black or low-risk text;
- cover;
- table of contents;
- declaration or promise letter;
- reference list;
- appendix;
- school template text;
- formulas, code, paths, APIs, table names, field names, parameters, experiment data.

Purple text is processed only when it is in the same paragraph as red/orange or needed for local coherence.

## 3. Current Report Red-Orange Task Table

| id | section | paragraph_id | current_report_band | mapped_confidence | original_fragment | risk_reason | protected_items | required_strategy |
|---|---|---|---|---|---|---|---|---|

Rules:

- Include all current-report red paragraphs.
- Include all current-report orange paragraphs.
- Do not process only red.
- Do not run broad full-text polishing.
- A red/orange paragraph without a task-table row is unprocessed.

## 4. Paragraph Processing Record

Every red/orange paragraph must produce one record:

| id | section | original_band | original_fragment | risk_reason | action_type | evidence_used | char_delta | self_audit_result | passed |
|---|---|---|---|---|---|---|---:|---|---|

Allowed action types:

- `A_EVIDENCE_RECONSTRUCTION`
- `B_ARGUMENT_PATH_REWRITE`
- `C_TEMPLATE_SKELETON_BREAK`
- `D_AUTHOR_MATERIAL_REQUEST`

If a red/orange paragraph has no action type, it is unprocessed.

For management and HR papers, `evidence_used` must state whether the rewrite used company, questionnaire, interview, process, post, form, responsibility, review-cycle, or indicator evidence.

## 5. AIGC Acceptance Self-Audit

For each red/orange paragraph, run `references/aigc_acceptance_self_audit.md`:

| id | synonym_only | template_still_present | mechanical_enumeration | abstract_noun_dense | lacks_local_context | lacks_evidence_or_boundary | more_ai_like | result | next_action |
|---|---|---|---|---|---|---|---|---|---|

If any item fails:

1. Run a second-pass rewrite with a different strategy.
2. Audit again.
3. If still failing, output `workflow/author_evidence_pack_template.md` and mark the paragraph not complete.

## 6. Candidate Revision

Output only safe revised red/orange paragraphs.

Requirements:

- Use replacement-based reconstruction.
- Avoid synonym-only rewriting.
- Avoid smoother generic management prose.
- Preserve citations, facts, data, formulas, code, APIs, paths, table names, fields, parameters, references, and conclusions.
- Do not fabricate questionnaire, interview, company, process, or indicator evidence.
- If evidence is missing, use `D_AUTHOR_MATERIAL_REQUEST` rather than generic management prose.

## 7. Red-Orange Coverage Acceptance Table

| current_report_red_total | current_report_orange_total | processed_red_count | processed_orange_count | unprocessed_red_orange_count | completion_status |
|---:|---:|---:|---:|---:|---|

If `unprocessed_red_orange_count` is greater than zero, `completion_status` must not be `COMPLETED`.

## 8. Unprocessed Red-Orange List

| id | section | paragraph_id | original_band | reason_not_processed | required_next_action |
|---|---|---|---|---|---|

Allowed reasons:

- `PROTECTED_CONTENT`
- `LOW_MAPPING_CONFIDENCE`
- `UNMAPPED`
- `EVIDENCE_LIMITED`
- `CHARACTER_DELTA_BLOCKED`
- `SECOND_PASS_FAILED`

## 9. Character Delta Table

| scope | original_chars | revised_chars | delta_chars | delta_ratio | allowed_range | status |
|---|---:|---:|---:|---:|---|---|

## 10. Final Gate

The task can be marked complete only if:

- all red current-report paragraphs are represented;
- all orange current-report paragraphs are represented;
- every represented paragraph has a processing record;
- every red/orange record has one of the four allowed action types;
- unprocessed red/orange count is zero;
- character delta guard passes;
- integrity checks pass.

No external detection result is promised.
