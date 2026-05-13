# Prompt: NO_REPORT_FALLBACK_WORKFLOW

## Purpose

Use this mode when the user asks for dual optimization without a similarity or AIGC report.

## Workflow

1. State that no-report mode is heuristic and cannot promise actual detection changes.
2. Build chapter or paragraph structure.
3. Build protected list.
4. Score AIGC and similarity risk by paragraph.
5. Mark high-editability paragraphs.
6. Run first pass: structure rebuild and similarity fallback optimization.
7. Run second pass: AIGC deep self-audit and second rewrite if needed.
8. Recommend report-based follow-up for precise localization.

## Output

- Diagnosis table.
- High-editability target list.
- First-pass revision.
- AIGC self-audit.
- Second-pass revision if triggered.
- Remaining risk and report recommendation.

## Safety

Do not claim precise reduction without a report.
