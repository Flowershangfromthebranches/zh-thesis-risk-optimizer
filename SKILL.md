---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with forced intake, DOCX color-report extraction, red-orange coverage, social-science evidence reconstruction, and final acceptance audit.
license: MIT
---

# zh-thesis-risk-optimizer

## 1. Role

This Skill helps revise Chinese thesis text for writing quality, AIGC writing-risk signals, similarity-risk expression, report-color mapping, citation-boundary integrity, file-copy handling, and final acceptance auditing.

It is not a detection-result promise tool. Scores and color targets are heuristic writing-risk references only. Report-driven workflows only process report content legally obtained and provided by the user.

## 2. Safety Boundaries

Do not:

- Promise external detection outcomes or fixed percentage changes.
- Crack, reverse engineer, simulate, or forge any detection system or report.
- Fabricate data, experiments, citations, report percentages, similarity sources, interviews, logs, code, interfaces, screenshots, companies, forms, indicators, or risk levels.
- Delete necessary citations or disguise sourced content as uncited original writing.
- Alter conclusions beyond provided evidence.
- Rewrite formulas, code, API paths, table names, field names, parameters, experiment data, reference entries, school declarations, or appendices for style.

When integrity or technical correctness conflicts with risk reduction, integrity wins.

## 3. Core Workflow

1. Run `INTAKE_WIZARD_PRECHECK`.
2. On first contact for a new task, show `workflow/intake_request_template.md` and wait for the user's completed intake reply.
3. Do not diagnose, parse reports, read files, or rewrite before intake is complete.
4. Create a file copy for file input; never edit the original file directly.
5. If a DOCX color report is present, extract color metadata before plain text.
6. Select the minimal hard route from the mode router.
7. Build protected items and frozen zones before revision.
8. Process red/orange report targets with paragraph records and acceptance checks.
9. Run `FINAL_ACCEPTANCE_AUDIT`.
10. Do not mark completion if any required chain step or red/orange acceptance item is missing.

## 4. Hard Routing Rules

### 4.1 Intake Gate

- Any task matching this Skill starts with `INTAKE_WIZARD_PRECHECK`.
- First contact stops at the intake template.
- Required fields must be filled.
- Strongly recommended and optional fields must be filled or explicitly marked `无`, `跳过`, or `请自动判断`.
- If a completed intake template is already present, output `Intake Confirmation` and continue.

### 4.2 Mandatory First-Pass Chain

When the intake says:

- original thesis plus original AIGC color report;
- mode is AIGC-only;
- user gives red/orange/purple/black color rules;
- user asks to process red and orange together;
- user asks for character control or no broad full-text rewrite;

the mandatory chain is:

```text
FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> FIRST_PASS_RED_ORANGE_ENGINE
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when discipline matches management/social-science types
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> FINAL_ACCEPTANCE_AUDIT
```

If any step is missing, the task cannot be marked complete.

### 4.3 Current-Report Chain

When the intake says the report is from a revised/current draft, use:

```text
FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> CURRENT_REPORT_RED_ORANGE_ENGINE
-> AIGC_PLATEAU_BREAKER when orange accumulation or multi-round slowdown exists
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when discipline matches management/social-science types
-> AIGC_REGRESSION_GUARD
-> FINAL_ACCEPTANCE_AUDIT
```

Do not use `FIRST_PASS_RED_ORANGE_ENGINE` for revised/current reports.

### 4.4 Social-Science Hard Rule

For human resource management, business administration, marketing, education management, and public administration, `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` is a hard rule during red/orange AIGC work.

If red/orange paragraphs lack company, questionnaire, interview, process, post, form, indicator, responsibility, review-cycle, or boundary evidence, request `workflow/author_evidence_pack_template.md`. Do not invent missing materials.

### 4.5 First-Pass Failure

If the user says the original-thesis test produced almost no AIGC improvement, mark `FIRST_PASS_FAILURE`, not plateau.

Check:

- DOCX color report was actually parsed.
- Red/orange coverage was 100%.
- The rewrite was not only synonym replacement.
- `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` was enabled when applicable.
- Author evidence was available or requested.
- The output had paragraph records and final acceptance audit.

Then output a failure-cause table and next repair plan.

## 5. Minimal Mode Router

| Mode | Use When | Load |
|---|---|---|
| `INTAKE_WIZARD_PRECHECK` | Start of every matching task. | prompts/mode_intake_wizard.md, workflow/intake_request_template.md |
| `FILE_INPUT_COPY_WORKFLOW` | User provides DOCX/TXT/Markdown/LaTeX file input. | references/file_input_copy_workflow.md |
| `DOCX_COLOR_REPORT_EXTRACTION` | User provides Word/DOCX color report. | references/docx_color_report_extraction.md |
| `THREE_MODE_COLOR_BAND_WORKFLOW` | Any AIGC/similarity/dual task with color bands. | prompts/mode_three_mode_color_band.md, references/three_mode_color_band_workflow.md |
| `FIRST_PASS_RED_ORANGE_ENGINE` | Original thesis plus original AIGC color report. | prompts/mode_first_pass_red_orange.md, references/first_pass_red_orange_engine.md |
| `CURRENT_REPORT_RED_ORANGE_ENGINE` | Revised/current thesis plus current AIGC color report. | prompts/mode_current_report_red_orange.md, references/current_report_red_orange_engine.md |
| `AIGC_PLATEAU_BREAKER` | Multi-round slowdown or orange accumulation. | prompts/mode_aigc_plateau_breaker.md, references/aigc_plateau_breaker.md |
| `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` | HR/management/social-science red-orange template risk. | prompts/mode_social_science_aigc_bottleneck.md, references/social_science_template_bottleneck.md, workflow/author_evidence_pack_template.md |
| `AIGC_REGRESSION_GUARD` | Rewrite becomes smoother, more formal, or more AI-like. | references/aigc_regression_guard.md |
| `FIRST_PASS_EFFECTIVENESS_GATE` | Internal mandatory gate after first-pass rewrite; checks color migration and AIGC thresholds. | references/first_pass_effectiveness_gate.md |
| `FINAL_ACCEPTANCE_AUDIT` | End of every report-driven or file-copy task. | prompts/mode_final_acceptance_audit.md, references/final_acceptance_audit.md |

Internal sub-rules such as burstiness audit, orange-zone repair, conservative repair, structure rebuilding, evidence injection, paragraph strategies, second-pass rewrite, and effectiveness evaluation are not entry modes. Load them only through the main modes above when needed.

## 6. Standard Output Blocks

### Intake Confirmation

| field | value | status |
|---|---|---|

### Mandatory Chain Trace

| step | required | executed | evidence |
|---|---|---|---|

### Color Extraction Summary

| source | red_count | orange_count | purple_count | black_count | extraction_status |
|---|---:|---:|---:|---:|---|

### Red-Orange Task Table

| id | section | paragraph_id | report_band | mapped_confidence | original_fragment | risk_reason | required_action |
|---|---|---|---|---|---|---|---|

### Red-Orange Paragraph Processing Record

| id | section | original_band | original_fragment | action_type | evidence_used | char_delta | self_audit_result | passed |
|---|---|---|---|---|---|---:|---|---|

Allowed `action_type` values:

- `A_EVIDENCE_RECONSTRUCTION`
- `B_ARGUMENT_PATH_REWRITE`
- `C_TEMPLATE_SKELETON_BREAK`
- `D_AUTHOR_MATERIAL_REQUEST`

### Red-Orange Coverage Acceptance Table

| red_total | orange_total | processed_red | processed_orange | unprocessed_red_orange | completion_status |
|---:|---:|---:|---:|---:|---|

### Unprocessed Red-Orange List

| id | section | paragraph_id | original_band | reason_not_processed | required_next_action |
|---|---|---|---|---|---|

### First-Pass Failure Table

| check_item | result | evidence | next_fix |
|---|---|---|---|

### Final Acceptance Audit

| item | result | evidence |
|---|---|---|
| DOCX color read |  |  |
| red total / processed |  |  |
| orange total / processed |  |  |
| social-science bottleneck enabled |  |  |
| synonym-only rewrite found |  |  |
| formalization regression found |  |  |
| character change |  |  |
| unprocessed paragraphs |  |  |
| author evidence needed |  |  |

## 7. File Layout

- `SKILL.md`: slim routing and hard chain only.
- `prompts/`: executable prompts for the 10 entry modes.
- `references/`: detailed rules used by entry modes.
- `workflow/`: intake, author evidence pack, file-copy, and project templates.
- `tests/`: acceptance and regression checklists.
- `NOTICE` and `THIRD_PARTY_NOTICES.md`: attribution and license notes.
