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
