# Risk Intake Gate

## Purpose

`RISK_INTAKE_GATE` is the mandatory pre-rewrite gate for all `zh-thesis-risk-optimizer` tasks. It collects current risk metrics before any rewrite decision, then decides how much `CONTROLLED_HUMANIZATION_ENGINE`, `LOCAL_ESCALATED_HUMANIZATION`, and Level 4 intervention may be used.

This gate does not promise any external detection result. Percentages must come from the user or from user-provided reports.

## Required Fields

The user must provide or explicitly fill:

| field | required meaning |
|---|---|
| `current_similarity_rate` | Current overall similarity/check rate, percentage. |
| `current_aigc_rate` | Current overall AIGC suspicion rate, percentage. |
| `target_similarity_rate` | User target for similarity risk. This is an optimization target, not a guarantee. |
| `target_aigc_rate` | User target for AIGC risk. This is an optimization target, not a guarantee. |
| `task_type` | `aigc_only`, `similarity_only`, or `dual_optimization`. |
| `has_similarity_report` | `true` or `false`. |
| `has_aigc_color_report` | `true` or `false`. |
| `preserve_docx_format_required` | `true` or `false`. |
| `discipline` | Thesis discipline. |
| `stage` | `original`, `first_pass`, `second_pass`, `current_report_pass`, or `first_pass_failure`. |

If `current_similarity_rate` or `current_aigc_rate` is missing:

- output `INTAKE_INCOMPLETE`;
- ask the user to provide both current rates;
- file reading and report parsing may continue only to complete intake;
- do not enter the rewrite chain;
- do not select Level 4 or generate candidate rewrites.

## AIGC Strategy Rules

Normative thresholds:

- `current_aigc_rate < 30`: `strategy = conservative_repair`, `max_humanization_level = 2`, `level_4_allowed = false`.
- `30 <= current_aigc_rate < 50`: `strategy = moderate_controlled_humanization`, `max_humanization_level = 3`, `level_4_allowed = false`.
- `50 <= current_aigc_rate < 70`: `strategy = high_risk_controlled_humanization`, `max_humanization_level = 3.5`, `level_4_allowed = local_only`.
- `current_aigc_rate >= 70`: `strategy = escalated_local_humanization`, `max_humanization_level = 4`, `level_4_allowed = local_only`.
- `current_aigc_rate >= 75` and `stage = second_pass` or `first_pass_failure`: `strategy = aggressive_but_localized_repair`, with `style_risk_warning` and `academic_tone_repair_plan`.

| current_aigc_rate | selected_strategy | max_humanization_level | level_4_allowed | rule |
|---:|---|---:|---|---|
| `<30` | `conservative_repair` | 2 | `false` | Only repair local grammar issues, template residue, and red segments. Avoid broad rewriting. |
| `30-49.99` | `moderate_controlled_humanization` | 3 | `false` | Focus on red and large orange blocks while preserving thesis register. |
| `50-69.99` | `high_risk_controlled_humanization` | 3.5 | `local_only` | Level 4 may be used only in Chapter 4/5 problem-analysis and countermeasure paragraphs. Abstract, theory, and conclusion max at 3.5. |
| `>=70` | `escalated_local_humanization` | 4 | `local_only` | Allow `LOCAL_ESCALATED_HUMANIZATION` for residual red/orange paragraphs. Never use full-text Level 4. Strict sections max at 3.5 and must pass `THESIS_REGISTER_GUARD`. |
| `>=75` and `stage in [second_pass, first_pass_failure]` | `aggressive_but_localized_repair` | 4 | `local_only` | Allow local Level 4 only in Chapter 4/5 high-risk residual paragraphs. Output `style_risk_warning` and `academic_tone_repair_plan`. |

## Similarity Rules

| condition | similarity_status | required behavior |
|---|---|---|
| `current_similarity_rate <= target_similarity_rate` | `already_passed` | Do not perform broad similarity rewriting. If `task_type = aigc_only`, process only AIGC red/orange targets and template residue. |
| `current_similarity_rate > target_similarity_rate` | `needs_similarity_reduction` | Prioritize overlap between high similarity risk and AIGC red/orange risk. Do not preserve highly similar expression just because humanization is active. |
| `current_similarity_rate <= 10` and `current_aigc_rate <= 30` | `already_low_risk` | Set `final_strategy = minimal_repair_only`; warn that broad rewriting is not recommended. |

## Level 4 Trigger Contract

Level 4 is never self-selected by a rewriter. It requires all of:

1. `RISK_INTAKE_GATE` sets `level_4_allowed = local_only`;
2. `FIRST_PASS_EFFECTIVENESS_GATE` or current-report diagnosis shows unresolved high-risk residuals;
3. `TEMPLATE_RESIDUE_DETECTOR` identifies remaining high-risk template skeletons or report red/orange targets;
4. the target section allows local Level 4 under `references/local_escalated_humanization.md`;
5. `THESIS_REGISTER_GUARD` can repair the result back to thesis register.

## Output

```yaml
risk_intake_decision:
  current_similarity_rate: <percentage>
  current_aigc_rate: <percentage>
  target_similarity_rate: <percentage>
  target_aigc_rate: <percentage>
  task_type: aigc_only | similarity_only | dual_optimization
  has_similarity_report: true | false
  has_aigc_color_report: true | false
  preserve_docx_format_required: true | false
  discipline: <discipline>
  stage: original | first_pass | second_pass | current_report_pass | first_pass_failure
  similarity_status: already_passed | needs_similarity_reduction | already_low_risk
  selected_strategy: <strategy>
  max_humanization_level: 2 | 3 | 3.5 | 4
  level_4_allowed: false | local_only
  final_strategy: minimal_repair_only | targeted_repair | report_driven_repair
  style_risk_warning: <required when strategy is aggressive_but_localized_repair>
  academic_tone_repair_plan: <required when local Level 4 may be used>
```

## Relation To SKILL.md

`RISK_INTAKE_GATE` runs before `INTAKE_WIZARD_PRECHECK` and before all rewrite chains. It supplies the humanization ceiling used by `CONTROLLED_HUMANIZATION_ENGINE`, `LOCAL_ESCALATED_HUMANIZATION`, `THESIS_REGISTER_GUARD`, and `FINAL_ACCEPTANCE_AUDIT`.
