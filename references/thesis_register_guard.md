# Thesis Register Guard

## Purpose

`THESIS_REGISTER_GUARD` is a section-aware academic register gate. It is stricter than generic tone checking because local humanization can lower AIGC risk while damaging thesis style.

## Section Strictness

### Strict Sections

Applies to:

- 摘要
- 英文摘要
- 理论基础
- 结论

These sections prohibit Level 4 and prohibit chat-like expressions such as:

- 一圈查下来
- 头一个是
- 比较头疼
- 发帖子
- 等简历
- 人工筛
- 抢人
- 弄清楚
- 没那么乐观
- 这块
- 能不能
- 好不好
- 光靠
- 说白了
- 做这个研究有什么用呢

### Moderate Sections

Applies to:

- 绪论
- 研究方法
- 企业概况

Natural expression is allowed, but the paragraph must still read like a thesis. Avoid conversational questions, diary narration, and social-media tone.

### Flexible Sections

Applies to:

- 第四章问题分析
- 第五章对策分析

These sections may use stronger explanatory texture and local Level 4 when triggered, but still must preserve thesis register. Student diary style remains prohibited.

## Guard Output

| paragraph_id | section | strictness | violation | corrected_to | result |
|---|---|---|---|---|---|

## Verdicts

| condition | result |
|---|---|
| no prohibited expression and thesis register preserved | `PASSED` |
| violation corrected successfully | `PASSED_AFTER_REPAIR` |
| strict section contains Level 4 or chat-like expression | `FAILED_STRICT_SECTION` |
| flexible section becomes diary-like or casual | `FAILED_OVER_HUMANIZATION` |

## Relation To SKILL.md

This gate runs after `TEMPLATE_RESIDUE_DETECTOR` and before `AIGC_REGRESSION_GUARD`. It is mandatory whenever `CONTROLLED_HUMANIZATION_ENGINE` or `LOCAL_ESCALATED_HUMANIZATION` runs.
