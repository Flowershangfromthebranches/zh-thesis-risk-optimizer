# v0.8.4 Social-Science Template Bottleneck Cases

## Case 1: Human Resource Management Plateau

Input:

```yaml
major: human_resource_management
section: countermeasure
phrases: 完善招聘体系, 优化招聘流程, 加强培训, 健全激励机制
```

Expected:

- Enter `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`.
- Mark `COUNTERMEASURE_LIST_PLATEAU`.
- Request company,岗位, process, survey, or interview evidence if missing.

## Case 2: Education Management Thesis

Input:

```yaml
major: education_management
structure: 现状 -> 问题 -> 原因 -> 对策
evidence: teacher_interview_missing
```

Expected:

- Mark `SOCIAL_SCIENCE_TEMPLATE_PLATEAU`.
- Do not add fictional teacher interview content.
- Output human evidence request.

## Case 3: Marketing Strategy Thesis

Input:

```yaml
major: marketing
phrases: 提升品牌影响力, 拓宽营销渠道, 完善服务体系
survey_data: available
```

Expected:

- Move survey data before generic evaluation.
- Break list-style strategy paragraph.
- Preserve data.

## Case 4: Public Administration Thesis

Input:

```yaml
major: public_administration
phrases: 健全治理机制, 强化协同, 提升服务能力
policy_citation: present
```

Expected:

- Preserve policy citation boundaries.
- Replace policy-style plateau with local process or service scenario when evidence exists.
- If evidence is missing, request it.

## Case 5: Accounting / Financial Management Thesis

Input:

```yaml
major: financial_management
phrases: 完善内部控制, 加强风险管理, 提升财务管理水平
data: protected
```

Expected:

- Preserve financial data and table values.
- Revise surrounding analysis only.
- Mark protected data where necessary.
