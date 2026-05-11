# Prompt: SENTENCE_LEVEL_DIAGNOSIS_MODE

Use this mode to analyze or revise paragraphs at sentence level.

## Workflow

1. Split paragraph into sentences without breaking citations, formulas, code, or LaTeX commands.
2. Assign sentence IDs: S1, S2, S3.
3. Add AIGC labels, similarity labels, and protection labels.
4. Classify each sentence as可改写、轻改、不建议改写、保留引用、人工确认.
5. If rewriting is requested, revise only eligible sentences and preserve protected content.

## Output for Diagnosis Only

```markdown
段落编号：P-001
综合风险：
建议模式：
建议强度：

句子级定位：
- S1：
- S2：
- S3：

处理建议：
- 可改写句：
- 轻改句：
- 不建议改写句：
- 需要保留引用句：
- 涉及术语/公式/代码保护句：
```

## Output for Revision

```markdown
## 句子级定位

## 改写结果
- 原文：
- 改写后：
- 保留项：
- 评分变化：

## 自检
```

Scores must remain heuristic writing-risk scores.
