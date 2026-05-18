# AIGC Below 20 Strategy

## Purpose

This strategy supports user goals such as AIGC below 20%. It is an optimization target, not a promised result.

AIGC below 20 usually cannot be approached through synonym replacement. It requires report-color coverage, discipline-aware structure rebuilding, evidence-based writing, and strict freeze rules for low-risk or non-scored text.

Always load `references/one_pass_cross_discipline_strategy.md` with this strategy.

## 1. Color-Band Priority

Use the report legend or the default legend:

- red: `>=70%`;
- orange: `>=60%` and `<70%`;
- purple: `>=50%` and `<60%`;
- black: `<50%`;
- gray: too-short fragments, headings, English, references, template pages, or other non-scored/excluded spans.

For below-20 targets:

1. red and orange are primary targets and must be structurally repaired or validly frozen;
2. purple is mandatory low-intensity rebalance when current AIGC remains above target;
3. black and gray are frozen by default;
4. do not add new smooth explanatory text merely to restore word count.

## 2. Template Removal

Delete or rebuild discipline-appropriate patterns such as:

- 随着...发展
- 然而...
- 本文设计并实现...
- 实验结果表明...
- 具有重要意义
- 提供便捷解决方案
- 构建体系
- 优化路径
- 赋能
- 协同
- 闭环
- 提供参考与借鉴

## 3. Discipline-Specific Local Specificity

Each high-risk paragraph should try to include one paper-specific object. Select by discipline:

- management / HR: company process, department,岗位, questionnaire item, interview finding, channel metric, review cycle;
- computer science / software: module, API, path, parameter, table/field name, test case, log, screenshot, dataset;
- engineering: design constraint, parameter, unit, equipment, test condition, result table, drawing number;
- medicine / nursing / public health: sample, inclusion criteria, outcome indicator, intervention, guideline boundary, ethics note;
- law: article number, case fact, legal relationship, dispute focus, jurisdiction, consequence;
- education / psychology: classroom scene, learner group, scale item, intervention step, teaching material, evaluation indicator;
- humanities / communication / arts: text fragment, corpus example, work detail, design element, historical context.

## 4. Uneven but Formal Rhythm

- Avoid identical three-part, parallel, or summary-heavy structures.
- Keep the style formal but not mechanical.
- Do not turn the thesis into conversational prose.
- Near the 20% threshold, prefer shorter replacement and compression over expansion.

## 5. Boundary and Limitation

Use real boundaries when supported. Examples:

- management: the questionnaire sample is internal, and implementation effects still require recruitment-cycle tracking;
- computer science: local testing cannot fully represent production traffic;
- engineering: the experiment conditions limit direct generalization;
- medicine: the sample size or observation period limits conclusion strength;
- law: the conclusion applies under the cited rule and case context;
- education: the classroom intervention may depend on grade, school type, and teacher practice.

## 6. Evidence Density

High-risk paragraphs must improve evidence density: the number of concrete objects, parameters, results, modules, survey/interview items, cases, or test conditions per 100 Chinese characters.

If evidence density cannot be improved from available sources, output `建议作者补充：...`.

## 7. Near-Threshold Stop Rule

When current AIGC is already close to the target, do not run another broad rewrite. Process only:

- residual red/orange;
- purple targets required by `COLOR_BAND_ROUTER`;
- template residue found by `TEMPLATE_RESIDUE_DETECTOR`;
- user-specified local problems.

If the remaining risk is black/gray/protected or evidence-limited, stop and output the limitation instead of rewriting more.

## Relation To SKILL.md

Use this file when the user target includes AIGC below 20% or when a new draft shows AIGC regression.
