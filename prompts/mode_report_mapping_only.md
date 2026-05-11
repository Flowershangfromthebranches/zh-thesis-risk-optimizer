# Prompt: REPORT_TO_SOURCE_MAPPING

Use this prompt when the user wants report fragments mapped back to the source text before any rewrite.

## Workflow

1. Extract report fragments and risk/source notes.
2. Search the source text for exact matches.
3. If exact matching fails, try normalized matching.
4. If normalized matching fails, try keyword/context inference.
5. Mark confidence as HIGH, MEDIUM, LOW, or UNMAPPED.
6. For LOW and UNMAPPED, do not rewrite.
7. If a fragment maps to multiple locations, list all locations.

## Output

```markdown
## 映射表
| 编号 | 报告片段 | 可能位置 | 前后文 | 映射方式 | 映射置信度 | 下一步 |
|---|---|---|---|---|---|---|

## 无法映射片段

## 需要用户确认的问题
```
