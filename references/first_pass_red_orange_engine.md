# First-Pass Red-Orange Engine

## Purpose

`FIRST_PASS_RED_ORANGE_ENGINE` is used when the user provides the original thesis and the original AIGC report. It prevents the common failure mode where the first pass only reduces red/high-risk text and leaves orange/medium-risk text as the next bottleneck.

This engine treats red and orange report bands as the first-pass main work area. It does not promise that any external system will mark the result as purple, black, or low risk.

## Activation Conditions

Enter this mode when:

- The user provides the original thesis plus the original AIGC report.
- The report has color bands or risk bands such as red, orange, purple, and black/white.
- The user wants AIGC reduction in the first pass.
- The user asks to avoid repeated second/third rounds caused by orange plateau.

Do not use this mode when the user provides a revised/current draft and the current report after a prior rewrite. Use `references/current_report_red_orange_engine.md` instead.

## Band Policy

| report_band | role in first pass | action |
|---|---|---|
| red/high | primary target | strong reconstruction with protection checks |
| orange/medium | primary target | structural repair, rhythm repair, evidence placement |
| purple/light | secondary target | local cleanup only when safe |
| black/white/low | frozen | do not rewrite unless user explicitly asks |
| protected | no-edit or surrounding-edit only | preserve exact data, code, citations, terms, formulas, paths, parameters |

Red and orange paragraphs must both enter the first-pass task table. Orange is not deferred to a later plateau stage.

## First-Pass Workflow

1. Parse the user-provided report and record the meaning of each color/risk band.
2. Map red and orange fragments back to the thesis source.
3. Build a protected list before any rewrite.
4. Create a red-orange task table.
5. Run sentence-level localization inside each red/orange paragraph.
6. For each red/orange paragraph, choose one required action type:
   - `A_EVIDENCE_RECONSTRUCTION`
   - `B_ARGUMENT_PATH_REWRITE`
   - `C_TEMPLATE_SKELETON_BREAK`
   - `D_AUTHOR_MATERIAL_REQUEST`
7. Apply replacement-based reconstruction, not append-based expansion.
8. Record the action type in the paragraph processing record.
9. Run band-target self-audit.
10. If red/orange risk remains in the heuristic self-audit, run one limited internal retry with a different repair move.
11. Stop when the paragraph is heuristically reduced to purple/black, protected, evidence-limited, author-material-needed, or no-progress.

If a red/orange paragraph does not have one of the four action types, it is unprocessed.

## Required First-Pass Action Types

| action_type | use when | required behavior |
|---|---|---|
| `A_EVIDENCE_RECONSTRUCTION` | The source has usable company, questionnaire, interview, process, post, indicator, time, or owner evidence. | Move evidence before evaluation and rebuild the paragraph around it. |
| `B_ARGUMENT_PATH_REWRITE` | The paragraph follows "definition -> meaning -> countermeasure". | Rebuild as "survey/field phenomenon -> reason judgment -> limited solution". |
| `C_TEMPLATE_SKELETON_BREAK` | The paragraph uses "一是、二是、三是、四是", "首先、其次、最后", or repeated countermeasure chains. | Break enumeration, group by process stage, merge empty items, and delete generic value endings. |
| `D_AUTHOR_MATERIAL_REQUEST` | Evidence is missing and safe rewriting would require invention. | Stop and request `workflow/author_evidence_pack_template.md`; do not fabricate. |

## Internal Recursive Loop

The loop is finite and must not become uncontrolled rewriting.

```text
for each red/orange task:
  diagnose sentence risks
  revise using at least two valid repair moves
  run self-audit
  if target_band is purple_or_black_like:
    mark PASS
  else if protected_or_evidence_limited:
    mark STOP_WITH_REASON
  else if retry_count < max_internal_passes:
    retry with a different repair move
  else:
    mark NEEDS_REPORT_RECHECK_OR_HUMAN_EVIDENCE
```

Default:

- `max_internal_passes = 2`.
- Do not run a third internal rewrite unless the user explicitly asks and the paragraph has enough evidence.
- Do not use the same repair move twice.

## Allowed Repair Moves

At least one required action type above must be selected. Within that action, at least two of the following should change unless `D_AUTHOR_MATERIAL_REQUEST` is used:

- paragraph opening angle,
- information order,
- sentence relationship,
- local evidence placement,
- repeated expression,
- paragraph rhythm,
- generic conclusion,
- discipline-template skeleton.

## Character Change Control

First-pass red-orange work must obey `references/character_delta_guard.md`.

Default whole-thesis range:

- `allowed_total_delta_ratio = ±10%`.

If red/orange repair would exceed this range:

- compress generic transitions first,
- delete repeated value claims,
- preserve technical facts and citations,
- stop expansion and ask for author evidence if needed.

## Exit States

- `RED_ORANGE_FIRST_PASS_COMPLETED`: red/orange tasks were safely handled and self-audit passed.
- `PURPLE_BLACK_HEURISTIC_TARGET_REACHED`: the paragraph is heuristically reduced to light/low risk.
- `PROTECTED_STOP`: risk remains but protected content prevents deeper rewriting.
- `EVIDENCE_LIMITED_STOP`: risk remains because the paragraph lacks author-provided evidence.
- `AUTHOR_MATERIAL_REQUIRED`: risk remains because the paragraph needs `workflow/author_evidence_pack_template.md`.
- `CHARACTER_DELTA_FAIL`: revision exceeds the allowed whole-thesis character-change range.
- `NO_PROGRESS_INTERNAL_LOOP`: internal retries did not materially change the risk pattern.
- `FIRST_PASS_FAILURE`: original-thesis first-pass testing barely changed AIGC risk.

## First-Pass Failure Handling

If the user says "original test barely changed AIGC" or similar, do not label it plateau. Label it `FIRST_PASS_FAILURE`.

Check:

| check_item | failure signal |
|---|---|
| DOCX color parsing | report was flattened to plain text or colors were not counted |
| red/orange coverage | red/orange coverage was below 100% |
| action type | red/orange paragraphs lack A/B/C/D action records |
| shallow rewrite | many paragraphs are synonym replacement or smoother formal prose |
| social-science overlay | HR/management paper did not enable social-science bottleneck rules |
| evidence pack | missing company/questionnaire/interview/process evidence was not requested |

Output the failure-cause table and next repair plan. Do not pretend the first pass was complete.

## Safety

Do not fabricate data, experiments, citations, interviews, code, APIs, logs, screenshots, report percentages, or external detection outcomes. The color-band target is a heuristic writing goal only.

## Relation To SKILL.md

Use this file before `AIGC_PLATEAU_BREAKER` when the user provides the original AIGC report at the start of the task.
