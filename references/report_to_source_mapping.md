# Report-to-Source Mapping

Mapping links a report fragment back to the user's thesis text. Do not rewrite until the mapping is clear enough and protected zones are checked.

## Exact Match

Use exact matching when the report fragment and the thesis text are identical.

Output:

- 原文章节。
- 原文段落编号。
- 报告片段。
- 前后文。
- 映射置信度：HIGH。

## Normalized Match

Use normalized matching when differences are limited to:

- Full-width/half-width characters.
- Spaces.
- Line breaks.
- Punctuation.
- Sentence segmentation.
- Simplified/traditional Chinese.
- Report omission of part of a sentence.

Output:

- 映射置信度：MEDIUM。
- Explain the normalization basis.
- Preserve citations and protected terms.

## Keyword Match

Use keyword matching when the report fragment is incomplete but includes multiple terms, phrase skeletons, or distinctive wording.

Output:

- 映射置信度：LOW。
- Do not directly rewrite.
- Request user confirmation or mark "需人工确认".

## Multiple Matches

When the same fragment appears in multiple positions:

- List all possible positions.
- Do not choose only one.
- Mark "多处匹配".
- Ask the user to confirm the priority location.
- If all positions repeat the same issue, group them for batch handling.

## Unmapped

When the position cannot be confirmed:

- Mark `UNMAPPED`.
- Do not fabricate a location.
- Do not force a rewrite.
- Ask the user to provide source context.

## Mapping Output

```markdown
| 编号 | 报告片段 | 可能位置 | 前后文 | 映射方式 | 映射置信度 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
```
