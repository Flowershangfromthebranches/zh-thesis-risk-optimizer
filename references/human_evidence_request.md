# Human Evidence Request

## Purpose

When a paragraph lacks real content, the Skill must not fabricate detail or add empty expansion to reduce AIGC risk. It should ask for targeted author evidence.

## Trigger Conditions

- The paragraph has high AIGC risk.
- There are no usable modules, parameters, test results, running conditions, or design reasons.
- Further rewriting would become generic.
- AIGC needs repair but the length budget is tight.

## Output Format

| section | paragraph_id | missing_evidence | why_needed | suggested_question_to_author | rewrite_after_supplied |
|---|---|---|---|---|---|

## Material Gap Table (For Social-Science / Management Theses)

For social-science and management theses, when evidence is missing, output a **Material Gap Table** instead of continuing to write. Do NOT silently fill gaps.

| section | paragraph_id | missing_evidence_type | why_needed | current_state | suggested_question_to_author |
|---|---|---|---|---|---|
| 2.1 理论基础 | P03 | which theory dimension is used | paragraph is encyclopedia definition | no thesis-specific anchor | 人岗匹配理论中您用到了哪个维度？衡量指标是什么？ |
| 3.2 问卷分析 | P12 | survey item wording | paragraph is generic description | no item text or scale | 第8-10题的具体表述和量表类型是什么？ |
| 4.1 现状分析 | P07 | company recruitment process | paragraph uses consulting-speak | only "优化流程" type sentences | A公司的招聘包含哪几个具体环节？各环节负责人是谁？ |

The Material Gap Table is mandatory when any of the following is needed but not provided by the author.

## Prohibited Self-Fabricated Data Types

The following data types must **NOT** be generated or estimated by the model. If missing, output a Material Gap Table row requesting them:

1. **行业平均水平** (industry average levels) — unless present in the original thesis, cited source, or user-provided material.
2. **预算比例** (budget ratios or percentages) — e.g., "招聘预算占HR总预算的15%".
3. **增速** (growth rates) — e.g., "年增长20%", "逐年上升趋势".
4. **流失率 / 离职率** (turnover rates) — unless directly from the thesis data or questionnaire.
5. **员工规模** (employee headcount) — e.g., "全公司共500人", "HR部门8人".
6. **系统上线年份** (system launch years) — e.g., "2019年上线了E-HR系统".
7. **竞品企业案例** (competitor company cases) — e.g., "B公司采用了类似做法", "行业领先企业的实践表明".
8. **默认比例或分布** (default percentages or distributions) — e.g., "70%的员工认为……", "大部分集中在……".
9. **问卷样本量 / 回收率** (survey sample size / response rate) — unless explicitly stated in the thesis.
10. **访谈人数 / 对象描述** (interview count / participant description) — unless explicitly stated.

### Exception Rule

The above data MAY be used if and only if one of these sources provides it:
- The original thesis text.
- A user-provided AIGC or similarity report.
- Questionnaire raw data or summary tables.
- Interview transcripts or summaries.
- User-provided evidence pack (`workflow/author_evidence_pack_template.md`).
- A cited external reference (published paper, industry report, government statistics) with a verifiable citation.

If the data appears in any of these sources, cite the source in the gap table's `current_state` column.

## Example Questions

### For Engineering / Computer-Science Theses

- 这个模块为什么选择 `ThreadPoolExecutor`，而不是 `asyncio`？
- `max_depth` 和 `max_pages` 的值是如何确定的？
- 本地靶场包含哪些测试页面？
- SQL 注入误报有没有出现？
- XSS 检测是否只覆盖反射型？
- HTML 报告中具体包含哪些字段？
- 系统目前不支持哪些漏洞类型？

### For Social-Science / Management Theses

- A公司目前的招聘流程包含哪几个具体环节？
- 哪个岗位最难招？平均需要多少天？
- 问卷中得分最低的题目是哪几道？分值是多少？
- 访谈中有没有原话可以引用（不泄露隐私的前提下）？
- 各招聘渠道的简历占比大概是多少？
- 面试评分表目前有没有统一标准？
- 试用期流失集中在哪些岗位？主要原因是什么？

## Rules

- Do not invent answers.
- Do not fabricate debugging experience.
- Do not fabricate comparison experiments.
- Do not fabricate performance metrics.
- Do not fabricate industry averages, budget ratios, growth rates, turnover rates, headcount, system launch years, competitor cases, default distributions, sample sizes, or interview counts.
- **Material Gap Table is mandatory**: if evidence is missing and needed, output the gap table. Do not continue writing without it.
- If the author does not supplement evidence, use conservative repair (do not fabricate).

## Relation To SKILL.md

Use this file in `HUMAN_EVIDENCE_REQUEST` and before any evidence-dependent AIGC repair.
