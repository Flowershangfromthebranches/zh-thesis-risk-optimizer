# Prompt: REPORT_DUAL_OPTIMIZATION

Use this prompt when the user provides both similarity and AIGC reports, or one report contains both similarity and AIGC-style risks.

## Required Order

1. Process high-contribution similarity fragments first.
2. Check whether those fragments also have AIGC risk.
3. Prioritize fragments with both risks and safe rewrite conditions.
4. Protect citations, formulas, code, experiment data, interfaces, table names, and field names.
5. If historical reports exist, compare trends before rewriting again.
6. After similarity repair, run AIGC regression guard and evidence-based reconstruction.
7. After revision, run heuristic AIGC-risk scoring.
8. Output dual-optimization task table and human review checklist.

## Output

```markdown
## 双报告任务表
| 编号 | 原文位置 | 查重风险 | AIGC风险 | 映射置信度 | 优先级 | 保护项 | 处理顺序 |
|---|---|---|---|---|---|---|---|

## 定点修改

## 改写前后启发式评分

## 人工复核清单
```

Do not claim that revision changes any real detection result.
