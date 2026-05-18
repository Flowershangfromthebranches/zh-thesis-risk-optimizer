# Risk Band Coverage Gate

## Purpose

`RISK_BAND_COVERAGE_GATE` prevents the workflow from stopping after it has only identified red, orange, and purple report targets. A task is not complete unless each risk-band target has one of three auditable outcomes:

- handled by an allowed action;
- lightly rebalanced when the band rules allow light treatment;
- frozen with a valid protection reason.

This gate exists because a first pass that identifies 90 risk paragraphs but modifies only 34 paragraphs is not an acceptable first-pass result.

## Inputs

The gate requires:

- `COLOR_BAND_ROUTER` output;
- red, orange, and purple target lists;
- per-target `band_action_plan`;
- per-paragraph processing records from `FIRST_PASS_RED_ORANGE_ENGINE`, `CURRENT_REPORT_RED_ORANGE_ENGINE`, and `PURPLE_BAND_REBALANCER` when used;
- frozen target list with reasons;
- current `stage`;
- `current_aigc_rate`;
- `target_aigc_rate`.

## Valid Actions

Allowed red/orange actions:

- `rewrite`;
- `restructure`;
- `evidence_rebuild`;
- `local_escalated_humanization`;
- `freeze_with_reason` only for valid protected or non-body content.

Allowed purple actions:

- `purple_light_rebalance`;
- `observe_with_reason` only when the purple rules permit observation;
- `freeze_with_reason` only for valid protected or non-body content.

Black text is frozen by default. It may only receive tiny connector edits when `GLOBAL_STYLE_VARIANCE_ENGINE` explicitly selects a few connector sentences.

## Coverage Rules

### Red Targets

- `red_targets` must be 100% handled or explicitly frozen with a valid reason.
- Body red targets must not be skipped without a reason.
- Red actions must be `rewrite`, `restructure`, `evidence_rebuild`, or `local_escalated_humanization`.
- `observe_with_reason` is not valid handling for red body text.

### Orange Targets

- `orange_targets` must be at least 85% handled in first pass.
- If `current_aigc_rate >= 70`, orange targets must be 100% handled or explicitly frozen.
- Body orange targets must not be only observed.
- Large orange blocks must be handled.

### Purple Targets

- `purple_targets` must be 100% present in the task table.
- In first pass, purple can use `purple_light_rebalance` or `observe_with_reason`, but it must have an action.
- If `stage >= second_pass` or `current_aigc_rate > 50`, at least 80% of purple targets must receive `purple_light_rebalance` or stronger low-intensity handling.
- If `stage >= third_pass`, or `current_aigc_rate > target_aigc_rate` and red/orange already decreased, purple must use `mandatory_rebalance`.

### Black Targets

- Black targets are frozen by default.
- `GLOBAL_STYLE_VARIANCE_ENGINE` may nominate a few connector sentences for tiny adjustment.
- Protected black text must not be rewritten.

## Valid Freeze Reasons

Valid reasons include:

- appendix;
- questionnaire appendix;
- reference entry;
- school declaration;
- cover page;
- table of contents;
- formula;
- code;
- path;
- parameter;
- figure/table number;
- citation quotation;
- data table;
- protected technical identifier.

Invalid reasons include:

- `too many targets`;
- `will handle after retest`;
- `low priority`;
- `already diagnosed`;
- `model chose not to edit`;
- `style risk`;
- `no time`.

## Required Coverage Fields

Every final output must include:

| field | description |
|---|---|
| `red_targets_count` | total red report targets |
| `orange_targets_count` | total orange report targets |
| `purple_targets_count` | total purple report targets |
| `red_handled_count` | red targets with valid handling or valid freeze |
| `orange_handled_count` | orange targets with valid handling or valid freeze |
| `purple_handled_count` | purple targets with valid action or valid freeze |
| `red_coverage_rate` | red_handled_count / red_targets_count |
| `orange_coverage_rate` | orange_handled_count / orange_targets_count |
| `purple_coverage_rate` | purple_handled_count / purple_targets_count |
| `skipped_red_targets` | red targets without valid handling |
| `skipped_orange_targets` | orange targets without valid handling |
| `skipped_purple_targets` | purple targets without valid action |
| `valid_freeze_reasons` | protected or non-body targets frozen with reason |
| `invalid_skips` | skipped targets with invalid/no reason |
| `next_batch_plan` | required next batch if coverage is incomplete |

## Batch Mode

When risk targets are too numerous for one output, the Skill must enter batch mode instead of claiming completion.

| batch | scope |
|---|---|
| Batch 1 | red/orange in 摘要, 绪论, 理论基础, 第四章, 第五章, 结论 |
| Batch 2 | red/orange in 第三章, 研究方法, 企业概况 |
| Batch 3 | remaining body orange targets and purple light rebalance targets |

Only after all batches pass this gate can `first_pass_status` be `passed`.

## Failure Conditions

Set:

```yaml
risk_band_coverage_gate_result: failed
final_delivery_status: RISK_BAND_COVERAGE_FAILURE
```

when any condition is true:

- `red_coverage_rate < 100%`;
- `orange_coverage_rate < 85%`;
- `current_aigc_rate >= 70` and `orange_coverage_rate < 100%`;
- `stage >= second_pass` and `purple_coverage_rate < 80%`;
- `invalid_skips` is not empty;
- any red/orange body target is only observed;
- any purple target is missing from the task table.

## Output

```yaml
risk_band_coverage_gate:
  risk_band_coverage_gate_result: passed | failed
  red_targets_count: <count>
  orange_targets_count: <count>
  purple_targets_count: <count>
  red_handled_count: <count>
  orange_handled_count: <count>
  purple_handled_count: <count>
  red_coverage_rate: <percent>
  orange_coverage_rate: <percent>
  purple_coverage_rate: <percent>
  skipped_red_targets: <list>
  skipped_orange_targets: <list>
  skipped_purple_targets: <list>
  valid_freeze_reasons: <list>
  invalid_skips: <list>
  next_batch_plan: <plan or none>
```

## Relation To SKILL.md

Run this gate immediately after `COLOR_BAND_ROUTER` to confirm the planned coverage, and run it again before `FINAL_ACCEPTANCE_AUDIT` to confirm actual coverage.
