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
