# Template Residue Detector

## Purpose

`TEMPLATE_RESIDUE_DETECTOR` checks whether red/orange paragraphs still contain high-risk AIGC template residue after rewriting and DOCX patching.

If residue remains in the patched document, the task cannot be marked complete even if a rewrite table exists.

## Residue Patterns

Detect these patterns in patched red/orange paragraphs:

- 随着……深度发展
- 已成为……必然选择
- 直接关系到……效率与质量
- 本研究以……为研究对象
- 综合运用文献研究法、问卷调查法与访谈法
- 研究发现……存在四个核心问题
- 针对上述问题
- 提出系统性的优化对策
- 提供实践参考与借鉴
- 招聘是组织为获取合格人才而进行的一系列系统性活动
- 其本质是……
- 具有重要意义
- 构建……体系
- 赋能……
- 闭环优化机制
- 成为支撑组织战略的引擎

The detector should use exact matching where possible and conservative fuzzy matching for ellipsis-like variants.

## High-Priority Sections

Residue in these sections is especially severe:

- 摘要
- 理论基础
- 第五章 / 分析章
- 结论

If any of these sections still contain the listed residue in red/orange targets, mark `template_residue_detector_result = failed`.

## Failure Rules

When residue appears in patched red/orange paragraphs:

- Set `residue_detected = true`.
- Set `template_residue_detector_result = failed`.
- Set `final_delivery_status = TEMPLATE_RESIDUE_FAILURE` in `FINAL_ACCEPTANCE_AUDIT`.
- Do not mark the task `COMPLETED`.
- Re-enter `CONTROLLED_HUMANIZATION_ENGINE`.
- If safe rewriting needs missing evidence, output `material_gap_table`.

## Required Output

| section | paragraph_id | residue_pattern | residue_text | target_band | action_required |
|---|---|---|---|---|---|

## Relation To SKILL.md

Run this detector after `REWRITE_APPLICATION_GATE` and before `AIGC_REGRESSION_GUARD`, `FIRST_PASS_EFFECTIVENESS_GATE`, and `FINAL_ACCEPTANCE_AUDIT`.
