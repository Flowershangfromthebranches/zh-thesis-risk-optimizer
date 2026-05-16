# Prompt: AIGC_PLATEAU_BREAKER

Use this mode when multiple AIGC reduction rounds show diminishing returns.

If the user provides the original thesis and original AIGC report before any revision, use `FIRST_PASS_RED_ORANGE_ENGINE` instead so red and orange are handled together in the first pass.

## Inputs

- Original text.
- Current draft.
- Previous AIGC reports.
- Latest AIGC report.
- Report color/risk-band meaning.
- Discipline or thesis type.
- Protected list.

## 1. Trend Diagnosis

```yaml
original_aigc:
round_1_aigc:
round_2_aigc:
round_3_aigc:
red_trend:
orange_trend:
purple_trend:
plateau_status:
```

Do not invent missing percentages. Use only user-provided report values.

## 2. Plateau Type

- RED_HIGH_RISK_PASS still needed:
- ORANGE_PLATEAU_PASS needed:
- PURPLE_CLEANUP_PASS needed:
- TECHNICAL_PROTECTED_PLATEAU:
- MANAGEMENT_TEMPLATE_PLATEAU:
- EVIDENCE_LIMITED_PLATEAU:
- REPORT_MODEL_FLOOR:

## 3. Report-Band Task Table

| id | section | paragraph_summary | band | repeated_skeleton | bottleneck_reason | repair_mode | protected_items | action |
|---|---|---|---|---|---|---|---|---|

## 4. Orange-Zone Rewrite Plan

Use `references/orange_zone_rewrite_strategy.md`.

- Enumeration break:
- Evidence-first reordering:
- Case-local anchor:
- Rhythm disruption:
- Compression before expansion:
- Protected-fact bypass:

## 5. Candidate Revision

Only revise paragraphs whose band is red/orange/purple and whose protected constraints allow safe editing.

Requirements:

- Freeze white/low-risk paragraphs.
- Do not repeat the same rewrite strategy from the last round.
- Do not expand all paragraphs.
- Do not fabricate survey, interview, system, code, or test facts.

## 6. No-Progress Decision

- Continue targeted repair:
- Stop and request evidence:
- Mark protected plateau:
- Mark report-model floor:

## Safety

This prompt improves writing-risk handling only. It does not promise any external report outcome.
