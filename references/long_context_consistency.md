# Long Context Consistency

Long thesis revision needs memory-like tracking. Without it, later chapters may use different terms, repeat definitions, or contradict earlier findings.

## Required Working Notes

For each long task, maintain four lightweight notes in the conversation or a project file if the user asks for file output.

For full-thesis projects, these notes should be represented in `workflow/thesis_master_overview_template.md`, `workflow/progress_tracker_template.md`, and `workflow/revision_log_template.md`.

### 1. Protected Terms

Track:

- Term.
- First-use form.
- Accepted abbreviation.
- Forbidden changes.
- Chapter where it appears.

### 2. Citation Map

Track:

- Citation marker.
- Claim supported by the citation.
- Whether the claim is background, method, data, or discussion.
- Any missing-source warning.

### 3. Rolling Section Summary

After each section, write 3-5 bullets:

- What the section argues.
- Key data or examples.
- Important terms introduced.
- Conclusions or limitations.
- Risks already handled.

### 4. Revision Strategy Log

Track:

- Mode used.
- Intensity used.
- Main risk repaired.
- Items deliberately left unchanged.

## Before Revising the Next Block

Check:

- Does terminology match the protected list?
- Does the paragraph repeat an already defined term?
- Does a later conclusion contradict an earlier section?
- Does the citation marker still support the same claim?
- Is the writing style drifting too far from previous revised sections?

## Handling Inconsistency

- Minor wording inconsistency: fix directly.
- Repeated definition: remove the duplicate explanation or convert it into a local reminder.
- Possible logic conflict: flag it for user review.
- Missing data, missing figure, or contradictory result: do not invent a fix; report it.

## Project Handoff

Before a long task pauses, create or update `workflow/project_handoff_template.md` with:

- Current chapter status.
- Protected terms.
- Open report mappings.
- Revision log summary.
- Next actions.

## Suggested Rolling Summary Template

```markdown
## Rolling Summary
- Section:
- Core claim:
- Key evidence:
- Protected terms:
- Citation notes:
- Revision mode and intensity:
- Open issues:
```
