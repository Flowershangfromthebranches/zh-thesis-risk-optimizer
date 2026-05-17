# Content Substance Injection

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Purpose

This rule reduces template-like writing by increasing real content substance, not by surface polishing.

## 1. Existing Evidence

Use evidence already present in the thesis or user-provided materials:

- Module names.
- Class names.
- Function or method names.
- Parameters.
- Input and output.
- Test environment.
- Test count.
- Running result.
- Figure or table information.
- Code path.
- Database field.
- Report file name.
- Screenshot description.

## 2. Author-Supplied Evidence

Ask the author to supplement:

- Why a library was selected.
- Problems encountered during implementation.
- Why a parameter was set in a certain way.
- How test samples were constructed.
- Target vulnerable page structure.
- False-positive or false-negative cases.
- Comparison with similar tools.
- System limitations.

## 3. Forbidden Evidence

Do not fabricate:

- Debugging experiences that did not happen.
- Untested performance data.
- Nonexistent interfaces.
- Unused algorithms.
- Uncited literature claims.
- Comparison experiments that were not conducted.
- User interviews that did not exist.
- Runtime logs that were not provided.

## Paragraph Repair Rule

A high-AIGC paragraph can enter L4/L5 repair only when at least two conditions are satisfied:

- It introduces one concrete technical object.
- It introduces one input/output relation.
- It introduces one parameter or configuration.
- It introduces one test condition.
- It introduces one result value.
- It introduces one applicability boundary or limitation.
- It changes the original information order.

If these cannot be satisfied from available evidence, output an author supplementation list.

## Relation To SKILL.md

Use this file in `CONTENT_SUBSTANCE_INJECTION`, `AIGC_REGRESSION_GUARD`, and `TARGETED_MULTIPASS_ENGINE`.
