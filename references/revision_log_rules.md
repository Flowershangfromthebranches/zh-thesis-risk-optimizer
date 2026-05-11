# Revision Log Rules

Use `REVISION_LOG_MODE` whenever text is changed.

## Log Purpose

Revision logs preserve context across long thesis work and prevent accidental repeated rewriting.

## Required Fields

Use `workflow/revision_log_template.md` and record:

- Time.
- Chapter.
- Paragraph.
- Mode used.
- Intensity.
- Revision target.
- Protected items.
- Citation handling.
- Risk change.
- Human review items.

## Logging Rules

- Log every meaningful revision.
- Separate report-derived risk from heuristic diagnosis.
- Record why citations were kept or why a section needs human review.
- Mark any LOW or UNMAPPED report mapping as unresolved.
- If no text changed, log the diagnostic action instead of pretending a revision occurred.

## Do Not

- Do not use logs to claim external detection results.
- Do not erase unresolved risks from later handoff.
- Do not mark a chapter complete when protected items still need review.
