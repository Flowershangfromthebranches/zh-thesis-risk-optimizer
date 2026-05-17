# Controlled Humanization Engine

## Purpose

`CONTROLLED_HUMANIZATION_ENGINE` is an internal engine that applies controlled de-AIGC strategies to social-science and management thesis text. It absorbs the effective strategies from older Skill versions (strong template-breaking, varied rhythm, author judgment) while preventing the failure modes those versions produced (excessive colloquialism, diary-like tone, format destruction).

This engine is NOT a "colloquialization engine." It is a controlled humanization engine that breaks AI statistical patterns while preserving formal thesis standards.

## Activation

This engine activates automatically when:

- The discipline is social-science or management (HR, business admin, marketing, education admin, public admin);
- Red/orange AIGC processing is active;
- `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` has been applied;
- AIGC risk remains high after template-bottleneck repair.

Do NOT activate for engineering, computer-science, medical, or natural-science theses unless the user explicitly requests it.

## Style Intensity Levels

The engine supports three intensity levels:

### Level 1: Light

- Only reduces template sentences.
- Maintains strong academic register.
- Suitable for AIGC below 50%.
- Minimal author-judgment insertions.

### Level 2: Medium (Default)

- Breaks template skeletons.
- Adds author judgment where evidence exists.
- Varies sentence length moderately.
- Maintains thesis-standard register.
- Suitable for AIGC 50%-75%.

### Level 3: Strong

- Significantly increases human-interpretation feel.
- Allows more short sentences and asymmetric structures.
- Still constrained by `ACADEMIC_TONE_GUARD`.
- Suitable for AIGC above 75% in management theses.
- Output must include a warning: "高强度人类化可能降低学术正式度，需要人工复核。"

There is NO unlimited aggressive colloquialization mode.

## Core Strategies

### Strategy A: Template Skeleton Dispersal

Break the standard "研究发现→四个问题→四项对策→提供参考" structure.

**Before (AI template):**
```
研究发现A公司招聘管理存在四个问题：招聘渠道单一、筛选标准模糊、面试流程不规范、入职跟踪缺失。针对上述问题，本文提出四项优化对策。
```

**After (controlled humanization):**
```
本研究先依据问卷和访谈确认主要卡点，再围绕最影响招聘效率和匹配质量的环节提出调整方案。渠道方面，传统平台贡献了85%以上的简历来源；筛选环节，用人部门和HR对同一岗位的要求经常不一致。
```

**Prohibited (diary-like):**
```
一圈查下来，头一个是渠道太窄，第二个是筛人没标准。
```

### Strategy B: Non-Uniform Sentence Length

Allow short, medium, and long sentences to mix naturally.

**Allowed:**
```
这个结果说明，问题并不只在系统采购，而在流程和数据使用方式没有同步调整。问卷中仅22%的员工认为现有激励机制与实际贡献挂钩。
```

**Prohibited (fragmented for AIGC reduction):**
```
这说明什么？说明系统买了但没用起来。问卷说了啥？22%觉得激励没用。
```

### Strategy C: Author Judgment Insertion

Insert author judgment anchored to evidence:

**Allowed phrases:**
- 从访谈结果看
- 这意味着
- 问题并不完全在于
- 更现实的做法是
- 在A公司现有条件下
- 这一发现与问卷数据一致
- 值得注意的是
- 从流程角度看

**Prohibited phrases (see also ACADEMIC_TONE_GUARD):**
- 说白了
- 一圈查下来
- 做这个研究有什么用呢
- 头一个
- 画饼
- 天天等着用人
- 零零星星
- 搞清楚

### Strategy D: Anti-Consulting-Speak

Reduce consulting-jargon density. When 2+ of these appear in one paragraph, rewrite:

构建体系、提升效率、优化路径、赋能、协同、动态调整、精细化运营、智能引擎、数据驱动、生态、漏斗、闭环、雇主品牌、可复制范式、提供参考与借鉴

Replace with: specific process nodes, post names, form names, indicator names, timeframes, and implementation boundaries.

### Strategy E: Theory Section De-Encyclopedia

Do not write:
```
人岗匹配理论是人力资源管理的基石理论之一，其核心在于个体特征与岗位要求的一致性。
```

Write:
```
本文使用人岗匹配理论中的"要求—能力"匹配维度，主要用于分析A公司岗位JD模板化、面试评分标准模糊和新人试用期离职率22%三个问题之间的关联。
```

### Strategy F: Abstract/Conclusion De-Template

Abstract must not retain: 背景→对象→方法→四个问题→四个对策→意义.

Conclusion must include: research boundaries, implementation conditions, unresolved problems, data gaps.

## Output Requirements

When this engine is active, output:

```markdown
## Controlled Humanization Report

| paragraph_id | section | original_template_type | humanization_strategy | intensity_level | academic_tone_guard_result | passed |
|---|---|---|---|---|---|---|

### Style Intensity Used
- level: 1 / 2 / 3
- warning (if level 3): 高强度人类化可能降低学术正式度，需要人工复核。

### Academic Tone Guard Summary
- total_paragraphs_checked:
- violations_found:
- violations_corrected:
- remaining_issues:
```

## Safety

- Do not sacrifice thesis formality for AIGC score reduction.
- Do not produce text that reads like a student diary, social media post, or chat log.
- Every humanization move must be anchored to source evidence or author judgment, not invented casualness.
- If `ACADEMIC_TONE_GUARD` flags a violation, correct before proceeding.

## Relation To SKILL.md

This engine runs after `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` and before `AIGC_REGRESSION_GUARD` in the mandatory chain. It is an internal engine, not a user-facing entry mode.
