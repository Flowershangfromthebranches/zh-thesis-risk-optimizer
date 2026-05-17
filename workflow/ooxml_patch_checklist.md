# OOXML Patch Checklist

Use this checklist before and after every OOXML DOCX patch operation.

## Pre-Patch Checklist

- [ ] Original file is not modified; copy was created.
- [ ] Copy was unzipped successfully.
- [ ] word/document.xml exists and is well-formed XML.
- [ ] styles.xml, numbering.xml, headers, footers, footnotes, endnotes, comments, media, and rels are identified.
- [ ] All revised text fragments have a corresponding paragraph match in document.xml.
- [ ] Every match has a confidence level assigned.
- [ ] No LOW-confidence matches are scheduled for writeback.
- [ ] No DUPLICATE matches exist (same text matching multiple locations).
- [ ] Protected items (citations, data, formulas, code, paths, parameters) are preserved in revised text.

## Patch Execution Checklist

- [ ] Only `w:t` nodes are modified.
- [ ] `w:rPr` (bold, italic, font, size, color) are preserved on every modified run.
- [ ] `w:pPr` (style, numbering, alignment, spacing) are preserved on every modified paragraph.
- [ ] No new `w:p` or `w:r` nodes are added unless explicitly required.
- [ ] No existing `w:p` or `w:r` nodes are deleted unless explicitly required.

## Post-Patch Validation Checklist

- [ ] Repackaged zip is valid (can be opened without error).
- [ ] All original files are present in the repackaged zip.
- [ ] styles.xml is unchanged.
- [ ] numbering.xml is unchanged.
- [ ] Headers and footers are unchanged.
- [ ] Footnotes and endnotes are unchanged.
- [ ] Comments are unchanged.
- [ ] Media files (images) are unchanged.
- [ ] Rels files are unchanged.
- [ ] document.xml is well-formed XML after replacement.
- [ ] No 100+ character text segment appears more than twice (duplicate insertion check).
- [ ] Page count did not increase by more than 10%.
- [ ] Patch log is complete and accurate.

## Failure Handling

If any checklist item fails:

1. Do not deliver the patched file as completed.
2. Document the failure in the patch log.
3. For duplicate insertion: list candidate locations and request human review.
4. For resource loss: restore from the original copy and retry with narrower scope.
5. For XML corruption: restore from the original copy and diagnose the cause.
