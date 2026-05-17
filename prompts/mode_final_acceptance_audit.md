# Prompt: FINAL_ACCEPTANCE_AUDIT

Use this prompt at the end of every report-driven or file-copy task.

Do not mark a task complete until this audit passes.

## Inputs

- Intake confirmation.
- Risk intake decision from `RISK_INTAKE_GATE`.
- Discipline strategy router result.
- Color band router result.
- Purple band rebalancer result.
- Global style variance result.
- Mandatory chain trace.
- DOCX color extraction summary.
- Red-orange task table.
- Paragraph processing records.
- Character delta table.
- Protected item review.
- Author evidence requests, if any.
- Controlled humanization report (if applicable).
- Local escalated humanization report (if applicable).
- Thesis register guard report (if applicable).
- Academic tone guard report (if applicable).
- OOXML patch log (if applicable).
- Duplicate insertion guard report (if applicable).
- Rewrite application gate report (if DOCX writeback or patching occurred).
- Template residue detector report.
- Minimum diff-ratio report for red/orange target paragraphs.

## 1. Mandatory Chain Trace

| step | required | executed | evidence |
|---|---|---|---|
| RISK_INTAKE_GATE | yes |  |  |
| DISCIPLINE_STRATEGY_ROUTER | yes |  |  |
| INTAKE_WIZARD_PRECHECK | yes |  |  |
| FILE_INPUT_COPY_WORKFLOW |  |  |  |
| OOXML_DOCX_PATCH_WORKFLOW when DOCX |  |  |  |
| DOCX_COLOR_REPORT_EXTRACTION |  |  |  |
| THREE_MODE_COLOR_BAND_WORKFLOW |  |  |  |
| COLOR_BAND_ROUTER | yes when color report exists |  |  |
| FIRST_PASS_RED_ORANGE_ENGINE or CURRENT_REPORT_RED_ORANGE_ENGINE |  |  |  |
| SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable |  |  |  |
| CONTROLLED_HUMANIZATION_ENGINE when applicable |  |  |  |
| LOCAL_ESCALATED_HUMANIZATION when triggered |  |  |  |
| PURPLE_BAND_REBALANCER when triggered |  |  |  |
| GLOBAL_STYLE_VARIANCE_ENGINE | yes for AIGC color-report work |  |  |
| REWRITE_APPLICATION_GATE when DOCX writeback or patch verification is required |  |  |  |
| TEMPLATE_RESIDUE_DETECTOR |  |  |  |
| THESIS_REGISTER_GUARD |  |  |  |
| AIGC_REGRESSION_GUARD |  |  |  |
| FIRST_PASS_EFFECTIVENESS_GATE |  |  |  |
| FINAL_ACCEPTANCE_AUDIT | yes | yes | current table |

If a required step is missing, final status is `BLOCKED`.

## 2. Red-Orange Coverage

| red_total | orange_total | processed_red | processed_orange | unprocessed_red_orange | completion_status |
|---:|---:|---:|---:|---:|---|

If `unprocessed_red_orange > 0`, final status is not `COMPLETED`.

## 3. Paragraph Action Verification

| id | original_band | action_type | processing_record_exists | audit_passed | evidence_status |
|---|---|---|---|---|---|

Allowed action types:

- `A_EVIDENCE_RECONSTRUCTION`
- `B_ARGUMENT_PATH_REWRITE`
- `C_TEMPLATE_SKELETON_BREAK`
- `D_AUTHOR_MATERIAL_REQUEST`

If a red/orange paragraph has no action type, treat it as unprocessed.

## 4. Social-Science Hard Rule

When the paper is human resource management, business administration, marketing, education management, or public administration:

- confirm `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` was enabled;
- reject generic management prose that only says 构建体系, 提升效率, 优化流程, 强化能力, 丰富渠道, 数据驱动, 智能高效, or 提供参考;
- confirm missing evidence triggered `workflow/author_evidence_pack_template.md`.

## 5. Regression Review

| item | result | evidence |
|---|---|---|
| synonym-only rewrite found |  |  |
| more formal / smoother / more AI-like |  |  |
| abstract management jargon increased |  |  |
| over-humanization (too colloquial/casual) |  |  |
| A/B/C/D action missing |  |  |
| protected content damaged |  |  |
| fabricated evidence found |  |  |
| character delta status |  |  |

If any red/orange paragraph only replaces words, preserves the same template skeleton, or becomes more formal without local evidence, final status is not `COMPLETED`.

If any paragraph is too colloquial, diary-like, or social-media-like, final status is not `COMPLETED`.

## 6. Risk Intake Review

| item | result | evidence |
|---|---|---|
| current_similarity_rate |  |  |
| current_aigc_rate |  |  |
| target_similarity_rate |  |  |
| target_aigc_rate |  |  |
| selected_strategy |  |  |
| max_humanization_level |  |  |
| level_4_allowed | false / local_only |  |
| similarity_status |  |  |

If either current rate is missing, set `final_delivery_status = BLOCKED`.

## 7. Controlled Humanization Review

When `CONTROLLED_HUMANIZATION_ENGINE` was active:

| item | result | evidence |
|---|---|---|
| intensity level used | 1 / 2 / 3 / 3.5 / N/A |  |
| level_4_self_selected | yes/no | must be no |
| academic_tone_guard_result | PASSED / FAILED / N/A |  |
| thesis_register_guard_result | PASSED / PASSED_AFTER_REPAIR / FAILED / N/A |  |
| over_humanization_regression_found | yes / no |  |
| level_3_warning_issued | yes / no |  |

## 8. Local Escalation Review

When `LOCAL_ESCALATED_HUMANIZATION` was active or required:

| item | result | evidence |
|---|---|---|
| local_escalation_applied | yes/no/not_applicable |  |
| local_escalation_sections | none/list |  |
| level_4_forbidden_section_found | yes/no |  |
| thesis_register_guard_result | PASSED / PASSED_AFTER_REPAIR / FAILED / N/A |  |
| style_risk_warning_issued | yes/no/not_applicable |  |
| academic_tone_repair_plan | present/missing/not_applicable |  |

If local escalation was required but skipped, set `final_delivery_status = LOCAL_ESCALATION_SKIPPED`.
If Level 4 was used in 摘要, 英文摘要, 理论基础, or 结论, set `final_delivery_status = LEVEL_4_SECTION_BLOCKED`.

## 9. Format Preservation Review

When DOCX input was used:

| item | result | evidence |
|---|---|---|
| ooxml_patch_result | USED_AND_PASSED / USED_AND_FAILED / NOT_USED |  |
| duplicate_insertion_guard_result | PASSED / FAILED / N/A |  |
| format_preservation_result | PASSED / FAILED / N/A |  |
| page_count_change | +N / -N / 0 |  |
| resource_preservation | OK / FAIL |  |

## 10. Rewrite Application Review

When generated rewrites are written back to DOCX, confirm the rewrite was applied to the actual body text.

| item | result | evidence |
|---|---|---|
| rewrite_application_gate_result | PASSED / FAILED / N/A |  |
| original_text_hash_changed | yes / no / N/A |  |
| patched_text_matches_rewrite | yes / no / N/A |  |
| min_diff_ratio_passed | yes / no / N/A |  |
| unchanged_high_risk_sections | none / list |  |
| patch_status_summary | all_applied / patch_not_applied / patch_mismatch / patch_ineffective / N/A |  |

If `rewrite_application_gate_result = FAILED`, set `final_delivery_status = REWRITE_NOT_APPLIED_FAILURE`.

## 11. Template Residue Review

| item | result | evidence |
|---|---|---|
| template_residue_detector_result | PASSED / FAILED / N/A |  |
| template_residue_sections | none / list |  |
| residue_patterns_found | none / list |  |

If `template_residue_detector_result = FAILED`, set `final_delivery_status = TEMPLATE_RESIDUE_FAILURE`.

## 12. Purple And Global Style Review

| item | result | evidence |
|---|---|---|
| purple_targets_count |  |  |
| purple_action | skip / observe / light_rebalance / mandatory_rebalance |  |
| purple_band_rebalancer_result | PASSED / FAILED / NOT_RUN / NOT_REQUIRED |  |
| purple_deferred_reason | none / reason |  |
| purple_remaining_risk | low / medium / high / unknown |  |
| global_style_variance_result | PASSED / FAILED / NOT_RUN / NOT_APPLICABLE |  |

If `current_aigc_rate > target_aigc_rate` and `purple_action = skip`, set `final_delivery_status = PURPLE_BAND_NOT_HANDLED_FAILURE`.

If `stage = second_pass`, `third_pass`, or `current_report_pass`, and `purple_band_rebalancer_result = NOT_RUN` while AIGC remains above target, final status is not completed.

## 12. First-Pass Failure Branch

If the user says original first-pass testing barely changed AIGC risk, output:

| check_item | result | evidence | next_fix |
|---|---|---|---|
| DOCX color extraction performed |  |  |  |
| red-orange coverage 100% |  |  |  |
| synonym-only rewrite avoided |  |  |  |
| social-science bottleneck enabled |  |  |  |
| author evidence pack requested when needed |  |  |  |
| controlled humanization applied |  |  |  |
| local escalation applied when triggered |  |  |  |
| thesis register guard passed |  |  |  |
| academic tone guard passed |  |  |  |
| format preservation verified |  |  |  |
| rewrite application gate passed |  |  |  |
| template residue detector passed |  |  |  |
| red+orange below 40% |  |  |  |

If current AIGC was above 50 and remains above 50, do not only output "retest later"; route eligible residual targets to `LOCAL_ESCALATED_HUMANIZATION`.

Final status should be `FIRST_PASS_FAILURE` unless all checks pass and a new repair plan is ready.

## 13. Final Status and Delivery Status

Use `final_delivery_status` as the primary status:

| status | meaning |
|---|---|
| `COMPLETED` | All checks pass; ready to deliver |
| `FIRST_PASS_FAILURE` | First-pass effectiveness gate failed |
| `REWRITE_NOT_APPLIED_FAILURE` | Generated rewrite was not actually written into DOCX body text |
| `TEMPLATE_RESIDUE_FAILURE` | Patched output still contains high-risk template residue |
| `LOCAL_ESCALATION_SKIPPED` | Local Level 4 repair was required but not executed |
| `LEVEL_4_SECTION_BLOCKED` | Level 4 was used in a forbidden strict section |
| `PURPLE_BAND_NOT_HANDLED_FAILURE` | Purple needed rebalance but was skipped |
| `DISCIPLINE_PROFILE_MISSING_FAILURE` | Discipline profile was not selected |
| `GLOBAL_VARIANCE_NOT_RUN_FAILURE` | Global style variance check was skipped |
| `NEEDS_ACADEMIC_TONE_REPAIR` | AIGC reduced but academic tone guard failed |
| `FORMAT_FAILURE` | Duplicate insertion or format corruption detected |
| `FORMAT_RISK_REVIEW_REQUIRED` | OOXML patch not used but user requires DOCX format |
| `BLOCKED` | Mandatory chain step missing |
| `NEEDS_AUTHOR_EVIDENCE` | Author evidence missing |

Never promise external detector results.

## 14. Required Output Table (Extended)

The final output table must include these additional rows:

| item | result | evidence |
|---|---|---|
## 15. Required Output Table

The final output table must include all these rows:

| item | result | evidence |
|---|---|---|
| current_similarity_rate |  |  |
| current_aigc_rate |  |  |
| target_similarity_rate |  |  |
| target_aigc_rate |  |  |
| selected_strategy |  |  |
| selected_discipline_profile |  |  |
| discipline_strategy_router_result | PASSED / FAILED / NOT_APPLICABLE |  |
| color_band_router_result | PASSED / FAILED / NOT_APPLICABLE |  |
| purple_targets_count |  |  |
| purple_action | skip / observe / light_rebalance / mandatory_rebalance |  |
| purple_band_rebalancer_result | PASSED / FAILED / NOT_RUN / NOT_REQUIRED |  |
| purple_deferred_reason | none / reason |  |
| purple_remaining_risk | low / medium / high / unknown |  |
| global_style_variance_result | PASSED / FAILED / NOT_RUN / NOT_APPLICABLE |  |
| section_profile_violations | none / list |  |
| protected_element_violations | none / list |  |
| final_aigc_strategy_summary |  |  |
| max_humanization_level |  |  |
| level_4_allowed | false / local_only |  |
| similarity_status |  |  |
| local_escalation_applied | yes / no / not_applicable |  |
| local_escalation_sections | none / list |  |
| thesis_register_guard_result | PASSED / PASSED_AFTER_REPAIR / FAILED / NOT_APPLICABLE |  |
| DOCX color read | yes/no/not_applicable |  |
| red total / processed |  |  |
| orange total / processed |  |  |
| social-science bottleneck enabled | yes/no/not_applicable |  |
| synonym-only rewrite found | yes/no |  |
| formalization regression found | yes/no |  |
| character change | pass/fail |  |
| unprocessed paragraphs | count/list |  |
| author evidence needed | count/list |  |
| color migration assessment | 红转橙未突破 / 有效降低 / 无原版对比 |  |
| first-pass effectiveness gate | PASSED / FIRST_PASS_FAILURE / NOT_APPLICABLE |  |
| first_pass_effectiveness_gate_result | PASSED / FIRST_PASS_FAILURE / NOT_APPLICABLE |  |
| color_migration_conclusion | 有效降低 / 红转橙未突破 / 无原版对比 |  |
| red_to_orange_migration_detected | yes / no / not_applicable |  |
| next_required_route | FINAL_ACCEPTANCE_AUDIT / AIGC_PLATEAU_BREAKER / not_applicable |  |
| priority_sections | 摘要、理论基础、第五章、结论 / not_applicable |  |
| material_gap_table_required | yes / no / not_applicable |  |
| controlled_humanization_level | 1 / 2 / 3 / not_applicable |  |
| academic_tone_guard_result | PASSED / FAILED / NOT_APPLICABLE |  |
| ooxml_patch_result | USED_AND_PASSED / USED_AND_FAILED / NOT_USED |  |
| duplicate_insertion_guard_result | PASSED / FAILED / NOT_APPLICABLE |  |
| format_preservation_result | PASSED / FAILED / NOT_APPLICABLE |  |
| rewrite_application_gate_result | PASSED / FAILED / NOT_APPLICABLE |  |
| template_residue_detector_result | PASSED / FAILED / NOT_APPLICABLE |  |
| min_diff_ratio_passed | yes / no / not_applicable |  |
| patch_status_summary | all_applied / patch_not_applied / patch_mismatch / patch_ineffective / not_applicable |  |
| unchanged_high_risk_sections | none / list |  |
| template_residue_sections | none / list |  |
| over_humanization_regression_found | yes / no / not_applicable |  |
| final_delivery_status | COMPLETED / FIRST_PASS_FAILURE / REWRITE_NOT_APPLIED_FAILURE / TEMPLATE_RESIDUE_FAILURE / LOCAL_ESCALATION_SKIPPED / LEVEL_4_SECTION_BLOCKED / NEEDS_ACADEMIC_TONE_REPAIR / FORMAT_FAILURE / FORMAT_RISK_REVIEW_REQUIRED / BLOCKED / NEEDS_AUTHOR_EVIDENCE |  |
