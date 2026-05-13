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

## Example Questions

- 这个模块为什么选择 `ThreadPoolExecutor`，而不是 `asyncio`？
- `max_depth` 和 `max_pages` 的值是如何确定的？
- 本地靶场包含哪些测试页面？
- SQL 注入误报有没有出现？
- XSS 检测是否只覆盖反射型？
- HTML 报告中具体包含哪些字段？
- 系统目前不支持哪些漏洞类型？

## Rules

- Do not invent answers.
- Do not fabricate debugging experience.
- Do not fabricate comparison experiments.
- Do not fabricate performance metrics.
- If the author does not supplement evidence, use conservative repair.

## Relation To SKILL.md

Use this file in `HUMAN_EVIDENCE_REQUEST` and before any evidence-dependent AIGC repair.
