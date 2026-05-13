# No Report Fallback Workflow

## Purpose

`NO_REPORT_FALLBACK_WORKFLOW` improves dual optimization when the user has not provided a similarity or AIGC report.

## Boundary

No-report mode is heuristic. It cannot promise actual detection changes and should recommend report-based localization for precise follow-up.

## Required Workflow

1. Build chapter structure.
2. Build protected list.
3. Self-score AIGC risk by paragraph.
4. Self-score similarity risk by paragraph.
5. Mark highly editable paragraphs.
6. Prioritize:
   - Introduction background padding.
   - Theoretical definition repetition.
   - Generalized conclusion endings.
   - Literature review stacking.
   - Empty system-design advantage sentences.
7. Do not prioritize:
   - Formula-heavy paragraphs.
   - Experiment-data paragraphs.
   - Code/interface/field paragraphs.
   - Citation-heavy paragraphs.
8. Output diagnosis table first.
9. Revise only after user confirmation or clear task scope.
10. State that no-report mode cannot guarantee actual detection changes.

## Mandatory Two Passes

First pass:

- Structure rebuilding.
- Similarity-expression fallback optimization.

Second pass:

- AIGC deep self-audit.
- Second-pass rewrite when needed.

## Relation To SKILL.md

Routed from no-report dual optimization and complete-thesis workflows.
