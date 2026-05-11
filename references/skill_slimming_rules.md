# Skill Slimming Rules

Use `SKILL_SLIM_MODE` when maintaining this repository.

## Goal

Keep `SKILL.md` as a short routing and safety document. Move implementation details into:

- `references/` for rules and domain knowledge.
- `prompts/` for task-specific execution prompts.
- `workflow/` for templates.
- `examples/` for examples.
- `tests/` for manual validation checklists.

## What Belongs in SKILL.md

- YAML frontmatter.
- Role.
- Scope.
- Non-goals.
- Core principles.
- Mode router.
- Standard workflow.
- Output format index.
- Safety boundaries.
- Upstream acknowledgement index.

## What Does Not Belong in SKILL.md

- Full AI writing pattern library.
- Full similarity strategy library.
- Full sentence-label list.
- Full report-mapping rules.
- Full citation integrity rules.
- Full chapter strategies.
- Full examples.
- Full templates.

## Maintenance Rule

If a new section would make `SKILL.md` exceed the target length, create or update a reference, prompt, workflow template, example, or test instead.
