# Purple Band Trigger Cases

## Case 1: Original AIGC High, Purple Unknown

Input:

```yaml
original_aigc_rate: 76.67%
red_count: 50
orange_count: 36
purple_count: unknown
has_aigc_color_report: true
```

Expected:

```yaml
COLOR_BAND_ROUTER: requires purple extraction
do_not_only_process_red_orange: true
rewrite_before_color_distribution: blocked
```

## Case 2: Third Round Still High

Input:

```yaml
stage: third_pass
current_aigc_rate: 36.42%
target_aigc_rate: 20%
red_count: 1
orange_count: 17
purple_count: many
```

Expected:

```yaml
purple_action: mandatory_rebalance
purple_band_rebalancer_required: true
final_delivery_status: not_completed_unless_purple_band_rebalancer_result_passed
```

## Case 3: AIGC Low, Purple Low

Input:

```yaml
current_aigc_rate: 25%
red_count: low
orange_count: low
purple_count: low
```

Expected:

```yaml
purple_action: observe_or_skip
large_rewrite: forbidden
```
