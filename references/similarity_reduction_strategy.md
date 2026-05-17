# Similarity Reduction Strategy

Similarity-risk optimization must preserve citation integrity. The goal is clearer and more original expression around the author's real research, not hiding source dependence.

## Risk Type 1: High-Repeat Definition

Symptoms:

- Concept definitions are close to textbooks, standards, or encyclopedic wording.
- The paragraph explains a term without saying how this thesis uses it.

Strategy:

- Keep necessary technical accuracy.
- Shift from universal definition to thesis-specific usage.
- Add scope, boundary, or analytical role already present in the thesis.
- Keep citation if the definition comes from a source.

Labels:

- `查重-定义重复`
- `查重-概念解释冗余`
- `保护-经典定义` when the definition should not be freely rewritten.

## Risk Type 2: Textbook-Like Explanation

Symptoms:

- A paragraph teaches general knowledge.
- It could appear unchanged in many papers.

Strategy:

- Compress general background.
- Keep only concepts needed for the following method or analysis.
- Connect explanation to dataset, method, system, chapter problem, or research question.

Labels:

- `查重-教材式表述`
- `查重-背景套话`

## Risk Type 3: Generic Background

Symptoms:

- Long claims about industry value, social value, development trend, or broad importance.
- Little relation to the paper's actual method.

Strategy:

- Replace broad claims with the concrete research gap.
- Move from macro background to the local problem.
- Delete repeated motivational sentences.

Labels:

- `查重-背景套话`
- `AI-宣传式表达`

## Risk Type 4: Source-Close Expression

Symptoms:

- Sentence order, examples, and key terms follow a source too closely.
- Synonym replacement was used but structure remains similar.

Strategy:

- Rebuild the argument order.
- Change the paragraph function: definition -> application, source comparison -> limitation, background -> research gap.
- Preserve citation boundaries.

Labels:

- `查重-相似源过近`
- `查重-来源边界不清` when attribution is weak.

## Risk Type 5: Citation Boundary Risk

Symptoms:

- A claim depends on another author but no citation remains after rewriting.
- Several sources are blended into one unsourced statement.

Strategy:

- Keep the original citation.
- If the citation is missing, mark "建议补充来源".
- Separate the author's own analysis from cited claims.

Labels:

- `查重-引用转述不足`
- `查重-来源边界不清`
- `保护-必要引用`

## Risk Type 6: Literature Review Stack

Symptoms:

- Multiple papers are summarized with the same sentence pattern.
- Differences between sources disappear.

Strategy:

- Group sources by method, object, data, or conclusion.
- Keep author/source identities visible.
- Add comparison words only when supported by the source.

Labels:

- `查重-综述堆叠`
- `查重-引用转述不足`

## Risk Type 7: No-Edit Similarity Zone

Symptoms:

- Text is a law, standard, policy clause, classic definition, formula, report excerpt, or required direct quotation.
- Similarity may be high because the wording is intentionally fixed.

Strategy:

- Preserve the original text.
- Mark the reason.
- Ask for human confirmation before any change.
- Only revise the explanatory prose before and after the protected material.

Labels:

- `保护-法规标准原文`
- `保护-经典定义`
- `保护-必要引用`

## Scoring Signals

When running similarity-risk scoring, treat these signals as heuristic features:

- Definition repetition.
- Textbook-like background expression.
- Source-close wording.
- Citation-heavy but under-paraphrased text.
- Repeated common concept explanation.
- Legal, standard, and classic definition zones that should be protected.
- Dense professional terminology that should not be misread as a rewrite target.

## Internal Task-Type Selection

- Use `task_type = similarity_only` inside `THREE_MODE_COLOR_BAND_WORKFLOW` when expression is source-close but not mechanically written.
- Use `task_type = aigc_only` inside `THREE_MODE_COLOR_BAND_WORKFLOW` when the paragraph is original but template-like.
- Use `task_type = dual_optimization` inside `THREE_MODE_COLOR_BAND_WORKFLOW` when both risks appear, then run `AIGC_REGRESSION_GUARD` after similarity repair.
- Recommend no modification when the paragraph is precise, cited, and technically constrained.

## Report-Driven Similarity Handling

When a similarity report is provided:

1. Extract marked fragments, source notes, contribution rates, and risk levels from the user-provided report text.
2. Map each report fragment back to the thesis source text.
3. Assign mapping confidence before making any revision decision.
4. Classify the source type: citation-caused, definition-caused, textbook-like, source-close, literature-review stacking, dense self-citation, or protected no-edit content.
5. Preserve necessary citations even if they contribute to similarity.
6. For LOW or UNMAPPED mappings, request source context before rewriting.

Do not invent report percentages, source names, URLs, or risk levels.

## Dual-Optimization Follow-Up

Similarity repair can accidentally create smoother, more template-like prose. In dual mode:

1. Repair source-close expression first.
2. Preserve citations and source boundaries.
3. Run `references/post_rewrite_aigc_self_audit.md`.
4. If the audit still finds three or more AI-like risks, use `prompts/mode_second_pass_rewrite.md`.
