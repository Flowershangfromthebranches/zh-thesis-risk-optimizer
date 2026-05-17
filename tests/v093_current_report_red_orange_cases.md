# v0.9.3 Current Report Red-Orange Cases

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Use this checklist to verify forced routing, current-report red/orange coverage, social-science hard rules, and AIGC acceptance self-audit.

## Case 1: Forced Route For AIGC-Only DOCX Color Report

Input:

```text
【任务目标】只降 AIGC
【论文输入】第一次降后论文 DOCX：/path/revised_1.docx
【处理范围】全文，只处理红橙片段
【输出形式】创建副本并回写，同时输出诊断表
【字数约束】全文 ±10%
【保护项】引用、问卷数据、图表编号、参考文献、学校声明
【AIGC 报告】第一次降后 AIGC 颜色报告 DOCX：/path/revised_1_aigc.docx
【查重报告】无
【报告颜色规则】红色 >70%，橙色 60%-70%，紫色 50%-60%，黑色 <50%
【论文专业和题目】人力资源管理，《A公司招聘管理优化研究》
【当前状态】第一次改写后，复检 AIGC 仍然偏高
【历史版本】原文和原版报告可提供
【用户目标】继续降低 AIGC，但不全文大改
【可用证据】问卷、访谈、招聘流程、岗位、指标
【特殊要求】低风险内容冻结
```

Expected:

- Route to `THREE_MODE_COLOR_BAND_WORKFLOW`.
- Use `CURRENT_REPORT_RED_ORANGE_ENGINE`.
- Overlay `AIGC_PLATEAU_BREAKER` if orange concentration is present.
- Overlay `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`.
- Do not route to plain `AIGC_ONLY`.
- Do not route to generic polishing.
- Do not route to `FIRST_PASS_RED_ORANGE_ENGINE`.

## Case 2: Real Failure Pattern, Red Down But Orange Accumulates

Input:

```text
major: 人力资源管理
round: after_first_rewrite
current_aigc_rate: above_60_percent_user_reported
report_trend:
  original_red: high
  first_rewrite_red: lower
  first_rewrite_orange: accumulated
request: continue AIGC reduction with current DOCX color report
```

Expected:

- Mark orange plateau.
- Current report red paragraphs all enter the task table.
- Current report orange paragraphs all enter the task table.
- Low-risk, black, cover, table of contents, declaration, references, appendices, and school-template text are frozen.
- Output red-orange coverage acceptance table.
- Do not process only red.
- Do not run full-text polishing.
- Do not use synonym-only rewriting.

## Case 3: Red-Orange Coverage Acceptance

Input:

```text
current_report_red_total: 8
current_report_orange_total: 21
processed_red_count: 8
processed_orange_count: 19
```

Expected:

- `unprocessed_red_orange_count = 2`.
- Completion status is not `COMPLETED`.
- Output unprocessed red-orange list.
- Every unprocessed item has a reason and required next action.

## Case 4: Paragraph Without Processing Record

Input:

```text
red_orange_task_table_contains: P-12
paragraph_processing_records_missing: P-12
```

Expected:

- Treat P-12 as unprocessed.
- Completion forbidden.
- Add P-12 to unprocessed red-orange list.

## Case 5: AIGC Acceptance Self-Audit Failure

Input:

```text
paragraph_band: orange
rewrite: 企业应构建科学的人力资源管理体系，优化招聘流程，提升招聘效率，强化人才获取能力，为企业发展提供参考。
```

Expected:

- Fail `AIGC_ACCEPTANCE_SELF_AUDIT`.
- Reasons include generic management terms, synonym-like polishing, missing A company scene, missing questionnaire/interview/process/post/indicator evidence, and smoother AI-like style.
- Run second-pass rewrite.
- If evidence is unavailable, output author evidence request.
- Do not mark the paragraph complete.

## Case 6: HR Evidence Hard Rule

Input:

```text
section: 对策
paragraph_type: recruitment_countermeasure
rewrite_strategy: 泛化管理语言
available_evidence: A公司岗位、招聘渠道、问卷比例、访谈反馈、复盘周期
```

Expected:

- Use company/post/process/form/indicator/responsibility/review-cycle/questionnaire/interview/boundary evidence.
- Do not accept only "构建体系", "提升效率", "优化流程", "强化能力", "丰富渠道", "数据驱动", "智能高效", or "提供参考".

## Case 7: Protected Low-Risk Freeze

Input:

```text
report_band: black
location: reference_list
request: current report AIGC-only revision
```

Expected:

- Freeze.
- Do not rewrite.
- Do not count as unprocessed red/orange.
