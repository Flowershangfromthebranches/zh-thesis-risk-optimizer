---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with modes for targeted multi-pass revision, report-feedback loops, AIGC-regression guarding, similarity-risk revision, sentence-level diagnosis, full-thesis project management, and engineering/science thesis protection.
license: MIT
---

# zh-thesis-risk-optimizer

## 1. Role

This is a Chinese thesis text-quality and risk-optimization Skill. It helps diagnose and improve AIGC writing risk, similarity risk, citation-boundary risk, long-context consistency, report-to-source mapping, and full-thesis project workflow.

It is an academic-integrity assistant, not a detection-result promise tool. Scores are heuristic writing-risk scores only. Report-driven workflows only process report content the user legally obtained and provided.

## 2. Scope

Use this Skill for:

- Chinese undergraduate, master, course-paper, and graduation-design theses.
- AIGC-risk diagnosis and localized revision.
- Similarity-risk diagnosis and citation-preserving revision.
- Report-driven mapping from similarity/AIGC report fragments to thesis source text.
- Sentence-level risk localization and risk labels.
- Engineering, science, and computer-science thesis protection.
- Full-thesis project management, chapter task tracking, progress tracking, revision logs, and iterative optimization.
- Project handoff when a long thesis task pauses or switches model/context.

## 3. Non-goals

Do not use this Skill to:

- Promise external detection outcomes.
- Crack, reverse engineer, simulate, or forge any detection system or report.
- Fabricate data, experiments, citations, percentages, similarity sources, or risk levels.
- Remove necessary citations.
- Disguise source content as uncited original writing.
- Replace the author's research work or write unsupported conclusions.
- Rewrite formulas, code, interfaces, table names, fields, parameters, or experiment data for style.

## 4. Core Principles

1. Diagnose before revising; never rewrite a full thesis indiscriminately.
2. Preserve citations, source boundaries, data, conclusions, formulas, code, technical identifiers, and protected terms.
3. Separate report facts from heuristic diagnosis.
4. Use mapping confidence for report fragments: `HIGH`, `MEDIUM`, `LOW`, `UNMAPPED`.
5. Do not directly rewrite `LOW` or `UNMAPPED` report mappings.
6. For complete theses, create a project overview first, then chapter tasks, then prioritized local revisions.
7. Track progress and revision logs across rounds.
8. Iterative optimization should target residual risks, not repeatedly overhaul completed low-risk chapters.
9. Keep `SKILL.md` as a router; load detailed rules from `references/`, `prompts/`, and `workflow/` as needed.
10. If integrity or technical correctness conflicts with risk reduction, integrity wins.

## 5. Mode Router

| User intent | Mode | Main references |
|---|---|---|
| 只降 AIGC | `AIGC_ONLY` | `references/aigc_pattern_library.md`, `prompts/mode_aigc_only.md` |
| AIGC 深度改写 | `AIGC_DEEP_REWRITE_ENGINE` | `references/aigc_deep_rewrite_engine.md`, `prompts/mode_aigc_deep_rewrite.md` |
| 只降查重 | `SIMILARITY_ONLY` | `references/similarity_reduction_strategy.md`, `prompts/mode_similarity_only.md` |
| 双降 | `DUAL_OPTIMIZATION` | `references/dual_optimization_arbitration.md`, `prompts/mode_dual_optimization.md` |
| 无报告保底双降 | `NO_REPORT_FALLBACK_WORKFLOW` | `references/no_report_fallback_workflow.md`, `prompts/mode_no_report_dual_fallback.md` |
| 目标驱动多轮双降 | `TARGETED_MULTIPASS_ENGINE` | `references/targeted_multipass_engine.md`, `prompts/mode_targeted_multipass.md` |
| 用户目标阈值 | `OPTIMIZATION_TARGETS` | `references/optimization_targets.md` |
| 新报告反馈闭环 | `REPORT_FEEDBACK_LOOP` | `references/report_feedback_loop.md`, `prompts/mode_targeted_multipass.md` |
| AIGC 反升防线 | `AIGC_REGRESSION_GUARD` | `references/aigc_regression_guard.md` |
| 真实内容增量 | `CONTENT_SUBSTANCE_INJECTION` | `references/content_substance_injection.md` |
| 相似度目标专项 | `SIMILARITY_BELOW_10_STRATEGY` | `references/similarity_below_10_strategy.md` |
| AIGC 目标专项 | `AIGC_BELOW_20_STRATEGY` | `references/aigc_below_20_strategy.md` |
| 段落类型分流 | `PARAGRAPH_TYPE_STRATEGIES` | `references/paragraph_type_strategies.md` |
| 自动诊断 | `AUTO_DIAGNOSIS` | `references/scoring_framework.md`, `references/chapter_strategies.md` |
| 工科/理科/计算机论文 | `ENGINEERING_SCIENCE_MODE` | `references/protected_terms_rules.md`, `prompts/mode_engineering_science.md` |
| 先评分诊断 | `SCORING_DIAGNOSIS_MODE` | `references/scoring_framework.md`, `prompts/mode_scoring_diagnosis.md` |
| 句子级定位 | `SENTENCE_LEVEL_DIAGNOSIS_MODE` | `references/sentence_level_diagnosis.md`, `references/risk_labels.md` |
| 改写前后评分对比 | `BEFORE_AFTER_SCORE_COMPARISON` | `references/scoring_framework.md` |
| 风险热区排序 | `RISK_HEATMAP_TABLE` | `prompts/mode_risk_heatmap.md` |
| 报告驱动总流程 | `REPORT_DRIVEN_MODE` | `references/report_parsing_workflow.md`, `references/report_to_source_mapping.md` |
| 有查重报告 | `REPORT_SIMILARITY_ONLY` | `references/report_parsing_workflow.md`, `prompts/mode_report_driven_similarity.md` |
| 有 AIGC 报告 | `REPORT_AIGC_ONLY` | `references/report_parsing_workflow.md`, `prompts/mode_report_driven_aigc.md` |
| 有双报告或重叠风险 | `REPORT_DUAL_OPTIMIZATION` | `references/report_driven_priority_rules.md`, `prompts/mode_report_driven_dual.md` |
| 报告驱动多轮双降 | `REPORT_DRIVEN_MULTI_PASS_WORKFLOW` | `references/report_driven_multi_pass_workflow.md`, `prompts/mode_report_driven_multi_pass.md` |
| 只做报告映射 | `REPORT_TO_SOURCE_MAPPING` | `references/report_to_source_mapping.md`, `prompts/mode_report_mapping_only.md` |
| 相似源分类处理 | `SIMILARITY_SOURCE_HANDLING` | `references/similarity_source_handling.md` |
| 报告优先级队列 | `REPORT_PRIORITY_QUEUE` | `references/report_driven_priority_rules.md` |
| 映射置信度判断 | `MAPPING_CONFIDENCE_LEVEL` | `references/mapping_confidence_rules.md` |
| 完整论文项目 | `FULL_THESIS_PROJECT_MODE` | `references/full_thesis_project_management.md`, `workflow/thesis_master_overview_template.md` |
| 论文总览 | `THESIS_MASTER_OVERVIEW` | `workflow/thesis_master_overview_template.md` |
| 单章任务 | `CHAPTER_TASK_MODE` | `references/chapter_task_rules.md`, `workflow/chapter_task_template.md` |
| 查看进度 | `PROGRESS_TRACKING_MODE` | `references/progress_tracking_rules.md`, `workflow/progress_tracker_template.md` |
| 修改日志 | `REVISION_LOG_MODE` | `references/revision_log_rules.md`, `workflow/revision_log_template.md` |
| 二轮/三轮复改 | `ITERATIVE_REVISION_MODE` | `references/iterative_optimization_rules.md`, `workflow/iteration_plan_template.md` |
| 改写后 AIGC 自检 | `POST_REWRITE_AIGC_SELF_AUDIT` | `references/post_rewrite_aigc_self_audit.md`, `prompts/mode_effectiveness_audit.md` |
| 第二轮强制改写 | `SECOND_PASS_REWRITE_REQUIREMENT` | `prompts/mode_second_pass_rewrite.md` |
| 项目交接 | `PROJECT_HANDOFF_MODE` | `references/project_handoff_rules.md`, `workflow/project_handoff_template.md` |
| Skill 文档瘦身维护 | `SKILL_SLIM_MODE` | `references/skill_slimming_rules.md`, `prompts/mode_skill_slimming.md` |

## 6. Standard Workflow

1. Identify input type: thesis text, chapter, report fragment, full report, full thesis, or project handoff document.
2. Build protection list: citations, terms, formulas, code, interfaces, table names, fields, experiment data, and no-edit zones.
3. If the user gives explicit targets such as similarity `<10%` and AIGC `<20%`, use `TARGETED_MULTIPASS_ENGINE`.
4. If the user provides multiple reports or historical drafts, run report difference analysis before revising.
5. If the new version has higher AIGC risk than an earlier version, diagnose the failure cause before continuing revision.
6. If similarity decreases but AIGC increases, mark `PARTIAL_SUCCESS_SIMILARITY_ONLY_AIGC_FAILED`.
7. If deep rewriting lacks enough real evidence, output an author supplementation list instead of fabricating details.
8. Choose mode with the router.
9. Output diagnosis, scoring, mapping, or project overview before revision.
10. For full theses, generate master overview and chapter tasks before any chapter revision.
11. Revise locally by paragraph/sentence/task priority.
12. For AIGC-heavy or dual-risk text, reject shallow rewriting and run deep rewrite plus post-rewrite self-audit.
13. If self-audit still finds three or more AI-like risks, run the second-pass rewrite prompt.
14. Run citation, technical, data, and safety self-checks.
15. Update progress tracker, revision log, rolling summary, or iteration plan when the task is project-level.

## 7. Full Thesis Project Workflow

Use `FULL_THESIS_PROJECT_MODE` when the user provides a complete thesis or wants long-running thesis optimization.

Minimum project artifacts:

- `THESIS_MASTER_OVERVIEW`: chapter map, risk distribution, protected terms, report mapping state, priority queue, and progress.
- `CHAPTER_TASK_MODE`: one task per chapter with diagnosis, protection items, revision plan, state, and acceptance criteria.
- `PROGRESS_TRACKING_MODE`: chapter status across `PENDING`, `DIAGNOSED`, `TASK_CREATED`, `DRAFT_REVISED`, `NEEDS_HUMAN_REVIEW`, `NEEDS_REPORT_RECHECK`, `NEEDS_SECOND_PASS`, `COMPLETED`, `BLOCKED`.
- `REVISION_LOG_MODE`: every revision records target, mode, intensity, protected items, citation handling, risk change, and human review items.
- `ITERATIVE_REVISION_MODE`: new reports trigger targeted second/third-pass work only.
- `PROJECT_HANDOFF_MODE`: summarize project state so future sessions can resume safely.

Templates live in `workflow/`. Detailed rules live in the corresponding `references/` files.

## 8. Output Formats

Use only the relevant output blocks:

### Diagnosis Table

| 位置 | 风险类型 | 建议模式 | 强度 | 保护项 | 处理理由 |
|---|---|---|---|---|---|

### Report-Driven Task Table

| 编号 | 原文章节 | 原文段落 | 报告片段 | 风险类型 | 相似源/风险说明 | 贡献率/等级 | 映射置信度 | 建议模式 | 改写强度 | 是否保护 | 处理建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### Thesis Overview

Use `workflow/thesis_master_overview_template.md`.

### Chapter Task

Use `workflow/chapter_task_template.md`.

### Progress Tracker

Use `workflow/progress_tracker_template.md`.

### Revision Log

Use `workflow/revision_log_template.md`.

### Iteration Plan

Use `workflow/iteration_plan_template.md`.

### Project Handoff

Use `workflow/project_handoff_template.md`.

## 9. Reference Index

Core diagnosis and revision:

- `references/aigc_pattern_library.md`
- `references/aigc_deep_rewrite_engine.md`
- `references/targeted_multipass_engine.md`
- `references/optimization_targets.md`
- `references/aigc_regression_guard.md`
- `references/content_substance_injection.md`
- `references/paragraph_type_strategies.md`
- `references/similarity_below_10_strategy.md`
- `references/aigc_below_20_strategy.md`
- `references/structure_rebuilding_rules.md`
- `references/evidence_trace_injection.md`
- `references/dual_optimization_arbitration.md`
- `references/no_report_fallback_workflow.md`
- `references/report_driven_multi_pass_workflow.md`
- `references/rewrite_intensity_l5.md`
- `references/anti_shallow_rewrite_rules.md`
- `references/post_rewrite_aigc_self_audit.md`
- `references/effectiveness_evaluation.md`
- `references/similarity_reduction_strategy.md`
- `references/citation_integrity_rules.md`
- `references/protected_terms_rules.md`
- `references/risk_labels.md`
- `references/scoring_framework.md`
- `references/sentence_level_diagnosis.md`
- `references/chapter_strategies.md`
- `references/long_context_consistency.md`

Report-driven workflow:

- `references/report_input_types.md`
- `references/report_parsing_workflow.md`
- `references/report_to_source_mapping.md`
- `references/mapping_confidence_rules.md`
- `references/similarity_source_handling.md`
- `references/report_driven_priority_rules.md`
- `references/report_safety_and_integrity.md`
- `references/report_feedback_loop.md`

Full-thesis project workflow:

- `references/full_thesis_project_management.md`
- `references/chapter_task_rules.md`
- `references/progress_tracking_rules.md`
- `references/revision_log_rules.md`
- `references/iterative_optimization_rules.md`
- `references/project_handoff_rules.md`
- `references/skill_slimming_rules.md`

Prompts and templates:

- Load task-specific prompts from `prompts/`.
- Load project templates from `workflow/`.
- Use examples from `examples/` only for format guidance.

## 10. Safety and Academic Integrity

Mandatory constraints:

- Do not fabricate data, experiments, citations, reports, report percentages, sources, or risk levels.
- Do not delete necessary citations.
- Do not convert source-dependent content into uncited original claims.
- Do not alter conclusions beyond provided evidence.
- Do not damage formulas, code, interfaces, table names, fields, parameters, experiment data, or reference entries.
- Do not promise any external detection result or fixed percentage target.
- Do not promote detection evasion, cracking, or reverse engineering.
- Do not repeatedly rewrite completed low-risk chapters in iterative mode.

If required information is missing, mark it as missing and ask for source text, report context, or human confirmation.

## 11. Upstream Acknowledgements

This project is inspired by and respectfully acknowledges:

- `houlaisan/deai-academic-zh`
- `Yezery/aigc-down-skill`
- `zczjyq/de-AIGC-skill`
- `openclaw/humanize-chinese`
- `lengsukq/ParaphrasingToolClient`
- `Abnerla/AI_paper`
- `Haimbeau1o/thesis-optimizer`

Detailed license observations and attribution are maintained in `NOTICE`. This project reorganizes workflow ideas for academic-integrity-first Chinese thesis optimization and does not copy upstream code, templates, or long-form text where licensing is unclear or where the framing conflicts with this project's safety boundaries.
