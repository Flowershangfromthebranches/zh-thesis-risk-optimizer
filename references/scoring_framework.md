# Scoring Framework

This framework defines heuristic writing-risk scores for Chinese thesis revision. Scores are diagnostic hints, not real detection-system results.

## Required Disclaimer

Every scoring output must include:

> 该评分为启发式写作风险评分，仅用于提示文本可能存在的模板化、相似表达和改写优先级问题，不代表知网、维普、万方、Turnitin 或任何商业检测系统的真实结果。

## Score Scale

Use 0-100 only as a relative risk scale:

| Score | Level | Meaning |
| ---: | --- | --- |
| 0-24 | 低 | 当前维度风险较低，通常只需人工通读 |
| 25-49 | 中 | 存在局部风险，可做 L1-L2 调整 |
| 50-74 | 高 | 多处风险集中，应优先处理 |
| 75-100 | 很高 | 风险密度高，但仍需结合保护区和引用边界判断 |

## Overall Score

Overall risk can be reported as a weighted summary:

- AIGC risk score.
- Similarity risk score.
- Dual-optimization priority.
- Protection-zone penalty that lowers automatic rewrite intensity.

Do not calculate false precision. Integer bands are enough.

## AIGC Risk Dimensions

Score these dimensions heuristically:

1. 模板化表达密度。
2. 机械连接词密度。
3. 四字套话与泛化词密度。
4. 句长均匀度。
5. 段落结构过度对称。
6. 泛化结论比例。
7. 模糊归因表达。
8. 绝对化断言。
9. 缺少具体对象、流程、参数或例证。
10. AI 高频表达重复率。

Suggested weighting:

| Dimension | Weight |
| --- | ---: |
| 模板化表达密度 | 12 |
| 机械连接词密度 | 10 |
| 四字套话与泛化词密度 | 10 |
| 句长均匀度 | 8 |
| 段落结构过度对称 | 10 |
| 泛化结论比例 | 12 |
| 模糊归因表达 | 10 |
| 绝对化断言 | 8 |
| 缺少具体对象、流程、参数或例证 | 12 |
| AI 高频表达重复率 | 8 |

## Similarity Risk Dimensions

Score these dimensions heuristically:

1. 定义性重复。
2. 教材式背景表达。
3. 相似源表述过近。
4. 引用密集但转述不足。
5. 常见概念解释重复。
6. 法规、标准、经典定义不可改区域。
7. 专业术语密集但不应误判区域。

Suggested weighting:

| Dimension | Weight |
| --- | ---: |
| 定义性重复 | 18 |
| 教材式背景表达 | 16 |
| 相似源表述过近 | 22 |
| 引用密集但转述不足 | 14 |
| 常见概念解释重复 | 12 |
| 法规、标准、经典定义不可改区域 | 10 |
| 专业术语密集但不应误判区域 | 8 |

The last two dimensions should also generate protection labels and may lower rewrite intensity.

## Dual-Optimization Priority

Score and rank paragraphs by:

1. 同时具备 AIGC 风险和查重风险的段落优先。
2. 长段落优先。
3. 对全文重复率或 AIGC 风险贡献较高的段落优先。
4. 易安全改写的段落优先。
5. 公式、代码、标准定义、必要引用段落降级处理。
6. 摘要、结论、绪论等高可见章节可适当提高优先级。
7. 技术实现、实验数据、公式密集段落必须降低自动改写强度。

Priority levels:

| Level | Meaning |
| --- | --- |
| 高 | 风险高且可安全处理，优先改写 |
| 中 | 有局部风险，建议轻中度处理 |
| 低 | 风险低或保护项较多，谨慎处理 |
| 暂缓 | 保护区、引用原文、数据密集或需要人工确认 |

## Score Output Template

```markdown
## 评分声明
该评分为启发式写作风险评分，不代表任何真实检测系统结果。

## 段落评分
| 位置 | 总体风险 | AIGC风险 | 查重风险 | 双降优先级 | 主要标签 | 建议模式 | 建议强度 |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |

## 评分依据
- AIGC 风险：
- 查重相似风险：
- 保护区：
- 人工核查点：
```

## Before/After Comparison

Use estimated scores after revision:

```markdown
修改前：
- AIGC 风险：82/100
- 查重相似风险：68/100
- 双降优先级：高

修改后：
- AIGC 风险：预计 45/100
- 查重相似风险：预计 39/100
- 剩余风险：引用边界需人工核查
```

Never present the after score as guaranteed.

## Post-Rewrite Self-Audit

After any L3-L5 rewrite, run `references/post_rewrite_aigc_self_audit.md` before finalizing the paragraph.

If three or more AI-like risk items remain, the first rewrite is not sufficient. Run `prompts/mode_second_pass_rewrite.md` and compare the final text with the protected facts and no-change list.

## Report-Driven Scoring

When a report is provided, keep report values and heuristic scores separate:

- Report value: a value copied from the user-provided report.
- Heuristic score: this Skill's writing-risk estimate.

Output them in separate fields. Do not infer report percentages from heuristic scores, and do not claim that a revised heuristic score predicts a future report result.

## Full-Thesis Scoring

For long theses, avoid pretending the entire manuscript has a precise score. Prefer chapter-level and paragraph-level bands:

- Low, medium, high, very high.
- Heatmap rank.
- Suggested mode.
- Protection status.

Use the score to prioritize work, not to promise a target.
