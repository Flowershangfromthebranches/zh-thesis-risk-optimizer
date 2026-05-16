# Discipline AIGC Bottleneck Rules

## Purpose

Different disciplines hit different AIGC bottlenecks. A computer-science thesis and a management thesis should not use the same final-pass strategy.

## Computer-Science Theses

Common bottleneck:

- Code, APIs, table names, parameters, formulas, and tool names must be protected.
- System design and implementation chapters often become repetitive module descriptions.
- Detection tools may keep flagging technical overview and conclusion even after wording changes.
- Around 20% may become a practical plateau when remaining risk is protected technical prose, English abstract, fixed definitions, or short generic summary text.

Final-pass strategy:

- Freeze code, API, path, parameter, table, field, and formula tokens.
- Modify only surrounding explanation.
- Use concrete module flow, input/output, exception path, and test condition.
- Avoid adding fictional debugging or performance data.
- If remaining high-risk text is protected or evidence-limited, mark `TECHNICAL_PROTECTED_PLATEAU`.

## Management / Business / Applied Social-Science Theses

Common bottleneck:

- The prose naturally uses abstract nouns such as process, mechanism, capability, channel, and system.
- Problem and countermeasure chapters often use standard policy/report rhythm.
- Survey data exists but is underused in the paragraph structure.
- Repeated "现状-问题-对策-意义" scaffolds create orange/medium AIGC risk.

High-risk thesis types:

- Human resource management.
- Business administration.
- Marketing.
- E-commerce operation and management.
- Accounting and financial management.
- Public administration.
- Education management.
- Tourism management.
- Logistics management.
- Public service, social work, and community governance.

Use `references/social_science_template_bottleneck.md` when the thesis is dominated by "concept -> status -> problem -> cause -> countermeasure -> guarantee" structures.

Final-pass strategy:

- Use survey/interview/company-specific evidence as paragraph anchors.
- Break list structures.
- Replace generic management claims with local observations.
- Compress broad value statements.
- Keep citations and questionnaire facts intact.
- If evidence is insufficient, request author details instead of adding theory.

## Plateau Labels

- `TECHNICAL_PROTECTED_PLATEAU`
- `MANAGEMENT_TEMPLATE_PLATEAU`
- `SOCIAL_SCIENCE_TEMPLATE_PLATEAU`
- `SURVEY_DATA_UNDERUSED`
- `COUNTERMEASURE_LIST_PLATEAU`
- `POLICY_STYLE_PLATEAU`
- `CASE_EVIDENCE_MISSING`
- `EVIDENCE_LIMITED_PLATEAU`
- `REPORT_MODEL_FLOOR`

## Relation To SKILL.md

Use this file when a thesis remains above the user target after multiple rounds, especially when the remaining risk differs by discipline.
