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
