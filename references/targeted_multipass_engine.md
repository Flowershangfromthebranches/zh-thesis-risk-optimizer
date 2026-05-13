# Targeted Multipass Engine

## Purpose

`TARGETED_MULTIPASS_ENGINE` is the v0.6 core workflow: target-driven, report-feedback-based, evidence-injected, multi-pass, and regression-guarded.

It is designed for real Chinese thesis optimization tasks where similarity risk and AIGC risk must be improved across multiple rounds. It does not promise any external platform result.

## Optimization Targets

```yaml
similarity_target: "<10%"
aigc_target: "<20%"
targets_are_not_guarantees: true
```

These values are user goals and regression-test targets. They are not promises about any commercial or institutional detection system. Any concrete percentage must come from a user-provided report.

## Why Single-Pass Rewrite Fails

Single-pass full-text polishing often fails because:

- It tends to replace words without rebuilding paragraph logic.
- Similarity may drop while AIGC risk rises.
- Plain thesis prose may be turned into more formal, abstract, and smoother AI-like prose.
- There is no second localization based on new reports.
- The rewrite adds little real content substance from the paper itself.

## Multi-Pass Workflow

### Pass 0: Source and Report Alignment

Align:

- Original thesis text.
- Current draft.
- Similarity report.
- AIGC report.
- Historical versions.
- User targets.

Keep report values separate from heuristic scoring.

### Pass 1: Similarity Reduction

Prioritize:

- High-similarity fragments.
- Repeated definitions.
- Textbook-like background.
- Literature-review stacking.
- Source-close expression.

Preserve citations and protected content.

### Pass 2: AIGC Risk Reduction

Target:

- Template openings.
- Over-smooth rhythm.
- Generic endings.
- High-frequency AI-like phrases.
- Abstract noun inflation.

Do not replace ordinary wording with grander formal wording.

### Pass 3: Evidence-Based Reconstruction

Rebuild paragraphs using evidence that already exists in the thesis or is provided by the author:

- Modules.
- Parameters.
- Interfaces.
- Class names or method names.
- Test targets.
- Experiment results.
- Boundary conditions.

If evidence is missing, output `建议作者补充：...` instead of inventing it.

### Pass 4: Regression Audit

Check whether the new draft caused:

- Similarity decreased but AIGC increased.
- AIGC decreased but similarity increased.
- Factual damage.
- Citation damage.
- Technical detail damage.
- v0.5-style formalization regression.

## Completion Rule

Mark a task `COMPLETED` only when all conditions are met:

- A new user-provided report shows both similarity and AIGC moving toward the user targets.
- No obvious factual error was introduced.
- No necessary citation was removed.
- No technical detail was damaged.
- No v0.5-style formalization regression appears.

If similarity improves but AIGC worsens, mark:

`PARTIAL_SUCCESS_SIMILARITY_ONLY_AIGC_FAILED`

If AIGC improves but similarity remains high, mark:

`PARTIAL_SUCCESS_AIGC_ONLY_SIMILARITY_FAILED`

If neither metric improves clearly, mark:

`FAILED_REWRITE_STRATEGY`

## Relation To SKILL.md

`SKILL.md` routes explicit target-based and multi-report tasks here through `TARGETED_MULTIPASS_ENGINE`.
