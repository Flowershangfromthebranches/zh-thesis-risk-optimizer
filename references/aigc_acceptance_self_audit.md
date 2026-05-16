# AIGC Acceptance Self-Audit

## Purpose

`AIGC_ACCEPTANCE_SELF_AUDIT` is the acceptance gate for red/orange AIGC report paragraphs. It is stricter than a normal style check.

The audit is heuristic and does not represent any external detector result.

## Required Audit Items

For every red/orange paragraph after rewriting, check:

1. Is the rewrite only synonym replacement?
2. Does it still follow a "definition + meaning + countermeasure" template?
3. Does it still contain mechanical enumeration such as "一是、二是、三是、四是"?
4. Is abstract noun density still high, especially 体系, 机制, 能力, 价值, 保障, 路径, 赋能, 支撑?
5. Does it lack the specific company, organization, system, module, or research object?
6. For management and HR papers, does it lack questionnaire, interview, process, post, indicator, responsibility, review cycle, or execution-boundary evidence?
7. Did the rewrite become smoother, more formal, more balanced, or more AI-like?

## Pass Rule

- If any item fails, the paragraph does not pass.
- A failing paragraph must enter a second-pass rewrite with a different repair strategy.
- If the second pass still fails, output `HUMAN_EVIDENCE_REQUEST` and do not pretend the paragraph is complete.

## Required Output

| id | audit_item | pass_or_fail | evidence | next_action |
|---|---|---|---|---|

## Second-Pass Strategy

The second pass must not repeat the first-pass method. Choose at least one different action:

- break the template skeleton;
- move local evidence before evaluation;
- replace abstract nouns with company/process/indicator language;
- turn enumeration into process-stage prose;
- add a real boundary or responsibility owner from the source;
- compress generic value claims instead of adding more explanation.

## Management And HR Addendum

For human resource management, business administration, marketing, education management, and public administration theses, an accepted paragraph must connect to at least one real local anchor when available:

- company or department;
- post or role;
- recruitment, training, performance, incentive, service, or management process;
- questionnaire or interview evidence;
- form, system, indicator, responsibility owner, review cycle, or implementation boundary.

If no such evidence exists in the source, request author evidence. Do not fabricate it.

## Relation To SKILL.md

Use this audit for `CURRENT_REPORT_RED_ORANGE_ENGINE`, `FIRST_PASS_RED_ORANGE_ENGINE`, `AIGC_PLATEAU_BREAKER`, and `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`.
