# Evidence and Trace Injection

## Purpose

`EVIDENCE_AND_TRACE_INJECTION` increases concrete research trace without fabricating content.

In v0.6, this mechanism is strengthened as content substance injection: the rewrite should increase evidence density when the source provides enough information.

## Allowed Sources

Only use information from:

1. User-provided original text.
2. User-provided system description.
3. User-provided detection report.
4. User-provided experiment data.
5. User-provided code, interface, or table structure.
6. User-confirmed additional facts.

## Useful Trace Types

- Why a design choice was made.
- What concrete problem was handled.
- Which module, interface, field, dataset, or experiment object is involved.
- Under which condition a conclusion applies.
- What limitation is already implied by the user's data or text.
- How a result supports a conclusion.

## Evidence Density

Evidence density means the amount of concrete technical material per 100 Chinese characters, such as modules, parameters, input/output relations, test conditions, result values, class names, methods, local addresses, and report fields.

For high AIGC-risk paragraphs, do not only reduce template phrases. Try to increase evidence density using provided facts.

## Evidence Categories

### Existing Evidence

Use directly when provided:

- Class names.
- Method names.
- Parameters.
- Local addresses.
- Test counts.
- Vulnerability counts.
- Report fields.
- Database fields.
- Dependency library versions.
- Module names and input/output relations.

### Author-Supplied Evidence

Ask for these when missing:

- Why a library was chosen.
- Why a parameter was set.
- How the test sample was built.
- What false-positive or false-negative cases appeared.
- What limitation the current implementation has.

### Forbidden Evidence

Do not invent:

- Untested data.
- Missing interfaces.
- Unused algorithms.
- Unprovided runtime logs.
- Uncited literature claims.
- Nonexistent comparison experiments.

## Forbidden Injections

Do not fabricate:

1. Data.
2. Experiments.
3. Interfaces.
4. Modules.
5. User roles.
6. Test results.
7. References.
8. Failure cases.

## Missing Detail Pattern

If a paragraph needs more concrete detail but the source does not provide it, output:

```text
此处建议作者补充：……
```

Do not invent the missing detail.

## Relation To SKILL.md

Used by deep rewriting and second-pass rewriting to add specificity safely.
