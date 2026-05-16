# AIGC Deep Rewrite Engine

## Purpose

`AIGC_DEEP_REWRITE_ENGINE` reduces AIGC detection risk by making text **sound more human**, not more polished. AIGC detectors measure statistical fingerprints (perplexity, burstiness, structure patterns), not writing quality. A rewrite that produces smoother, more balanced, more abstract prose will **increase** AIGC rates.

The goal is to shift the text's statistical distribution from "AI-generated" to "human-written". This requires burstiness injection, rhythm disruption, specificity increase, and controlled imperfection — not synonym replacement or formal polishing.

**Early diagnostic read**: `references/burstiness_injection_rules.md` — run rhythm audit early, but do not keep adding short sentences when rhythm is already varied. For HR, management, education, and other social-science theses, template-skeleton repair and evidence-first reconstruction often matter more than sentence-length variation.

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

## Twelve Required Rewrite Actions

Priority order — rhythm audit and anti-formalization come first:

### Tier 1: Statistical Fingerprint Shift (highest impact)

1. **Run rhythm gate**.
   Apply `references/burstiness_injection_rules.md` to decide whether rhythm repair is actually needed. If sentence-length variation is already adequate and the paragraph remains red/orange, do not add more short sentences; switch to template-skeleton repair, evidence placement, or discipline-specific reconstruction.

2. **Delete connectors aggressively**.
   Remove "首先、其次、此外、因此、综上所述、与此同时". Replace with object relationships, conditions, or direct statements. Target: < 3 connectors per paragraph.

3. **Break mechanical structures**.
   Avoid stacked "首先、其次、最后" and "一是、二是、三是". Rebuild around business flow, experiment flow, or argument chain. Convert enumeration to flowing prose or process-stage grouping.

### Tier 2: Specificity and Evidence (medium impact)

4. **Delete empty significance sentences**.
   Remove "具有重要意义", "提供了参考", "奠定基础", "推动发展" when they add no evidence. Do not replace with other value claims — delete or redirect to a concrete detail.

5. **Introduce concrete thesis objects**.
   Use existing objects from the source text: system name, module name, algorithm, dataset, experiment object, interface, table name, department name, position name, survey data, or sample. Do not fabricate.

6. **Compress empty explanation**.
   For "提高效率", "增强稳定性", "优化体验": which module, which process, which operation, what evidence? If no evidence exists, delete the claim.

7. **Put evidence before evaluation**.
   Start from data, survey result, interview finding, or process observation. Then explain the issue. Do not lead with a generic claim and follow with data.

### Tier 3: Structure Disruption (supporting impact)

8. **Change sentence relationships**.
   Add real limitation, contrast, cause, condition, exception, boundary, weakness, or tradeoff when supported by the source.

9. **Rewrite conclusion sentences**.
   Delete "综上所述". End with the paragraph's concrete design, boundary, result, or next-step connection. Alternate between data-ending, limitation-ending, and transition-ending across paragraphs.

10. **Vary paragraph openings**.
    Do not start two consecutive paragraphs with the same pattern. Alternate between data-point opening, process-node opening, contrast opening, and direct-object opening.

### Tier 4: Anti-Regression (guard)

11. **Prevent formalization regression**.
    Do NOT replace common words with more formal, abstract, or "academic-sounding" alternatives. Do NOT add abstract nouns (体系, 机制, 路径, 维度, 价值, 能力, 保障) without concrete anchors. If the rewrite sounds more polished than the original, it has failed.

12. **Preserve controlled imperfection**.
    Allow incomplete sentences, varied paragraph lengths, and asymmetric argument structures. Do not make every sentence equally complete and balanced. The goal is human-like academic writing, not perfect AI-generated prose.

## v0.8 Anti-Formalization Requirements

Deep rewriting must NOT make text sound more polished, more balanced, or more "academic". A rewrite that increases formality will increase AIGC detection rates.

Mandatory rules:

- Do not replace common expressions with grander abstract phrases just to look academic.
- Do not output pure polishing as deep rewriting.
- Deep rewriting must increase specificity, not abstraction.
- Each high-risk paragraph should introduce at least one concrete object or boundary from the available source.
- If information is insufficient, output `建议作者补充：...` instead of inventing modules, data, interfaces, test results, or limitations.
- Prefer module names, parameters, input/output relations, local test environments, result values, and supported limitations over words such as "体系", "机制", "价值", or "能力".
- If the rewritten text reads smoother, more balanced, or more formal than the original, it is a FAILED rewrite. Diagnose whether the problem is rhythm, report-color targeting, template skeleton, or evidence placement before retrying.
- Deliberately introduce controlled imperfection: vary sentence completeness, allow asymmetric argument structures, use short punchy sentences between longer explanations.
- For management and HR theses, do not turn paragraphs into slogan-like short sentences. Keep formal thesis tone while disrupting repeated templates.

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
