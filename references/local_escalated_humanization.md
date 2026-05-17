# Local Escalated Humanization

## Purpose

`LOCAL_ESCALATED_HUMANIZATION` is the only path for controlled Level 4 de-AIGC work. It is not a full-thesis mode and must never be used as broad rewriting.

## Activation

It may run only when all are true:

1. `RISK_INTAKE_GATE` allows `level_4_allowed = local_only`;
2. `FIRST_PASS_EFFECTIVENESS_GATE`, current-report diagnosis, or `TEMPLATE_RESIDUE_DETECTOR` identifies unresolved high-risk residuals;
3. the target paragraph is in an allowed section or is a confirmed report red/orange/template-residue target;
4. `THESIS_REGISTER_GUARD` is scheduled after the rewrite.

## Allowed Targets

Local escalation may apply to:

- current-report red paragraphs;
- large orange blocks;
- paragraphs hit by `TEMPLATE_RESIDUE_DETECTOR`;
- high-risk residuals in abstract, theory, Chapter 5, or conclusion, but with section ceilings below.

## Section Ceilings

| section | max level | Level 4 allowed |
|---|---:|---|
| 摘要 | 3.5 | no |
| 英文摘要 | 3.5 | no |
| 理论基础 | 3.5 | no |
| 结论 | 3.5 | no |
| 第四章问题分析 | 4 | yes, controlled and local |
| 第五章对策分析 | 4 | yes, controlled and local |
| 研究方法 | 3 | no |
| 企业现状分析 | 3.5 | no |

## Level 4 Behavior

Level 4 may:

- break the original sentence skeleton more aggressively;
- reorder evidence, problem judgment, and bounded recommendations;
- add stronger author interpretation when anchored to provided evidence;
- reduce dense abstract management jargon;
- vary sentence rhythm more than Level 3.

Level 4 must not:

- rewrite the whole thesis;
- apply to every red/orange paragraph automatically;
- use chat-like, diary-like, or social-media expressions;
- invent interviews, questionnaire data, company systems, forms, indicators, or operational facts;
- alter citations, data, conclusions, formulas, code, paths, table names, field names, or references.

## Required Output

| paragraph_id | section | original_band | trigger | level_used | evidence_anchor | thesis_register_guard_result | status |
|---|---|---|---|---:|---|---|---|

## Failure States

| condition | status |
|---|---|
| Level 4 requested in abstract/theory/conclusion | `LEVEL_4_SECTION_BLOCKED` |
| no evidence anchor for stronger interpretation | `NEEDS_AUTHOR_EVIDENCE` |
| thesis register guard fails after local rewrite | `NEEDS_ACADEMIC_TONE_REPAIR` |
| user asks for full-text Level 4 | `BLOCKED_FULL_TEXT_LEVEL_4` |

## Relation To SKILL.md

This engine runs after `CONTROLLED_HUMANIZATION_ENGINE` and before `REWRITE_APPLICATION_GATE`. Its output must be checked by `THESIS_REGISTER_GUARD`, `AIGC_REGRESSION_GUARD`, and `FINAL_ACCEPTANCE_AUDIT`.
