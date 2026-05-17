# Controlled Humanization Engine Test Cases

## Case 1: Anti-Consulting-Speak

**Input (AI template with consulting speak):**
```
A公司应构建科学的招聘体系，优化招聘流程，提升招聘效率，通过数据驱动的方式赋能招聘管理，形成可复制的招聘范式，为同类企业提供参考与借鉴。
```

**Expected output:**
- Does NOT retain "构建体系", "提升效率", "数据驱动", "赋能", "可复制范式", "提供参考与借鉴" in the same paragraph (6 consulting-speak terms → must rewrite).
- Replaces with specific process nodes, post names, or evidence.
- Reads like a thesis paragraph, not a consulting report or diary entry.

**Prohibited output:**
```
说白了，招聘就是从外面找人，搞清楚要什么样的人就行了。
```

## Case 2: Template Skeleton Dispersal

**Input (four-problem-four-solution template):**
```
研究发现A公司招聘管理存在四个问题：招聘渠道单一、筛选标准模糊、面试流程不规范、入职跟踪缺失。针对上述问题，本文提出四项优化对策。
```

**Expected output:**
- Breaks the "四个问题→四项对策" symmetry.
- Groups findings by root cause or process stage, not by numbered list.
- Maintains formal thesis register.

**Prohibited output:**
```
一圈查下来，头一个问题是渠道太窄，第二个是筛人没标准，第三个是面试乱来，第四个是入职没人管。
```

## Case 3: Sentence Length Variation

**Input (uniform 25-35 char sentences):**
```
该企业在招聘渠道方面存在较为单一的问题，主要依赖传统招聘平台。社交媒体渠道的利用程度较低，影响了人才获取的效率和质量。这种渠道结构导致企业在技术岗位和复合型岗位的招聘中面临较大困难。
```

**Expected output:**
- Contains at least one short sentence (<15 chars) and one longer sentence (>35 chars).
- Does NOT fragment into chat-like staccato.
- Maintains analytical content.

**Prohibited output:**
```
渠道太单一。就靠传统平台。社交媒体没用上。所以招不到人。技术岗更难。
```

## Case 4: Author Judgment Anchored to Evidence

**Input (generic statement without perspective):**
```
招聘渠道较为单一，影响了企业人才获取效率。
```

**Expected output:**
- Adds author perspective anchored to evidence: "从问卷结果看", "在A公司现有条件下", etc.
- Does NOT add casual filler: "说白了", "其实吧", "我觉得".

## Case 5: Theory De-Encyclopedia

**Input (encyclopedia-style theory):**
```
人岗匹配理论是人力资源管理的基石理论之一，其核心在于个体特征与岗位要求的一致性，具有重要的理论意义和实践价值。
```

**Expected output:**
- States which specific dimension of the theory is used.
- Links to A company's specific problem.
- Maps to questionnaire items or analysis dimensions.
- Does NOT use casual tone: "说白了就是人和岗位要对得上".

## Case 6: Abstract De-Template

**Input (standard abstract template):**
```
随着数字化转型的深入推进，电商企业招聘管理面临着新的挑战和机遇。本文以A公司为例，分析了招聘管理的现状，发现存在四个问题。针对上述问题，提出了四项对策。希望能为同类企业提供参考与借鉴。
```

**Expected output:**
- Opens with specific data or finding, not macro background.
- Reduces to 1-2 critical findings, not four enumerated problems.
- Deletes "提供参考与借鉴".
- Does NOT become diary-like: "我研究这个就是因为A公司招聘太烂了".

## Case 7: Intensity Level 3 Warning

**Input:** AIGC 78% management thesis paragraph.

**Expected output:**
- Level 3 intensity applied.
- Output includes warning: "高强度人类化可能降低学术正式度，需要人工复核。"
- Academic tone guard passes (no prohibited expressions).
- Text is more humanized than level 2 but still thesis-appropriate.
