# Prompt: Quality Checklist

Use this checklist before final output.

## Mandatory Integrity Checks

- [ ] No fabricated data.
- [ ] No fabricated experiments.
- [ ] No fabricated citations.
- [ ] No altered conclusions.
- [ ] No deleted necessary citations.
- [ ] No damaged technical terms.
- [ ] No accidental changes to formulas, code, interfaces, table names, field names, or parameters.
- [ ] No promised detection outcome.
- [ ] No score is presented as a real commercial detection result.
- [ ] No forged report content, percentages, source names, or risk levels.
- [ ] No commercial detection-system cracking or reverse-engineering workflow.

## Scoring Checks

- [ ] Scores are explicitly described as heuristic writing-risk scores.
- [ ] The output does not claim equivalence to 知网、维普、万方、Turnitin or other commercial systems.
- [ ] AIGC risk, similarity risk, and dual-optimization priority are separated.
- [ ] Before/after scores are phrased as diagnostic estimates, not guaranteed results.
- [ ] Risk heatmap ranking does not override citation or technical protection.

## Sentence-Level Checks

- [ ] Each analyzed sentence has risk labels or a clear no-risk note.
- [ ] Protection labels are applied to formulas, code, citations, experiment data, and technical identifiers.
- [ ] The output separates可改写句、轻改句、不建议改写句、需要保留引用句、涉及术语/公式/代码保护句.
- [ ] No-edit zones are preserved unless the user explicitly asks for a targeted change.

## AIGC-Risk Checks

- [ ] Template openings were replaced or localized.
- [ ] Mechanical three-part structures were reduced.
- [ ] Overly symmetric sentence structures were varied.
- [ ] Empty positive endings were removed or made evidence-based.
- [ ] Vague attribution was replaced with citation reminders or concrete source boundaries.
- [ ] Sentence rhythm varies naturally without becoming casual.
- [ ] The rewrite is not only synonym replacement, connector replacement, or word-order shuffling.
- [ ] High-risk AIGC paragraphs changed at least two of: information order, sentence relationship, concrete object density, generic conclusion, supported boundary.
- [ ] L3-L5 rewrites include preserved facts and no-change items where needed.
- [ ] Post-rewrite AIGC self-audit was performed for substantial rewrites.
- [ ] If three or more AI-risk items remain, second-pass rewrite was triggered.

## v0.6 Targeted Multipass Checks

- [ ] User targets are treated as optimization goals, not guaranteed detection results.
- [ ] The output checks whether the draft is moving toward the user targets.
- [ ] The output flags cases where similarity improved but AIGC worsened.
- [ ] Formalization regression was checked.
- [ ] Evidence density increased where source evidence exists.
- [ ] Citations and technical details were preserved.
- [ ] A next-pass task table exists when targets are not reached.
- [ ] Protected areas are clearly marked.
- [ ] Missing evidence is listed as author supplementation instead of being fabricated.

## v0.7 AIGC-Focused Length-Control Checks

- [ ] Similarity is not still being aggressively reduced after it is already acceptable.
- [ ] Whole-thesis growth stays within the user's budget, default 0-2000 Chinese characters.
- [ ] AIGC repair uses replacement-based reconstruction instead of appending explanations.
- [ ] Not every paragraph is expanded.
- [ ] A length budget table is included for whole-thesis or multi-chapter work.
- [ ] Sentence-level AIGC localization was performed before high-risk paragraph rewriting.
- [ ] Repeated AI-like expressions were compressed or replaced.
- [ ] Technical facts, protected tokens, and citations were preserved.
- [ ] Missing evidence is listed for the author when needed.
- [ ] Formalization regression phrases such as "持续演进", "深度嵌入", "赋能", "支撑", "机制", "体系", and "价值" are avoided unless technically necessary.

## v0.8 AIGC Plateau Breaker Checks

- [ ] Multi-round AIGC reports were compared before another rewrite.
- [ ] Red/high-risk reduction was not treated as completion when orange/medium risk remained high.
- [ ] White/low-risk paragraphs were frozen.
- [ ] Orange/medium-risk paragraphs were treated as primary targets, not minor cleanup.
- [ ] Persistent orange paragraphs changed structure, evidence placement, or paragraph rhythm, not only wording.
- [ ] Enumerated "第一、第二、第三" structures were broken or justified when they caused standard-answer rhythm.
- [ ] Discipline plateau type was identified: technical protected, management template, evidence limited, or report-model floor.
- [ ] Computer-science protected tokens were preserved exactly.
- [ ] Repeated no-progress paragraphs were marked `NO_PROGRESS_REWRITE_LOOP` instead of being rewritten with the same strategy.

## v0.8.1 Red-Orange First-Pass Checks

- [ ] Original thesis plus original AIGC report routes to `FIRST_PASS_RED_ORANGE_ENGINE`.
- [ ] Red/high-risk and orange/medium-risk fragments both appear in the first-pass primary task table.
- [ ] Orange/medium-risk fragments are not deferred until plateau mode.
- [ ] Purple/light-risk fragments are only local cleanup unless clearly connected to red/orange risks.
- [ ] Black/white/low-risk paragraphs are frozen.
- [ ] Internal rewrite loops have a fixed retry limit and use different repair moves.
- [ ] The heuristic target is purple/black-like when safe, not merely red-to-orange demotion.
- [ ] Whole-thesis character change is within `±10%` unless the user specified another range.
- [ ] `CHARACTER_DELTA_FAIL` triggers compression before completion.
- [ ] Protected or evidence-limited paragraphs stop with a reason instead of being recursively rewritten.

## v0.8.3 Three-Mode File Workflow Checks

- [ ] The task is routed to similarity-only, AIGC-only, or dual revision.
- [ ] AIGC-only + DOCX AIGC color report + red/orange/purple/black rules + character control routes to `THREE_MODE_COLOR_BAND_WORKFLOW`, not plain `AIGC_ONLY`.
- [ ] A revised/current draft plus current AIGC report routes to `CURRENT_REPORT_RED_ORANGE_ENGINE`, not `FIRST_PASS_RED_ORANGE_ENGINE`.
- [ ] If a relevant report is provided, report-driven processing is used.
- [ ] If no report is provided, the output states that report-based localization would be better.
- [ ] Color legend is applied correctly: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%, unless the report says otherwise.
- [ ] Red and orange are primary targets.
- [ ] Current-report red and orange paragraphs are all included in the task table.
- [ ] Purple is only light cleanup.
- [ ] Black, gray, and white text are frozen unless needed for context.
- [ ] Every red/orange fragment includes a reason analysis for its color.
- [ ] Red-orange coverage acceptance table is output.
- [ ] Each red/orange paragraph has a processing record.
- [ ] Unprocessed red/orange count is zero before completion.
- [ ] Whole-thesis character delta stays within `±10%` unless the user specified another range.
- [ ] File input creates a copy and keeps the original untouched.
- [ ] Revisions are written back only to HIGH or safe MEDIUM confidence mappings.
- [ ] LOW or UNMAPPED file fragments are not written back automatically.

## v0.8.4 Social-Science Template Bottleneck Checks

- [ ] HR, management, marketing, education, public administration, accounting, tourism, logistics, or similar applied-social-science thesis is routed to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` when template plateau appears.
- [ ] For HR, business administration, marketing, education management, and public administration, `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` is treated as a hard rule during report-driven red/orange work.
- [ ] The output identifies repeated "status -> problem -> cause -> countermeasure -> guarantee" skeletons.
- [ ] Generic countermeasure lists are not only polished into smoother language.
- [ ] Rewrites do not only say 构建体系, 提升效率, 优化流程, 强化能力, 丰富渠道, 数据驱动, 智能高效, or 提供参考.
- [ ] Current situation, problem, countermeasure, and conclusion paragraphs are grounded in company, post, process, form, system, indicator, responsibility, review-cycle, questionnaire, interview, or boundary evidence when available.
- [ ] Available organization, survey, interview, process, department, post,制度, indicator, or case evidence is used before evaluation.
- [ ] Missing evidence triggers author questions instead of invented details.
- [ ] Policy, theory, citation, questionnaire, and data boundaries are preserved.

## AIGC Acceptance Self-Audit Checks

- [ ] Every current-report red/orange paragraph ran `AIGC_ACCEPTANCE_SELF_AUDIT`.
- [ ] The audit checks synonym-only rewriting.
- [ ] The audit checks "definition + meaning + countermeasure" templates.
- [ ] The audit checks mechanical "一是、二是、三是、四是" enumeration.
- [ ] The audit checks abstract noun density.
- [ ] The audit checks missing company/local context.
- [ ] The audit checks missing questionnaire, interview, process, post, indicator, responsibility, review-cycle, or boundary evidence when needed.
- [ ] The audit checks whether the rewrite became smoother, more formal, or more AI-like.
- [ ] Any failed audit item triggers second-pass rewrite.
- [ ] Second-pass failure outputs an author evidence request and is not marked complete.

## v0.8.5 Intake Wizard Checks

- [ ] `INTAKE_WIZARD_PRECHECK` runs whenever the task is routed to this Skill.
- [ ] `INTAKE_WIZARD` is used when goal, input type, report availability, scope, output format, or protection rules are unclear after precheck.
- [ ] The wizard is skipped when enough context is already present.
- [ ] The wizard asks only for missing information.
- [ ] Options include "自动判断 / 其他补充".
- [ ] Defaults are visible: whole-thesis `±10%` character delta, default color legend, file-copy handling, and protected items.
- [ ] No rewrite starts before the required route and safety constraints are clear.
- [ ] No fabricated report facts, data, experiments, citations, interviews, case facts, or risk percentages are requested or invented.

## v0.9.2 Intake Precheck Template Checks

- [ ] The task starts with intake precheck even when the user does not explicitly say "use this Skill".
- [ ] First contact for a new task shows `workflow/intake_request_template.md` and waits for the user's intake reply.
- [ ] If a completed intake reply is already present, the output contains `Intake Confirmation` and proceeds to the selected mode.
- [ ] If only required information is present, the output still asks the user to fill, skip, or auto-judge strongly recommended and optional fields.
- [ ] Required, strongly recommended, and optional fields are clearly separated.
- [ ] The user is not asked to memorize the full mode router.
- [ ] The intake template includes character constraint and protected-item defaults.
- [ ] File input defaults to copy-based handling and does not modify the original file.
- [ ] The intake flow does not ask the user to invent reports, facts, data, citations, interviews, cases, or detection percentages.

## v0.8.6 DOCX Color Report And Social-Science Failure Checks

- [ ] Color-marked DOCX reports are parsed for color metadata before plain-text extraction.
- [ ] Raw DOCX color values are recorded and mapped only to the user's report legend or a clearly marked default.
- [ ] Red/orange task tables come from colored report spans, not from flattened plain text.
- [ ] If rhythm is already varied but AIGC risk remains high, the output switches to template-skeleton repair instead of adding more short sentences.
- [ ] HR, management, education, business, and public-administration theses are checked for document-level "现状 -> 问题 -> 原因 -> 对策 -> 保障" skeletons.
- [ ] Short-sentence burstiness does not become slogan-like or conversational.
- [ ] The output diagnoses upstream-style failures without blaming or misrepresenting upstream projects.

## Similarity-Risk Checks

- [ ] High-repeat definitions were converted into thesis-specific explanations.
- [ ] Textbook-like background was compressed.
- [ ] Source-close wording was restructured.
- [ ] Literature review still preserves author/source boundaries.
- [ ] Required citations remain visible.

## Long-Text Checks

- [ ] Terminology matches the protected list.
- [ ] Abbreviations are introduced once and used consistently.
- [ ] Rolling summaries are updated after each section.
- [ ] Later sections do not contradict earlier findings.
- [ ] Rewrite intensity is consistent across chapters unless intentionally varied.

## Report-Driven Checks

- [ ] Report facts are separated from heuristic diagnosis.
- [ ] Each report fragment has mapping confidence.
- [ ] LOW and UNMAPPED fragments are not directly rewritten.
- [ ] Multiple matches are listed instead of silently choosing one.
- [ ] Necessary citations remain visible.
- [ ] Similarity-source content is not turned into uncited original writing.

## Full-Thesis Project Checks

- [ ] Complete thesis work starts with a master overview.
- [ ] Chapter tasks exist before chapter revisions.
- [ ] Progress states are updated after each major step.
- [ ] Revision logs record mode, intensity, protected items, and human review items.
- [ ] Iterative revision targets residual risk only.
- [ ] Completed low-risk chapters are not repeatedly overhauled.
