# First-Pass Failure: Color Migration Case

## Case Origin

Real test failure from a human resource management thesis:
- Thesis: 《数智化时代 A 电商公司招聘管理优化研究》
- Original AIGC: 76.67%
- Post-first-pass AIGC: ~68.6%
- Result: FIRST_PASS_FAILURE — red-to-orange migration, orange plateau formed

## Input Data

### Original Report Color Distribution

| band | threshold | chars | percentage |
|---|---|---|---|
| red | >=70% AIGC suspicion | 8601 | 39.4% |
| orange | 60%-70% | 5311 | 24.4% |
| purple | 50%-60% | 692 | 3.2% |
| black | <50% | 1502 | 6.9% |
| **total analyzed** | — | **16106** | **73.9%** (rest is cover/toc/references) |

- Original AIGC overall: **76.67%**
- Red + Orange combined: **63.8%**

### Post-First-Pass Report Color Distribution

| band | threshold | chars | percentage |
|---|---|---|---|
| red | >=70% AIGC suspicion | 3027 | 13.6% |
| orange | 60%-70% | 9376 | 42.3% |
| purple | 50%-60% | 905 | 4.1% |
| black | <50% | 3237 | 14.6% |
| **total analyzed** | — | **16545** | **74.6%** |

- Post-first-pass AIGC overall: **68.6%**
- Red + Orange combined: **55.9%**

## Expected Gate Verdict

### FIRST_PASS_EFFECTIVENESS_GATE Conditions

| condition | original | post-first-pass | verdict |
|---|---|---|---|
| 1. AIGC > 60% | 76.67% | 68.6% | **FAIL** — still above 60% |
| 2. Red+Orange > 40% | 63.8% | 55.9% | **FAIL** — combined still > 40% |
| 3. Orange rose > 10pp | 24.4% | 42.3% (+17.9pp) | **FAIL** — orange share surged |
| 4. Red→Orange migration | red 39.4%→13.6% | orange 24.4%→42.3% | **FAIL** — red dropped but orange accumulated |
| 5. Key sections still red/orange | — | to verify | **CHECK** |
| 6. Black < 25% | 6.9% | 14.6% | **FAIL** — black still below 25% |
| 7-8. Processing records | — | to verify | **CHECK** |

### Final Verdict

**FIRST_PASS_FAILURE**

Reasons:
1. **红转橙，橙色平台期**: Red decreased by 25.8pp (39.4% → 13.6%), but orange surged by 17.9pp (24.4% → 42.3%). The mass of risk was not eliminated — it was transferred.
2. **AIGC 降幅不足**: Overall AIGC only dropped 8.07pp (76.67% → 68.6%). Still above 60%.
3. **黑色占比不足**: Black coverage at 14.6% is far below the 25% minimum threshold.

### Color Migration Assessment

| band | original | post-first-pass | delta | assessment |
|---|---|---|---|---|
| red | 39.4% | 13.6% | -25.8pp | reduced — but mostly to orange, not black |
| orange | 24.4% | 42.3% | +17.9pp | SURGED — red-to-orange migration |
| purple | 3.2% | 4.1% | +0.9pp | stable |
| black | 6.9% | 14.6% | +7.7pp | improved but insufficient |

**Color migration conclusion**: 红转橙，未突破

## Expected Output

### 1. Diagnosis

```
FIRST_PASS_FAILURE
Cause: 红转橙，橙色平台期
AIGC delta: 76.67% → 68.6% (-8.07pp)
Conclusion: 失败，需要二轮
```

### 2. Must NOT Output

- ❌ "完成" or "COMPLETED" in final status.
- ❌ "有效" in any summary text.
- ❌ "红橙均已处理" — because red→orange migration means processing was incomplete.
- ❌ "可通过" or "可交付".

### 3. Must Route To

```
AIGC_PLATEAU_BREAKER
```

With priority sections:
- Abstract (摘要)
- Theoretical Basis 2.1/2.2 (理论基础)
- Chapter 5 / Analysis Chapter (第五章/实证分析)
- Conclusion (结论)

### 4. Must Output Material Gap Table

At minimum, the following gaps should be identified:

| section | missing_evidence | why_needed |
|---|---|---|
| 摘要 | thesis-specific data to replace background opening | current abstract starts with generic趋势 |
| 2.1 理论基础 | which theory dimension is specifically used | paragraph is encyclopedia definition |
| 第五章 | specific survey findings per dimension | analysis is generic "问题→原因" template |
| 结论 | unresolved problems and boundaries | conclusion is achievement-list style |

### 5. FINAL_ACCEPTANCE_AUDIT Status

| item | expected result |
|---|---|
| final status | FIRST_PASS_FAILURE |
| color migration assessment | 红转橙，未突破 |
| first-pass effectiveness gate | FIRST_PASS_FAILURE |
| conclusion text | 失败，需要二轮 |

## Testing Steps

1. Feed the input color distributions into `FIRST_PASS_EFFECTIVENESS_GATE`.
2. Verify each of the 8 conditions produces the expected verdict.
3. Verify the color migration table matches the expected assessment.
4. Verify the gate routes to `AIGC_PLATEAU_BREAKER`.
5. Verify the final status is `FIRST_PASS_FAILURE` with conclusion "失败，需要二轮".
6. Verify no output contains "完成", "有效", or "COMPLETED".

## Expected Processing Record Check

For this failure case, the processing record should reveal:

| check | expected finding |
|---|---|
| red paragraph minimum target (purple/black) reached? | NO — most red only demoted to orange |
| orange paragraph minimum target (black/near-black) reached? | NO — orange share increased |
| A/B/C/D action type recorded per paragraph? | should verify |
| social-science bottleneck enabled? | MUST be YES for HR management thesis |
| evidence pack requested? | should verify |
| anti-consulting-speak check triggered? | should verify in plateau breaker phase |
