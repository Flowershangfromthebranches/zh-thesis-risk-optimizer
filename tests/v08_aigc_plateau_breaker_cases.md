# v0.8 AIGC Plateau Breaker Cases

## Case 1: Red Down, Orange Still High

Input:

```yaml
red_trend: sharply_down
orange_trend: still_high
overall_aigc: slow_decrease
```

Expected:

- Enter `AIGC_PLATEAU_BREAKER`.
- Use `ORANGE_PLATEAU_PASS`.
- Do not run another normal rewrite.

## Case 2: Three Rounds With Diminishing Returns

Input:

```yaml
original: 76
round_1: 65
round_2: 57
round_3: 54
```

Expected:

- `NO_PROGRESS_REWRITE_LOOP`.
- Diagnose bottleneck before another rewrite.

## Case 3: Management Template Plateau

Input contains:

- 第一，第二，第三.
- 流程、工具、团队、渠道.
- Survey percentages.

Expected:

- `MANAGEMENT_TEMPLATE_PLATEAU`.
- Break enumeration and anchor with local evidence.

## Case 4: Computer Protected Plateau

Input contains:

- Code.
- API path.
- Table name.
- Parameter.
- Test result.

Expected:

- `TECHNICAL_PROTECTED_PLATEAU` when only protected prose remains.
- Modify only surrounding explanation.

## Case 5: White Paragraph Freeze

Input:

- Low-risk paragraph mixed with orange paragraphs.

Expected:

- `WHITE_FREEZE`.
- Do not rewrite low-risk paragraphs.
