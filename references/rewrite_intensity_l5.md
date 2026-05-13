# Rewrite Intensity L1-L5

## Purpose

This file upgrades rewrite intensity from L1-L4 to L1-L5 and clarifies when deep rewriting is allowed.

## L1: Light Cleanup

- Adjust connectors.
- Remove small amounts of empty wording.
- Do not change paragraph structure.

## L2: Moderate Paraphrase

- Change sentence form.
- Adjust limited word order.
- Suitable for low to medium similarity risk.

## L3: Structural Reorganization

- Change internal paragraph order.
- Merge or split sentences.
- Suitable for high AIGC risk or medium-high similarity risk.

## L4: Argument Rebuilding

- Change the argument angle.
- Reorganize from concrete problem, process, or result.
- Suitable for high AIGC-risk paragraphs.

## L5: Rewrite Rebuild

Use only for high-risk, non-protected, non-citation-heavy paragraphs.

Requirements:

- Preserve facts, data, terms, and conclusions.
- Rebuild the whole paragraph expression.
- Output preserved fact list.
- Output no-change list.
- Do not fabricate.
- Increase evidence density using provided facts.
- Run AIGC regression guard before accepting the final version.

Do not use L5 to produce smoother but more abstract prose. If the paragraph lacks enough evidence for L5, ask the author to supplement evidence instead of inventing it.

## Relation To SKILL.md

Used by AIGC deep rewrite, dual optimization, and second-pass rewrite.
