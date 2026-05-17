# Purple Band Rebalancer Cases

## Case 1: Purple Is Substantial

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
purple_action: mandatory_rebalance
rewrite_intensity: low
level_4_used: false
chat_style: forbidden
```

## Case 2: Purple Low And AIGC Low

Input:

```yaml
current_aigc_rate: 25%
target_aigc_rate: 30%
red_count: 0
orange_count: 1
purple_count: 2
stage: current_report_pass
```

Expected:

```yaml
purple_action: observe_or_skip
broad_rewrite: forbidden
```
