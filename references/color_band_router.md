# Color Band Router

## Purpose

`COLOR_BAND_ROUTER` assigns red, orange, purple, black, and gray text to different intervention strategies immediately after the first `DOCX_COLOR_REPORT_EXTRACTION`. It prevents the workflow from treating only red/orange paragraphs while ignoring the purple band that may keep overall AIGC risk above the user target.

Purple is not a late-stage afterthought. Red, orange, purple, black, and gray must all be counted, routed, and audited from the first color report. Their processing intensity differs, but their presence must be visible in the task table or freeze summary.

The router must output `band_action_plan` for every red, orange, and purple target. A target list without a planned action is incomplete and must fail `RISK_BAND_COVERAGE_GATE`.

## Color Band Rules

| band | threshold | objective | route |
|---|---:|---|---|
| red | `>=70%` | structure reconstruction | `FIRST_PASS_RED_ORANGE_ENGINE`, `TEMPLATE_RESIDUE_DETECTOR` |
| orange | `>=60%` and `<70%` | statistical disruption | red-orange engine plus controlled humanization and template cleanup |
| purple | `>=50%` and `<60%` | global statistical rebalance | `PURPLE_BAND_REBALANCER` when `purple_action` is `light_rebalance` or `mandatory_rebalance` |
| black | `<50%` | protection | freeze by default; only tiny connector edits if global variance requires it |
| gray | non-scored / excluded | protection | freeze by default; do not rewrite headings, too-short fragments, English, references, or school-template text |

## Red Strategy

- Every red target must receive an action.
- Body red targets cannot use `observe_with_reason`.
- Change argument order.
- Delete high-frequency templates.
- Put evidence before conclusion.
- Rebuild abstract/theory/conclusion skeletons.
- Must pass `TEMPLATE_RESIDUE_DETECTOR`.

## Orange Strategy

- Every body orange target must receive an action or enter a batch plan.
- Body orange targets cannot use `observe_with_reason` unless citation, format, or protected-element risk blocks rewriting.
- Large orange blocks must be processed.
- Vary sentence length.
- Break mechanical enumeration.
- Replace repeated connectors.
- Specificize abstract value claims.
- Add evidence-grounded author judgment.
- Large orange blocks must be processed in the first relevant pass.

## Purple Strategy

- Every purple target must enter the task table.
- Purple targets must receive `purple_light_rebalance`, `observe_with_reason`, or `freeze_with_reason`.
- Do not perform large rewrites.
- Preserve facts, terminology, citations, formulas, code, and data.
- Apply low-intensity rhythm variation, transition changes, and repeated-opening reduction.
- Route to `PURPLE_BAND_REBALANCER` from the first pass when `purple_action` requires it.

## Band Action Plan

`band_action_plan` must assign one action to every red/orange/purple target:

| action | allowed for | notes |
|---|---|---|
| `rewrite` | red/orange | direct rewrite of body risk text |
| `restructure` | red/orange | argument or paragraph skeleton reconstruction |
| `evidence_rebuild` | red/orange | rebuild around provided evidence |
| `local_escalated_humanization` | red/orange | local-only high-risk residual action when permitted |
| `purple_light_rebalance` | purple | low-intensity rhythm or transition rebalance |
| `observe_with_reason` | purple only by default | not valid for body red/orange unless protected risk blocks editing |
| `freeze_with_reason` | protected/non-body targets | appendix, questionnaire appendix, references, declarations, cover, table of contents, code, formula, citation, data, path, parameter |

Invalid plans:

- body red target with `observe_with_reason`;
- body orange target with `observe_with_reason` and no protected reason;
- any red/orange/purple target without action;
- using `freeze_with_reason` because the target list is long;
- deferring risk targets to "after retest" without a batch plan.

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

If `target_aigc_rate <= 20%` and `current_aigc_rate > target_aigc_rate`, set:

```yaml
purple_action: mandatory_rebalance
below_20_pushdown: true
```

unless every purple target is protected, non-body, or too short and therefore validly frozen.

If third pass has finished and AIGC is still above 30%, set:

```yaml
purple_action: mandatory_rebalance
final_acceptance_must_include_purple: true
```

## Black Strategy

- Freeze by default.
- Only allow tiny connector or transition adjustment when `GLOBAL_STYLE_VARIANCE_ENGINE` identifies whole-text uniformity.
- Never rewrite protected black text.

## Gray Strategy

- Freeze by default.
- Treat gray as non-scored or excluded text: too-short fragments, titles/headings, English abstract/text, references, declarations, cover pages, table of contents, school-template text, or other report-excluded spans.
- Do not spend rewrite budget on gray text.
- Do not use gray text to pad word count after high-risk paragraph compression.
- Gray can provide context for mapping, but must not be automatically rewritten.

## Output

```yaml
color_band_router:
  red_targets: <list/count>
  orange_targets: <list/count>
  purple_targets: <list/count>
  black_targets: <list/count>
  gray_targets: <list/count>
  frozen_black_targets: <list/count>
  frozen_gray_targets: <list/count>
  red_count: <count>
  orange_count: <count>
  purple_count: <count>
  black_count: <count>
  gray_count: <count>
  red_ratio: <ratio>
  orange_ratio: <ratio>
  purple_ratio: <ratio>
  black_ratio: <ratio>
  gray_ratio: <ratio>
  purple_action: skip | observe | light_rebalance | mandatory_rebalance
  band_action_plan:
    red:
      - target_id: <id>
        action: rewrite | restructure | evidence_rebuild | local_escalated_humanization | freeze_with_reason
        reason: <required>
    orange:
      - target_id: <id>
        action: rewrite | restructure | evidence_rebuild | local_escalated_humanization | freeze_with_reason
        reason: <required>
    purple:
      - target_id: <id>
        action: purple_light_rebalance | observe_with_reason | freeze_with_reason
        reason: <required>
    black:
      - target_id: <id>
        action: freeze_with_reason
        reason: <required>
    gray:
      - target_id: <id>
        action: freeze_with_reason
        reason: too_short | heading | english | reference | declaration | cover | toc | school_template | non_scored
```
