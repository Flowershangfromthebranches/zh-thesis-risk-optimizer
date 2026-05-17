# Risk Intake Gate Cases

## Case 1: Similarity Passed, AIGC High

Input:

```yaml
current_similarity_rate: 11%
current_aigc_rate: 68.6%
target_similarity_rate: 15%
target_aigc_rate: 30%
task_type: aigc_only
has_similarity_report: true
has_aigc_color_report: true
preserve_docx_format_required: true
discipline: 人力资源管理
stage: first_pass
```

Expected:

```yaml
similarity_status: already_passed
selected_strategy: high_risk_controlled_humanization
max_humanization_level: 3.5
level_4_allowed: local_only
strict_section_ceiling:
  摘要: 3.5
  理论基础: 3.5
  结论: 3.5
local_level_4_sections:
  - 第四章问题分析
  - 第五章对策分析
```

## Case 2: Already Low Risk

Input:

```yaml
current_similarity_rate: 8%
current_aigc_rate: 25%
target_similarity_rate: 10%
target_aigc_rate: 30%
task_type: aigc_only
stage: current_report_pass
```

Expected:

```yaml
similarity_status: already_low_risk
final_strategy: minimal_repair_only
max_humanization_level: 2
level_4_allowed: false
```

## Case 3: Similarity And AIGC Both High

Input:

```yaml
current_similarity_rate: 23%
current_aigc_rate: 72%
target_similarity_rate: 10%
target_aigc_rate: 30%
task_type: dual_optimization
stage: original
```

Expected:

```yaml
similarity_status: needs_similarity_reduction
selected_strategy: escalated_local_humanization
level_4_allowed: local_only
priority: similarity high-risk + AIGC red/orange overlap
```

## Case 4: Missing Current Rates

Input:

```yaml
target_similarity_rate: 10%
target_aigc_rate: 30%
task_type: aigc_only
```

Expected:

```yaml
status: INTAKE_INCOMPLETE
rewrite_allowed: false
message: require current_similarity_rate and current_aigc_rate
```
