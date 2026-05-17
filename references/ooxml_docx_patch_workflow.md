# OOXML DOCX Patch Workflow

## Purpose

`OOXML_DOCX_PATCH_WORKFLOW` modifies DOCX files by directly editing the underlying OOXML structure, preserving maximum formatting fidelity. It replaces the older approach of reading full text and regenerating the entire DOCX, which destroyed styles, headers, footers, footnotes, images, and numbering.

## When To Use

Use this workflow when:

- Input is a DOCX file.
- User requires format preservation.
- Changes are limited to paragraph-level text replacement.
- The mapping between original and revised text is confirmed.

Do NOT use when:

- User explicitly requests plain-text output.
- The DOCX is password-protected or corrupted.
- The changes require restructuring the document layout.

## Core Principles

1. **Never modify the original file.** Always work on a copy.
2. **Never rebuild the entire DOCX.** Only modify confirmed text nodes.
3. **Preserve everything else:** styles.xml, numbering.xml, headers, footers, footnotes, endnotes, comments, media, rels, table structures, formulas, fields, table of contents.
4. **Only replace `w:t` text nodes** that have confirmed high-confidence mappings.
5. **Low-confidence mappings are NOT written back.** They are output for human review.
6. **Duplicate matches must stop writeback.** If one source fragment maps to multiple locations, list all candidates and halt.

## Workflow

### Step 1: Copy and Unzip

```bash
cp original.docx copy.docx
mkdir -p /tmp/docx_work
cd /tmp/docx_work
unzip copy.docx
```

The unzipped structure contains:
```
word/
  document.xml          ← main body (modify this only)
  styles.xml            ← DO NOT TOUCH
  numbering.xml         ← DO NOT TOUCH
  header1.xml           ← DO NOT TOUCH
  footer1.xml           ← DO NOT TOUCH
  footnotes.xml         ← DO NOT TOUCH
  endnotes.xml          ← DO NOT TOUCH
  comments.xml          ← DO NOT TOUCH
  media/                ← DO NOT TOUCH
  _rels/                ← DO NOT TOUCH
  theme/                ← DO NOT TOUCH
[Content_Types].xml     ← DO NOT TOUCH
_rels/                  ← DO NOT TOUCH
```

### Step 2: Parse document.xml

Extract paragraph nodes with their `w:pPr` (paragraph properties) and `w:r/w:t` (run text) content.

For each paragraph, record:
- `w:pPr` attributes (style, numbering, alignment, spacing)
- All `w:r` runs with their `w:rPr` (run properties: bold, italic, font, size, color)
- The concatenated text of all `w:t` nodes in the paragraph

### Step 3: Match Revised Text To Paragraphs

For each revised text fragment:

1. Find the paragraph in document.xml whose text matches the original fragment.
2. Verify the match is unique (n-gram check).
3. If multiple paragraphs match → STOP, list candidate_locations.
4. If match confidence is LOW → skip, output for human review.
5. If match confidence is HIGH → proceed to replacement.

### Step 4: Replace Text In Place

Replace ONLY the `w:t` node content. Preserve:
- All `w:rPr` (bold, italic, font, size, color)
- All `w:pPr` (style, numbering, alignment, spacing)
- The run/paragraph structure

If the revised text is longer or shorter than the original, adjust `w:t` content only. Do NOT add or remove `w:r` or `w:p` nodes unless the mapping explicitly requires it.

### Step 5: Repackage

```bash
cd /tmp/docx_work
zip -r ../copy_revised.docx . -x ".*"
```

### Step 6: Validate

After repackaging:

1. **Structural integrity:** Verify the zip is valid and contains all expected files.
2. **No duplicate insertion:** Check that no 100+ character segment appears more than twice in document.xml.
3. **Resource preservation:** Verify styles.xml, numbering.xml, headers, footers, footnotes, endnotes, comments, media, and rels are unchanged.
4. **Page count:** If page count increases by >10%, flag FORMAT_REGRESSION_RISK.
5. **document.xml well-formedness:** Verify XML is parseable.

### Step 7: Output Patch Log

```markdown
## OOXML Patch Log

| replacement_id | paragraph_location | original_text | revised_text | confidence | writeback_status |
|---|---|---|---|---|---|
| 1 | word/document.xml § body § p[42] | ... | ... | HIGH | WRITTEN |
| 2 | word/document.xml § body § p[87] | ... | ... | LOW | SKIPPED |
| 3 | word/document.xml § body § p[103] | ... | ... | HIGH | MULTI_MATCH_STOP |

### Validation Summary
- zip_integrity: OK / FAIL
- duplicate_insertion_risk: NONE / DETECTED
- resource_preservation: OK / FAIL
- page_count_change: +N / -N / 0
- format_regression_risk: NONE / DETECTED
- xml_wellformed: OK / FAIL
```

## Confidence Levels

| level | criteria | action |
|---|---|---|
| HIGH | Unique n-gram match (≥5 consecutive words), same paragraph context, no ambiguity | Write back |
| MEDIUM | Unique substring match, context mostly clear | Write back if user permits; otherwise skip |
| LOW | Partial match, ambiguous context, or match in header/footer/table cell | Skip, output for human review |
| DUPLICATE | Same text matches multiple paragraph locations | STOP writeback, list candidates |

## Safety

- Never modify styles.xml, numbering.xml, headers, footers, footnotes, endnotes, comments, media, or rels.
- Never add new paragraphs or runs unless the mapping explicitly requires it and confidence is HIGH.
- Never silently choose one location when multiple matches exist.
- Always output the patch log for review.
- If any validation step fails, do not deliver as completed.

## Relation To SKILL.md

This workflow is the default DOCX writeback method when format preservation is required. It replaces full-document regeneration. Use after `FILE_INPUT_COPY_WORKFLOW` creates the initial copy.
