# Rewrite Application Gate Cases

## Case 1: Generated Rewrite Was Not Patched

Input:

- Red/orange target paragraph has `rewrite_text`.
- OOXML patch log has no matching `replacement_id`.
- Re-read `document.xml` still contains the original paragraph.

Expected:

- `rewrite_application_gate_result = failed`
- `gate_result = rewrite_not_applied`
- `final_delivery_status = REWRITE_NOT_APPLIED_FAILURE`
- Must not output `COMPLETED`.

## Case 2: Patch Hash Did Not Change

Input:

- `original_text_hash == patched_text_hash`
- `patch_status = WRITTEN`

Expected:

- `patch_status = patch_not_applied`
- `rewrite_application_gate_result = failed`
- Must re-run `OOXML_DOCX_PATCH_WORKFLOW`.

## Case 3: Diff Ratio Too Low

Input:

- Section: 摘要
- `diff_ratio = 18%`
- Threshold: 45%
- Only several words changed.

Expected:

- `rewrite_not_applied`
- `shallow_rewrite = true`
- `synonym_rewrite_only = true`
- Must re-enter `CONTROLLED_HUMANIZATION_ENGINE`.

## Case 4: Protected Content Blocks Deep Rewrite

Input:

- Red/orange paragraph contains necessary cited definition and protected data.
- Diff ratio cannot safely reach threshold without changing facts.

Expected:

- `material_gap_table` is required.
- Do not fabricate missing facts.
- Do not mark `COMPLETED`.
