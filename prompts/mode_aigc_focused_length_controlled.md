# Prompt: AIGC_FOCUSED_LENGTH_CONTROLLED

Use this prompt when similarity is already acceptable or similarity reduction is enough, but AIGC risk remains high and the user wants controlled length growth.

## Input

- Original text.
- Current revised draft.
- Similarity report, if provided.
- AIGC report, if provided.
- User targets.
- Original character count.
- Current draft character count.
- Allowed growth range, such as 0-2000 Chinese characters.
- Protected list.

## 1. Mode Decision

- Enter AIGC_FOCUSED_LENGTH_CONTROLLED: yes/no.
- Reason:
- Similarity mode downgraded to stability check: yes/no.

## 2. Metrics and Budget

```yaml
original_chars:
current_chars:
current_delta:
allowed_delta:
budget_status:
remaining_budget:
```

## 3. AIGC Hotspot Table

| id | section | sentence_or_paragraph | aigc_pattern | severity | repair_action | length_action | protected_items |
|---|---|---|---|---|---|---|---|

## 4. Repeated AI Expression Table

| expression | count | locations | action |
|---|---:|---|---|

## 5. Rewrite Plan

### Replace Without Expansion

-

### Slight Expansion Within Budget

-

### Human Evidence Needed

-

## 6. Candidate Revision

Only output paragraphs that can be safely modified.

Requirements:

- Prefer replacing risky sentences.
- Do not expand heavily.
- Do not add unsupported facts.
- Do not damage citations or technical details.
- Keep formal academic tone while reducing AI-like smoothness.

## 7. Length Budget Table

| section | before_chars | after_chars | delta | budget | status |
|---|---:|---:|---:|---:|---|

## 8. Self Audit

- aigc_pattern_reduction:
- formalization_regression_check:
- over_expansion_check:
- similarity_stability_check:
- integrity_check:
- human_review_needed:

## Safety

Do not promise external detection results. Do not fabricate data, experiments, citations, interfaces, logs, screenshots, or running results.
