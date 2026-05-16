# Burstiness and Rhythm Control

## Purpose

Use this file to audit and reduce overly smooth, overly uniform AIGC-like rhythm.

AIGC-high text is often not wrong at the sentence level. The problem is that the paragraph is too even, too complete, and too connector-driven.

**Primary reference**: `references/burstiness_injection_rules.md` contains the core injection techniques. This file focuses on audit and verification.

## 1. Sentence Length Variation

- Do not make every sentence in one paragraph a neat 25-35-character sentence.
- Mix short, medium, and longer sentences.
- Do not deliberately write ungrammatical sentences.

## 2. Connector Reduction

- Reduce mechanical connectors such as "首先", "其次", "此外", "因此", and "综上所述".
- Use object relationships instead of connector chains.

## 3. Local Detail Placement

- Do not put every concrete detail at the sentence end.
- Place details in the middle when they work as conditions or object descriptions.

## 4. Controlled Imperfection

- Allow natural variation in formal thesis prose.
- Do not make every sentence sound like a standard answer.
- Do not turn the thesis into conversational prose.

## 5. Rhythm Audit

For each paragraph, check:

- Is every sentence overly complete?
- Are there too many connectors?
- Is the paragraph still "background-problem-measure-significance"?
- Is there no short sentence?
- Do all sentences sound uniformly generated?

## 6. Orange-Zone Rhythm

When a paragraph stays in an orange/medium-risk band after multiple rounds, inspect paragraph rhythm before changing more words.

Common orange-zone rhythm problems:

- Every sentence follows "problem -> effect -> improvement".
- Each item in a list has the same grammatical length.
- Survey data or case evidence appears after a generic conclusion instead of shaping the sentence.
- Management or technical nouns repeat without local anchors.

Repair by changing the paragraph skeleton:

- Put one concrete observation before the general explanation.
- Merge duplicate list items.
- Split a long enumerated paragraph only when it clarifies the argument.
- Delete one generic value sentence before adding any new detail.

## Relation To SKILL.md

Use this file in AIGC-focused repair and sentence-level localization.
