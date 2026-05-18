---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with forced risk intake, discipline-aware routing, color-band routing, purple-band rebalancing, global style variance checks, DOCX protection, local humanization, thesis-register guard, and final acceptance audit.
license: MIT
---

# zh-thesis-risk-optimizer

## 1. Role

This Skill helps revise Chinese thesis text for writing quality, AIGC writing-risk signals, similarity-risk expression, discipline-aware routing, report-color mapping, purple-band rebalancing, global style variance, citation-boundary integrity, file-copy handling, and final acceptance auditing.

It is not a detection-result promise tool. Scores and color targets are heuristic writing-risk references only. Report-driven workflows only process report content legally obtained and provided by the user.

## 2. Safety Boundaries

Do not:

- Promise external detection outcomes or fixed percentage changes.
- Crack, reverse engineer, simulate, or forge any detection system or report.
- Fabricate data, experiments, citations, report percentages, similarity sources, interviews, logs, code, interfaces, screenshots, companies, forms, indicators, or risk levels.
- Delete necessary citations or disguise sourced content as uncited original writing.
- Alter conclusions beyond provided evidence.
- Rewrite formulas, code, API paths, table names, field names, parameters, experiment data, reference entries, school declarations, or appendices for style.

When integrity or technical correctness conflicts with risk reduction, integrity wins.

## 3. Core Workflow

1. Run `RISK_INTAKE_GATE` before any rewrite route.
2. Use `INTAKE_WIZARD_PRECHECK` only to display and complete the intake template when the user has not supplied the required fields.
3. Run `DISCIPLINE_STRATEGY_ROUTER` before selecting rewrite moves.
4. On first contact for a new task, show `workflow/intake_request_template.md` and wait for the user's completed intake reply.
5. If `current_similarity_rate`, `current_aigc_rate`, or required color distribution is missing, output `INTAKE_INCOMPLETE`; file reading and report parsing may continue, but rewriting must not start.
6. Create a file copy for file input; never edit the original file directly.
7. If a DOCX color report is present, extract color metadata before plain text.
8. Run `COLOR_BAND_ROUTER` after report-color extraction.
9. Run `RISK_BAND_COVERAGE_GATE` after color routing to verify red/orange/purple coverage planning.
10. Select the minimal hard route from the mode router.
11. Build protected items and frozen zones before revision.
12. Process red/orange report targets with paragraph records and acceptance checks.
13. Run `PURPLE_BAND_REBALANCER` and `GLOBAL_STYLE_VARIANCE_ENGINE` when triggered.
14. Run `RISK_BAND_COVERAGE_GATE` again before final acceptance.
15. Run `FINAL_ACCEPTANCE_AUDIT`.
16. Do not mark completion if any required chain step, risk intake field, discipline profile, color-band decision, coverage gate item, or acceptance item is missing.

## 4. Hard Routing Rules

### 4.1 Risk Intake Gate

- Any task matching this Skill starts with `RISK_INTAKE_GATE`.
- Required risk fields: `current_similarity_rate`, `current_aigc_rate`, `target_similarity_rate`, `target_aigc_rate`, `task_type`, `has_similarity_report`, `has_aigc_color_report`, `preserve_docx_format_required`, `discipline`, `stage`, and current red/orange/purple/black counts or ratios when an AIGC color report exists.
- If `current_similarity_rate` or `current_aigc_rate` is missing, do not enter a rewrite chain. Output `INTAKE_INCOMPLETE` and ask for both current rates.
- Report parsing and file inspection may continue only to complete intake; rewriting must wait.
- `RISK_INTAKE_GATE` determines `selected_strategy`, `max_humanization_level`, `level_4_allowed`, `similarity_status`, and whether color distribution is sufficient for purple rebalancing decisions.

### 4.2 Discipline Strategy Gate

- `DISCIPLINE_STRATEGY_ROUTER` must run before rewrite strategy selection.
- It chooses a discipline profile and protected elements.
- Management strategies must not be forced onto computer-science, engineering, medicine, law, education, or humanities papers.
- If discipline confidence is low, request confirmation before strong humanization.

### 4.3 Intake Gate

- Any task matching this Skill starts with `INTAKE_WIZARD_PRECHECK`.
- First contact stops at the intake template.
- Required fields must be filled.
- Strongly recommended and optional fields must be filled or explicitly marked `无`, `跳过`, or `请自动判断`.
- If a completed intake template is already present, output `Intake Confirmation` and continue.

### 4.4 Mandatory First-Pass Chain

When the intake says:

- original thesis plus original AIGC color report;
- mode is AIGC-only;
- user gives red/orange/purple/black color rules;
- user asks to process red and orange together;
- user asks for character control or no broad full-text rewrite;

the mandatory chain is:

```text
RISK_INTAKE_GATE
-> DISCIPLINE_STRATEGY_ROUTER
-> FILE_INPUT_COPY_WORKFLOW
-> OOXML_DOCX_PATCH_WORKFLOW when DOCX format preservation is required
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> COLOR_BAND_ROUTER
-> RISK_BAND_COVERAGE_GATE
-> FIRST_PASS_RED_ORANGE_ENGINE
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when discipline matches management/social-science types
-> CONTROLLED_HUMANIZATION_ENGINE when AIGC remains high or discipline is template-heavy
-> LOCAL_ESCALATED_HUMANIZATION when RISK_INTAKE_GATE and later gates trigger local Level 4
-> PURPLE_BAND_REBALANCER when triggered
-> GLOBAL_STYLE_VARIANCE_ENGINE
-> REWRITE_APPLICATION_GATE
-> TEMPLATE_RESIDUE_DETECTOR
-> THESIS_REGISTER_GUARD
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> RISK_BAND_COVERAGE_GATE final check
-> FINAL_ACCEPTANCE_AUDIT
```

If any step is missing, the task cannot be marked complete.

### 4.5 Current-Report Chain

When the intake says the report is from a revised/current draft, use:

```text
RISK_INTAKE_GATE
-> DISCIPLINE_STRATEGY_ROUTER
-> FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> COLOR_BAND_ROUTER
-> RISK_BAND_COVERAGE_GATE
-> CURRENT_REPORT_RED_ORANGE_ENGINE
-> AIGC_PLATEAU_BREAKER when orange accumulation or multi-round slowdown exists
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when discipline matches management/social-science types
-> CONTROLLED_HUMANIZATION_ENGINE when AIGC remains high or discipline is template-heavy
-> LOCAL_ESCALATED_HUMANIZATION when RISK_INTAKE_GATE and later gates trigger local Level 4
-> PURPLE_BAND_REBALANCER when triggered
-> GLOBAL_STYLE_VARIANCE_ENGINE
-> REWRITE_APPLICATION_GATE
-> TEMPLATE_RESIDUE_DETECTOR
-> THESIS_REGISTER_GUARD
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> RISK_BAND_COVERAGE_GATE final check
-> FINAL_ACCEPTANCE_AUDIT
```

Do not use `FIRST_PASS_RED_ORANGE_ENGINE` for revised/current reports.

### 4.6 Color Band Rules

- `COLOR_BAND_ROUTER` splits red, orange, purple, and black text into different actions.
- Red and orange enter red-orange engines.
- Purple may enter `PURPLE_BAND_REBALANCER` when global AIGC remains high or style distribution is too uniform.
- Purple is counted and routed from the first color report, not after red/orange is cleared.
- Black text is frozen by default.
- `RISK_BAND_COVERAGE_GATE` verifies that every red/orange/purple target has valid handling, a valid low-intensity purple action, or a valid freeze reason.
- If red coverage is below 100%, orange coverage is below the required threshold, purple targets lack actions, or invalid skips exist, the task cannot be marked complete.

### 4.7 Social-Science Hard Rule

For human resource management, business administration, marketing, education management, and public administration, `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` is a hard rule during red/orange AIGC work.

If red/orange paragraphs lack company, questionnaire, interview, process, post, form, indicator, responsibility, review-cycle, or boundary evidence, request `workflow/author_evidence_pack_template.md`. Do not invent missing materials.

### 4.8 First-Pass Failure

If the user says the original-thesis test produced almost no AIGC improvement, mark `FIRST_PASS_FAILURE`, not plateau.

Check:

- DOCX color report was actually parsed.
- Red/orange coverage was 100%.
- The rewrite was not only synonym replacement.
- `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` was enabled when applicable.
- Author evidence was available or requested.
- The output had paragraph records and final acceptance audit.

Then output a failure-cause table and next repair plan.

### 4.9 DOCX Format Preservation

When input is DOCX and the user requires format preservation, use `OOXML_DOCX_PATCH_WORKFLOW` as the default writeback method. Only modify confirmed `w:t` text nodes in `word/document.xml`. Do not rebuild the entire DOCX. Preserve styles, numbering, headers, footers, footnotes, endnotes, comments, media, and rels.

Run `DOCX_DUPLICATE_INSERTION_GUARD` after every DOCX patch to prevent the failure mode where the same paragraph is inserted multiple times.

### 4.10 Thesis Register Guard

When `CONTROLLED_HUMANIZATION_ENGINE` or `LOCAL_ESCALATED_HUMANIZATION` is active, run `THESIS_REGISTER_GUARD` to prevent over-humanization. The thesis must remain in formal academic register. Strict sections such as 摘要, 英文摘要, 理论基础, and 结论 must not use chat-like expressions or Level 4 wording.

## 5. Minimal Mode Router

| Mode | Use When | Load |
|---|---|---|
| `RISK_INTAKE_GATE` | Before every rewrite task; collects current/target rates and selects strategy and humanization ceiling. | prompts/mode_risk_intake_gate.md, references/risk_intake_gate.md |
| `DISCIPLINE_STRATEGY_ROUTER` | Selects discipline profile, protection scope, and allowed humanization level. | prompts/mode_discipline_strategy_router.md, references/discipline_strategy_router.md |
| `INTAKE_WIZARD_PRECHECK` | Start of every matching task. | prompts/mode_intake_wizard.md, workflow/intake_request_template.md |
| `FILE_INPUT_COPY_WORKFLOW` | User provides DOCX/TXT/Markdown/LaTeX file input. | references/file_input_copy_workflow.md |
| `OOXML_DOCX_PATCH_WORKFLOW` | DOCX format preservation required; default writeback method. | references/ooxml_docx_patch_workflow.md, workflow/ooxml_patch_checklist.md |
| `DOCX_COLOR_REPORT_EXTRACTION` | User provides Word/DOCX color report. | references/docx_color_report_extraction.md |
| `THREE_MODE_COLOR_BAND_WORKFLOW` | Any AIGC/similarity/dual task with color bands. | prompts/mode_three_mode_color_band.md, references/three_mode_color_band_workflow.md |
| `COLOR_BAND_ROUTER` | Splits red/orange/purple/black bands into different actions. | references/color_band_router.md |
| `RISK_BAND_COVERAGE_GATE` | Verifies red/orange/purple target coverage before and after rewrite. | references/risk_band_coverage_gate.md |
| `FIRST_PASS_RED_ORANGE_ENGINE` | Original thesis plus original AIGC color report. | prompts/mode_first_pass_red_orange.md, references/first_pass_red_orange_engine.md |
| `CURRENT_REPORT_RED_ORANGE_ENGINE` | Revised/current thesis plus current AIGC color report. | prompts/mode_current_report_red_orange.md, references/current_report_red_orange_engine.md |
| `AIGC_PLATEAU_BREAKER` | Multi-round slowdown or orange accumulation. | prompts/mode_aigc_plateau_breaker.md, references/aigc_plateau_breaker.md |
| `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` | HR/management/social-science red-orange template risk. | prompts/mode_social_science_aigc_bottleneck.md, references/social_science_template_bottleneck.md, workflow/author_evidence_pack_template.md |
| `CONTROLLED_HUMANIZATION_ENGINE` | Internal engine for controlled de-AIGC humanization of social-science text. | prompts/mode_controlled_humanization.md, references/controlled_humanization_engine.md, references/academic_tone_guard.md |
| `LOCAL_ESCALATED_HUMANIZATION` | Local-only Level 4 escalation for high-risk residual red/orange/template sections. | references/local_escalated_humanization.md |
| `PURPLE_BAND_REBALANCER` | Low-intensity statistical rebalance for purple-band text. | prompts/mode_purple_band_rebalancer.md, references/purple_band_rebalancer.md |
| `GLOBAL_STYLE_VARIANCE_ENGINE` | Whole-thesis style uniformity check and local variance plan. | prompts/mode_global_style_variance.md, references/global_style_variance_engine.md |
| `REWRITE_APPLICATION_GATE` | Verifies generated rewrites were actually patched into DOCX body text. | references/rewrite_application_gate.md |
| `TEMPLATE_RESIDUE_DETECTOR` | Detects residual high-risk AIGC template sentences after patching. | references/template_residue_detector.md |
| `THESIS_REGISTER_GUARD` | Section-aware academic-register guard after local escalation and before regression audit. | references/thesis_register_guard.md |
| `AIGC_REGRESSION_GUARD` | Rewrite becomes smoother/more AI-like OR too colloquial/casual. | references/aigc_regression_guard.md, references/academic_tone_guard.md |
| `FIRST_PASS_EFFECTIVENESS_GATE` | Internal mandatory gate after first-pass rewrite; checks color migration, AIGC thresholds, tone, and format. | references/first_pass_effectiveness_gate.md |
| `FINAL_ACCEPTANCE_AUDIT` | End of every report-driven or file-copy task. | prompts/mode_final_acceptance_audit.md, references/final_acceptance_audit.md |

Internal sub-rules such as burstiness audit, orange-zone repair, conservative repair, structure rebuilding, evidence injection, paragraph strategies, second-pass rewrite, and effectiveness evaluation are not entry modes. Load them only through the main modes above when needed.

## 6. Standard Output Blocks

### Intake Confirmation

| field | value | status |
|---|---|---|

### Risk Intake Decision

| field | value | status |
|---|---|---|
| current_similarity_rate |  | required |
| current_aigc_rate |  | required |
| target_similarity_rate |  | required |
| target_aigc_rate |  | required |
| task_type |  | required |
| discipline |  | required |
| current_red_count / ratio |  | required when report exists |
| current_orange_count / ratio |  | required when report exists |
| current_purple_count / ratio |  | required when report exists |
| current_black_count / ratio |  | required when report exists |
| similarity_status |  |  |
| selected_strategy |  |  |
| max_humanization_level |  |  |
| level_4_allowed |  |  |

### Discipline Strategy Router Output

| field | value |
|---|---|
| detected_discipline |  |
| selected_profile |  |
| protected_elements |  |
| allowed_humanization_level |  |
| forbidden_rewrite_actions |  |
| preferred_rewrite_moves |  |

### Color Band Router Output

| field | value |
|---|---|
| red_targets |  |
| orange_targets |  |
| purple_targets |  |
| black_targets |  |
| red_count / red_ratio |  |
| orange_count / orange_ratio |  |
| purple_count / purple_ratio |  |
| black_count / black_ratio |  |
| purple_action | skip / observe / light_rebalance / mandatory_rebalance |
| frozen_black_targets |  |
| band_action_plan |  |

### Risk Band Coverage Gate Output

| field | value |
|---|---|
| risk_band_coverage_gate_result | passed / failed |
| red_targets_count |  |
| orange_targets_count |  |
| purple_targets_count |  |
| red_handled_count |  |
| orange_handled_count |  |
| purple_handled_count |  |
| red_coverage_rate |  |
| orange_coverage_rate |  |
| purple_coverage_rate |  |
| skipped_red_targets |  |
| skipped_orange_targets |  |
| skipped_purple_targets |  |
| valid_freeze_reasons |  |
| invalid_skips |  |
| next_batch_plan |  |

### Mandatory Chain Trace

| step | required | executed | evidence |
|---|---|---|---|

### Color Extraction Summary

| source | red_count | orange_count | purple_count | black_count | extraction_status |
|---|---:|---:|---:|---:|---|

### Red-Orange Task Table

| id | section | paragraph_id | report_band | mapped_confidence | original_fragment | risk_reason | required_action |
|---|---|---|---|---|---|---|---|

### Red-Orange Paragraph Processing Record

| id | section | original_band | original_fragment | action_type | evidence_used | char_delta | self_audit_result | passed |
|---|---|---|---|---|---|---:|---|---|

Allowed `action_type` values:

- `A_EVIDENCE_RECONSTRUCTION`
- `B_ARGUMENT_PATH_REWRITE`
- `C_TEMPLATE_SKELETON_BREAK`
- `D_AUTHOR_MATERIAL_REQUEST`

### Red-Orange Coverage Acceptance Table

| red_total | orange_total | processed_red | processed_orange | unprocessed_red_orange | completion_status |
|---:|---:|---:|---:|---:|---|

### Unprocessed Red-Orange List

| id | section | paragraph_id | original_band | reason_not_processed | required_next_action |
|---|---|---|---|---|---|

### First-Pass Failure Table

| check_item | result | evidence | next_fix |
|---|---|---|---|

### Final Acceptance Audit

| item | result | evidence |
|---|---|---|
| DOCX color read |  |  |
| red total / processed |  |  |
| orange total / processed |  |  |
| risk_band_coverage_gate_result |  |  |
| red_targets_count |  |  |
| orange_targets_count |  |  |
| purple_targets_count |  |  |
| red_coverage_rate |  |  |
| orange_coverage_rate |  |  |
| purple_coverage_rate |  |  |
| invalid_skips |  |  |
| next_batch_plan |  |  |
| social-science bottleneck enabled |  |  |
| synonym-only rewrite found |  |  |
| formalization regression found |  |  |
| character change |  |  |
| unprocessed paragraphs |  |  |
| author evidence needed |  |  |
| color migration assessment |  |  |
| first-pass effectiveness gate |  |  |
| controlled_humanization_level |  |  |
| current_similarity_rate |  |  |
| current_aigc_rate |  |  |
| target_similarity_rate |  |  |
| target_aigc_rate |  |  |
| selected_strategy |  |  |
| max_humanization_level |  |  |
| level_4_allowed |  |  |
| selected_discipline_profile |  |  |
| discipline_strategy_router_result |  |  |
| color_band_router_result |  |  |
| purple_band_rebalancer_result |  |  |
| purple_targets_count |  |  |
| purple_action |  |  |
| purple_deferred_reason |  |  |
| purple_remaining_risk |  |  |
| global_style_variance_result |  |  |
| section_profile_violations |  |  |
| protected_element_violations |  |  |
| final_aigc_strategy_summary |  |  |
| local_escalation_applied |  |  |
| local_escalation_sections |  |  |
| thesis_register_guard_result |  |  |
| academic_tone_guard_result |  |  |
| ooxml_patch_result |  |  |
| duplicate_insertion_guard_result |  |  |
| format_preservation_result |  |  |
| rewrite_application_gate_result |  |  |
| template_residue_detector_result |  |  |
| min_diff_ratio_passed |  |  |
| patch_status_summary |  |  |
| unchanged_high_risk_sections |  |  |
| template_residue_sections |  |  |
| over_humanization_regression_found |  |  |
| final_delivery_status |  |  |

## 7. File Layout

- `SKILL.md`: slim routing and hard chain only.
- `prompts/`: executable prompts for entry modes and internal engines.
- `references/`: detailed rules used by entry modes and internal engines.
- `workflow/`: intake, author evidence pack, file-copy, OOXML patch, and project templates.
- `tests/`: acceptance and regression checklists.
- `NOTICE` and `THIRD_PARTY_NOTICES.md`: attribution and license notes.
