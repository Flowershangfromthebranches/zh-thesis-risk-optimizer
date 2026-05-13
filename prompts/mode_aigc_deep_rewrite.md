# Prompt: AIGC_DEEP_REWRITE_ENGINE

## Purpose

Use this mode when AIGC risk remains high or when shallow rewriting is likely to fail.

## Input

- Original paragraph.
- Protected facts and no-change items.
- Optional report fragment or diagnosis.

## Workflow

1. List preserved facts.
2. List no-change items.
3. Identify empty significance, mechanical structure, missing objects, and over-smooth rhythm.
4. Apply at least two effective rewrite actions from `references/anti_shallow_rewrite_rules.md`.
5. Rebuild paragraph structure using `references/structure_rebuilding_rules.md`.
6. Add only supported trace from `references/evidence_trace_injection.md`.
7. Check formalization regression with `references/aigc_regression_guard.md`.
8. Run `references/post_rewrite_aigc_self_audit.md`.
9. If the audit triggers second pass, run `prompts/mode_second_pass_rewrite.md`.

## Output

- Preserved fact list.
- No-change list.
- Deep rewrite.
- Evidence-density change.
- Regression guard result.
- AIGC self-audit.
- Second-pass decision.

## Safety

Do not fabricate data, experiments, modules, interfaces, roles, failures, or references.
