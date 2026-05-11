# Full Thesis Project Management

Use `FULL_THESIS_PROJECT_MODE` when the user provides a complete thesis, multiple chapters, or a long-running revision project.

## 1. Input Confirmation

Supported inputs:

- Complete thesis text.
- Chaptered thesis text.
- Word-copied text.
- LaTeX source.
- Similarity report.
- AIGC report.
- Marked fragments only.

If the input is incomplete, record what is available and what is missing. Do not invent missing chapters, reports, percentages, or sources.

## 2. Thesis Overview

Create a master overview before any full-thesis rewrite. Include:

- Title.
- Discipline or field.
- Chapter structure.
- Total word count or estimated word count.
- Protected terminology list.
- Citation density.
- Technical protection zones.
- AIGC risk distribution.
- Similarity risk distribution.
- Report mapping status.
- Suggested processing order.

Use `workflow/thesis_master_overview_template.md`.

## 3. Chapter Task Split

For each chapter:

- Create one chapter task.
- Mark suggested mode.
- Mark protected items.
- Mark risk source.
- Mark processing priority.
- Define acceptance criteria.

Use `workflow/chapter_task_template.md`.

## 4. Progress Tracking

Use these states:

- `PENDING`
- `DIAGNOSED`
- `TASK_CREATED`
- `DRAFT_REVISED`
- `NEEDS_HUMAN_REVIEW`
- `NEEDS_REPORT_RECHECK`
- `NEEDS_SECOND_PASS`
- `COMPLETED`
- `BLOCKED`

Use `workflow/progress_tracker_template.md`.

## 5. Iterative Optimization

Round 1:

- Process high-risk, high-contribution, safely editable paragraphs.
- Do not modify low-risk paragraphs.
- Do not modify no-edit zones.

Round 2:

- Use a new report to locate residual risks.
- Prioritize fragments that remain high risk.
- Do not heavily rewrite already completed content.
- Record why each item is processed again.

Round 3:

- Local micro-adjustment only.
- Terminology consistency check.
- Citation integrity check.
- Format and chapter transition check.

## Forbidden

- Do not rewrite a full thesis in one pass.
- Do not change style every round.
- Do not remove citations because of detection pressure.
- Do not change facts for similarity reduction.
- Do not add casual filler to reduce AIGC risk.
- Do not fabricate limitations, failures, or experiment data.
