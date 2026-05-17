# Safety Checklist

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Run this checklist before release.

## Forbidden Positioning

The project must not claim that it can ensure any external evaluation result. It must not present itself as a tool for replacing academic work, hiding source dependence, or disguising copied expression.

## Required Repeated Principles

- [ ] Do not fabricate data.
- [ ] Do not fabricate experiments.
- [ ] Do not fabricate citations.
- [ ] Do not alter conclusions.
- [ ] Do not remove necessary citations.
- [ ] Do not damage technical terms.
- [ ] Do not accidentally change formulas, code, interfaces, table names, field names, or parameters.

## Citation Safety

- [ ] Cited claims keep citation markers.
- [ ] Source-dependent claims are not rewritten as original claims.
- [ ] Missing citations are flagged rather than invented.
- [ ] LaTeX citation keys are preserved.

## Technical Safety

- [ ] Formulas are unchanged unless the user explicitly supplies corrections.
- [ ] Code blocks are not rewritten for style.
- [ ] API names, table names, field names, and parameters are unchanged.
- [ ] Experimental settings and values are unchanged.

## Mode Safety

- [ ] AIGC_ONLY does not perform broad semantic rewriting.
- [ ] SIMILARITY_ONLY keeps citation boundaries.
- [ ] DUAL_OPTIMIZATION handles similarity risk before AIGC-style adjustment.
- [ ] AUTO_DIAGNOSIS outputs a diagnosis table before revision.
- [ ] ENGINEERING_SCIENCE_MODE builds a protected technical list.

## Example Coverage

- [ ] AIGC-only example exists.
- [ ] Similarity-only example exists.
- [ ] Dual optimization example exists.
- [ ] Engineering thesis example exists.
- [ ] Citation-heavy example exists.
- [ ] Long-thesis workflow example exists.
