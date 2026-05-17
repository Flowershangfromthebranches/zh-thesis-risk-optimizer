# Example 06: Long Thesis Workflow

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Scenario

用户一次性提供完整论文正文，希望先诊断再分段修改。

## Step 1: Identify Chapter Structure

```markdown
| Chapter | Function | Initial Risk |
| --- | --- | --- |
| 摘要 | 总述研究对象、方法和结论 | AIGC 风险中 |
| 绪论 | 背景和研究意义 | 相似风险高 |
| 理论基础 | 概念解释 | 相似风险高 |
| 系统设计 | 模块和接口 | AIGC 风险中，技术保护高 |
| 实验分析 | 数据和图表解释 | 技术保护高 |
| 总结 | 工作总结和不足 | AIGC 风险高 |
```

## Step 2: Build Protected List

```markdown
| Type | Item | Rule |
| --- | --- | --- |
| Term | 端侧推理 | 保持一致 |
| API | /api/health/latest | 不改 |
| Table | health_record | 不改 |
| Field | blood_oxygen | 不改 |
| Citation | [12] | 保留来源边界 |
```

## Step 3: Mode Assignment

```markdown
| Paragraph | Risk | Mode | Intensity |
| --- | --- | --- | --- |
| 绪论 P2 | 背景套话，相似风险 | SIMILARITY_ONLY | L2 |
| 理论基础 P1 | 教材式定义 | SIMILARITY_ONLY | L2 |
| 系统设计 P3 | 空泛模块描述 | AIGC_ONLY + ENGINEERING | L1 |
| 总结 P1 | 泛化结尾 | AIGC_ONLY | L2 |
```

## Step 4: Rolling Summary

After each section:

```markdown
## Rolling Summary
- Section: 系统设计
- Core claim: 健康数据与用户资料分表存储，降低耦合。
- Key evidence: health_record stores heart_rate, blood_oxygen, record_time.
- Protected terms: health_record, blood_oxygen, /api/health/latest.
- Citation notes: no external claim added.
- Revision mode and intensity: AIGC_ONLY, L1.
- Open issues: 用户未提供异常阈值来源，后续涉及阈值时需补充依据。
```

## Step 5: Final Review

- Citation boundaries remain visible.
- Terms are consistent.
- Engineering identifiers are unchanged.
- No fabricated data, experiments, citations, or conclusions.
