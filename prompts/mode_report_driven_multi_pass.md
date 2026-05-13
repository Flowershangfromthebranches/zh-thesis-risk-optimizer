# Prompt: REPORT_DRIVEN_MULTI_PASS_WORKFLOW

## Purpose

Use this mode when the user provides a report and asks for stronger dual optimization.

## Workflow

1. Round 0: map report fragments to source text and mark confidence.
2. Round 1: handle high-contribution similarity fragments while preserving citations.
3. Round 2: run AIGC deep rewrite on revised target paragraphs.
4. Round 3: inject existing evidence and run AIGC regression guard.
5. Round 4: review terms, citations, formulas, data, conclusions, and report trend state.
6. Round 5: suggest recheck and local follow-up from a new report.

## Output

- Mapping table.
- Round 1 similarity revision.
- Round 2 AIGC deep rewrite.
- Evidence reconstruction.
- Regression audit.
- Safety review.
- Recheck advice.

## Safety

Do not invent report fields or claim a future report result.
