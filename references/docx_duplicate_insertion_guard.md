# DOCX Duplicate Insertion Guard

## Purpose

`DOCX_DUPLICATE_INSERTION_GUARD` prevents the failure mode observed in older Skill versions where the same paragraph text was inserted multiple times into a DOCX file, causing page count explosion, format confusion, and unreadable output.

## Real Failure Case

In older version bff6860, a human resource management thesis experienced this failure:

- Section 5.2 paragraph "工具优化的目标是让系统从记录工具变成决策辅助……" was inserted into multiple locations across several pages.
- The document grew from ~30 pages to ~45+ pages.
- Formatting became inconsistent and unreadable.

## Rules

### Rule 1: One Replacement Per ID

Each `replacement_id` can only write back to ONE confirmed target location. If the same revised text needs to appear in multiple locations, each must have a separate `replacement_id` with explicit confirmation.

### Rule 2: Stop On Duplicate Match

If one original text fragment matches multiple paragraph locations in document.xml:

1. List all `candidate_locations` with their paragraph indices.
2. STOP writeback immediately.
3. Output a `DUPLICATE_MATCH_WARNING`.
4. Request human review to confirm which location is correct.

### Rule 3: Post-Writeback N-Gram Check

After all writebacks are complete:

1. Extract all paragraphs from document.xml.
2. For every paragraph of 100+ characters, check if the same text appears more than twice.
3. If a 100+ character segment repeats more than twice → flag `DUPLICATE_INSERTION_RISK`.

### Rule 4: Page Count Anomaly Check

Compare the page count of the patched file against the original:

1. If page count increases by more than 10% → flag `FORMAT_REGRESSION_RISK`.
2. If page count decreases by more than 10% → also flag `FORMAT_REGRESSION_RISK`.

### Rule 5: No Silent Duplication

Never:

- Copy a revised paragraph into multiple locations without explicit per-location confirmation.
- Assume that because a source fragment appears in multiple places, all instances should be replaced.
- Write back a mapping when the match count exceeds the expected count.

## Output

```markdown
## Duplicate Insertion Guard Report

| check | result | details |
|---|---|---|
| duplicate_match_warnings | count | <list of replacement_ids with multiple candidate locations> |
| post_writeback_ngram_check | PASS / FAIL | <details of any repeated segments> |
| page_count_original | <N> |  |
| page_count_patched | <N> |  |
| page_count_change_pct | <±N%> |  |
| format_regression_risk | NONE / DETECTED |  |
| duplicate_insertion_risk | NONE / DETECTED |  |
```

## Failure Handling

If `DUPLICATE_INSERTION_RISK` is detected:

1. Do NOT deliver the file as completed.
2. Set `final_delivery_status = FORMAT_FAILURE`.
3. List the duplicated segments and their locations.
4. Offer to re-run with stricter matching or manual location confirmation.

If `FORMAT_REGRESSION_RISK` is detected:

1. Do NOT deliver the file as completed.
2. Set `final_delivery_status = FORMAT_FAILURE`.
3. Compare the original and patched files to identify the cause.

## Relation To SKILL.md

This guard runs as part of `OOXML_DOCX_PATCH_WORKFLOW` validation. Its result is checked by `FIRST_PASS_EFFECTIVENESS_GATE` and `FINAL_ACCEPTANCE_AUDIT`.
