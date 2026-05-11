# Prompt: SCORING_DIAGNOSIS_MODE

Use this mode when the user asks for diagnosis and scoring before any rewrite.

## Required Disclaimer

Always include:

```text
该评分为启发式写作风险评分，仅用于提示文本可能存在的模板化、相似表达和改写优先级问题，不代表知网、维普、万方、Turnitin 或任何商业检测系统的真实结果。
```

## Workflow

1. Identify chapter and paragraph structure.
2. Build protected list and no-edit zones.
3. Score AIGC risk using heuristic dimensions.
4. Score similarity risk using heuristic dimensions.
5. Determine dual-optimization priority.
6. Assign paragraph-level risk labels.
7. Locate sentence-level risks for high-priority paragraphs.
8. Output risk heatmap and suggested mode/intensity.
9. Do not rewrite unless the user asks.

## Output

```markdown
## 评分声明

## 总体诊断
- 总体风险：
- AIGC 风险：
- 查重相似风险：
- 双降优先级：

## 风险热区表
| 排名 | 位置 | AIGC风险 | 查重风险 | 双降优先级 | 主要标签 | 建议模式 | 建议强度 | 是否保护 |
|---|---|---:|---:|---:|---|---|---|---|

## 句子级定位

## 不建议修改区域

## 建议处理顺序
```
