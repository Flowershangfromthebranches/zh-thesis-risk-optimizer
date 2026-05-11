# Report Mapping Output Check

Use this checklist before publishing v0.3-report-driven-mapping.

## Mode Coverage

- [ ] `REPORT_DRIVEN_MODE` exists.
- [ ] `REPORT_AIGC_ONLY` exists.
- [ ] `REPORT_SIMILARITY_ONLY` exists.
- [ ] `REPORT_DUAL_OPTIMIZATION` exists.
- [ ] `REPORT_TO_SOURCE_MAPPING` exists.
- [ ] `SIMILARITY_SOURCE_HANDLING` exists.
- [ ] `REPORT_PRIORITY_QUEUE` exists.
- [ ] `MAPPING_CONFIDENCE_LEVEL` exists.

## Output Coverage

- [ ] Report-driven task table exists.
- [ ] Single-paragraph handling format exists.
- [ ] Mapping confidence levels `HIGH`, `MEDIUM`, `LOW`, and `UNMAPPED` exist.
- [ ] Unmapped fragments require human confirmation.
- [ ] Low-confidence mappings are not directly rewritten.

## Safety Coverage

- [ ] Citations are protected.
- [ ] Formulas, code, API paths, table names, fields, and experiment data are protected.
- [ ] The project does not forge detection results.
- [ ] The project does not promote detection evasion.
- [ ] README thanks `lengsukq/ParaphrasingToolClient` and `Abnerla/AI_paper`.
- [ ] NOTICE records `lengsukq/ParaphrasingToolClient` and `Abnerla/AI_paper`.
