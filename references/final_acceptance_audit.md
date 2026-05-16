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
- no fabricated data, interviews, citations, company facts, forms, systems, indicators, or report facts were introduced.

If evidence is missing, `D_AUTHOR_MATERIAL_REQUEST` is a valid action record, but the paragraph should be marked as needing author input rather than rewritten as complete.

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
| final status | COMPLETED / BLOCKED / NEEDS_AUTHOR_EVIDENCE / FIRST_PASS_FAILURE |  |

## First-Pass Failure

If the user reports that an original-thesis first-pass test barely changed AIGC risk, mark `FIRST_PASS_FAILURE`, not plateau.

Check:

- Was DOCX color metadata actually extracted?
- Was red/orange coverage 100%?
- Did every red/orange paragraph have an A/B/C/D action record?
- Was the rewrite mostly synonym replacement?
- Was social-science bottleneck handling skipped?
- Was author evidence missing but not requested?

Output a failure-cause table and a next repair plan.
