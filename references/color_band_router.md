# Color Band Router

## Purpose

`COLOR_BAND_ROUTER` assigns red, orange, purple, and black text to different intervention strategies immediately after the first `DOCX_COLOR_REPORT_EXTRACTION`. It prevents the workflow from treating only red/orange paragraphs while ignoring the purple band that may keep overall AIGC risk at 30%-40%.

Purple is not a late-stage afterthought. Red, orange, purple, and black must all be counted, routed, and audited from the first color report. Their processing intensity differs, but their presence must be visible in the task table.

## Color Band Rules

| band | threshold | objective | route |
|---|---:|---|---|
| red | `>=70%` | structure reconstruction | `FIRST_PASS_RED_ORANGE_ENGINE`, `TEMPLATE_RESIDUE_DETECTOR` |
| orange | `60%-70%` | statistical disruption | red-orange engine plus controlled humanization and template cleanup |
| purple | `50%-60%` | global statistical rebalance | `PURPLE_BAND_REBALANCER` when `purple_action` is `light_rebalance` or `mandatory_rebalance` |
| black | `<50%` | protection | freeze by default; only tiny connector edits if global variance requires it |

## Red Strategy

- Change argument order.
- Delete high-frequency templates.
- Put evidence before conclusion.
- Rebuild abstract/theory/conclusion skeletons.
- Must pass `TEMPLATE_RESIDUE_DETECTOR`.

## Orange Strategy

- Vary sentence length.
- Break mechanical enumeration.
- Replace repeated connectors.
- Specificize abstract value claims.
- Add evidence-grounded author judgment.
- Large orange blocks must be processed in the first relevant pass.

## Purple Strategy

- Do not perform large rewrites.
- Preserve facts, terminology, citations, formulas, code, and data.
- Apply low-intensity rhythm variation, transition changes, and repeated-opening reduction.
- Route to `PURPLE_BAND_REBALANCER` from the first pass when `purple_action` requires it.

## Purple Action Rules

`purple_action` must be one of:

- `skip`: purple is low-volume and current AIGC is already near or below target.
- `observe`: purple exists but does not yet require modification; it must still be counted and audited.
- `light_rebalance`: low-intensity purple adjustment is required.
- `mandatory_rebalance`: purple adjustment is required before completion.

### First Pass

Purple enters the task table immediately. Set `purple_action = light_rebalance` if any condition is true:

- `purple_ratio >= 10%`;
- `purple_count >= 10`;
- `current_aigc_rate >= 50%`;
- red + orange decreased but AIGC remains above 30%;
- `GLOBAL_STYLE_VARIANCE_ENGINE` detects over-uniform sentence pattern, connectors, or paragraph rhythm.

### Second / Third / Current-Report Pass

If `stage = second_pass`, `third_pass`, or `current_report_pass`, and `current_aigc_rate > target_aigc_rate`, set:

```yaml
purple_action: mandatory_rebalance
```

If third pass has finished and AIGC is still above 30%, set:

```yaml
purple_action: mandatory_rebalance
final_acceptance_must_include_purple: true
```

## Black Strategy

- Freeze by default.
- Only allow tiny connector or transition adjustment when `GLOBAL_STYLE_VARIANCE_ENGINE` identifies whole-text uniformity.
- Never rewrite protected black text.

## Output

```yaml
color_band_router:
  red_targets: <list/count>
  orange_targets: <list/count>
  purple_targets: <list/count>
  black_targets: <list/count>
  frozen_black_targets: <list/count>
  red_count: <count>
  orange_count: <count>
  purple_count: <count>
  black_count: <count>
  red_ratio: <ratio>
  orange_ratio: <ratio>
  purple_ratio: <ratio>
  black_ratio: <ratio>
  purple_action: skip | observe | light_rebalance | mandatory_rebalance
  band_action_plan:
    red: <plan>
    orange: <plan>
    purple: <plan>
    black: <plan>
```
