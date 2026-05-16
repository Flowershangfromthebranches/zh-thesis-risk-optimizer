# Orange Zone Rewrite Strategy

## Purpose

Orange-zone paragraphs are medium-risk AIGC fragments. They are often not obviously template-like enough for red/high-risk repair, but they still preserve AI-like structure.

## Orange-Zone Symptoms

- Long enumerated paragraphs.
- Smooth management-language explanation.
- Repeated "problem-cause-impact" or "measure-effect-value" structures.
- Generic words such as "流程", "工具", "能力", "渠道", "体系", "机制" without local evidence nearby.
- Survey data exists but appears as a list instead of shaping the paragraph logic.
- Every sentence has similar length and grammatical completeness.

## Required Repair Moves

Use at least two moves; do not only replace words.

### 1. Enumeration Break

Break "第一、第二、第三" chains when they create a standard-answer rhythm.

Options:

- Split one long enumerated paragraph into shorter function-based paragraphs.
- Merge repeated list items.
- Convert part of the list into a direct observation sentence.

### 2. Evidence-First Reordering

Start from local evidence when available:

- survey percentage,
- interview finding,
- company process,
-岗位或部门信息,
- existing chart/table reference.

Then explain the issue.

### 3. Case-Local Anchor

Replace generic claims with A-company-specific wording:

- "招聘团队能力不足" -> "问卷中仅 20% 的受访者认可团队的数据与工具能力".
- "渠道单一" -> "传统平台贡献超过 85%，社交媒体和专业社区合计不足 15%".

### 4. Rhythm Disruption

Use short sentence plus medium sentence plus longer explanation. Do not keep all sentences in the same length band.

### 5. Compression Before Expansion

Delete repeated transitional and value statements before adding any evidence. Medium-risk paragraphs usually need structure changes, not more words.

### 6. Protected-Fact Bypass

If a sentence is mostly numbers, chart names, citations, or fixed institutional facts, protect it and revise only the surrounding explanatory sentence.

## Orange-Zone Output

```markdown
## Orange-Zone Diagnosis
| paragraph_id | risk_band | retained_skeleton | plateau_reason | repair_moves | protected_items |
|---|---|---|---|---|---|

## Orange-Zone Revision
- Replace:
- Compress:
- Preserve:
- Result:
```

## Relation To SKILL.md

Use this file after `AIGC_PLATEAU_BREAKER` identifies persistent orange/medium-risk paragraphs.
