**ARCHIVED_COMPATIBILITY_ONLY**

Do not call directly. Route through `SKILL.md` Minimal Mode Router.

# Prompt: REPORT_AIGC_ONLY

Use this prompt when the user provides an AIGC report and wants targeted AIGC-risk optimization.

## Boundaries

This mode only works with report content the user provides. Do not simulate, crack, reverse engineer, or forge any detection system.

## Workflow

1. Identify report type.
2. If the report is a color-marked DOCX, load `references/docx_color_report_extraction.md` and extract color metadata before plain-text processing.
3. Extract high AIGC-risk fragments.
4. If the report uses color bands, apply the default legend unless the report states otherwise: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
5. If this is the original thesis plus original AIGC report, route to `FIRST_PASS_RED_ORANGE_ENGINE`.
6. In first-pass mode, extract both red/high-risk and orange/medium-risk fragments as primary targets.
7. Analyze why each red/orange fragment has its color before rewriting.
8. Map each fragment back to the thesis source text.
9. Assign mapping confidence.
10. Diagnose AI writing patterns.
11. Identify protected content.
12. Choose rewrite intensity.
13. Apply character delta control for whole-thesis work; default total change is `±10%`.
14. Perform targeted revision only for confirmed or safe mappings.
15. Output before/after heuristic score comparison.

If a DOCX report appears identical to the thesis after plain-text extraction, treat that as a warning that color metadata was lost. Do not proceed as if the report has no labels.

If file input is provided, create a copy and write safe revisions back to the copy only.

## Output

```markdown
## 报告驱动任务表
| 编号 | 原文章节 | 原文段落 | 报告片段 | 风险类型 | 相似源/风险说明 | 贡献率/等级 | 映射置信度 | 建议模式 | 改写强度 | 是否保护 | 处理建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 红橙首轮任务表
| 编号 | 原文章节 | 原文段落 | 风险带 | 是否首轮主处理 | 目标风险带 | 保护项 | 内部重试上限 | 字符变动策略 |
|---|---|---|---|---|---|---|---:|---|

## 颜色原因分析
| 编号 | 原文位置 | 报告颜色 | 疑似度区间 | 被标记原因 | 修复动作 | 自评目标 |
|---|---|---|---|---|---|---|

## 单段处理
【定位】
【判断】
【修改后】
【复核】

## 文件回写表
```
