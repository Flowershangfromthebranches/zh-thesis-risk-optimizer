# Rewrite Application Gate

## Purpose

`REWRITE_APPLICATION_GATE` verifies that high-risk red/orange target paragraphs were not only rewritten in a draft table, but were actually applied to the DOCX body text.

This gate exists because a first pass can appear successful in logs while the delivered DOCX still contains the original high-risk template paragraphs.

## Required Inputs

- Red/orange target paragraph table.
- `rewrite_text` for every target paragraph.
- Academic tone guard result for each `rewrite_text`.
- OOXML patch log from `OOXML_DOCX_PATCH_WORKFLOW`.
- Re-read `word/document.xml` after patching.
- Original paragraph text and patched paragraph text.

## Required Checks

For every red/orange target paragraph:

1. `rewrite_text` exists.
2. `rewrite_text` passed `ACADEMIC_TONE_GUARD`.
3. `rewrite_text` was patched into `word/document.xml`.
4. Re-read `document.xml` after patching and locate the patched paragraph.
5. The original high-risk text no longer remains in the mapped target paragraph.
6. Character-level diff ratio meets the minimum threshold.
7. Template residue is not present in the patched paragraph.

## Minimum Diff Ratio

| section type | minimum diff ratio | failure status |
|---|---:|---|
| Abstract / 摘要 | 45% | `rewrite_not_applied` |
| Theoretical basis / 理论基础 | 45% | `rewrite_not_applied` |
| Chapter 5 / 第五章 / analysis chapter | 45% | `rewrite_not_applied` |
| Conclusion / 结论 | 45% | `rewrite_not_applied` |
| Other red/orange paragraph | 35% | `rewrite_not_applied` |

Diff ratio is a heuristic character-level difference between the original target paragraph and patched paragraph. It is not a detector score.

## Failure Rules

Mark `rewrite_application_gate_result = failed` when any condition appears:

- `rewrite_text` is missing.
- `ACADEMIC_TONE_GUARD` failed.
- `patch_status` is not `WRITTEN`.
- `patched_text` is missing or cannot be found after re-reading `document.xml`.
- `patched_text` differs from `rewrite_text` in a material way.
- The original high-risk text still appears in the patched target location.
- `diff_ratio` is below the required threshold.
- The paragraph is only synonym replacement or shallow rewrite.
- Abstract, theoretical basis, Chapter 5, or conclusion still contains template residue.

If a paragraph cannot be changed because factual evidence is missing or protected content prevents deeper rewriting, do not keep the original text silently. Output `material_gap_table` and mark the paragraph as blocked.

## Required Output

| replacement_id | section | original_text_excerpt | rewrite_text_excerpt | patched_text_excerpt | diff_ratio | threshold | patch_status | gate_result |
|---|---|---|---|---|---:|---:|---|---|

## Status Values

- `passed`: rewrite exists, was patched, and passes diff/template checks.
- `rewrite_not_applied`: rewrite was generated but not reflected in DOCX body text.
- `patch_not_applied`: `document.xml` hash did not change.
- `patch_mismatch`: patched text differs from intended rewrite text.
- `patch_ineffective`: patch occurred, but the patched paragraph still keeps the original template skeleton or high-risk residue.
- `shallow_rewrite`: text changed but structure stayed too close.
- `synonym_rewrite_only`: only a few words changed.
- `material_gap`: evidence is insufficient for safe rewriting.

Any `rewrite_not_applied`, `patch_not_applied`, `patch_mismatch`, `patch_ineffective`, `shallow_rewrite`, or `synonym_rewrite_only` status in a red/orange target forces `FIRST_PASS_FAILURE` unless the paragraph is explicitly blocked by `material_gap_table` for author evidence.

## Relation To SKILL.md

Run this gate after `CONTROLLED_HUMANIZATION_ENGINE` and before `TEMPLATE_RESIDUE_DETECTOR`, `AIGC_REGRESSION_GUARD`, and `FIRST_PASS_EFFECTIVENESS_GATE`.
