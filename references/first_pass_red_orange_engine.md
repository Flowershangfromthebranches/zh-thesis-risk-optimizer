# First-Pass Red-Orange Engine

## Purpose

`FIRST_PASS_RED_ORANGE_ENGINE` is used when the user provides the original thesis and the original AIGC report. It prevents the common failure mode where the first pass only reduces red/high-risk text and leaves orange/medium-risk text as the next bottleneck.

This engine treats red and orange report bands as the first-pass main work area, but it must not ignore purple. It receives red/orange/purple/black routing from `COLOR_BAND_ROUTER` immediately after the first color extraction.

It does not promise that any external system will mark the result as purple, black, or low risk.

## Activation Conditions

Enter this mode when:

- The user provides the original thesis plus the original AIGC report.
- The report has color bands or risk bands such as red, orange, purple, and black/white.
- The user wants AIGC reduction in the first pass.
- The user asks to avoid repeated second/third rounds caused by orange plateau.

Do not use this mode when the user provides a revised/current draft and the current report after a prior rewrite. Use `references/current_report_red_orange_engine.md` instead.

## Band Policy

| report_band | role in first pass | action | minimum_target |
|---|---|---|---|
| red/high | primary target | strong reconstruction with protection checks | must reach purple or below; red→orange is UNPASSED |
| orange/medium | primary target | structural repair, rhythm repair, evidence placement | must reach black or near-black; orange→light-orange is UNPASSED |
| purple/light | tracked target | light rebalance if `COLOR_BAND_ROUTER` sets `purple_action = light_rebalance` or `mandatory_rebalance` | no Level 4 |
| black/white/low | frozen | do not rewrite unless user explicitly asks | — |
| protected | no-edit or surrounding-edit only | preserve exact data, code, citations, terms, formulas, paths, parameters | — |

Red and orange paragraphs must both enter the first-pass task table. Orange is not deferred to a later plateau stage. Purple must also enter the color task table with `purple_targets_count`, `purple_action`, `purple_deferred_reason`, and `next_purple_action_trigger`.

**Critical rule**: Demoting a red paragraph to orange is NOT a success. It is `UNPASSED`. The engine must not consider a paragraph "processed" or "passed" unless it reaches its minimum target band. Red→orange migration in aggregate is the primary signal of `FIRST_PASS_FAILURE`.

## Hard Targets

- **Red paragraph target**: priority is to reduce to black; minimum acceptable is below purple (i.e., purple or black). Red→orange only is **not passed**.
- **Orange paragraph target**: must reduce to black or near-black. Orange→light-orange is **not passed**.
- If red paragraphs only drop to orange, the first pass is **not passed**.
- If the aggregate orange share increases compared to the original, the first pass is **not passed**.
- If red + orange combined is still above 40%, the first pass is **not passed**.
- If the overall AIGC suspicion percentage is still above 60%, the first pass is **not passed**.

## First-Pass Workflow

1. Parse the user-provided report and record the meaning of each color/risk band.
2. Call `COLOR_BAND_ROUTER` and receive `red_targets`, `orange_targets`, `purple_targets`, `black_targets`, counts, ratios, and `purple_action`.
3. Map red and orange fragments back to the thesis source.
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
11. Record purple handling:
   - `purple_targets_count`;
   - `purple_action`;
   - `purple_deferred_reason`;
   - `next_purple_action_trigger`.
12. Stop when the paragraph is heuristically reduced to purple/black, protected, evidence-limited, author-material-needed, or no-progress.

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
  determine minimum_target based on original_band:
    if original_band is RED:  minimum_target = PURPLE_OR_BLACK
    if original_band is ORANGE: minimum_target = BLACK_OR_NEAR_BLACK
  diagnose sentence risks
  revise using at least two valid repair moves
  run self-audit
  if reached minimum_target:
    mark PASS
  else if protected_or_evidence_limited:
    mark STOP_WITH_REASON
  else if still_red_or_orange but retry_count < max_internal_passes:
    retry with a different repair move (different from previous)
  else:
    mark UNPASSED
```

Default:

- `max_internal_passes = 2` for red paragraphs; `max_internal_passes = 3` for orange paragraphs (orange is harder to shift to black).
- Do not run additional internal rewrites unless the user explicitly asks and the paragraph has enough evidence.
- Do not use the same repair move twice.
- If a paragraph exits with `UNPASSED`, the aggregate output must include it in the `unprocessed_or_partially_processed` list with reason "only_demoted_one_band" or "cannot_reach_minimum_target".

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

- `RED_ORANGE_FIRST_PASS_COMPLETED`: red/orange tasks were safely handled, minimum targets reached, and self-audit passed.
- `PURPLE_BLACK_HEURISTIC_TARGET_REACHED`: the paragraph is heuristically reduced to light/low risk.
- `PROTECTED_STOP`: risk remains but protected content prevents deeper rewriting.
- `EVIDENCE_LIMITED_STOP`: risk remains because the paragraph lacks author-provided evidence.
- `AUTHOR_MATERIAL_REQUIRED`: risk remains because the paragraph needs `workflow/author_evidence_pack_template.md`.
- `CHARACTER_DELTA_FAIL`: revision exceeds the allowed whole-thesis character-change range.
- `NO_PROGRESS_INTERNAL_LOOP`: internal retries did not materially change the risk pattern.
- `UNPASSED`: a red paragraph was only demoted to orange, or an orange paragraph could not reach black/near-black. Must be recorded in the unprocessed list.
- `FIRST_PASS_FAILURE`: original-thesis first-pass testing barely changed AIGC risk, or color migration shows red→orange transfer.
- `PURPLE_TRACKED_NOT_REWRITTEN`: purple was recorded but not rewritten because `purple_action = observe`.
- `PURPLE_REBALANCE_REQUIRED`: purple must route to `PURPLE_BAND_REBALANCER`.

## Required Purple Output

Even when first-pass rewriting focuses on red/orange, output:

| field | value |
|---|---|
| `purple_targets_count` | count |
| `purple_action` | skip / observe / light_rebalance / mandatory_rebalance |
| `purple_deferred_reason` | reason or none |
| `next_purple_action_trigger` | trigger or none |

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
| **red→orange migration** | red decreased but orange increased; red paragraphs only dropped one band to orange |
| **minimum target not reached** | red paragraphs still orange, orange paragraphs still not black/near-black |

### Red→Orange Migration Handling

If a red paragraph was only demoted to orange (not to purple or black):

1. Mark that paragraph `UNPASSED` in the processing record.
2. Include it in the `unprocessed_or_partially_processed` list with reason `only_demoted_one_band`.
3. In the aggregate color migration table, note the total number of paragraphs that fell into this category.
4. Do NOT count these paragraphs as "processed" for coverage reporting. Coverage counts only paragraphs that reached their minimum target.

If aggregate red→orange migration exceeds 10% of the original red paragraphs, the entire first pass must enter `FIRST_PASS_FAILURE` handling, regardless of individual paragraph successes.

Output the failure-cause table and next repair plan. Do not pretend the first pass was complete.

## Safety

Do not fabricate data, experiments, citations, interviews, code, APIs, logs, screenshots, report percentages, or external detection outcomes. The color-band target is a heuristic writing goal only.

## Relation To SKILL.md

Use this file before `AIGC_PLATEAU_BREAKER` when the user provides the original AIGC report at the start of the task.
