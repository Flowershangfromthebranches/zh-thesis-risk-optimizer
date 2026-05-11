# Mapping Confidence Rules

Use confidence levels to avoid over-editing report fragments that cannot be reliably located in the source text.

## HIGH

Use `HIGH` when:

- The report fragment and source text are identical.
- Or the only differences are spaces, line breaks, or punctuation.

Action:

- Direct targeted diagnosis is allowed.
- Revision is allowed if no protected zone blocks it.

## MEDIUM

Use `MEDIUM` when:

- The report fragment omits part of the sentence.
- Report sentence segmentation differs from the thesis text.
- Normalization is needed for full-width/half-width characters, simplified/traditional Chinese, or punctuation.

Action:

- Targeted revision is allowed with a mapping explanation.
- Preserve citations and protected terms.
- Mention that manual review is still recommended.

## LOW

Use `LOW` when:

- The position can only be inferred from keywords, terms, or sentence fragments.

Action:

- Do not directly rewrite.
- Mark human confirmation required.
- Ask for source context or paragraph number.

## UNMAPPED

Use `UNMAPPED` when:

- No source position can be found.

Action:

- Do not force a rewrite.
- Do not fabricate position, percentage, source, or risk level.
- Ask the user to provide the original paragraph or surrounding context.

## Output

```markdown
| 报告片段 | 映射置信度 | 依据 | 是否可直接改写 | 下一步 |
| --- | --- | --- | --- | --- |
```
