# Prompt: REPORT_DUAL_OPTIMIZATION

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Use this prompt when the user provides both similarity and AIGC reports, or one report contains both similarity and AIGC-style risks.

## Required Order

1. Process high-contribution similarity fragments first.
2. If reports use color bands, use the default legend unless the report states otherwise: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
3. Red and orange in either report are primary targets.
4. Check whether similarity fragments also have AIGC risk.
5. Prioritize fragments with both risks and safe rewrite conditions.
6. Analyze why each red/orange fragment has its color.
7. Protect citations, formulas, code, experiment data, interfaces, table names, and field names.
8. If historical reports exist, compare trends before rewriting again.
9. After similarity repair, run AIGC regression guard and evidence-based reconstruction.
10. Apply whole-thesis character delta guard, default `±10%`.
11. After revision, run heuristic AIGC-risk scoring.
12. Output dual-optimization task table and human review checklist.

If file input is provided, create a copy and write safe revisions back to the copy only.

## Output

```markdown
## 双报告任务表
| 编号 | 原文位置 | 查重风险 | AIGC风险 | 映射置信度 | 优先级 | 保护项 | 处理顺序 |
|---|---|---|---|---|---|---|---|

## 颜色原因分析

## 定点修改

## 字符变动表

## 文件回写表

## 改写前后启发式评分

## 人工复核清单
```

Do not claim that revision changes any real detection result.
