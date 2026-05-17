# Prompt: RISK_HEATMAP_TABLE

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Use this mode for long text or multiple paragraphs when the user needs priority ranking.

## Workflow

1. Number chapters, paragraphs, and sentences.
2. Score AIGC risk and similarity risk heuristically.
3. Identify protected and no-edit zones.
4. Compute dual-optimization priority qualitatively: high, medium, low, or pause.
5. Sort by priority, then by combined risk, then by safe-editability.
6. Recommend mode and intensity for each hot zone.

## Heatmap Template

```markdown
| 排名 | 位置 | AIGC风险 | 查重风险 | 双降优先级 | 主要标签 | 建议模式 | 建议强度 | 是否保护 |
|---|---|---:|---:|---:|---|---|---|---|
| 1 | 绪论 P3 | 86 | 72 | 高 | AI-泛化结尾；查重-背景套话 | DUAL_OPTIMIZATION | L2 | 否 |
| 2 | 理论基础 P8 | 42 | 88 | 高 | 查重-定义重复；保护-经典定义 | SIMILARITY_ONLY | L1 | 是 |
| 3 | 系统设计 P5 | 65 | 30 | 中 | AI-机械连接；保护-接口路径 | AIGC_ONLY | L1 | 是 |
```

## Notes

- Protected rows can still rank high, but their suggested strength should be lower.
- If a row is a no-edit zone, recommend explanation-only edits or human confirmation.
- Do not turn heatmap ranking into a guarantee about external systems.
