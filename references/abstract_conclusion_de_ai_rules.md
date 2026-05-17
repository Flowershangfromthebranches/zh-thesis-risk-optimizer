# Abstract & Conclusion De-AI Rules

## Purpose

Abstract (摘要) and Conclusion (结论) are the two highest-risk sections for AIGC detection in Chinese theses. They are short, dense, and follow highly formulaic patterns. Even when other chapters are successfully de-risked, these two sections often remain red/orange.

This file provides targeted rules for abstract and conclusion revision. It is loaded during `FIRST_PASS_RED_ORANGE_ENGINE` or `AIGC_PLATEAU_BREAKER` when either section is identified as red/orange.

## Prohibited Abstract Template

The following abstract structure is banned:

```text
随着[宏观背景]，[行业/领域]面临着[挑战/机遇]。本文以[研究对象]为例，分析了[问题领域]的现状，发现存在[问题1]、[问题2]、[问题3]、[问题4]等问题。
针对上述问题，本文提出了[对策1]、[对策2]、[对策3]、[对策4]等对策。
希望能为[相关领域]提供参考与借鉴。
```

This structure, even when words are changed, scores consistently high on AIGC detection. It must be broken structurally, not just reworded.

## Abstract Rewrite Rules

### Rule A1: Lead With Data, Not Background

Open the abstract with 1-2 key numbers from the thesis — not with "随着……的发展" or "在……背景下".

| ❌ Wrong | ✅ Correct |
|---|---|
| "随着数字化转型的深入推进，电商企业招聘管理面临着新的挑战和机遇。" | "A公司2024年招聘数据显示：关键岗位平均招聘周期47天，是行业标杆的1.8倍；试用期离职率22%，高于公司目标的15%。本文基于这些数据……" |
| "在当前数智化时代，人力资源管理的重要性日益凸显。" | "对A公司237份有效问卷的分析显示，仅31%的员工认为招聘流程与实际岗位需求匹配。本文聚焦这一匹配缺口……" |

### Rule A2: Keep Only the Most Important Finding

Abstracts typically list 3-4 problems and 3-4对策. This symmetry is a strong AIGC signal.

- Reduce to 1-2 critical findings.
- Do not enumerate "问题一、问题二、问题三".
- Group issues by root cause where possible.

| ❌ Wrong | ✅ Correct |
|---|---|
| "研究发现A公司招聘存在以下四个问题：招聘渠道单一、筛选标准模糊、面试流程不规范、入职跟踪缺失。" | "A公司招聘的核心堵点集中在简历筛选到面试之间的衔接环节——该环节平均耗时8天，占整个招聘周期的60%以上。" |

### Rule A3: Cut Generic Background Sentences

Remove any sentence in the abstract that:
- Describes a general trend ("在……背景下", "随着……发展", "在……时代")
- States the importance of the topic ("……具有重要意义")
- Claims broad relevance ("……是……的重要组成")
- Provides a definition ("所谓……是指……")

These sentences consume character budget without adding thesis-specific content.

### Rule A4: Delete "提供参考与借鉴"

This exact phrase (or any variant like "供同类企业参考", "为……提供借鉴") must be deleted from the abstract.

## Conclusion Rewrite Rules

### Rule C1: Write Research Boundaries, Not Achievement Lists

The conclusion must include what the thesis did NOT cover or could not resolve.

| ❌ Wrong | ✅ Correct |
|---|---|
| "本文提出了四项优化对策，能够有效提升A公司的招聘管理效率。" | "本文提出的招聘环节优化方案仅在A公司人力资源部试行，未覆盖业务部门的直接招聘需求。方案的实际效果需3-6个月运行数据验证。" |

### Rule C2: State Conditions for Implementation

For each proposed measure/solution, state the condition under which it would or would not work.

| ❌ Wrong | ✅ Correct |
|---|---|
| "A公司应建立科学的招聘管理体系。" | "缩短筛选周期的前提是业务部门提前2个工作日提交用人需求——目前仅40%的部门能做到这一点。" |

### Rule C3: No Grand Value Statements

Ban these patterns from the conclusion:
- "对同类企业具有借鉴意义"
- "为……提供了新思路"
- "推动了……的发展"
- "具有重要的理论意义和实践价值"
- "有助于……的提升"

Replace with specific limitations or open questions.

### Rule C4: Acknowledge Unresolved Problems

Every conclusion must contain at least one sentence acknowledging what was NOT solved:

```text
本文未解决的问题包括：
- ……
- ……
```

This single change significantly reduces the "textbook answer" pattern.

### Rule C5: Do Not Summarize the Entire Thesis

The conclusion should not repeat the chapter-by-chapter summary of what each chapter did. Instead:
- Pick 1-2 concrete findings.
- State what they mean for the research object.
- State what remains unknown or untested.

## Abstract Self-Audit

| check | pass/fail |
|---|---|
| Opens with data (not background trend) |  |
| No generic background sentence |  |
| At most 2 findings (not 4 enumerated problems) |  |
| No "提供参考与借鉴" or variants |  |
| Includes at least one A-company-specific number |  |

## Conclusion Self-Audit

| check | pass/fail |
|---|---|
| States a research boundary or limitation |  |
| At least one implementation condition mentioned |  |
| No grand value statements |  |
| At least one unresolved problem acknowledged |  |
| Not a chapter-by-chapter summary |  |

If any check fails, the section is not ready for acceptance.

## Relation To SKILL.md

Load this file when processing Abstract or Conclusion sections during `FIRST_PASS_RED_ORANGE_ENGINE` or `AIGC_PLATEAU_BREAKER`. These sections should be prioritized in the task table (high risk, high impact).
