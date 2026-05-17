# OOXML DOCX Patch Workflow Test Cases

## Case 1: Basic Paragraph Text Replacement

**Input:** DOCX with paragraph containing "招聘渠道较为单一" in document.xml.

**Action:** Replace with "问卷显示85%的简历来自传统招聘平台，社交媒体和专业社区合计不到15%".

**Expected:**
- Only the `w:t` node content changes.
- `w:rPr` (font, size, bold, italic, color) preserved.
- `w:pPr` (style, numbering, alignment) preserved.
- styles.xml unchanged.
- numbering.xml unchanged.
- Headers, footers, footnotes, endnotes, comments, media unchanged.

## Case 2: Low-Confidence Mapping Skipped

**Input:** Revised text fragment that partially matches two paragraphs.

**Action:** Attempt writeback.

**Expected:**
- Confidence = LOW or DUPLICATE.
- Writeback skipped.
- Fragment appears in "Skipped for human review" list.
- No modification to document.xml.

## Case 3: Duplicate Match Stops Writeback

**Input:** Same source text appears in paragraph 42 and paragraph 103 of document.xml.

**Action:** Attempt writeback.

**Expected:**
- Writeback stops immediately.
- Both candidate_locations listed.
- DUPLICATE_MATCH_WARNING output.
- Human must confirm which location is correct.

## Case 4: Resource Preservation

**Input:** DOCX with images, headers, footers, footnotes, endnotes, comments, table of contents.

**Action:** Patch 5 paragraphs.

**Expected after patch:**
- All images in word/media/ preserved and unchanged.
- All header XML files preserved and unchanged.
- All footer XML files preserved and unchanged.
- footnotes.xml preserved and unchanged.
- endnotes.xml preserved and unchanged.
- comments.xml preserved and unchanged.
- styles.xml preserved and unchanged.
- numbering.xml preserved and unchanged.
- All rels files preserved and unchanged.

## Case 5: No Duplicate Insertion

**Input:** Section 5.2 paragraph "工具优化的目标是让系统从记录工具变成决策辅助……"

**Action:** Patch with revised text.

**Expected:**
- The revised text appears exactly ONCE in document.xml.
- N-gram check: no 100+ character segment repeats more than twice.
- Page count does not increase by more than 10%.
- DUPLICATE_INSERTION_RISK = NONE.

## Case 6: Page Count Anomaly Detection

**Input:** Original DOCX is 30 pages.

**Action:** Patch 20 paragraphs.

**Expected:**
- Patched DOCX is 30-33 pages (≤10% increase).
- If patched DOCX is 34+ pages → FORMAT_REGRESSION_RISK = DETECTED.
- File not delivered as completed until cause is diagnosed.

## Case 7: XML Well-Formedness

**Input:** Any DOCX after patching.

**Expected:**
- document.xml parses as valid XML.
- No unclosed tags, missing attributes, or encoding errors.
- If XML is malformed → patch failed, restore from original copy.
