# Chapter Strategies

Different thesis chapters need different risk strategies.

For full-thesis projects, convert each chapter strategy into a `CHAPTER_TASK_MODE` task using `workflow/chapter_task_template.md`. Do not revise the whole thesis before chapter tasks are created.

## Abstract

Risk:

- Formulaic structure.
- Over-condensed claims.
- Broad value statements.

Strategy:

- Use L1-L2.
- Preserve research object, method, data, and conclusion.
- Do not add missing results.
- Remove empty value language.

## Introduction

Risk:

- Generic background.
- Repeated "importance" claims.
- Weak research gap.

Strategy:

- Compress broad context.
- Move quickly to the local problem.
- Make the research gap specific.
- Keep citations for background claims.

## Literature Review

Risk:

- Similar source summaries.
- Blended citation boundaries.
- Mechanical author-by-author listing.

Strategy:

- Group studies by method, object, data, or limitation.
- Keep source identities visible.
- Avoid turning cited views into uncited claims.

## Theoretical Basis

Risk:

- Textbook-like definitions.
- Long concept explanation disconnected from the thesis.

Strategy:

- Keep only the parts needed by later analysis.
- Explain how the thesis uses the concept.
- Preserve standard definitions and citations where necessary.

## Method Research

Risk:

- Formula explanation becomes vague after rewriting.
- Variables or assumptions are changed accidentally.

Strategy:

- Protect formulas and variables first.
- Rewrite explanatory prose around derivation logic.
- Keep assumptions and applicability conditions.

## System Design

Risk:

- Generic module descriptions.
- Interface and table names accidentally changed.

Strategy:

- Preserve module, interface, table, and field names.
- Connect design choices to data flow and constraints.
- Do not invent modules or implementation details.

## Experiment Analysis

Risk:

- Data interpretation becomes overgeneralized.
- Chart and table references are lost.

Strategy:

- Preserve numbers, conditions, chart references, and metrics.
- Explain mechanism only when evidence supports it.
- Add limitations if already implied by the result.

## Conclusion and Outlook

Risk:

- Generic achievement summary.
- Unsupported future claims.

Strategy:

- List completed work based on actual chapters.
- Keep real limitations.
- Avoid broad future promises.

## Project-Level Use

When operating in `FULL_THESIS_PROJECT_MODE`:

- Add each chapter to `THESIS_MASTER_OVERVIEW`.
- Assign a status from `references/progress_tracking_rules.md`.
- Mark high-risk, high-impact, safely editable chapters first.
- Move citation-heavy, formula-heavy, or experiment-data-heavy chapters into human review if needed.
- Update progress and revision logs after each chapter-level action.
