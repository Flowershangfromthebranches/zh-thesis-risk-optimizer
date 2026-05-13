# Chapter Task Rules

Use `CHAPTER_TASK_MODE` to create a bounded task for each thesis chapter.

## Abstract

- Minimal revision.
- Preserve research object, method, result, and conclusion.
- Do not expand or fabricate content.

## Introduction

- Reduce broad narratives, background padding, and generalized significance.
- Move toward the concrete research problem and object.

## Literature Review

- Protect citations.
- Do not merge literature claims into uncited original claims.
- Reduce repetitive literature stacking.

## Theoretical Basis / Related Technology

- Compress textbook-like definitions.
- Preserve terms, formulas, and necessary citations.
- Explain how the thesis uses each concept.

## System Design

- Protect module names, interfaces, database table names, and fields.
- Strengthen data flow, permissions, exception handling, and module relationships.

## Implementation

- Protect code, file names, class names, function names, and paths.
- Clarify input, processing, output, and exception logic.

## Experiment / Testing

- Protect data, parameters, metrics, chart numbers, and conclusions.
- Strengthen environment, test cases, result explanation, and limitations.

## Conclusion and Outlook

- Reduce empty significance statements.
- Preserve completed work.
- Write concrete limitations and future improvement directions.

## v0.5 Rewrite Intensity Guidance

- Use L3 when the chapter has repeated paragraph order but few protected entities.
- Use L4 when the argument must be rebuilt from concrete problem, process, or result.
- Use L5 only for high-risk, non-protected, non-citation-heavy paragraphs.
- For high AIGC-risk chapter tasks, run post-rewrite self-audit before marking the task complete.
- If three or more AI-risk items remain after self-audit, create a second-pass revision item instead of accepting the paragraph.

## Chapter Task Output

Use `workflow/chapter_task_template.md` and include:

- Chapter info.
- Diagnosis table.
- Revision plan.
- Revision log.
- Acceptance checklist.
