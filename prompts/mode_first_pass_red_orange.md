# Prompt: FIRST_PASS_RED_ORANGE_ENGINE

Use this prompt when the user provides the original thesis and the original AIGC report and wants the first revision to attack both red and orange bands.

Do not use this prompt for a revised/current draft plus a current report after prior rewriting. That case uses `prompts/mode_current_report_red_orange.md`.

## Inputs

- Original thesis text.
- Original AIGC report.
- Color/risk-band meaning.
- User target, if provided.
- Original character count, if provided.
- Protected list.
- Discipline or thesis type.

## 1. Mode Decision

```yaml
enter_first_pass_red_orange_engine:
reason:
report_bands_detected:
red_is_primary_target: true
orange_is_primary_target: true
purple_policy: local_cleanup_only
white_policy: freeze
```

Do not invent report percentages or color meanings. If the report meaning is unclear, ask the user or mark it uncertain.

## 2. Character Delta Guard

Use `references/character_delta_guard.md`.

```yaml
original_chars:
allowed_delta_ratio: 10%
min_allowed_chars:
max_allowed_chars:
current_estimated_delta:
character_delta_status:
```

If the user provides another allowed range, use the user's range.

## 3. Red-Orange Task Table

| id | section | paragraph_id | report_band | mapped_confidence | risk_pattern | protected_items | target_band | action_type | max_internal_passes |
|---|---|---|---|---|---|---|---|---|---:|

Rules:

- Include both red and orange paragraphs.
- Do not include black/white paragraphs unless they are directly connected to a red/orange fragment.
- Purple paragraphs are optional low-intensity cleanup.
- Every red/orange paragraph must use one action type:
  - `A_EVIDENCE_RECONSTRUCTION`
  - `B_ARGUMENT_PATH_REWRITE`
  - `C_TEMPLATE_SKELETON_BREAK`
  - `D_AUTHOR_MATERIAL_REQUEST`
- A red/orange paragraph without one of these action types is unprocessed.

## 4. Sentence-Level Localization

| id | paragraph_id | sentence_id | sentence | band | aigc_pattern | repair_action | length_action | protected_items |
|---|---|---|---|---|---|---|---|---|

Process 1-3 key sentences per paragraph unless the whole paragraph skeleton is the problem.

## 5. Internal Loop Plan

For each red/orange paragraph:

```yaml
paragraph_id:
pass_1_action:
pass_1_self_audit:
pass_2_needed:
pass_2_action:
stop_reason:
```

Allowed stop reasons:

- `PURPLE_BLACK_HEURISTIC_TARGET_REACHED`
- `PROTECTED_STOP`
- `EVIDENCE_LIMITED_STOP`
- `CHARACTER_DELTA_FAIL`
- `NO_PROGRESS_INTERNAL_LOOP`

## 6. Candidate Revision

Output only safe revised paragraphs.

Requirements:

- Prefer replacement over appending.
- Avoid uncontrolled expansion.
- Use at least two valid repair moves for red/orange paragraphs.
- Do not repeat the same rewrite move if the first internal pass fails.
- Preserve citations, data, technical terms, code, formulas, paths, parameters, table names, and field names.
- Do not fabricate evidence.

If evidence is missing, output an author material request using `workflow/author_evidence_pack_template.md` instead of generating generic management prose.

## 7. Character Delta Table

| scope | original_chars | revised_chars | delta_chars | delta_ratio | allowed_range | status |
|---|---:|---:|---:|---:|---|---|

## 8. Self Audit

- red_band_handled:
- orange_band_handled:
- all_red_orange_have_action_type:
- purple_black_heuristic_target:
- white_freeze_respected:
- repeated_strategy_avoided:
- synonym_only_rewrite_found:
- social_science_bottleneck_enabled:
- author_evidence_pack_needed:
- character_delta_status:
- integrity_check:
- human_evidence_needed:
- external_detection_promise: false

## 9. First-Pass Failure Branch

If the user reports that original-thesis first-pass testing barely changed AIGC risk, output:

| check_item | result | evidence | next_fix |
|---|---|---|---|
| DOCX color extraction performed |  |  |  |
| red-orange coverage 100% |  |  |  |
| A/B/C/D action recorded |  |  |  |
| synonym-only rewrite avoided |  |  |  |
| social-science bottleneck enabled |  |  |  |
| author evidence pack requested when needed |  |  |  |

Status: `FIRST_PASS_FAILURE` unless all checks pass.

## Safety

This prompt uses report feedback to guide writing-risk revision. It does not promise any real detector outcome and does not simulate, crack, or reverse engineer detection systems.
