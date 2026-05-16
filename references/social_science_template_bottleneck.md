# Social-Science Template Bottleneck

## Purpose

This file handles AIGC-risk plateaus common in management, business, education, public administration, and applied social-science theses.

These papers often have reports and still reduce poorly because the issue is not only wording. The issue is a repeated standard-answer structure with insufficient local evidence.

## High-Risk Thesis Types

Use this workflow for these thesis types when AIGC risk remains high after normal rewriting:

- Human resource management.
- Business administration.
- Marketing.
- E-commerce operation and management.
- Accounting and financial management.
- Public administration.
- Education management.
- Tourism management.
- Logistics management.
- Public service / social work / community governance.
- Innovation and entrepreneurship management.
- Rural revitalization, enterprise governance, service quality, customer satisfaction, employee satisfaction, training, performance, recruitment, incentive, and channel optimization topics.

This list is not exhaustive. Any thesis dominated by "status -> problem -> reason -> countermeasure -> guarantee" should be treated as a possible template bottleneck.

## Common Bottleneck Structure

Typical high-risk scaffolds:

```text
概念界定 -> 现状分析 -> 问题归纳 -> 原因分析 -> 优化对策 -> 保障措施
```

```text
第一，完善机制。第二，优化流程。第三，加强培训。第四，健全保障。
```

```text
通过上述措施，可以提升效率、增强能力、促进发展、提供参考。
```

These structures can remain orange/medium-risk even after synonym replacement.

## Why Reports Still Do Not Help Enough

Reports locate the risky paragraph, but they do not supply missing local evidence.

Poor reduction usually happens when:

- The paragraph still reads like a policy recommendation.
- Red/orange text is rewritten into smoother management language.
- Survey or interview data exists but is placed after generic conclusions.
- The same "problem -> reason -> effect -> measure" skeleton repeats.
- Measures are not tied to a specific department, post, process, group, or data point.
- The model adds abstract nouns such as 机制, 体系, 能力, 保障, 路径, 价值, 协同 without adding evidence.

## Evidence Types That Break The Template

Use only evidence from the thesis, user, or report:

- Company or organization profile.
- Department and岗位 structure.
- Recruitment channels and proportions.
- Survey percentages and cross-tab observations.
- Interview excerpts or summarized feedback.
- Existing制度,流程,表单,考核指标.
- Training frequency, attendance, satisfaction, turnover, conversion, cost, cycle, or complaint data.
- Specific process nodes where problems occur.
- Before/after workflow differences proposed by the author.
- Case-specific constraints such as budget, staff size, region, platform, season, or policy environment.

If the text lacks such evidence, output `HUMAN_EVIDENCE_REQUEST` rather than inventing details.

## Repair Strategy

### 1. Replace Generic Topic Sentences

Bad:

```text
企业应进一步完善招聘管理体系，提高招聘工作的科学性和有效性。
```

Better:

```text
该企业的招聘问题集中在简历初筛和用人部门反馈两个环节，因此本节先调整岗位需求确认流程，再处理渠道筛选标准。
```

### 2. Put Evidence Before Evaluation

Bad:

```text
招聘渠道较为单一，影响了企业人才获取效率。问卷结果显示，传统招聘平台占比较高。
```

Better:

```text
问卷中多数应聘者来自传统招聘平台，社交媒体和专业社区的来源占比较低。渠道结构过窄，使企业在技术岗和复合型岗位上难以触达更合适的候选人。
```

### 3. Break Enumeration Chains

Do not keep long "第一、第二、第三、第四" structures unless the thesis format requires it.

Options:

- Group measures by process stage.
- Convert one list item into a case observation.
- Merge repeated measures.
- Delete empty value endings.

### 4. Use Process Nodes

For HR and management topics, revise around concrete process nodes:

- recruitment demand confirmation,
- resume screening,
- interview coordination,
- onboarding,
- probation assessment,
- training needs survey,
- performance indicator setting,
- incentive feedback,
- channel review,
- customer complaint handling,
- service recovery.

### 5. Keep The Academic Tone

Do not make the text casual. The goal is formal but case-specific prose.

## Stop Conditions

Stop and request author input when:

- No company, department, survey, interview, case, or process evidence is available.
- Further rewriting only produces smoother abstract language.
- The paragraph depends on cited theory and cannot be safely localized.
- Character delta would exceed the allowed range.

Use labels:

- `SOCIAL_SCIENCE_TEMPLATE_PLATEAU`
- `CASE_EVIDENCE_MISSING`
- `SURVEY_DATA_UNDERUSED`
- `COUNTERMEASURE_LIST_PLATEAU`
- `POLICY_STYLE_PLATEAU`

## Output

```markdown
## Social-Science Bottleneck Diagnosis
| section | paragraph_id | template_skeleton | available_evidence | missing_evidence | repair_strategy |
|---|---|---|---|---|---|

## Evidence Request
| section | missing_evidence | question_to_author | why_needed |
|---|---|---|---|
```

## Relation To SKILL.md

Use this file with `DISCIPLINE_AIGC_BOTTLENECK_RULES`, `AIGC_PLATEAU_BREAKER`, and `THREE_MODE_COLOR_BAND_WORKFLOW`.
