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
