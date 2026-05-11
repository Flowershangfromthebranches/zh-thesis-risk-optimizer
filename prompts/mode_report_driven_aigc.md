# Prompt: REPORT_AIGC_ONLY

Use this prompt when the user provides an AIGC report and wants targeted AIGC-risk optimization.

## Boundaries

This mode only works with report content the user provides. Do not simulate, crack, reverse engineer, or forge any detection system.

## Workflow

1. Identify report type.
2. Extract high AIGC-risk fragments.
3. Map each fragment back to the thesis source text.
4. Assign mapping confidence.
5. Diagnose AI writing patterns.
6. Identify protected content.
7. Choose rewrite intensity.
8. Perform targeted revision only for confirmed or safe mappings.
9. Output before/after heuristic score comparison.

## Output

```markdown
## 报告驱动任务表
| 编号 | 原文章节 | 原文段落 | 报告片段 | 风险类型 | 相似源/风险说明 | 贡献率/等级 | 映射置信度 | 建议模式 | 改写强度 | 是否保护 | 处理建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 单段处理
【定位】
【判断】
【修改后】
【复核】
```
