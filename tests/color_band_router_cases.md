# Color Band Router Cases

## Case 1: Third Round Still Above Target

Input:

```yaml
current_aigc_rate: 36.42%
target_aigc_rate: 20%
red_count: 1
orange_count: 17
purple_count: many
stage: third_pass
```

Expected:

```yaml
red_orange_engine: handle_remaining_red_orange
purple_action: mandatory_rebalance
purple_band_rebalancer_required: true
global_style_variance_engine: required
final_delivery_status: not_completed_until_purple_rebalancer_passes
```

## Case 2: Initial Report Has Unknown Purple

Input:

```yaml
current_aigc_rate: 76.67%
red_count: 50
orange_count: 36
purple_count: unknown
has_aigc_color_report: true
```

Expected:

```yaml
color_band_router: require_docx_color_report_extraction
purple_action: undecided_until_extracted
rewrite_allowed: false_until_distribution_known
```

## Case 3: Near-Threshold Below-20 Pushdown

Input:

```yaml
current_aigc_rate: 20.31%
target_aigc_rate: 15%
stage: current_report_pass
red_count: 0
orange_count: 23
purple_count: 6
black_count: many
gray_count: references_headings_english
```

Expected:

```yaml
selected_strategy: near_threshold_pushdown
one_pass_cross_discipline_strategy: enabled
orange_action: process_all_or_valid_freeze
purple_action: mandatory_rebalance
black_action: freeze_with_reason
gray_action: freeze_with_reason
length_expansion_policy: avoid_expansion
final_delivery_status: not_completed_until_orange_and_purple_gate_passes
```

## Case 4: Default Color Legend

Input:

```yaml
report_legend: not_provided
user_notes: 红色70%以上 橙色60到70 紫色50到60 黑色50以下 灰色不检测
```

Expected:

```yaml
red: ">=70%"
orange: ">=60% and <70%"
purple: ">=50% and <60%"
black: "<50%"
gray: non_scored_excluded
gray_examples:
  - too_short
  - heading
  - english
  - reference
rewrite_gray: false
```
