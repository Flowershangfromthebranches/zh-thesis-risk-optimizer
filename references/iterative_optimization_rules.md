# Iterative Optimization Rules

Use `ITERATIVE_REVISION_MODE` when the user provides a new report or asks for another pass after initial work.

## First Round

- Process high-risk, high-contribution, safely editable paragraphs.
- Do not modify low-risk paragraphs.
- Do not modify protected areas.
- Create overview, chapter tasks, and revision log entries.

## Second Round

- Use the new report to locate residual risk.
- Prioritize fragments that remain high risk.
- Do not heavily rewrite content that is already accepted or low risk.
- Record why each target is processed again.
- If residual risk is AIGC-heavy, run `AIGC_DEEP_REWRITE_ENGINE` instead of another light polish.
- If post-rewrite self-audit hits three or more AI-risk items, run `prompts/mode_second_pass_rewrite.md`.

## Third Round

- Local micro-adjustment only.
- Terminology consistency check.
- Citation integrity check.
- Format and chapter connection check.

## Forbidden

- Repeated full-text rewriting.
- Changing style every round.
- Deleting citations due to detection pressure.
- Changing facts to reduce similarity.
- Adding casual filler to lower AIGC risk.
- Fabricating limitations, failures, or experiment data.

## Iteration Plan

Use `workflow/iteration_plan_template.md`.
