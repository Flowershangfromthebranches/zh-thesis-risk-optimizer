# Project Handoff Rules

Use `PROJECT_HANDOFF_MODE` when the user pauses, changes model, moves to a new session, or asks for a resumable project summary.

## Handoff Must Include

- Current project state.
- Completed chapters and remaining chapters.
- Current progress tracker.
- Latest report mapping status.
- Protected terms and no-edit zones.
- Revision log summary.
- Open questions.
- Next recommended actions.

## Handoff Rules

- Do not hide unresolved LOW or UNMAPPED mappings.
- Preserve citation and technical protection notes.
- Include the latest accepted mode and intensity for each active chapter.
- State what should not be reworked.
- Make the resume prompt actionable.

Use `workflow/project_handoff_template.md`.
