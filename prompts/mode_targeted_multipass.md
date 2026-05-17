**ARCHIVED_COMPATIBILITY_ONLY**

Do not call directly. Route through `SKILL.md` Minimal Mode Router.

# Prompt: TARGETED_MULTIPASS_ENGINE

Use this prompt when the user provides any combination of original text, current draft, reports, historical versions, and target thresholds.

## Inputs

- Original text.
- Current draft.
- Similarity report.
- AIGC report.
- Historical versions.
- User target thresholds.

## Output Format

### 1. Current Metrics

```yaml
similarity_current:
aigc_current:
similarity_target:
aigc_target:
target_gap:
```

Only fill metrics that the user provided. Do not invent percentages.

### 2. Report Difference Diagnosis

- Improved paragraphs:
- Worsened paragraphs:
- Unchanged paragraphs:
- AIGC regression present:

### 3. Failure Cause

- similarity_source:
- aigc_pattern:
- formalization_regression:
- evidence_missing:
- over_smoothing:
- protected_area:

### 4. Next Pass Plan

- Pass 1 similarity tasks:
- Pass 2 AIGC tasks:
- Pass 3 evidence injection tasks:
- Pass 4 regression audit tasks:

### 5. Rewrite Task Table

| id | section | paragraph_summary | current_risk | target_gap | mode | rewrite_intensity | required_evidence | protected_items | action |
|---|---|---|---|---|---|---|---|---|---|

### 6. Candidate Rewrite

Only rewrite paragraphs confirmed safe to revise.

For missing information, output:

```text
建议作者补充：……
```

### 7. Self Audit

- similarity_risk_after_heuristic:
- aigc_risk_after_heuristic:
- evidence_density_change:
- regression_guard_result:
- integrity_check:

## Safety

Do not promise that the output will meet any report threshold. Do not fabricate data, experiments, citations, code, interfaces, screenshots, or running results.
