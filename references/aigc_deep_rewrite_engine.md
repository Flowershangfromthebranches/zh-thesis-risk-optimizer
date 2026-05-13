# AIGC Deep Rewrite Engine

## Purpose

`AIGC_DEEP_REWRITE_ENGINE` improves AIGC-risk reduction by rebuilding paragraph structure, information density, sentence relationships, and rhythm. It is not synonym replacement.

## When To Use

- AIGC risk remains high after basic revision.
- Paragraphs still sound template-like, smooth, or mechanically balanced.
- Dual optimization needs a second pass after similarity-risk handling.
- No-report fallback needs stronger AIGC self-revision.

## Inputs

- Original thesis paragraph.
- Protected facts, citations, terms, formulas, code, interfaces, tables, fields, data, and conclusions.
- Optional report-mapped risk fragments.

## Outputs

- Deep rewritten paragraph.
- Preserved fact list.
- No-change list.
- AIGC self-audit result.
- Need for second-pass rewrite if risk remains.

## Ten Required Rewrite Actions

1. Delete empty significance sentences.
   Remove or rewrite generic sentences such as "具有重要意义", "提供了参考", "奠定基础", "推动发展" when they do not add evidence.

2. Break mechanical three-part structures.
   Avoid stacked "首先、其次、最后". Rebuild around business flow, experiment flow, or argument chain.

3. Introduce concrete thesis objects.
   Use existing objects from the source text, such as system name, module name, algorithm, dataset, experiment object, interface, table, test scenario, or sample. Do not fabricate.

4. Change sentence relationships.
   Add real limitation, contrast, cause, condition, exception, boundary, weakness, or tradeoff when supported by the source.

5. Add research or implementation trace.
   Use existing information to explain why a design was chosen, what problem it handled, where it applies, what remains limited, or how results support the conclusion.

6. Reduce over-smoothness.
   Avoid making every sentence equally complete and balanced. Use varied sentence length while keeping academic tone.

7. Compress empty explanation.
   For phrases like "提高效率", "增强稳定性", or "优化体验", ask: which module, which process, which operation, and what evidence supports it?

8. Rewrite conclusion sentences.
   Avoid default endings such as "综上所述". End with the paragraph's concrete design, boundary, result, or next-step connection.

9. Preserve necessary imperfection.
   For system, method, or experiment text, keep supported limitation phrases such as "在当前测试条件下" or "该处理方式主要面向...". Do not invent limitations.

10. Reorganize meaning, not words.
    At least one of sentence structure, information order, or argument angle must change. Replacing "通过" with "借助" is not enough.

## v0.6 Specificity Requirements

Deep rewriting must not turn ordinary wording into more abstract, high-register prose. A paragraph that becomes smoother but loses concrete objects is a failed rewrite.

Mandatory rules:

- Do not replace common expressions with grander abstract phrases just to look academic.
- Do not output pure polishing as deep rewriting.
- Deep rewriting must increase specificity.
- Each high-risk paragraph should introduce at least one concrete object or boundary from the available source.
- If information is insufficient, output `建议作者补充：...` instead of inventing modules, data, interfaces, test results, or limitations.
- Prefer module names, parameters, input/output relations, local test environments, result values, and supported limitations over words such as "体系", "机制", "价值", or "能力".

## v0.7 Length-Controlled AIGC Rules

- AIGC deep rewriting is not expansion.
- Prefer replacing high-risk sentences instead of appending explanations after them.
- If similarity is already acceptable, do not continue high-intensity similarity restructuring.
- High-AIGC paragraphs must run sentence-level localization before L4/L5 rewriting.
- Process at most 1-3 key sentences per paragraph when possible.
- The length budget outranks nonessential detail supplementation.
- The main AIGC-reduction methods are structure, rhythm, evidence density, and template removal, not simply adding content.
- If an AIGC repair needs evidence that is not present, use `HUMAN_EVIDENCE_REQUEST` or `CONSERVATIVE_AIGC_REPAIR`.

## Safety Boundaries

- Do not fabricate data, experiments, modules, interfaces, roles, test results, references, failures, or limitations.
- Do not remove necessary citations.
- Do not change formulas, code, table names, field names, parameters, or conclusions.
- If needed detail is missing, write "此处建议作者补充：..." instead of inventing it.

## Relation To SKILL.md

`SKILL.md` routes AIGC-heavy paragraphs to this reference through `AIGC_DEEP_REWRITE_ENGINE`.
