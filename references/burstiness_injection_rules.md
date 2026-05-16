# Burstiness Injection Rules

## Purpose

Burstiness injection is a rhythm-repair technique for AIGC-risk revision. It is useful when a paragraph is too smooth, too symmetrical, or too uniform in sentence length.

It is not a universal solution. In management, HR, education, business, and other social-science theses, a paragraph can already have varied sentence lengths and still be marked red/orange because the deeper issue is template skeleton, abstract management language, or underused local evidence.

This file provides rules for auditing and repairing rhythm when rhythm is the actual problem.

## Detection原理

| 维度 | AI文本 | 人类文本 |
|------|--------|---------|
| 困惑度 | 低且稳定 | 高且波动大 |
| 突发度 | 句长均匀（25-40字/句） | 长短交替（8字~50字） |
| 结构模式 | 段落对称、总分总 | 长短不一、有跳跃 |

## Core Metric: Sentence Length Standard Deviation

Target: sentence-length standard deviation (σ) should normally be above 10 within each rewritten paragraph, but this target is a diagnostic aid, not a completion guarantee.

AI-typical paragraph: 28, 32, 30, 35, 29 (σ ≈ 2.5)
Human-typical paragraph: 12, 38, 8, 45, 22, 15 (σ ≈ 14)

## Burstiness Gate

Before applying rhythm repair, classify the paragraph:

| condition | action |
|---|---|
| Sentence lengths are uniform, connectors are dense, and the paragraph is red/orange | Apply burstiness repair. |
| Sentence lengths are already varied but the paragraph is still red/orange | Do not add more short sentences; switch to template-skeleton repair, evidence placement, or anti-formalization repair. |
| The paragraph is a theory definition, citation-heavy paragraph, legal/policy wording, or school template | Preserve the protected text and revise only surrounding explanation. |
| The paragraph belongs to HR/management/social science and uses "问题 -> 原因 -> 对策" or numbered countermeasures | Break the template skeleton before adding rhythm variation. |

## Controlled Burstiness Rules

### 1. Sentence Length Variation

When rhythm repair is needed, the paragraph should contain:

- At least one short sentence (8-15 chars)
- At least one medium sentence (20-30 chars)
- At least one longer sentence (35-50 chars) when the content supports it

Avoid three or more consecutive sentences in the 25-35 char range when it can be changed without damaging academic clarity.

### 2. Short Sentence Placement

Place short sentences at these positions for maximum effect:

- After a long explanation sentence (contrast rhythm)
- At the start of a new argument point (attention signal)
- Before a data or evidence sentence (setup signal)
- As a standalone judgment or observation

Examples:

```text
原句（AI风）：该企业在招聘渠道方面存在较为单一的问题，主要依赖传统招聘平台，社交媒体渠道的利用程度较低。
改写（保持正式语气）：问卷结果显示，传统平台贡献了85%以上的简历来源，社交媒体和专业社区合计不到15%。渠道结构偏窄，这是后续招聘触达不足的直接表现。
```

### 3. Connector Reduction

Delete or reduce these mechanical connectors. Replace with object relationships, conditions, or direct statements.

Must-delete connectors (appear > 3 times per chapter):

- 首先...其次...再次...最后
- 此外/另外
- 因此/因而/由此
- 综上所述/总之
- 与此同时
- 然而/但是（保留1-2次自然使用）
- 不仅...而且

Replacement strategies:

- "首先" → delete, start directly with the point
- "其次" → delete, or use a concrete transition like "在此基础上"/"进一步来看"
- "因此" → delete, let the cause-effect be implicit, or use "这使得"/"结果是"
- "综上所述" → delete entirely, end with a concrete detail or boundary
- "此外" → delete, or merge the point into the previous sentence

### 4. Paragraph Length Asymmetry

Do not make every paragraph the same length.

- Mix short paragraphs (2-3 sentences) with longer paragraphs (5-7 sentences)
- Allow one-sentence paragraphs for emphasis or transition
- Target: paragraph length standard deviation > 80 chars across a section

### 5. Set Up Questions (设问句)

Use rhetorical questions sparingly, and only when the discipline and school style allow it:

```text
AI风：企业在培训方面存在投入不足的问题，培训频率较低，员工参与度不高。
设问句：培训频率够不够？问卷中仅有23%的员工认为现有培训能满足岗位需求。
```

Do not overuse them. In formal undergraduate theses, direct questions may look out of place; prefer process-node openings or data-first openings when possible.

### 6. Incomplete Sentences (省略句)

Allow academically acceptable short or elliptical sentences only when they remain formal:

- 删除主语的观察句："问卷显示，仅20%的受访者认可现有激励机制。"
- 条件省略句："在现有人员配置下，很难覆盖所有培训需求。"
- 转折省略句："但实际情况并非如此。"

Do not make the text conversational. Keep academic register.

### 7. Information Density Variation

Some paragraphs should be evidence-dense, others should be more reflective. Do not make every paragraph pack the same amount of information.

- Evidence paragraph: 2-3 data points or observations
- Analysis paragraph: 1 data point + interpretation
- Transition paragraph: 1-2 sentences connecting to the next section

### 8. Enumeration Breaking

When the source text has "第一、第二、第三、第四":

- Option A: Merge 2 items into one sentence, break the rest apart
- Option B: Convert one list item into a case observation paragraph
- Option C: Group items by process stage instead of numbering
- Option D: Keep 2 items numbered, rewrite the rest as flowing prose

Never keep more than 3 consecutive numbered items.

### 9. Opening Sentence Variation

Do not start every paragraph with the same pattern.

Forbidden consecutive patterns:

- Two paragraphs starting with "在...方面"
- Two paragraphs starting with "该企业/该公司"
- Two paragraphs starting with a definition
- Two paragraphs starting with "从...角度来看"

Varied opening strategies:

- Start with a data point
- Start with a finding from the survey
- Start with a process node
- Start with a contrast or limitation
- Start with the object directly (no lead-in)

### 10. Conclusion Sentence Variation

Do not end every paragraph with a value claim or significance statement.

Varied ending strategies:

- End with a specific data point
- End with a limitation or boundary
- End with a question (rare, 1 per chapter max)
- End with a transition to the next section's concrete topic
- End with a concrete detail, not an evaluation

## Burstiness Self-Check

For each rewritten paragraph, verify:

| Check | Pass/Fail |
|---|---|
| Contains at least one sentence < 15 chars? | |
| No 3+ consecutive sentences in 25-35 char range? | |
| Sentence length σ > 10? | |
| Connectors reduced to < 3 per paragraph? | |
| Not every sentence starts with the same pattern? | |
| Not every sentence ends with a value claim? | |
| At least one sentence has a concrete object (name, number, process)? | |

If 3 or more checks fail because of rhythm uniformity, rewrite the paragraph with controlled rhythm repair. If the checks pass but report risk remains high, do not keep adding rhythm variation.

## Priority Order

1. First: audit whether rhythm is actually the bottleneck.
2. If yes: vary sentence length and reduce connectors.
3. If no: switch to report-color targeting, evidence placement, or template-skeleton repair.
4. Break enumeration when it is part of the risk pattern.
5. Use set-up questions only when they fit the paper style.

## Social-Science Specific Burstiness

For HR, management, marketing, education, and similar thesis types:

- Use survey percentages as anchors only when they exist in the source.
- Use interview quotes or summarized feedback only when the thesis or user provides them.
- Use process-node descriptions to replace generic claims.
- Use company, department, position, questionnaire, or process evidence as concrete anchors.
- Mix "数据 -> 分析 -> 对策" with "流程节点 -> 观察 -> 建议" paragraph structures.
- Avoid colloquial short sentences such as "渠道太单一" unless the requested style allows it. In formal thesis text, prefer "渠道结构偏窄" or a data-first sentence.

## Relation To SKILL.md

Use this file in all AIGC revision modes as an early rhythm audit. If a paragraph remains red or orange while its rhythm is already varied, do not keep injecting burstiness. Route to social-science template repair, evidence-first reconstruction, or report-color mapping instead.
