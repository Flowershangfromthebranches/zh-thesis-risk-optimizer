# Prompt: PROGRESS_TRACKING_MODE

Use this mode when the user asks for current project state, status table, pending work, or report-recheck queue.

## Workflow

1. Read the master overview and chapter tasks if provided.
2. Normalize chapter states using `references/progress_tracking_rules.md`.
3. List blocked items and human review items.
4. Summarize next actions.
5. Do not mark low-confidence mappings complete without confirmation.

Use `workflow/progress_tracker_template.md`.
