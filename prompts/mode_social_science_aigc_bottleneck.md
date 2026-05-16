# Prompt: SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK

Use this prompt when a management, business, education, public administration, or applied social-science thesis still has high AIGC risk after ordinary report-driven rewriting.

## Inputs

- Thesis text or file copy.
- AIGC report, if provided.
- Similarity report, if provided.
- Thesis major and topic.
- Survey, interview, case, organization, process, or indicator evidence.
- Protected list.

## 1. Discipline Diagnosis

```yaml
thesis_type:
likely_template_bottleneck:
template_skeleton:
report_colors_available:
red_orange_primary_targets:
character_delta_guard: enabled
```

Candidate bottleneck types:

- `SOCIAL_SCIENCE_TEMPLATE_PLATEAU`
- `MANAGEMENT_TEMPLATE_PLATEAU`
- `SURVEY_DATA_UNDERUSED`
- `COUNTERMEASURE_LIST_PLATEAU`
- `POLICY_STYLE_PLATEAU`
- `CASE_EVIDENCE_MISSING`

## 2. High-Risk Section Scan

| section | paragraph_id | report_band | template_skeleton | available_evidence | missing_evidence | priority |
|---|---|---|---|---|---|---|

Common high-risk sections:

- Research background.
- Theory overview.
- Current situation analysis.
- Problem analysis.
- Cause analysis.
- Countermeasure chapter.
- Guarantee measures.
- Conclusion.

## 3. Evidence-First Repair Plan

For each red/orange paragraph:

1. Identify the repeated template skeleton.
2. Identify available local evidence.
3. Move evidence before generic evaluation.
4. Tie the claim to a concrete organization, department, post, process, data point, or respondent group.
5. Delete broad value claims that do not add evidence.
6. Keep citations and data intact.

## 4. Human Evidence Request

If evidence is missing, do not fabricate it.

| section | paragraph_id | missing_evidence | question_to_author | conservative_repair_possible |
|---|---|---|---|---|

Example questions:

- Which department or岗位 does this problem occur in?
- What survey percentage supports this claim?
- What interview feedback shows this issue?
- Which step in the recruitment/training/performance process is affected?
- What existing制度 or表单 is being revised?

## 5. Candidate Revision

Only revise paragraphs with enough evidence or safe conservative repair.

Requirements:

- Do not use generic "完善机制、优化流程、提升能力、强化保障" as the main sentence skeleton.
- Do not keep long "第一、第二、第三" chains unless necessary.
- Do not invent company facts, survey data, interview content,制度, or指标.
- Keep whole-thesis character delta within the allowed range.

## 6. Self Audit

- template_skeleton_reduced:
- local_evidence_used:
- abstract_noun_density_reduced:
- enumeration_chain_broken:
- citations_preserved:
- data_preserved:
- character_delta_status:
- remaining_evidence_requests:

## Safety

This prompt improves writing-risk handling only. It does not promise any external AIGC or similarity result.
