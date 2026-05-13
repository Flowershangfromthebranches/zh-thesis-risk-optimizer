# Anti-Shallow Rewrite Rules

## Purpose

These rules reject ineffective revisions that only polish wording without reducing AIGC-style structure.

## Invalid Rewrites

The following are invalid when used alone:

1. Only replacing synonyms.
2. Only changing "通过" to "借助".
3. Only changing "使用" to "采用".
4. Only replacing "首先、其次、最后" with "第一、第二、第三".
5. Only adding vague modifiers such as "在一定程度上".
6. Only adding low-information hedges.
7. Only shuffling sentences while preserving the same logic.
8. Only changing active voice to passive voice.
9. Only deleting a few connectors.
10. Only turning formal prose into casual prose.

## Effective Rewrite Requirements

A valid rewrite must satisfy at least two:

- Change information order.
- Add concrete objects already present in the source.
- Delete empty significance sentences.
- Change sentence relationships.
- Add supported boundaries or limitations.
- Compress repeated definitions.
- Clarify the thesis-specific context.
- Replace generic conclusion with a concrete transition or boundary.

## Relation To SKILL.md

Used by all rewrite modes and mandatory post-rewrite audits.
