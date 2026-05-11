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

## Risk Type 2: Textbook-Like Explanation

Symptoms:

- A paragraph teaches general knowledge.
- It could appear unchanged in many papers.

Strategy:

- Compress general background.
- Keep only concepts needed for the following method or analysis.
- Connect explanation to dataset, method, system, chapter problem, or research question.

## Risk Type 3: Generic Background

Symptoms:

- Long claims about industry value, social value, development trend, or broad importance.
- Little relation to the paper's actual method.

Strategy:

- Replace broad claims with the concrete research gap.
- Move from macro background to the local problem.
- Delete repeated motivational sentences.

## Risk Type 4: Source-Close Expression

Symptoms:

- Sentence order, examples, and key terms follow a source too closely.
- Synonym replacement was used but structure remains similar.

Strategy:

- Rebuild the argument order.
- Change the paragraph function: definition -> application, source comparison -> limitation, background -> research gap.
- Preserve citation boundaries.

## Risk Type 5: Citation Boundary Risk

Symptoms:

- A claim depends on another author but no citation remains after rewriting.
- Several sources are blended into one unsourced statement.

Strategy:

- Keep the original citation.
- If the citation is missing, mark "建议补充来源".
- Separate the author's own analysis from cited claims.

## Risk Type 6: Literature Review Stack

Symptoms:

- Multiple papers are summarized with the same sentence pattern.
- Differences between sources disappear.

Strategy:

- Group sources by method, object, data, or conclusion.
- Keep author/source identities visible.
- Add comparison words only when supported by the source.

## Mode Selection

- Use SIMILARITY_ONLY when expression is source-close but not mechanically written.
- Use AIGC_ONLY when the paragraph is original but template-like.
- Use DUAL_OPTIMIZATION when both risks appear.
- Recommend no modification when the paragraph is precise, cited, and technically constrained.
