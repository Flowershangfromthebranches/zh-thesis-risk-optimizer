# First-Pass Effectiveness Gate

## Purpose

`FIRST_PASS_EFFECTIVENESS_GATE` is the quality checkpoint between `FIRST_PASS_RED_ORANGE_ENGINE` and `FINAL_ACCEPTANCE_AUDIT`. It prevents the common failure mode where a first pass reduces red text but produces an orange plateau — the AIGC score drops only a few points while color distribution shifts from red to orange rather than red to black.

This gate is not a rewriter. It is a diagnostic gate that evaluates the first-pass result and decides whether the task can proceed to acceptance or must enter `AIGC_PLATEAU_BREAKER` for a second pass.

**Core principle**: Red-to-orange migration is NOT success. If red decreased but orange accumulated, the first pass demoted risk levels but did not eliminate them. This is `FIRST_PASS_FAILURE`, not a plateau.

## Input Required

To evaluate the gate, the following must be available:

- Original AIGC report color distribution (red, orange, purple, black character counts and percentages).
- Post-first-pass AIGC report color distribution.
- Original overall AIGC suspicion percentage (if provided by the user).
- Post-first-pass overall AIGC suspicion percentage.
- Red/orange paragraph processing records (per-paragraph A/B/C/D action type and self-audit result).
- Whether special sections (abstract, theoretical basis, chapter 5, conclusion) still have whole-paragraph red/orange blocks.

## Gate Conditions

If **any** of the following conditions is met, the first pass must **NOT** be marked complete. The task must be routed to `AIGC_PLATEAU_BREAKER` or a second-pass rewrite. The output must include a `FIRST_PASS_FAILURE` diagnosis table.

### Condition 1: Overall AIGC Still Above 60%

If the post-first-pass overall AIGC suspicion percentage is still higher than 60%, the first pass has not achieved a meaningful risk reduction.

### Condition 2: Red + Orange Combined Still Above 40%

If red and orange combined coverage still exceeds 40% of the total analyzed text, the risk concentration is still too high for acceptance.

### Condition 3: Orange Share Rose by More Than 10 Percentage Points

If the orange band's character share increased by more than 10 percentage points compared to the original report (e.g. from 24.4% to 42.3%), this signals "red transferred to orange" rather than "red eliminated."

### Condition 4: Red Dropped but Orange Accumulated Significantly

If red decreased but orange increased by a non-trivial margin (more than 5 percentage points), the engine is demoting risk levels but not eliminating them. This is red-to-orange migration, not genuine reduction.

### Condition 5: Key Sections Still Have Whole-Paragraph Red/Orange

If any of these sections still contain paragraphs that are entirely red or orange:
- Abstract (摘要)
- Theoretical Basis (理论基础, typically 2.1/2.2)
- Chapter 5 / Analysis Chapter (第五章/实证分析)
- Conclusion (结论)

...the first pass has not penetrated the most critical areas.

### Condition 6: Black Coverage Below 25%

If black (low-risk) text coverage is below 25% of total analyzed characters, too much text remains in detectable risk bands.

### Condition 7: No Per-Paragraph Processing Record

If the output does not include a complete red/orange paragraph processing record showing each paragraph's action type (`A_EVIDENCE_RECONSTRUCTION`, `B_ARGUMENT_PATH_REWRITE`, `C_TEMPLATE_SKELETON_BREAK`, `D_AUTHOR_MATERIAL_REQUEST`), the first pass cannot be verified.

### Condition 8: No Action Type Per Paragraph

If any processed red/orange paragraph lacks a documented action type (A/B/C/D), the processing record is incomplete and the paragraph may have been only synonym-polished.

### Condition 9: Academic Tone Guard Failed

If `ACADEMIC_TONE_GUARD` reports violations that were not corrected, the text has been over-humanized. Even if AIGC dropped, the thesis is no longer academically appropriate.

### Condition 10: Format Preservation Failed

If `OOXML_DOCX_PATCH_WORKFLOW` was required but:
- `ooxml_patch_result` = NOT_USED and user required DOCX format preservation; or
- `duplicate_insertion_guard_result` = FAILED; or
- `format_preservation_result` = FAILED;

...the deliverable is not acceptable regardless of AIGC score.

## Output: Required Fields

The gate output must include all of the following:

| field | description |
|---|---|
| `original_color_distribution` | Red, orange, purple, black char counts and percentages from the original report |
| `post_first_pass_color_distribution` | Red, orange, purple, black char counts and percentages from the post-first-pass report |
| `color_migration_table` | Per-band delta and assessment (see below) |
| `gate_result` | PASSED or FIRST_PASS_FAILURE |
| `failure_reasons` | List of which conditions failed (empty if PASSED) |
| `next_required_route` | FINAL_ACCEPTANCE_AUDIT if PASSED; AIGC_PLATEAU_BREAKER if FAILED |
| `academic_tone_guard_result` | PASSED / FAILED / NOT_APPLICABLE |
| `format_preservation_result` | PASSED / FAILED / NOT_APPLICABLE |
| `duplicate_insertion_guard_result` | PASSED / FAILED / NOT_APPLICABLE |
| `ooxml_patch_result` | USED_AND_PASSED / USED_AND_FAILED / NOT_USED |

## Output: Gate Verdict Table

| condition | original_value | post_first_pass_value | met | verdict |
|---|---|---|---|---|
| 1. AIGC > 60% | 76.67% | 68.6% | YES | FAIL — still above 60% |
| 2. Red+Orange > 40% | 63.8% | 55.9% | YES | FAIL — combined still > 40% |
| 3. Orange rose > 10pp | 24.4% | 42.3% | YES | FAIL — orange share rose 17.9pp |
| 4. Red→Orange migration | 39.4%→24.4% | 13.6%→42.3% | YES | FAIL — red dropped but orange accumulated |
| 5. Key sections still red/orange | — | to be checked | ? | CHECK |
| 6. Black < 25% | 6.9% | 14.6% | YES | FAIL — black still below 25% |
| 7. Processing records present | — | to be checked | ? | CHECK |
| 8. Action type per paragraph | — | to be checked | ? | CHECK |

If **any** condition is met → `FIRST_PASS_FAILURE` → route to `AIGC_PLATEAU_BREAKER`.
| 9. Academic tone guard failed | — | to be checked | ? | CHECK |
| 10. Format preservation failed | — | to be checked | ? | CHECK |

If **any** condition is met → `FIRST_PASS_FAILURE` → route to `AIGC_PLATEAU_BREAKER` (or `ACADEMIC_TONE_GUARD` for condition 9, or `FORMAT_FAILURE` for condition 10).

## Output: Color Migration Table

The gate must produce a color migration table showing how each band's character share changed:

| band | original | post_first_pass | delta | assessment |
|---|---|---|---|---|
| red (>=70%) | 39.4% (8601 chars) | 13.6% (3027 chars) | -25.8pp | reduced — but mostly to orange, not black |
| orange (60-70%) | 24.4% (5311 chars) | 42.3% (9376 chars) | +17.9pp | SURGED — red-to-orange migration |
| purple (50-60%) | 3.2% (692 chars) | 4.1% (905 chars) | +0.9pp | stable |
| black (<50%) | 6.9% (1502 chars) | 14.6% (3237 chars) | +7.7pp | improved but insufficient |

**Color migration conclusion**: 红转橙，未突破。Red decreased but the displaced mass settled in orange. The first pass demoted risk levels but did not eliminate them.

## Next Action

| gate verdict | next action |
|---|---|
| ALL conditions clear | proceed to `FINAL_ACCEPTANCE_AUDIT` |
| Any condition met | enter `AIGC_PLATEAU_BREAKER`; output FIRST_PASS_FAILURE diagnosis |
| Processing records missing | return to `FIRST_PASS_RED_ORANGE_ENGINE` to complete records first |
| Author evidence missing | output material gap table and request `workflow/author_evidence_pack_template.md` |

## Relation To SKILL.md

This gate runs after `AIGC_REGRESSION_GUARD` and before `FINAL_ACCEPTANCE_AUDIT` in the mandatory first-pass chain:

```text
FIRST_PASS_RED_ORANGE_ENGINE
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK
-> CONTROLLED_HUMANIZATION_ENGINE when applicable
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE       ← here
-> FINAL_ACCEPTANCE_AUDIT
```
