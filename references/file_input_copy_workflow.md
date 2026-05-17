# File Input Copy Workflow

## Purpose

This workflow defines how the Skill should handle file input while preserving the original file and its formatting.

It applies to Word documents, plain text files, Markdown files, LaTeX files, and other thesis files provided by the user.

## Core Rule

Never modify the original file directly.

Always:

1. Create a copy of the original file.
2. Extract text from the copy for diagnosis and revision.
3. Rewrite only confirmed target text.
4. Write changes back to the corresponding locations in the copy.
5. Deliver the copy as the final file.

## File-Type Handling

### Plain Text / Markdown

- Create a copied file with a clear suffix such as `_revised`.
- Preserve headings, lists, code fences, citations, and table syntax.
- Replace only mapped text ranges.

### Word / DOCX

- Create a copied DOCX before editing.
- Preserve original styles, headings, tables, numbering, images, comments, footnotes, and references where possible.
- Prefer local text replacement over full-document regeneration.
- Do not flatten a DOCX into plain text unless the user explicitly asks for plain-text output.
- If visual QA is required and LibreOffice is available, render the copied DOCX and inspect it.

#### DOCX Writeback Priority

When the input is DOCX and format preservation is required, use this priority:

1. **OOXML confirmed paragraph patch** (via `OOXML_DOCX_PATCH_WORKFLOW`): directly edit `word/document.xml` text nodes while preserving all styles, numbering, headers, footers, footnotes, endnotes, comments, media, and rels. This is the default and preferred method.
2. **python-docx run-level patch**: only for simple files where OOXML approach is not available. Limited to simple formatting.
3. **Full-document regeneration**: ONLY if the user explicitly requests it AND accepts format risk. Must warn: "全文重建可能导致格式丢失，包括样式、页眉页脚、脚注、批注、目录、图片和编号。"

Never use full-document regeneration as the default. Always attempt OOXML patch first.

### LaTeX

- Create a copied `.tex` file.
- Do not alter commands, labels, citations, equations, bibliography keys, environments, or package declarations unless explicitly requested.
- Revise surrounding prose only.

## Mapping Back To The Copy

For every revised fragment, maintain:

| id | source_location | original_text | revised_text | mapping_confidence | protected_items | writeback_status |
|---|---|---|---|---|---|---|

Rules:

- `HIGH` mapping can be written back.
- `MEDIUM` mapping can be written back if the context is clear and the user did not ask for manual review.
- `LOW` or `UNMAPPED` must not be written back without user confirmation.
- If a fragment appears multiple times, list all locations instead of silently choosing one.

## Format Preservation Rules

- Preserve the original file extension.
- Preserve the document structure.
- Preserve citations, footnotes, endnotes, bibliography entries, formulas, code blocks, table structures, figure/table numbers, paths, parameters, and field names.
- Do not change school templates, declarations, reference entries, or report text unless explicitly requested.

## Output Requirements

When file input is used, output:

```markdown
## File Handling
- original_file:
- copied_file:
- original_untouched: yes
- format_preservation_notes:

## Writeback Table

## Character Delta Table

## Final Deliverable
```

## Safety

If the agent cannot preserve formatting or cannot confidently map revised text back to the copy, it must stop and ask for confirmation instead of overwriting content.

## Relation To SKILL.md

Use this workflow whenever the user provides a file instead of plain text.
