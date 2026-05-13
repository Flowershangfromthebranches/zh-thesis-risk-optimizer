# Conservative AIGC Repair

## Purpose

Use this mode when information is insufficient but AIGC risk still needs local reduction.

## Principles

- Do not add unsupported information.
- Do not expand heavily.
- Do not delete core content.
- Do not use grand abstract words.
- Reorder existing facts.
- Delete or replace empty value claims.
- Keep length close to the original.

## Applicable Sections

- Abstract.
- Introduction.
- Research significance.
- Technology overview.
- Conclusion.

## Not Applicable

- Paragraphs that need new experiment explanation.
- Paragraphs that need the author to provide real process details.
- Paragraphs where a report clearly requires large restructuring.

## Conservative Actions

- Replace template opening with an existing thesis object.
- Compress background.
- Remove generic value ending.
- Keep protected facts and citations.
- Prefer `REPLACE_WITH_SAME_LENGTH` or `COMPRESS`.

## Relation To SKILL.md

Use this file when `HUMAN_EVIDENCE_REQUEST` is triggered but the user asks for a safe interim revision.
