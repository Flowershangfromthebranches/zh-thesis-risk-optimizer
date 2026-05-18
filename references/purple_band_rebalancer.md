# Purple Band Rebalancer

## Purpose

`PURPLE_BAND_REBALANCER` handles light-risk purple text (`50%-60%`) from the first color report onward when `COLOR_BAND_ROUTER` sets `purple_action = light_rebalance` or `mandatory_rebalance`.

It performs low-intensity style rebalance, not deep rewriting.

Purple is not ignored in the first pass. Every purple target must enter the task table with an action. First pass may observe low-volume purple targets, but it must still record `purple_action`, `purple_targets_count`, and `purple_coverage_rate`.

## Trigger Conditions

Trigger from the first pass when one or more are true:

- overall AIGC remains above 30%;
- `purple_ratio >= 10%`;
- `purple_count >= 10`;
- `current_aigc_rate >= 50%`;
- red + orange decreased but AIGC remains above 30%;
- `FIRST_PASS_EFFECTIVENESS_GATE` says high-risk text is lower but the whole text still looks AI-like;
- `GLOBAL_STYLE_VARIANCE_ENGINE` finds over-uniform rhythm.

For `stage = second_pass`, `third_pass`, or `current_report_pass`, if `current_aigc_rate > target_aigc_rate`, `purple_action = mandatory_rebalance`.

If a third pass has finished and AIGC is still above 30%, `purple_action = mandatory_rebalance` and `FINAL_ACCEPTANCE_AUDIT` must not ignore purple text.

If `current_aigc_rate > 50`, purple targets must not all be `skip`.

If red/orange handling lowers high-risk bands but the overall AIGC rate remains above 30%, purple must enter `mandatory_rebalance`.

## Allowed Actions

- A. Slight sentence length variation.
- B. Connector replacement.
- C. Transition sentence rewrite.
- D. Disperse high-frequency `本文` / `本研究` openings.
- E. Split continuous parallel structures.
- F. Vary section openings.
- G. Compress abstract value claims.
- H. Add one bounded author judgment when evidence exists.

## Forbidden Actions

- Chat-like language.
- Expressions such as `一圈查下来`, `头一个是`, `比较头疼`.
- Data, terminology, formula, code, citation, path, table, field, or parameter changes.
- Large expansion.
- Level 4.

## Required Coordination

- `COLOR_BAND_ROUTER` must supply `purple_targets_count` and `purple_action`.
- `FIRST_PASS_RED_ORANGE_ENGINE` must record purple targets even when it does not rewrite all of them.
- `FINAL_ACCEPTANCE_AUDIT` must fail with `PURPLE_BAND_NOT_HANDLED_FAILURE` when `current_aigc_rate > target_aigc_rate` and `purple_action = skip`.
- `RISK_BAND_COVERAGE_GATE` must fail when purple targets are missing from the task table or required purple coverage is below threshold.

## Example

Original:

```text
本研究采用问卷调查法和访谈法，对 A 公司数智化招聘现状进行了分析。
```

Acceptable:

```text
为了解 A 公司招聘管理的实际运行情况，本文结合问卷与访谈材料，对流程、工具、团队和渠道四个方面进行了梳理。
```

Unacceptable:

```text
光靠问卷说不透，所以又做了访谈。
```

## Output

```yaml
purple_band_rebalancer:
  purple_targets_count: <count>
  purple_rebalanced_count: <count>
  purple_coverage_rate: <percent>
  purple_rewrite_intensity: low
  purple_action: skip | observe | light_rebalance | mandatory_rebalance
  purple_deferred_reason: <reason or none>
  next_purple_action_trigger: <trigger or none>
  global_distribution_effect: <expected effect>
  level_4_used: false
```
