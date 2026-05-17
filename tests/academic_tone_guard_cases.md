# Academic Tone Guard Test Cases

## Case 1: Over-Colloquial Detection

**Input:**
```
说白了，招聘就是企业从外面找人。一圈查下来，头一个问题是渠道太窄。
```

**Expected:**
- Violation detected: "说白了", "一圈查下来", "头一个"
- Corrected to formal thesis language
- Sentence meaning preserved
- academic_tone_guard_result = FAILED (pre-correction)

## Case 2: Diary-Like Detection

**Input:**
```
我觉得吧，这个公司的问题其实就是没人管招聘。做这个研究有什么用呢？说到底就是帮企业省钱。
```

**Expected:**
- Violation detected: "我觉得吧", "做这个研究有什么用呢", "说到底就是"
- Corrected to thesis-appropriate perspective statements
- No diary-feel remains

## Case 3: Social-Media Style Detection

**Input:**
```
A公司的招聘管理简直是痛点中的痛点，格局打开，我们来看看干货。
```

**Expected:**
- Violation detected: "痛点中的痛点", "格局打开", "干货"
- Corrected to analytical language with specific evidence anchors

## Case 4: Allowed Expressions NOT Flagged

**Input:**
```
从访谈结果看，用人部门反馈周期过长是招聘效率的主要瓶颈。在A公司现有条件下，更现实的做法是先统一岗位需求确认表，再调整面试评分维度。
```

**Expected:**
- No violations detected
- "从访谈结果看", "在A公司现有条件下", "更现实的做法是" are all allowed
- academic_tone_guard_result = PASSED

## Case 5: Correction Preserves Rhythm

**Input (violation with good rhythm):**
```
天天等着用人部门反馈，简历堆在那里没人看。平均5天才能进入面试安排。
```

**Expected correction:**
```
用人部门反馈周期较长，简历在筛选环节平均积压5天。面试安排需要跨3个部门协调。
```

- Removes "天天等着" (diary-feel)
- Preserves the short-long sentence variation
- Preserves the specific data (5天)

## Case 6: Mixed Violations

**Input:**
```
说实话，A公司的招聘搞来搞去就是那几个问题。其实吧，渠道单一、筛选不规范，这些都不是新鲜事。家人们，这不就解决了吗？用数据驱动的方式赋能招聘就行了。
```

**Expected:**
- Multiple violations: "说实话", "搞来搞去", "其实吧", "家人们", "这不就解决了吗", "赋能"
- All must be corrected
- Resulting text must be thesis-appropriate, not just less colloquial
