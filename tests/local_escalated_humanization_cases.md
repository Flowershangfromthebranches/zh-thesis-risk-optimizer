# Local Escalated Humanization Cases

## Case 1: Old-Version Casual Tone In Strict Section

Input:

```yaml
current_aigc_rate: 35%
section: 摘要
text_contains:
  - 一圈查下来
  - 头一个是
  - 比较头疼
```

Expected:

```yaml
thesis_register_guard_result: failed
final_delivery_status: NEEDS_ACADEMIC_TONE_REPAIR
level_4_allowed_for_section: false
```

## Case 2: New Version Orange Residue Around 50%

Input:

```yaml
current_aigc_rate: 50%
orange_residue: obvious
template_residue_detector_result: failed
sections:
  - 第四章
  - 第五章
```

Expected:

```yaml
local_escalation_applied: true
local_escalation_sections:
  - 第四章
  - 第五章
  - 红橙残留段
do_not_output: 复测后再说
```

## Case 3: Full Text Level 4 Request

Input:

```yaml
user_request: 全文 Level 4
current_aigc_rate: 78%
```

Expected:

```yaml
status: BLOCKED_FULL_TEXT_LEVEL_4
allowed: local_only
```
