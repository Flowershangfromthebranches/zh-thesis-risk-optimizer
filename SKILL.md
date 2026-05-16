---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with modes for AIGC-focused length-controlled revision, targeted multi-pass revision, report-feedback loops, AIGC-regression guarding, sentence-level diagnosis, full-thesis project management, and engineering/science thesis protection.
license: MIT
---

# zh-thesis-risk-optimizer

## 1. Role

This Skill helps revise Chinese thesis text for writing quality, AIGC writing-risk signals, similarity-risk expression, citation-boundary integrity, report-to-source mapping, and full-thesis workflow management.

It is not a detection-result promise tool. Scores are heuristic writing-risk references only. Report-driven workflows only process report content legally obtained and provided by the user.

## 2. Safety Boundaries

Do not:

- Promise external detection outcomes or fixed percentage changes.
- Crack, reverse engineer, simulate, or forge any detection system or report.
- Fabricate data, experiments, citations, report percentages, similarity sources, interviews, logs, code, interfaces, screenshots, or risk levels.
- Delete necessary citations or disguise sourced content as uncited original writing.
- Alter conclusions beyond provided evidence.
- Rewrite formulas, code, API paths, table names, field names, parameters, experiment data, or reference entries for style.

When integrity or technical correctness conflicts with risk reduction, integrity wins.

## 3. Core Workflow

1. Identify input type: thesis text, chapter, full thesis, report fragment, full report, historical draft, or project handoff.
2. Build protection list: citations, terms, formulas, code, interfaces, table names, fields, parameters, experiment data, and no-edit zones.
3. Choose the smallest applicable mode family below.
4. Output diagnosis, mapping, task table, or project overview before revision.
5. Run `BURSTINESS_INJECTION` as an early rhythm audit for AIGC-related revision; apply rhythm repair only when the paragraph actually lacks variation.
6. Revise only confirmed and safe paragraphs or sentences.
7. Run self-audit for AIGC style, similarity risk, citation integrity, technical facts, and character change.
8. Update project artifacts when working at full-thesis or multi-round scope.

**Critical principle**: AIGC detectors often react to **how** text is written, not only **what** is written. A rewrite that produces smoother, more balanced, more formal prose can increase AIGC risk. Rhythm matters, but it is not sufficient for management and social-science theses; these also need report-color parsing, template-skeleton repair, and evidence-first reconstruction.

Special routing:

- If the user wants to use the Skill but has not provided enough input to choose a mode, use `INTAKE_WIZARD` first.
- Default user-facing workflow: use `THREE_MODE_COLOR_BAND_WORKFLOW` to choose similarity-only, AIGC-only, or dual revision.
- File input: use `FILE_INPUT_COPY_WORKFLOW`; create a copy, edit the copy, and keep the original untouched.
- Color-marked DOCX report input: use `DOCX_COLOR_REPORT_EXTRACTION` before plain-text extraction or report-driven rewriting.
- **Any AIGC revision**: run `BURSTINESS_INJECTION` as an early rhythm audit. If rhythm is already varied but red/orange risk remains, switch to template-skeleton repair and evidence-first reconstruction instead of adding more short sentences.
- Management, business, education, public administration, or applied social-science thesis with repeated "status -> problem -> countermeasure" structure: use `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`. These theses are especially vulnerable to AIGC detection because their template structure is inherently AI-like; report-color parsing, evidence placement, and template breaking are critical.
- Original thesis plus original AIGC report: use `FIRST_PASS_RED_ORANGE_ENGINE`; red and orange bands both enter the first-pass primary task table.
- Multi-round AIGC reports with red down but orange still high: use `AIGC_PLATEAU_BREAKER`.
- Similarity already acceptable but AIGC still high: use `AIGC_FOCUSED_LENGTH_CONTROLLED`.
- Whole-thesis revision: apply `CHARACTER_DELTA_GUARD`; default total character change stays within `±10%` unless the user specifies another range.
- User targets such as similarity `<10%` and AIGC `<20%`: treat them as goals, not guarantees; use `TARGETED_MULTIPASS_ENGINE`.
- **AIGC rate increased after revision**: the rewrite likely produced more formal/balanced text, lost report color targeting, or preserved a social-science template skeleton. Apply `AIGC_REGRESSION_GUARD` before another rewrite.

## 4. Mode Router

### AIGC Revision Family

| Mode | Use When | Load |
|---|---|---|
| `AIGC_ONLY` | User asks only to reduce AIGC style risk. | `prompts/mode_aigc_only.md`, `references/aigc_pattern_library.md` |
| `AIGC_DEEP_REWRITE_ENGINE` | Shallow wording changes are not enough. | `prompts/mode_aigc_deep_rewrite.md`, `references/aigc_deep_rewrite_engine.md` |
| `BURSTINESS_INJECTION` | Any AIGC revision needs rhythm audit; apply rhythm repair only when uniformity is a real risk. | `references/burstiness_injection_rules.md` |
| `FIRST_PASS_RED_ORANGE_ENGINE` | Original AIGC report is available before first revision. | `prompts/mode_first_pass_red_orange.md`, `references/first_pass_red_orange_engine.md` |
| `AIGC_PLATEAU_BREAKER` | Multiple rounds plateau, especially red down but orange remains high. | `prompts/mode_aigc_plateau_breaker.md`, `references/aigc_plateau_breaker.md` |
| `AIGC_FOCUSED_LENGTH_CONTROLLED` | Similarity is acceptable and AIGC remains the main issue. | `prompts/mode_aigc_focused_length_controlled.md`, `references/aigc_focused_length_controlled_engine.md` |

Supporting AIGC references:

- `references/burstiness_injection_rules.md` — rhythm audit and controlled burstiness repair for AIGC modes
- `references/orange_zone_rewrite_strategy.md`
- `references/discipline_aigc_bottleneck_rules.md`
- `references/aigc_focused_rewrite_strategy.md`
- `references/sentence_level_aigc_localizer.md`
- `references/burstiness_rhythm_control.md`
- `references/repeated_expression_compressor.md`
- `references/human_evidence_request.md`
- `references/conservative_aigc_repair.md`
- `references/aigc_regression_guard.md`
- `references/aigc_below_20_strategy.md`
- `references/anti_shallow_rewrite_rules.md`
- `references/post_rewrite_aigc_self_audit.md`
- `references/social_science_template_bottleneck.md`
- `prompts/mode_second_pass_rewrite.md`
- `prompts/mode_social_science_aigc_bottleneck.md`

Mode aliases: `ORANGE_ZONE_REWRITE_STRATEGY`, `DISCIPLINE_AIGC_BOTTLENECK_RULES`, `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`, `SENTENCE_LEVEL_AIGC_LOCALIZER`, `BURSTINESS_RHYTHM_CONTROL`, `BURSTINESS_INJECTION`, `REPEATED_EXPRESSION_COMPRESSOR`, `HUMAN_EVIDENCE_REQUEST`, `CONSERVATIVE_AIGC_REPAIR`, `AIGC_REGRESSION_GUARD`, `AIGC_BELOW_20_STRATEGY`, `POST_REWRITE_AIGC_SELF_AUDIT`, `SECOND_PASS_REWRITE_REQUIREMENT`.

### Similarity And Dual Optimization Family

| Mode | Use When | Load |
|---|---|---|
| `THREE_MODE_COLOR_BAND_WORKFLOW` | Default workflow for similarity-only, AIGC-only, and dual revision. | `prompts/mode_three_mode_color_band.md`, `references/three_mode_color_band_workflow.md` |
| `SIMILARITY_ONLY` | User asks only to revise similarity-risk expression. | `prompts/mode_similarity_only.md`, `references/similarity_reduction_strategy.md` |
| `DUAL_OPTIMIZATION` | AIGC and similarity risks both matter. | `prompts/mode_dual_optimization.md`, `references/dual_optimization_arbitration.md` |
| `NO_REPORT_FALLBACK_WORKFLOW` | User has no report and needs heuristic fallback. | `prompts/mode_no_report_dual_fallback.md`, `references/no_report_fallback_workflow.md` |
| `TARGETED_MULTIPASS_ENGINE` | User provides goals, reports, or historical drafts. | `prompts/mode_targeted_multipass.md`, `references/targeted_multipass_engine.md` |

Supporting references:

- `references/file_input_copy_workflow.md`
- `references/optimization_targets.md`
- `references/report_feedback_loop.md`
- `references/content_substance_injection.md`
- `references/similarity_below_10_strategy.md`
- `references/paragraph_type_strategies.md`
- `references/effectiveness_evaluation.md`
- `references/structure_rebuilding_rules.md`
- `references/evidence_trace_injection.md`
- `references/rewrite_intensity_l5.md`

Mode aliases: `FILE_INPUT_COPY_WORKFLOW`, `OPTIMIZATION_TARGETS`, `REPORT_FEEDBACK_LOOP`, `CONTENT_SUBSTANCE_INJECTION`, `SIMILARITY_BELOW_10_STRATEGY`, `PARAGRAPH_TYPE_STRATEGIES`.

### Report-Driven Family

| Mode | Use When | Load |
|---|---|---|
| `REPORT_DRIVEN_MODE` | User provides any AIGC or similarity report. | `references/report_parsing_workflow.md`, `references/report_to_source_mapping.md` |
| `REPORT_AIGC_ONLY` | User provides AIGC report fragments. | `prompts/mode_report_driven_aigc.md` |
| `REPORT_SIMILARITY_ONLY` | User provides similarity report fragments. | `prompts/mode_report_driven_similarity.md` |
| `REPORT_DUAL_OPTIMIZATION` | Reports show overlapping AIGC and similarity risk. | `prompts/mode_report_driven_dual.md`, `references/report_driven_priority_rules.md` |
| `REPORT_TO_SOURCE_MAPPING` | User only wants report-to-source alignment. | `prompts/mode_report_mapping_only.md`, `references/mapping_confidence_rules.md` |

Supporting references:

- `references/docx_color_report_extraction.md`
- `references/report_input_types.md`
- `references/similarity_source_handling.md`
- `references/report_safety_and_integrity.md`
- `references/report_driven_multi_pass_workflow.md`
- `prompts/mode_report_driven_multi_pass.md`

Mode aliases: `REPORT_DRIVEN_MULTI_PASS_WORKFLOW`, `DOCX_COLOR_REPORT_EXTRACTION`, `SIMILARITY_SOURCE_HANDLING`, `REPORT_PRIORITY_QUEUE`, `MAPPING_CONFIDENCE_LEVEL`.

### Diagnosis And Guard Family

| Mode | Use When | Load |
|---|---|---|
| `INTAKE_WIZARD` | User wants to start but goal, input, report, scope, or output is unclear. | `prompts/mode_intake_wizard.md`, `references/intake_wizard.md` |
| `AUTO_DIAGNOSIS` | User provides text without a mode. | `references/scoring_framework.md`, `references/chapter_strategies.md` |
| `SCORING_DIAGNOSIS_MODE` | User wants diagnosis before rewriting. | `prompts/mode_scoring_diagnosis.md` |
| `SENTENCE_LEVEL_DIAGNOSIS_MODE` | User wants sentence-level risk localization. | `prompts/mode_sentence_level_revision.md`, `references/sentence_level_diagnosis.md` |
| `BEFORE_AFTER_SCORE_COMPARISON` | User wants before/after heuristic score comparison. | `references/scoring_framework.md` |
| `RISK_HEATMAP_TABLE` | User wants risk hot-zone ranking. | `prompts/mode_risk_heatmap.md` |
| `CHARACTER_DELTA_GUARD` | Whole-thesis character change must be controlled. | `references/character_delta_guard.md`, `references/length_budget_controller.md` |
| `LENGTH_BUDGET_CONTROLLER` | User needs expansion/compression control. | `prompts/mode_length_compression_pass.md`, `references/length_budget_controller.md` |

Supporting references:

- `references/risk_labels.md`
- `references/no_edit_zone_rules.md`
- `references/protected_terms_rules.md`
- `references/citation_integrity_rules.md`
- `references/long_context_consistency.md`
- `prompts/quality_checklist.md`

Mode aliases: `SAFE_NO_EDIT_ZONE`, `PROTECTED_TERMS_RULES`.

### Engineering And Full-Thesis Family

| Mode | Use When | Load |
|---|---|---|
| `ENGINEERING_SCIENCE_MODE` | Thesis contains formulas, code, APIs, tables, fields, or experiment data. | `prompts/mode_engineering_science.md`, `references/protected_terms_rules.md` |
| `FULL_THESIS_PROJECT_MODE` | User provides a complete thesis or long-running task. | `references/full_thesis_project_management.md`, `workflow/thesis_master_overview_template.md` |
| `CHAPTER_TASK_MODE` | Work should be split by chapter. | `references/chapter_task_rules.md`, `workflow/chapter_task_template.md` |
| `PROGRESS_TRACKING_MODE` | User asks for status or multi-round tracking. | `references/progress_tracking_rules.md`, `workflow/progress_tracker_template.md` |
| `REVISION_LOG_MODE` | User asks to record revision history. | `references/revision_log_rules.md`, `workflow/revision_log_template.md` |
| `ITERATIVE_REVISION_MODE` | New reports trigger second/third pass tasks. | `references/iterative_optimization_rules.md`, `workflow/iteration_plan_template.md` |
| `PROJECT_HANDOFF_MODE` | The project needs to pause or switch context. | `references/project_handoff_rules.md`, `workflow/project_handoff_template.md` |
| `SKILL_SLIM_MODE` | Maintainers need to keep Skill docs concise. | `references/skill_slimming_rules.md`, `prompts/mode_skill_slimming.md` |

Supporting files:

- `prompts/mode_general_academic.md`

## 5. Standard Output Blocks

Use only the blocks needed for the task.

### Diagnosis Table

| 位置 | 风险类型 | 建议模式 | 强度 | 保护项 | 处理理由 |
|---|---|---|---|---|---|

### Report-Driven Task Table

| 编号 | 原文章节 | 原文段落 | 报告片段 | 风险类型 | 贡献率/等级 | 映射置信度 | 建议模式 | 改写强度 | 是否保护 | 处理建议 |
|---|---|---|---|---|---|---|---|---|---|---|

### Red-Orange First-Pass Table

| 编号 | 原文章节 | 原文段落 | 风险带 | 是否首轮主处理 | 目标风险带 | 保护项 | 内部重试上限 | 字符变动策略 |
|---|---|---|---|---|---|---|---:|---|

### Color Reason Analysis Table

| 编号 | 模式 | 位置 | 报告颜色 | 疑似度区间 | 被标记原因 | 处理策略 | 是否保护 |
|---|---|---|---|---|---|---|---|

### Character Delta Table

| scope | original_chars | revised_chars | delta_chars | delta_ratio | allowed_range | status |
|---|---:|---:|---:|---:|---|---|

### File Writeback Table

| id | source_location | original_text | revised_text | mapping_confidence | writeback_status |
|---|---|---|---|---|---|

### Intake Decision

| item | selected_or_default | notes |
|---|---|---|

### Project Templates

- Thesis overview: `workflow/thesis_master_overview_template.md`
- Chapter task: `workflow/chapter_task_template.md`
- Progress tracker: `workflow/progress_tracker_template.md`
- Revision log: `workflow/revision_log_template.md`
- Iteration plan: `workflow/iteration_plan_template.md`
- Project handoff: `workflow/project_handoff_template.md`

## 6. File Layout

- `references/`: detailed rules and domain guidance.
- `prompts/`: executable mode prompts.
- `workflow/`: full-thesis project templates.
- `examples/`: format and behavior examples.
- `tests/`: manual validation checklists.
- `NOTICE` and `THIRD_PARTY_NOTICES.md`: upstream attribution and license notes.

## 7. Upstream Acknowledgements

This project is inspired by and respectfully acknowledges:

- `houlaisan/deai-academic-zh`
- `Yezery/aigc-down-skill`
- `zczjyq/de-AIGC-skill`
- `openclaw/humanize-chinese`
- `lengsukq/ParaphrasingToolClient`
- `Abnerla/AI_paper`
- `Haimbeau1o/thesis-optimizer`

Detailed attribution and license observations are maintained in `NOTICE` and `THIRD_PARTY_NOTICES.md`. This project reorganizes public workflow ideas for academic-integrity-first Chinese thesis optimization and does not copy upstream code, templates, or long-form text where licensing is unclear.
