# Global Style Variance Engine Cases

## Case 1: Repeated Transitions

Input:

```text
本文…… 本研究…… 因此…… 同时…… 首先…… 其次……
```

Expected:

```yaml
global_style_variance_engine: required
global_variance_plan: present
full_text_rewrite: forbidden
local_routes:
  - PURPLE_BAND_REBALANCER
  - COLOR_BAND_ROUTER
  - section_profiles
```

## Case 2: Uniform Section Openings

Expected:

```yaml
uniform_section_openings: detected
sections_needing_variance: present
```
