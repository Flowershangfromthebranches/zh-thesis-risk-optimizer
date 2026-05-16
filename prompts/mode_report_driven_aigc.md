# Prompt: REPORT_AIGC_ONLY

Use this prompt when the user provides an AIGC report and wants targeted AIGC-risk optimization.

## Boundaries

This mode only works with report content the user provides. Do not simulate, crack, reverse engineer, or forge any detection system.

## Workflow

1. Identify report type.
2. Extract high AIGC-risk fragments.
3. If this is the original thesis plus original AIGC report, route to `FIRST_PASS_RED_ORANGE_ENGINE`.
4. In first-pass mode, extract both red/high-risk and orange/medium-risk fragments as primary targets.
5. Map each fragment back to the thesis source text.
6. Assign mapping confidence.
7. Diagnose AI writing patterns.
8. Identify protected content.
9. Choose rewrite intensity.
10. Apply character delta control for whole-thesis work; default total change is `±10%`.
11. Perform targeted revision only for confirmed or safe mappings.
12. Output before/after heuristic score comparison.

## Output

```markdown
## 报告驱动任务表
| 编号 | 原文章节 | 原文段落 | 报告片段 | 风险类型 | 相似源/风险说明 | 贡献率/等级 | 映射置信度 | 建议模式 | 改写强度 | 是否保护 | 处理建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 红橙首轮任务表
| 编号 | 原文章节 | 原文段落 | 风险带 | 是否首轮主处理 | 目标风险带 | 保护项 | 内部重试上限 | 字符变动策略 |
|---|---|---|---|---|---|---|---:|---|

## 单段处理
【定位】
【判断】
【修改后】
【复核】
```
