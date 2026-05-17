# Final Acceptance Audit

## Purpose

`FINAL_ACCEPTANCE_AUDIT` is the final gate for report-driven and file-copy tasks. It prevents the Skill from claiming completion when the forced chain, color extraction, red/orange coverage, social-science evidence handling, regression checks, academic tone checks, or format preservation checks were skipped.

This audit is a workflow acceptance check. It does not promise any external detection result.

## Required Checks

The final output must report:

0. `RISK_INTAKE_GATE` result: current rates, target rates, selected strategy, humanization ceiling, and Level 4 permission.
1. Whether DOCX color metadata was read.
2. Red paragraph/fragment total and processed count.
3. Orange paragraph/fragment total and processed count.
4. Whether social-science bottleneck handling was enabled when applicable.
5. Whether any paragraph was only synonym replacement.
6. Whether any rewrite became more formal, smoother, or more AI-like.
7. Character change and whether it passed the user constraint.
8. Unprocessed paragraphs.
9. Author evidence still needed.
10. **Color migration check**: original vs. post-first-pass color distribution comparison.
11. **First-pass effectiveness gate result**: whether `FIRST_PASS_EFFECTIVENESS_GATE` conditions were checked and passed.
12. **Academic tone guard result**: whether `ACADEMIC_TONE_GUARD` found and corrected over-humanization.
13. **Format preservation result**: whether `OOXML_DOCX_PATCH_WORKFLOW` preserved the DOCX structure.
14. **Duplicate insertion guard result**: whether paragraph duplication was detected.
15. **Rewrite application gate result**: whether generated rewrites were actually patched into DOCX body text.
16. **Template residue detector result**: whether high-risk template sentences remain after patching.
17. **Minimum diff-ratio result**: whether every red/orange target meets the required character-level and structure-level change threshold.
18. **Patch status summary**: whether any target produced `patch_not_applied`, `patch_mismatch`, or `patch_ineffective`.
19. **Unchanged high-risk sections**: whether 摘要, 理论基础, 第五章, or 结论 still preserve their original high-risk skeleton.
20. **Template residue sections**: where residual template patterns remain.
21. **Local escalation result**: whether `LOCAL_ESCALATED_HUMANIZATION` was triggered, which sections it touched, and whether it stayed within section ceilings.
22. **Thesis register guard result**: whether `THESIS_REGISTER_GUARD` passed after controlled or local humanization.

This audit absorbs the older post-rewrite self-audit, anti-shallow-rewrite, and effectiveness-evaluation gates. These checks are no longer separate entry modes; completion depends on this final gate.

## Completion Rule

The task can be marked `COMPLETED` only when:

- all mandatory chain steps were executed;
- `current_similarity_rate`, `current_aigc_rate`, `target_similarity_rate`, and `target_aigc_rate` were collected before rewriting;
- DOCX color extraction was performed when a DOCX color report exists;
- every red/orange paragraph has a processing record;
- red/orange unprocessed count is zero;
- every red/orange paragraph used one of the allowed actions:
  - `A_EVIDENCE_RECONSTRUCTION`;
  - `B_ARGUMENT_PATH_REWRITE`;
  - `C_TEMPLATE_SKELETON_BREAK`;
  - `D_AUTHOR_MATERIAL_REQUEST`;
- social-science hard rule was enabled when applicable;
- no protected content was damaged;
- no fabricated data, interviews, citations, company facts, forms, systems, indicators, or report facts were introduced;
- if both `original_report_distribution` and `post_first_pass_report_distribution` exist, `FIRST_PASS_EFFECTIVENESS_GATE` was executed and passed.
- if both `original_report_distribution` and `post_first_pass_report_distribution` exist, `FIRST_PASS_EFFECTIVENESS_GATE` was executed and passed;
- `academic_tone_guard_result` is PASSED or NOT_APPLICABLE;
- `duplicate_insertion_guard_result` is PASSED or NOT_APPLICABLE;
- `format_preservation_result` is PASSED or NOT_APPLICABLE;
- `rewrite_application_gate_result` is PASSED or NOT_APPLICABLE;
- `template_residue_detector_result` is PASSED or NOT_APPLICABLE;
- `thesis_register_guard_result` is PASSED, PASSED_AFTER_REPAIR, or NOT_APPLICABLE;
- `LOCAL_ESCALATED_HUMANIZATION` was used only when `level_4_allowed = local_only`;
- no Level 4 rewrite was applied in 摘要, 英文摘要, 理论基础, or 结论;
- `min_diff_ratio_passed` is yes or NOT_APPLICABLE;
- no target has `patch_not_applied`, `patch_mismatch`, or `patch_ineffective`;
- the post-patch red+orange share is not above 40% when a post-patch AIGC report is available.

The task must not be marked `COMPLETED` when:

- the rewrite is only synonym replacement;
- the rewrite mainly makes the paragraph more formal, smoother, longer, or more abstract;
- red/orange paragraphs lack an A/B/C/D action record;
- social-science red/orange paragraphs still use generic "体系、机制、能力、价值、保障" prose without local evidence;
- missing author evidence was silently invented or ignored;
- `FIRST_PASS_EFFECTIVENESS_GATE` returned any `FAIL` verdict.
- `FIRST_PASS_EFFECTIVENESS_GATE` returned any `FAIL` verdict;
- `ACADEMIC_TONE_GUARD` found violations that were not corrected;
- `DOCX_DUPLICATE_INSERTION_GUARD` detected duplicate insertions.
- `REWRITE_APPLICATION_GATE` failed or was skipped for DOCX writeback;
- `TEMPLATE_RESIDUE_DETECTOR` failed or was skipped for patched red/orange targets;
- any required red/orange target failed the minimum diff-ratio threshold;
- post-patch text still contains the original high-risk paragraph skeleton in 摘要, 理论基础, 第五章, or 结论;
- red+orange remains above 40% in the post-patch report.
- `current_similarity_rate` or `current_aigc_rate` was missing before rewriting;
- Level 4 was applied without `RISK_INTAKE_GATE` approval;
- Level 4 was applied outside local eligible sections;
- `THESIS_REGISTER_GUARD` failed and the result was not repaired.

If evidence is missing, `D_AUTHOR_MATERIAL_REQUEST` is a valid action record, but the paragraph should be marked as needing author input rather than rewritten as complete.

## First-Pass Effectiveness Gate Hard Rules

When both `original_report_distribution` and `post_first_pass_report_distribution` are available:

1. `FIRST_PASS_EFFECTIVENESS_GATE` **must** be run before this audit.
2. If **any** gate condition fails:
   - final status **must** be `FIRST_PASS_FAILURE`;
   - output **must not** contain `COMPLETED`;
   - output **must not** contain "有效", "完成", "可交付", or any completion-affirming language;
   - output **must** include the Color Migration Table from the gate;
   - output **must** route to `AIGC_PLATEAU_BREAKER`;
   - output **must** list priority sections for the next pass: 摘要, 理论基础, 第五章, 结论;
   - output **must** include a `material_gap_table` if evidence is insufficient, and must not continue rewriting without author input.

When DOCX writeback is involved:

1. `REWRITE_APPLICATION_GATE` **must** be run before this audit.
2. `TEMPLATE_RESIDUE_DETECTOR` **must** be run after patch verification.
3. If `rewrite_application_gate_result = failed`, final delivery status must be `REWRITE_NOT_APPLIED_FAILURE`.
4. If `template_residue_detector_result = failed`, final delivery status must be `TEMPLATE_RESIDUE_FAILURE`.
5. If red+orange remains above 40%, final delivery status must be `FIRST_PASS_FAILURE`.
6. None of these failure states may be described as completed, effective, or ready to deliver.
7. If `local_escalation_required = yes`, `LOCAL_ESCALATED_HUMANIZATION` must be attempted on eligible residual sections or the audit must mark `LOCAL_ESCALATION_SKIPPED`.
8. If `THESIS_REGISTER_GUARD` fails, final delivery status must be `NEEDS_ACADEMIC_TONE_REPAIR`.

## Color Migration Check (First-Pass Only)

When both the original report and the post-first-pass report are available, the audit must produce a color migration comparison table.

| band | original_share | post_first_pass_share | delta | assessment |
|---|---|---|---|---|
| red (high risk) | % | % | ±pp |  |
| orange (medium risk) | % | % | ±pp |  |
| purple (light risk) | % | % | ±pp |  |
| black (low risk) | % | % | ±pp |  |

### Migration Assessment Rules

- If red decreased AND orange also decreased → assessment is "有效降低" (effective reduction).
- If red decreased AND orange increased → assessment is **"红转橙，未突破"** (red-to-orange, not resolved). The audit must NOT write "有效" in any summary text.
- If red decreased, orange increased, and the orange increase exceeds 10 percentage points → assessment is "红转橙，橙色平台期" (red-to-orange, orange plateau formed).
- If the combined red+orange share is still above 40% → assessment must note "风险集中度仍过高".
- If black coverage is below 25% → assessment must note "黑色占比不足".

### Color Migration Conclusion

The final status row's "result" column must include the color migration conclusion:

- "红转橙，未突破" when Condition 3 or 4 of `FIRST_PASS_EFFECTIVENESS_GATE` is met.
- "有效降低" only when red, orange, and combined risk all decreased.
- Do not write "有效" in any output when red decreased but orange accumulated.

## Delivery Status Rules

The `final_delivery_status` field replaces the simpler `final status` when format and tone checks are active:

| condition | final_delivery_status |
|---|---|
| AIGC risk reduced, all checks pass | COMPLETED |
| AIGC risk reduced but academic_tone_guard failed | NEEDS_ACADEMIC_TONE_REPAIR |
| AIGC risk reduced but duplicate_insertion_guard failed | FORMAT_FAILURE |
| AIGC risk reduced but ooxml_patch not used and user requires DOCX format | FORMAT_RISK_REVIEW_REQUIRED |
| Generated rewrites were not actually patched into DOCX text | REWRITE_NOT_APPLIED_FAILURE |
| Post-patch text still contains high-risk template residue | TEMPLATE_RESIDUE_FAILURE |
| Local escalation was required but not run | LOCAL_ESCALATION_SKIPPED |
| Level 4 applied in forbidden section | LEVEL_4_SECTION_BLOCKED |
| Red+orange remains above 40% in the post-patch report | FIRST_PASS_FAILURE |
| First-pass effectiveness gate failed | FIRST_PASS_FAILURE |
| Mandatory chain step missing | BLOCKED |
| Author evidence missing | NEEDS_AUTHOR_EVIDENCE |

## Required Output

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
| final status | COMPLETED / BLOCKED / NEEDS_AUTHOR_EVIDENCE / FIRST_PASS_FAILURE |  |
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

## First-Pass Failure

If the user reports that an original-thesis first-pass test barely changed AIGC risk, or if `FIRST_PASS_EFFECTIVENESS_GATE` returns any `FAIL` verdict, mark `FIRST_PASS_FAILURE`, not plateau.

**Final conclusion rule**: When FIRST_PASS_FAILURE is triggered, the `final status` must be `FIRST_PASS_FAILURE` and the conclusion text must read **"失败，需要二轮"**. Do NOT write "完成", "成功", "有效", "可通过", or any completion-affirming language.

Check:

- Was DOCX color metadata actually extracted?
- Was red/orange coverage 100%?
- Did every red/orange paragraph have an A/B/C/D action record?
- Was the rewrite mostly synonym replacement?
- Was social-science bottleneck handling skipped?
- Was author evidence missing but not requested?
- Was the color migration assessed? (See Color Migration Check section.)
- Does the color migration show red-to-orange transfer?
- Was academic tone guard applied and passed?
- Was format preservation verified?
- Did `REWRITE_APPLICATION_GATE` prove that every generated rewrite was actually written back?
- Did `TEMPLATE_RESIDUE_DETECTOR` confirm that the patched text no longer preserves the original high-risk template sentences?
- Did every red/orange target meet the minimum diff-ratio threshold?

Output a failure-cause table and a next repair plan. The next repair plan must reference `AIGC_PLATEAU_BREAKER` as the next step.
