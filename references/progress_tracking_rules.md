# Progress Tracking Rules

Use `PROGRESS_TRACKING_MODE` to maintain chapter states and project status.

## Status Definitions

- `PENDING`: 未开始。
- `DIAGNOSED`: 已诊断。
- `TASK_CREATED`: 已生成章节任务。
- `DRAFT_REVISED`: 已完成初改。
- `NEEDS_HUMAN_REVIEW`: 待人工核对。
- `NEEDS_REPORT_RECHECK`: 待报告复测。
- `NEEDS_SECOND_PASS`: 需二轮优化。
- `COMPLETED`: 已完成。
- `BLOCKED`: 缺少原文、报告或人工确认。

## State Transitions

1. Complete thesis input first enters `DIAGNOSED`.
2. After chapter tasks are generated, enter `TASK_CREATED`.
3. After first revision, enter `DRAFT_REVISED`.
4. If citations, experiment data, or low-confidence report mapping are involved, enter `NEEDS_HUMAN_REVIEW`.
5. After the user uploads a new report, affected chapters may enter `NEEDS_SECOND_PASS`.
6. Do not jump directly from `PENDING` to `COMPLETED`.
7. Low-confidence mappings cannot enter `COMPLETED` without human confirmation.

## Required Progress Fields

Use `workflow/progress_tracker_template.md` and track:

- Chapter.
- Word count.
- AIGC risk.
- Similarity risk.
- Report status.
- Suggested mode.
- Current state.
- Last modification.
- Pending issue.
- Next step.
