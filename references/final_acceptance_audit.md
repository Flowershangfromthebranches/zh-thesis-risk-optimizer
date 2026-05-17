# Final Acceptance Audit

## Purpose

`FINAL_ACCEPTANCE_AUDIT` is the final gate for report-driven and file-copy tasks. It prevents the Skill from claiming completion when the forced chain, color extraction, red/orange coverage, social-science evidence handling, or regression checks were skipped.

This audit is a workflow acceptance check. It does not promise any external detection result.

## Required Checks

The final output must report:

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

This audit absorbs the older post-rewrite self-audit, anti-shallow-rewrite, and effectiveness-evaluation gates. These checks are no longer separate entry modes; completion depends on this final gate.

## Completion Rule

The task can be marked `COMPLETED` only when:

- all mandatory chain steps were executed;
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

The task must not be marked `COMPLETED` when:

- the rewrite is only synonym replacement;
- the rewrite mainly makes the paragraph more formal, smoother, longer, or more abstract;
- red/orange paragraphs lack an A/B/C/D action record;
- social-science red/orange paragraphs still use generic "体系、机制、能力、价值、保障" prose without local evidence;
- missing author evidence was silently invented or ignored;
- `FIRST_PASS_EFFECTIVENESS_GATE` returned any `FAIL` verdict.

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
   - output **must** list priority sections for the next pass: 摘要, 理论基础, 第五章, 结论.

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

## Required Output

| item | result | evidence |
|---|---|---|
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
| final status | COMPLETED / BLOCKED / NEEDS_AUTHOR_EVIDENCE / FIRST_PASS_FAILURE |  |

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

Output a failure-cause table and a next repair plan. The next repair plan must reference `AIGC_PLATEAU_BREAKER` as the next step.
