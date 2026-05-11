# Sentence-Level Diagnosis

Sentence-level diagnosis is used when paragraph-level guidance is too coarse.

## Step 1: Split Paragraphs

Assign IDs:

- Paragraphs: `P-001`, `P-002`, `P-003`.
- Sentences within paragraph: `S1`, `S2`, `S3`.

Keep formulas, code blocks, tables, and references intact when splitting.

## Step 2: Label Each Sentence

For each sentence, assign:

- AIGC labels.
- Similarity labels.
- Protection labels.
- Risk level: low, medium, high, or no-edit.
- Suggested action.

Protection labels override rewrite labels.

## Step 3: Classify Action

Use these action classes:

| Action | Meaning |
| --- | --- |
| 可改写 | Risk is clear and protected content is limited |
| 轻改 | Risk exists but terms/citations need preservation |
| 不建议改写 | Protected material dominates |
| 保留引用 | Citation boundary is essential |
| 人工确认 | The sentence may affect data, law, standard text, or conclusion |

## Output Template

```markdown
段落编号：P-003
综合风险：高
建议模式：DUAL_OPTIMIZATION
建议强度：L2

句子级定位：
- S1：[AI-模板化起笔][查重-背景套话] 建议中度改写
- S2：[AI-机械连接][风险中] 建议轻度调整
- S3：[保护-术语密集][不建议大改] 保留技术术语
- S4：[AI-泛化结尾][查重-常见结论表达] 建议重写

处理建议：
- 可改写句：
- 轻改句：
- 不建议改写句：
- 需要保留引用句：
- 涉及术语/公式/代码保护句：
```

## Common Sentence-Level Decisions

- A sentence with `AI-模板化起笔` and no protection labels can usually be rewritten at L2.
- A sentence with `查重-定义重复` and `保护-经典定义` should usually be kept or lightly reframed around explanatory prose.
- A sentence with `保护-公式`, `保护-代码`, or `保护-LaTeX命令` should not be rewritten directly.
- A sentence with `查重-来源边界不清` should request citation review instead of inventing a source.
- A sentence with experimental values should preserve values and only improve explanation.

## Sentence-Level Scoring

Use sentence scoring only to support localization:

| Sentence | AIGC Risk | Similarity Risk | Protection | Action |
| --- | ---: | ---: | --- | --- |
| S1 | 78 | 64 | 否 | 可改写 |
| S2 | 44 | 30 | 术语 | 轻改 |
| S3 | 20 | 72 | 经典定义 | 不建议改写 |

Do not average sentence scores into a claim about external detection systems.
