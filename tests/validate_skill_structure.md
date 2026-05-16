# Validate Skill Structure

Use this manual checklist before publishing.

## Required Files

- [ ] `README.md`
- [ ] `SKILL.md`
- [ ] `LICENSE`
- [ ] `NOTICE`
- [ ] `AGENTS.md`
- [ ] `workflow/intake_request_template.md`
- [ ] `workflow/author_evidence_pack_template.md`
- [ ] `prompts/mode_intake_wizard.md`
- [ ] `prompts/mode_three_mode_color_band.md`
- [ ] `prompts/mode_first_pass_red_orange.md`
- [ ] `prompts/mode_current_report_red_orange.md`
- [ ] `prompts/mode_aigc_plateau_breaker.md`
- [ ] `prompts/mode_social_science_aigc_bottleneck.md`
- [ ] `prompts/mode_final_acceptance_audit.md`
- [ ] `prompts/quality_checklist.md`
- [ ] `references/file_input_copy_workflow.md`
- [ ] `references/docx_color_report_extraction.md`
- [ ] `references/three_mode_color_band_workflow.md`
- [ ] `references/first_pass_red_orange_engine.md`
- [ ] `references/current_report_red_orange_engine.md`
- [ ] `references/aigc_plateau_breaker.md`
- [ ] `references/social_science_template_bottleneck.md`
- [ ] `references/aigc_regression_guard.md`
- [ ] `references/final_acceptance_audit.md`
- [ ] `tests/validate_skill_structure.md`
- [ ] `tests/safety_checklist.md`

## SKILL.md Frontmatter

Expected:

```yaml
---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with forced intake, DOCX color-report extraction, red-orange coverage, social-science evidence reconstruction, and final acceptance audit.
license: MIT
---
```

## Required SKILL.md Sections

- [ ] 1. Role
- [ ] 2. Safety Boundaries
- [ ] 3. Core Workflow
- [ ] 4. Hard Routing Rules
- [ ] 5. Minimal Mode Router
- [ ] 6. Standard Output Blocks
- [ ] 7. File Layout
- [ ] No long supporting-reference index.
- [ ] No long mode alias list.
- [ ] Entry modes are kept to roughly 8-10.
- [ ] Detailed rules remain in `references/`, `prompts/`, and `workflow/`.

## Entry Mode Coverage

- [ ] `INTAKE_WIZARD_PRECHECK`
- [ ] `FILE_INPUT_COPY_WORKFLOW`
- [ ] `DOCX_COLOR_REPORT_EXTRACTION`
- [ ] `THREE_MODE_COLOR_BAND_WORKFLOW`
- [ ] `FIRST_PASS_RED_ORANGE_ENGINE`
- [ ] `CURRENT_REPORT_RED_ORANGE_ENGINE`
- [ ] `AIGC_PLATEAU_BREAKER`
- [ ] `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`
- [ ] `AIGC_REGRESSION_GUARD`
- [ ] `FINAL_ACCEPTANCE_AUDIT`

## Sub-Rules Not Entry Modes

- [ ] `AIGC_ONLY` is not an entry mode in `SKILL.md`.
- [ ] `REPORT_AIGC_ONLY` is not an entry mode in `SKILL.md`.
- [ ] `SECOND_PASS_REWRITE_REQUIREMENT` is not an entry mode in `SKILL.md`.
- [ ] `ORANGE_ZONE_REWRITE_STRATEGY` is not an entry mode in `SKILL.md`.
- [ ] `DISCIPLINE_AIGC_BOTTLENECK_RULES` is not an entry mode in `SKILL.md`.
- [ ] `CONSERVATIVE_AIGC_REPAIR` is not an entry mode in `SKILL.md`.
- [ ] `CONTENT_SUBSTANCE_INJECTION` is not an entry mode in `SKILL.md`.
- [ ] `EVIDENCE_TRACE_INJECTION` is not an entry mode in `SKILL.md`.
- [ ] `STRUCTURE_REBUILDING_RULES` is not an entry mode in `SKILL.md`.
- [ ] `PARAGRAPH_TYPE_STRATEGIES` is not an entry mode in `SKILL.md`.
- [ ] `EFFECTIVENESS_EVALUATION` is not an entry mode in `SKILL.md`.
- [ ] `BURSTINESS_RHYTHM_CONTROL` is not an entry mode in `SKILL.md`.
