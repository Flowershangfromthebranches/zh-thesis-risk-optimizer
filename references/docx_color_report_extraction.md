# DOCX Color Report Extraction

## Purpose

Use this reference when the user provides a Word / DOCX AIGC or similarity report whose risk levels are expressed through font colors or color-marked text.

Plain-text extraction is not enough for these reports. Tools such as `textutil`, copy-paste, or normal DOCX-to-TXT conversion can preserve the words but lose the color metadata. If the color metadata is lost, report-driven routing becomes unreliable and the Skill may rewrite the wrong paragraphs.

## Activation Conditions

Use this workflow when:

- The user provides a `.docx` report.
- The report contains red, orange, purple, black, gray, or other color-coded text.
- The user says the report marks AIGC risk or similarity risk by color.
- Plain-text extraction shows the report text but no risk labels.

## Required Extraction Fields

For each colored run or merged colored fragment, extract:

| field | meaning |
|---|---|
| `paragraph_index` | paragraph position in the report document |
| `full_paragraph_text` | complete paragraph text for mapping |
| `colored_text` | text span carrying a color |
| `font_color_hex` | raw OOXML color value, such as `F12828` |
| `inferred_band` | red / orange / purple / black / gray / unknown |
| `source_context` | nearby text before and after the colored span |
| `mapping_confidence` | HIGH / MEDIUM / LOW / UNMAPPED after mapping to source |

## OOXML Color Sources

For DOCX reports, inspect `word/document.xml` and check:

- `w:rPr/w:color @w:val`
- `w:rPr/w:highlight @w:val`
- `w:rPr/w:shd @w:fill`
- style-level color only when run-level color is absent

Do not rely only on visible text extraction.

## Common Color Values

The following values are common in some reports, but they must be verified against the user's report legend:

| hex color | possible meaning |
|---|---|
| `F12828` | red / high AIGC suspicion |
| `F39800` | orange / medium AIGC suspicion |
| `9D91E9` | purple / light AIGC suspicion |
| `000000` | black / low-risk normal text |
| `B0B0B0` | gray / non-scored or excluded text, such as too-short fragments, headings, English abstract/text, references, or template pages |

If the report uses different colors, record the raw hex values and ask the user or mark the legend as uncertain. Do not invent thresholds.

## Workflow

1. Create a file-processing copy if the user asks for file output.
2. Extract the report's color-coded runs from the DOCX XML.
3. Merge adjacent runs with the same color inside the same paragraph.
4. Count characters by color band.
5. Build a red/orange task table before rewriting.
6. Map each colored fragment back to the original thesis text.
7. After mapping confidence is assigned, route through `THREE_MODE_COLOR_BAND_WORKFLOW`.
8. If the input is original thesis plus original report, overlay `FIRST_PASS_RED_ORANGE_ENGINE`.
9. If the input is current draft plus current report, overlay `CURRENT_REPORT_RED_ORANGE_ENGINE`.
10. For similarity-only work, use `task_type = similarity_only` inside `THREE_MODE_COLOR_BAND_WORKFLOW`.
11. Freeze black, gray, reference, declaration, and school-template areas unless the user explicitly asks otherwise. Gray is not a rewrite target; it is recorded as non-scored/excluded text.

## Failure Mode

If the agent flattens a DOCX report to plain text and loses color metadata, the following failures are likely:

- Red and orange fragments are not prioritized.
- Black or gray paragraphs may be rewritten unnecessarily.
- The agent treats the report as another copy of the thesis.
- AIGC reduction appears random or may increase after revision.

If color metadata cannot be extracted, stop report-driven processing and ask the user to provide:

- the report color legend,
- copied red/orange fragments,
- screenshots with OCR text,
- or a report export that keeps risk labels.

## Safety

Do not fabricate report colors, percentages, or risk bands. Use only the colors, text, and legends available in the user-provided report.

## Relation To SKILL.md

Load this file before color-band AIGC or similarity work when the input report is a color-marked DOCX. After extraction and mapping, continue through `THREE_MODE_COLOR_BAND_WORKFLOW` and the appropriate red-orange engine.
