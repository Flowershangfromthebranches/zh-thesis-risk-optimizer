# Academic Tone Guard

## Purpose

`ACADEMIC_TONE_GUARD` prevents controlled humanization from crossing the line into excessive colloquialism, diary-like tone, or social-media style. It is the quality fence that ensures de-AIGC text remains suitable for a formal undergraduate or graduate thesis.

## Prohibited Expressions

The following expressions must NOT appear in the final thesis text. If found, they must be corrected before delivery.

### Category 1: Over-Colloquial

- 说白了
- 一圈查下来
- 做这个研究有什么用呢
- 头一个
- 第二个是 (when used as casual enumeration opener)
- 画饼
- 天天等着
- 搞清楚
- 各跑各的
- 零零星星
- 花大钱
- 能把人招来
- 能精准地把对的人招来
- 这事
- 这块
- 这头
- 看看再说
- 说多了没用
- 就这么回事
- 其实吧
- 说实话

### Category 2: Diary/Chat-Like

- 我觉得吧
- 你想想看
- 是不是很有意思
- 这不就解决了吗
- 说到底就是
- 搞来搞去
- 反反复复
- 来来回回
- 东一下西一下

### Category 3: Social-Media Style

- 家人们
- 宝子们
- 绝绝子
- YYDS
- 破防了
- 格局打开
- 赋能 (when used as buzzword without evidence)
- 痛点 (when not anchored to specific data)
- 干货 (when not anchored to specific content)

### Category 4: Exaggerated/Emotional

- 严重拖累
- 彻底失败
- 完全没有
- 根本不
- 一塌糊涂
- 惨不忍睹
- 一团糟

## Correction Principles

When a violation is found:

1. **Preserve the sentence-length variation** that the humanization introduced.
2. **Preserve the author judgment** if it was evidence-anchored.
3. **Remove only the diary-feel, chat-feel, or social-media-feel words**.
4. **Restore to undergraduate-thesis acceptable formality**.

### Correction Examples

**Violation:**
```
说白了，招聘就是企业从外面找人。
```

**Correction:**
```
从组织管理角度看，招聘是企业从外部劳动力市场识别、吸引并筛选候选人的过程。
```

**Violation:**
```
做这个研究有什么用呢？
```

**Correction:**
```
本研究的意义主要体现在企业改进、资源配置和行业参照三个层面。
```

**Violation:**
```
一圈查下来，头一个问题是渠道太窄。
```

**Correction:**
```
调研结果显示，首要问题在于招聘渠道覆盖面不足。
```

**Violation:**
```
天天等着用人部门反馈，简历堆在那里没人看。
```

**Correction:**
```
用人部门反馈周期较长，简历在筛选环节平均积压5天。
```

## Allowed Humanization

The following are acceptable and should NOT be flagged:

- 从访谈结果看 (author judgment anchored to evidence)
- 这意味着 (interpretation connector)
- 问题并不完全在于 (nuanced judgment)
- 更现实的做法是 (pragmatic recommendation)
- 在A公司现有条件下 (boundary statement)
- 值得注意的是 (analytical marker)
- 从流程角度看 (perspective marker)
- 短数据-anchored sentences (8-15 chars) mixed with longer analysis sentences
- Non-uniform paragraph structures
- Author perspective anchored to survey/interview/process evidence

## Output

When violations are found:

```markdown
## Academic Tone Guard Report

| paragraph_id | violation | prohibited_expression | corrected_to | status |
|---|---|---|---|---|

### Summary
- total_checked: <count>
- violations_found: <count>
- violations_corrected: <count>
- remaining_issues: <list or "none">
```

## Relation To SKILL.md

This guard runs inside `CONTROLLED_HUMANIZATION_ENGINE` and is also checked by `AIGC_REGRESSION_GUARD` and `FINAL_ACCEPTANCE_AUDIT`.
