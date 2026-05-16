# v0.8.3 Three-Mode File Workflow Cases

## Case 1: Similarity Report Provided

Input:

```yaml
mode: similarity_only
has_similarity_report: true
colors: red, orange, purple, black
```

Expected:

- Use report-driven similarity workflow.
- Red and orange fragments are primary targets.
- Purple is light cleanup.
- Black/gray/white fragments are frozen.
- Character delta guard is enabled.

## Case 2: AIGC Report Provided

Input:

```yaml
mode: aigc_only
has_aigc_report: true
red: above_70
orange: 60_to_70
purple: 50_to_60
black: below_50
```

Expected:

- Use report-driven AIGC workflow.
- Analyze why each red/orange fragment has its color.
- Internally self-audit whether revised text is closer to purple/black level.

## Case 3: No Report

Input:

```yaml
mode: aigc_only
has_aigc_report: false
```

Expected:

- Use heuristic diagnosis.
- State that a report would improve localization.
- Do not invent report colors or percentages.

## Case 4: Dual Revision

Input:

```yaml
mode: dual
has_similarity_report: true
has_aigc_report: true
```

Expected:

- Run similarity-oriented processing first.
- Then run AIGC-oriented processing.
- Dual-risk paragraphs are prioritized.
- Character delta guard remains enabled.

## Case 5: Character Delta

Input:

```yaml
original_chars: 10000
revised_chars: 11200
```

Expected:

- Mark `CHARACTER_DELTA_FAIL`.
- Required range is 9000 to 11000.
- Run compression before completion.

## Case 6: File Input

Input:

```yaml
input_type: docx_file
file: thesis.docx
```

Expected:

- Do not edit `thesis.docx` directly.
- Create a copied file.
- Extract target text from the copy.
- Write safe revisions back to corresponding locations in the copy.
- Preserve original document format as much as possible.

## Case 7: Low-Confidence Mapping

Input:

```yaml
mapping_confidence: LOW
```

Expected:

- Do not write back automatically.
- Request user confirmation or more context.
