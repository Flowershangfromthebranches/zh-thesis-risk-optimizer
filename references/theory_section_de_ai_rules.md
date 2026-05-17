# Theory Section De-AI Rules

## Purpose

Theoretical basis chapters (typically 2.1, 2.2, or sections labeled "理论基础", "相关理论概述") are a high-risk zone for AIGC detection. They frequently read as encyclopedia entries — generic definitions followed by abstract significance statements — which pattern-match strongly to AI-generated text.

This file defines rules specific to theoretical basis sections. It is loaded during `FIRST_PASS_RED_ORANGE_ENGINE` or `AIGC_PLATEAU_BREAKER` when the section is identified as red/orange in the report.

## Prohibited Structure: Encyclopedia Definition

The following structure is banned in theoretical basis sections:

```text
[某理论]是[学科领域]的[基石/核心/重要]理论之一。
其核心在于[概括性原理]。
它包括[概念A]、[概念B]、[概念C]等要素。
[该理论]对于理解[宽泛领域]具有重要意义。
在[本领域]中得到了广泛应用。
```

This structure is an immediate red/orange risk regardless of wording changes.

## Required Replacement Structure

Every theoretical basis paragraph must answer these three questions:

### Question 1: What part of this theory does THIS thesis actually use?

Do not summarize the full theory. Identify the specific dimension, concept, or relationship that appears in later analysis.

| ❌ Wrong | ✅ Correct |
|---|---|
| "人岗匹配理论是人力资源管理的基石理论之一，其核心在于个体特征与岗位要求的一致性。" | "本文使用人岗匹配理论中的'要求—能力'匹配维度，不展开'需要—供给'匹配维度，因后者涉及薪酬、福利等本文未深入讨论的激励因素。" |
| "期望理论认为，激励力量 = 效价 × 期望值。该理论由弗鲁姆提出，广泛应用于组织行为学领域。" | "本文取期望理论中的'期望值'概念——即员工认为努力能带来绩效结果的主观概率——用于解释问卷中'培训后绩效无明显变化'这一发现。" |

### Question 2: Which specific problem in Company A does this theory explain?

Each theory must be linked to a concrete phenomenon or question from the thesis:

| ❌ Wrong | ✅ Correct |
|---|---|
| "人岗匹配理论对招聘管理具有重要指导意义。" | "A公司目前存在的'JD模板化、面试评分标准模糊、新人试用期离职率22%'三个问题，都可以用人岗匹配理论中的'要求—能力'维度来分析。" |
| "双因素理论有助于理解员工激励问题。" | "在访谈中，多位员工提到'工资还可以，但做的活和当初面试说的完全不一样'——这恰好对应双因素理论中的保健因素满足但激励因素缺失。" |

### Question 3: How is this theory operationalized in this thesis?

Every theory must be mapped to a concrete research instrument or analysis dimension:

- Which **questionnaire item(s)** measure this theory's concept?
- Which **interview question(s)** explore it?
- Which **analysis dimension** in Chapter 4/5 uses it?
- Which **evaluation criterion** on a form reflects it?

| ❌ Wrong | ✅ Correct |
|---|---|
| "本研究基于人岗匹配理论设计了问卷。" | "问卷第8-10题对应人岗匹配理论的'岗位认知清晰度'维度，第11-13题对应'能力匹配感知'维度。第14题为开放题，收集匹配偏差的具体描述。" |
| "基于社会交换理论，分析了员工关系。" | "社会交换理论在本文中仅用于解释员工流失数据——具体来说，是用'感知组织支持→回报义务感→留任意愿'这一链条，对应问卷第22-25题（李克特5点量表）。" |

## Rules

### Rule 1: No Theory History

Do not include:
- The theory's founder, origin year, or development history unless it is directly cited and debated in the analysis.
- Schools, branches, or later evolutions of the theory.
- Applications of the theory in other industries/fields.
- Criticisms or limitations of the theory that are not used in the thesis.

Exception: If the thesis itself discusses theoretical debates (e.g., a literature review section that compares competing theories), preserve that content.

### Rule 2: No Generic Significance

Do not write:
- "对……具有重要指导意义"
- "为……提供了理论基础"
- "被广泛应用于……"
- "在……领域发挥着重要作用"

Replace with:
- "在本文中，该理论用于分析……（具体哪个数据/现象）"
- "第X章第X节使用该理论的……维度"

### Rule 3: Each Paragraph Must Contain At Least One Thesis-Specific Anchor

A theory section paragraph must contain at least one of:
- A reference to the company name (A公司/研究对象).
- A specific chapter/section where the theory is used ("第四章用此理论分析……").
- A questionnaire item number, interview question, or analysis dimension.
- A data point from the thesis that this theory helps explain.

If a paragraph has none of these anchors, it is encyclopedia-style writing and must be rewritten.

### Rule 4: Do Not Expand Unused Theory

If a theory is listed in the table of contents but not used in analysis chapters, do not expand its description. Either:
- Delete the theory section (if no chapter uses it).
- Or add a note: "本文仅引用此理论作为分析框架，不深入展开，因后文不依赖该理论的细分维度。"

## Self-Audit for Theory Paragraphs

After revising each theoretical basis paragraph, check:

| check | pass/fail |
|---|---|
| Does it name the specific dimension used? |  |
| Does it reference A company's specific problem? |  |
| Does it map to a questionnaire item, interview question, or analysis dimension? |  |
| Does it avoid theory history? |  |
| Does it avoid generic significance? |  |
| Does it contain at least one thesis-specific anchor? |  |

If any check fails, the paragraph is not ready and must be rewritten.

## Relation To SKILL.md

Load this file when processing theoretical basis sections (2.1, 2.2, or "理论基础" chapter) during `FIRST_PASS_RED_ORANGE_ENGINE` or `AIGC_PLATEAU_BREAKER`. Use in conjunction with `references/chapter_strategies.md` Chapter Strategy for Theoretical Basis.
