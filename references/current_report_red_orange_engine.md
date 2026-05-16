# Current Report Red-Orange Engine

## Purpose

`CURRENT_REPORT_RED_ORANGE_ENGINE` is used when the user provides a revised thesis file and the AIGC report for that revised/current file.

It is different from `FIRST_PASS_RED_ORANGE_ENGINE`. First-pass mode is only for `original thesis + original report`. Current-report mode treats the latest report as the active source of truth and must cover every red and orange fragment in that report.

This engine does not promise any external detection result. It only defines report-driven writing-risk handling and acceptance checks.

## Activation Conditions

Use this engine inside `THREE_MODE_COLOR_BAND_WORKFLOW` when all of the following are true:

1. The user chooses AIGC-only revision.
2. Input includes a DOCX AIGC color report or equivalent color-marked AIGC report.
3. The user provides or accepts red/orange/purple/black color rules.
4. The user asks for character control, no broad full-text rewrite, or file-copy output.
5. The report belongs to a revised/current draft, not the original unmodified thesis.

If there is evidence of a prior rewrite and a new report, do not route to `FIRST_PASS_RED_ORANGE_ENGINE`.

## Routing Overlays

- If the current report shows red decreased but orange remains high, overlay `AIGC_PLATEAU_BREAKER`.
- If the discipline is human resource management, business administration, marketing, education management, or public administration, overlay `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`.
- Do not fall back to plain `AIGC_ONLY` or generic polishing when current-report color targeting is available.

## Band Policy

| report band | current-report handling |
|---|---|
| red | all fragments must enter the task table and be processed unless protected or unmapped |
| orange | all fragments must enter the task table and be processed unless protected or unmapped |
| purple | only process when it shares the same paragraph with red/orange or is needed for local coherence |
| black / low risk | freeze |
| cover, table of contents, declaration, reference list, appendix | freeze by default |

If a red/orange fragment is protected, unmapped, or evidence-limited, it still counts as a task and must appear in the unprocessed list with a reason.

## Red-Orange Coverage Acceptance

Every completion output must include:

| field | meaning |
|---|---|
| `current_report_red_total` | total red paragraphs/fragments in the current report |
| `current_report_orange_total` | total orange paragraphs/fragments in the current report |
| `processed_red_count` | red paragraphs/fragments with processing records |
| `processed_orange_count` | orange paragraphs/fragments with processing records |
| `unprocessed_red_orange_count` | red/orange tasks without a passing record |
| `completion_status` | `COMPLETED` only when unprocessed count is zero |

If `unprocessed_red_orange_count > 0`, do not mark the task complete.

## Required Paragraph Processing Record

Each red/orange paragraph must have one record:

| field | requirement |
|---|---|
| section | chapter or location |
| original_band | red or orange |
| original_fragment | mapped source fragment |
| risk_reason | why the report likely marked it red/orange |
| rewrite_strategy | concrete strategy used |
| evidence_used | whether company, survey, interview, process, post, form, or indicator evidence was used |
| char_delta | character change for the paragraph |
| self_audit_result | pass, second-pass, evidence-limited, protected, or unmapped |
| passed | yes/no |

No record means the paragraph is unprocessed.

## Current-Report Workflow

1. Confirm the report is for the current/revised draft.
2. Extract DOCX color metadata before plain text when the report is a color-marked Word file.
3. Map every red and orange fragment back to the current draft.
4. Freeze black, low-risk, cover, table of contents, declarations, references, and appendices.
5. Build the red-orange task table.
6. For every red/orange paragraph, run `AIGC_ACCEPTANCE_SELF_AUDIT`.
7. If any audit item fails, run a second-pass rewrite with a different strategy.
8. If second pass still fails, output a human evidence request; do not mark the paragraph complete.
9. Output the coverage acceptance table and unprocessed list.

## Completion Rule

Completion requires:

- Every red paragraph has a processing record.
- Every orange paragraph has a processing record.
- All records either pass or are explicitly marked protected/unmapped/evidence-limited with human next action.
- The unprocessed red/orange count is zero.
- Character delta guard passes.
- No protected content is damaged.

`COMPLETED` is forbidden when any red/orange paragraph lacks a record.

## Relation To SKILL.md

Use this file after completed intake when the user provides a current/revised AIGC report. Use `references/first_pass_red_orange_engine.md` only when the report is the original report for the original thesis.
