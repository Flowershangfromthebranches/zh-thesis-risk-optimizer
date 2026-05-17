# Prompt: RISK_INTAKE_GATE

Use this prompt before selecting any rewrite route.

## Required Input

Collect these fields:

- `current_similarity_rate`
- `current_aigc_rate`
- `target_similarity_rate`
- `target_aigc_rate`
- `task_type`: `aigc_only` / `similarity_only` / `dual_optimization`
- `has_similarity_report`: `true` / `false`
- `has_aigc_color_report`: `true` / `false`
- `preserve_docx_format_required`: `true` / `false`
- `discipline`
- `stage`: `original` / `first_pass` / `second_pass` / `current_report_pass` / `first_pass_failure`

## Blocking Rule

If either `current_similarity_rate` or `current_aigc_rate` is missing:

```text
INTAKE_INCOMPLETE
还缺少当前查重总体相似度和/或当前 AIGC 总体疑似率。可以继续读取文件或解析报告来补全 intake，但不能进入改写链路。
请补充：
- current_similarity_rate：
- current_aigc_rate：
```

Do not generate rewritten text before both current rates are known.

## Decision Steps

1. Parse current and target rates as percentages.
2. Determine `similarity_status`.
3. Determine `selected_strategy`, `max_humanization_level`, and `level_4_allowed`.
4. Decide whether `LOCAL_ESCALATED_HUMANIZATION` is allowed.
5. Preserve strict section ceilings:
   - 摘要: max 3.5, no Level 4.
   - 英文摘要: max 3.5, no Level 4.
   - 理论基础: max 3.5, no Level 4.
   - 结论: max 3.5, no Level 4.
6. If aggressive local repair is possible, output `style_risk_warning` and `academic_tone_repair_plan`.

## Output

```markdown
## Risk Intake Decision

| field | value | status |
|---|---|---|
| current_similarity_rate |  | required |
| current_aigc_rate |  | required |
| target_similarity_rate |  | required |
| target_aigc_rate |  | required |
| task_type |  | required |
| has_similarity_report |  | required |
| has_aigc_color_report |  | required |
| preserve_docx_format_required |  | required |
| discipline |  | required |
| stage |  | required |
| similarity_status |  | derived |
| selected_strategy |  | derived |
| max_humanization_level |  | derived |
| level_4_allowed |  | derived |
| local_escalation_candidate |  | derived |

### Routing Decision
- can_rewrite: yes/no
- reason:
- next_route:
- style_risk_warning:
- academic_tone_repair_plan:
```
