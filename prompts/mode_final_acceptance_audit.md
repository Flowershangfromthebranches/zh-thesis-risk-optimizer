# Prompt: FINAL_ACCEPTANCE_AUDIT

Use this prompt at the end of every report-driven or file-copy task.

Do not mark a task complete until this audit passes.

## Inputs

- Intake confirmation.
- Mandatory chain trace.
- DOCX color extraction summary.
- Red-orange task table.
- Paragraph processing records.
- Character delta table.
- Protected item review.
- Author evidence requests, if any.

## 1. Mandatory Chain Trace

| step | required | executed | evidence |
|---|---|---|---|
| FILE_INPUT_COPY_WORKFLOW |  |  |  |
| DOCX_COLOR_REPORT_EXTRACTION |  |  |  |
| THREE_MODE_COLOR_BAND_WORKFLOW |  |  |  |
| FIRST_PASS_RED_ORANGE_ENGINE or CURRENT_REPORT_RED_ORANGE_ENGINE |  |  |  |
| SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable |  |  |  |
| AIGC_REGRESSION_GUARD |  |  |  |
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
| protected content damaged |  |  |
| fabricated evidence found |  |  |
| character delta status |  |  |

## 6. First-Pass Failure Branch

If the user says original first-pass testing barely changed AIGC risk, output:

| check_item | result | evidence | next_fix |
|---|---|---|---|
| DOCX color extraction performed |  |  |  |
| red-orange coverage 100% |  |  |  |
| synonym-only rewrite avoided |  |  |  |
| social-science bottleneck enabled |  |  |  |
| author evidence pack requested when needed |  |  |  |

Final status should be `FIRST_PASS_FAILURE` unless all checks pass and a new repair plan is ready.

## 7. Final Status

Use one:

- `COMPLETED`
- `BLOCKED`
- `NEEDS_AUTHOR_EVIDENCE`
- `FIRST_PASS_FAILURE`

Never promise external detector results.
