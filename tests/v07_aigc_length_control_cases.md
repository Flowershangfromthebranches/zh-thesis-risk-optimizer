# v0.7 AIGC Length Control Cases

## Case 1: Similarity Already OK, AIGC Still High

Input:

```text
查重已经达标，继续降 AIGC
```

Expected:

- `AIGC_FOCUSED_LENGTH_CONTROLLED`.
- Similarity repair downgraded to stability check.

## Case 2: Over-Expansion

Input:

```yaml
original_chars: 17000
revised_chars: 24000
max_added_chars: 2000
```

Expected:

- `LENGTH_BUDGET_FAIL`.
- Enter Compression Pass.

## Case 3: Length-Preserving Rewrite

Input:

- High AIGC paragraph.
- No new evidence.

Expected:

- `CONSERVATIVE_AIGC_REPAIR`.
- No expansion.

## Case 4: Sentence-Level Risk

Input contains:

- 随着...发展
- 实验结果表明
- 具有重要意义

Expected:

- Sentence-level table.
- `HIGH` or `CRITICAL` labels.

## Case 5: Repeated AI Expression

Input:

- Multiple occurrences of "本文设计并实现".
- Multiple occurrences of "提供便捷解决方案".

Expected:

- `REPEATED_EXPRESSION_COMPRESSOR`.

## Case 6: Protected Technical Data

Input contains:

- URL.
- Payload.
- `max_depth`.
- `max_pages`.
- Test result.

Expected:

- Protected items preserved exactly.
- Only surrounding prose may be revised.
