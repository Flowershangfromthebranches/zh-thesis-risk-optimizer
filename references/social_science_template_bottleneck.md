# Social-Science Template Bottleneck

## Purpose

This file handles AIGC-risk plateaus common in management, business, education, public administration, and applied social-science theses.

These papers often have reports and still reduce poorly because the issue is not only wording. The issue is a repeated standard-answer structure with insufficient local evidence.

For human resource management, business administration, marketing, education management, and public administration theses, this file is a hard rule when report-driven AIGC red/orange work is active. It is not an optional style suggestion.

## High-Risk Thesis Types

Use this workflow for these thesis types when AIGC risk remains high after normal rewriting:

- Human resource management.
- Business administration.
- Marketing.
- E-commerce operation and management.
- Accounting and financial management.
- Public administration.
- Education management.
- Tourism management.
- Logistics management.
- Public service / social work / community governance.
- Innovation and entrepreneurship management.
- Rural revitalization, enterprise governance, service quality, customer satisfaction, employee satisfaction, training, performance, recruitment, incentive, and channel optimization topics.

This list is not exhaustive. Any thesis dominated by "status -> problem -> reason -> countermeasure -> guarantee" should be treated as a possible template bottleneck.

## Common Bottleneck Structure

Typical high-risk scaffolds:

```text
概念界定 -> 现状分析 -> 问题归纳 -> 原因分析 -> 优化对策 -> 保障措施
```

```text
第一，完善机制。第二，优化流程。第三，加强培训。第四，健全保障。
```

```text
通过上述措施，可以提升效率、增强能力、促进发展、提供参考。
```

These structures can remain orange/medium-risk even after synonym replacement.

## Why Reports Still Do Not Help Enough

Reports locate the risky paragraph, but they do not supply missing local evidence. More critically, most rewriting approaches make social-science text **more AI-like** by:

- Replacing simple wording with more formal management jargon
- Making sentences more balanced and complete
- Adding more abstract nouns (机制, 体系, 能力, 保障, 路径, 价值)
- Preserving the "问题→原因→对策" template skeleton
- Making every paragraph the same length and rhythm

The root cause: social-science thesis text is already close to high-risk distribution because it uses standardized templates. Rewriting it with "academic polish" pushes it further into that pattern. The fix is to preserve report targeting, break the template skeleton, move evidence before evaluation, and repair rhythm only when rhythm is actually the problem.

Poor reduction usually happens when:

- The paragraph still reads like a policy recommendation.
- Red/orange text is rewritten into smoother management language.
- Survey or interview data exists but is placed after generic conclusions.
- The same "problem -> reason -> effect -> measure" skeleton repeats.
- Measures are not tied to a specific department, post, process, group, or data point.
- The model adds abstract nouns such as 机制, 体系, 能力, 保障, 路径, 价值, 协同 without adding evidence.
- Every sentence has the same 25-35 char length, or the paragraph has the opposite problem: varied rhythm but unchanged template skeleton.
- The report is a DOCX color report but the agent flattened it to plain text and lost red/orange/purple labels.
- Sentence rhythm is already varied, but the paragraph still follows a management-template skeleton.

## Why Some AIGC Skills Fail Or Increase Risk

This failure can happen even with report-driven AIGC Skills, including upstream-inspired scan-and-iteration workflows, when the workflow does not handle the following two conditions together:

1. **Color metadata loss**. A Word report may store risk bands as font color, such as red/orange/purple runs in DOCX XML. If the agent extracts only plain text, the report looks like another copy of the thesis and red/orange targeting fails.
2. **Template skeleton retention**. HR and management theses often use the same chapter grammar repeatedly: background, concept definition, current situation, problem, cause, countermeasure, guarantee, conclusion. If the rewrite only polishes language, the skeleton remains and the result may look more AI-like.

For this thesis type, "more academic" usually means worse: smoother transitions, more abstract nouns, and neater numbered measures all push the text toward the pattern detectors mark as AI-like.

## Report-First Requirement

When the user provides an AIGC report for a social-science thesis:

1. If the report is DOCX and color-marked, load `references/docx_color_report_extraction.md`.
2. Extract actual red/orange/purple/black spans before rewriting.
3. Count red and orange characters by section.
4. If red + orange covers a large part of the thesis, treat it as a document-level template problem, not a few sentence-level errors.
5. Freeze black, gray, declaration, reference, appendix, and school-template text unless the user explicitly asks otherwise.

Do not proceed from plain-text extraction alone when color metadata exists but has not been parsed.

## Evidence Types That Break The Template

Use only evidence from the thesis, user, or report:

- Company or organization profile.
- Department and岗位 structure.
- Recruitment channels and proportions.
- Survey percentages and cross-tab observations.
- Interview excerpts or summarized feedback.
- Existing制度,流程,表单,考核指标.
- Training frequency, attendance, satisfaction, turnover, conversion, cost, cycle, or complaint data.
- Specific process nodes where problems occur.
- Before/after workflow differences proposed by the author.
- Case-specific constraints such as budget, staff size, region, platform, season, or policy environment.

If the text lacks such evidence, output `HUMAN_EVIDENCE_REQUEST` rather than inventing details.

For HR/recruitment-management theses, use `workflow/author_evidence_pack_template.md` as the default request form.

## Repair Strategy

This file absorbs the social-science parts of the older evidence-injection, structure-rebuilding, anti-shallow-rewrite, and post-rewrite self-audit rules. Those rules are internal checks here, not separate runtime entry modes.

### 0. First Diagnostic Step: Report Color And Rhythm Gate

Before content-level repair, run two checks:

1. Report color gate: identify whether the paragraph is red, orange, purple, black, gray, or unmarked.
2. Rhythm gate: apply `references/burstiness_injection_rules.md` only if the paragraph is actually too uniform.

If sentence rhythm is already varied but the paragraph is red/orange, do not add more short sentences. Switch to evidence-first reconstruction and template-skeleton repair.

For current reports, every red/orange paragraph must still appear in the coverage table. Social-science repair does not replace red/orange coverage; it determines the rewrite strategy for each task.

For social-science text specifically:
- Mix short data-anchored sentences (8-15 chars) with longer analysis sentences (35-50 chars)
- Delete all mechanical connectors ("首先、其次、此外、因此、综上所述")
- Use survey percentages as short sentence anchors
- Allow one-sentence paragraphs only when they fit the formal thesis style

Example — before (σ ≈ 2, AI-detectable):
```text
该企业在招聘渠道方面存在较为单一的问题，主要依赖传统招聘平台，社交媒体渠道的利用程度较低。这种渠道结构导致企业在技术岗位和复合型岗位的招聘中面临较大困难，影响了人才获取的效率和质量。
```

After (σ ≈ 14, more varied but still formal if source data exists):
```text
问卷结果先给出了一个明显信号：传统平台贡献了85%以上的简历来源，社交媒体和专业社区合计不到15%。渠道结构偏窄。对技术岗和复合型岗位而言，这种来源结构会直接限制候选人覆盖面。
```

### 1. Replace Generic Topic Sentences

Bad:

```text
企业应进一步完善招聘管理体系，提高招聘工作的科学性和有效性。
```

Better:

```text
该企业的招聘问题集中在简历初筛和用人部门反馈两个环节。本节先处理岗位需求确认流程，再调整渠道筛选标准。
```

If the school style permits more concise sentences:

```text
问题主要落在两个环节：简历初筛和用人部门反馈。先看初筛。
```

### 2. Put Evidence Before Evaluation

Bad:

```text
招聘渠道较为单一，影响了企业人才获取效率。问卷结果显示，传统招聘平台占比较高。
```

Better:

```text
问卷中多数应聘者来自传统招聘平台，社交媒体和专业社区的来源占比较低。渠道结构过窄，使企业在技术岗和复合型岗位上难以触达更合适的候选人。
```

Better when source percentages exist:

```text
85%的简历来自传统招聘平台，社交媒体和专业社区合计不到15%。这不是渠道数量问题，而是候选人触达结构偏窄。技术岗和复合型岗位在这种结构下更难获得匹配简历。
```

### 3. Break Enumeration Chains

Do not keep long "第一、第二、第三、第四" structures. These are the strongest AI fingerprint in social-science text.

Options:

- Group measures by process stage.
- Convert one list item into a case observation.
- Merge repeated measures.
- Delete empty value endings.
- Use flowing prose with occasional short sentences instead of numbered lists.

Example — before:
```text
第一，完善招聘渠道管理。企业应拓展多元化的招聘渠道，提高人才获取的广度和深度。第二，优化面试流程。企业应建立标准化的面试评估体系，提高面试的科学性和有效性。第三，加强新员工培训。企业应制定系统化的入职培训计划，帮助新员工快速适应岗位要求。
```

After:
```text
渠道管理方面，问卷显示社交媒体和专业社区的使用率不到15%。拓展这两类渠道是当务之急。面试环节的问题在于评估标准不统一——用人部门和HR对同一岗位的要求经常不一致。建议先统一岗位需求确认表，再调整面试评分维度。入职培训目前只有1天的集中讲解，新员工反馈"信息量太大、消化不了"。可以考虑分阶段进行，第一周侧重制度和流程，第二周再安排岗位技能。
```

### 4. Use Process Nodes

For HR and management topics, revise around concrete process nodes:

- recruitment demand confirmation,
- resume screening,
- interview coordination,
- onboarding,
- probation assessment,
- training needs survey,
- performance indicator setting,
- incentive feedback,
- channel review,
- customer complaint handling,
- service recovery.

Each process node should appear with its specific data, problem, or observation — not as a generic category.

### 5. Anti-Formalization Rule

Do NOT make social-science text more formal during rewriting. Common mistakes:

- "招聘渠道单一" → "招聘渠道配置结构有待优化" (WRONG — more AI-like)
- "培训不够" → "培训体系的系统性和完备性有待加强" (WRONG — abstract noun inflation)
- "员工不满意" → "员工满意度处于较低水平" (WRONG — more formal, same meaning)

The correct direction is toward MORE concrete, LESS formal:

- "招聘渠道单一" → "85%的简历来自传统平台，社交媒体渠道几乎没用上"
- "培训不够" → "全年培训只有2次，每次1天，覆盖不到40%的员工"
- "员工不满意" → "问卷中仅22%的员工对现有激励机制表示认可"

### 6. Evidence Anchoring for Social-Science Text

Available evidence types in social-science theses (use only what exists in the source):

- Company name, department structure, position count
- Survey sample size, percentage distributions, cross-tab observations
- Interview participant count, summarized feedback themes
- Existing process flowcharts, forms, evaluation criteria
- Training frequency, attendance rates, satisfaction scores
- Turnover data, recruitment cycle, cost per hire
- Customer complaint categories, handling time, recovery rate
- Before/after workflow differences proposed by the author

If the text lacks such evidence, output `HUMAN_EVIDENCE_REQUEST` — do NOT invent data.

### 7. Paragraph Structure Alternation

Do not use the same paragraph structure throughout the chapter. Alternate between:

- **Data→Analysis→Implication**: Start with a survey finding, analyze what it means, state the implication
- **Case→Problem→Data**: Start with a specific scenario, identify the problem, support with data
- **Process→Observation→Recommendation**: Describe a process node, share what was observed, suggest improvement
- **Contrast→Evidence→Conclusion**: Present two sides or scenarios, show the evidence, draw a conclusion

Do NOT use "问题→原因→对策" for more than 2 consecutive paragraphs.

### 8. Required Self-Audit For Red/Orange Management Paragraphs

After every red/orange social-science paragraph revision, check:

- Was the change more than synonym replacement?
- Did it break or replace the "definition -> meaning -> countermeasure" skeleton when that skeleton existed?
- Did it reduce mechanical "一是、二是、三是、四是" or "首先、其次、最后" enumeration?
- Did it avoid abstract noun inflation such as 机制, 体系, 能力, 保障, 路径, 价值?
- Did it use available company, questionnaire, interview, process, post, indicator, owner, time, form, or boundary evidence?
- If evidence was missing, did it request `workflow/author_evidence_pack_template.md` instead of inventing facts?
- Did the revision avoid becoming smoother, more formal, or more AI-like?

If any red/orange paragraph fails this audit, it cannot be marked as completed. Retry once with a different action type, or output `D_AUTHOR_MATERIAL_REQUEST`.

### 9. 反咨询腔规则 (Anti-Consulting-Speak Rule)

Management thesis paragraphs frequently use consulting-style vocabulary that is a strong AIGC signal. This section defines an explicit prohibition.

#### 9.1 Prohibited High-Frequency Words

The following words are not automatically banned (they may appear naturally in context), but **if 2 or more appear in the same paragraph**, that paragraph must be rewritten:

1. **构建体系** — "构建招聘体系"、"构建培训体系"
2. **提升效率** — "提升招聘效率"、"提升管理效率"
3. **优化路径** — "优化招聘路径"、"优化发展路径"
4. **赋能** — "技术赋能"、"数据赋能"、"组织赋能"
5. **协同** — "部门协同"、"内外协同"、"协同机制"
6. **动态调整** — "根据实际情况动态调整"
7. **精细化运营** — "精细化招聘运营"
8. **智能引擎** — "招聘智能引擎"、"数据智能引擎"
9. **数据驱动** — "数据驱动决策"、"数据驱动招聘"
10. **生态** — "招聘生态"、"人才生态"
11. **漏斗** — "招聘漏斗"、"转化漏斗"
12. **闭环** — "招聘闭环"、"管理闭环"
13. **雇主品牌** — "提升雇主品牌"
14. **可复制范式** — "可复制的招聘范式"
15. **提供参考与借鉴** — "为同类企业提供参考与借鉴"

#### 9.2 Trigger Rule

If a single paragraph contains **2 or more** of the above terms (including variants), it is automatically classified as `CONSULTING_SPEAK_PLATEAU` and must be rewritten.

Counting rule:
- Count exact matches and stem variants. Example: "赋能" matches "技术赋能" and "数据赋能" separately but counts as only one match type. However, "构建招聘体系" and "优化招聘路径" in the same paragraph = 2 matches → trigger.
- The same word used twice in one paragraph counts as 1, not 2. Different words are counted separately.
- "提供参考" without "借鉴" does not count. "提供参考与借鉴" counts as 1 match.

#### 9.3 Rewrite Direction: From Consulting-Speak to Author-Observation

When a paragraph triggers `CONSULTING_SPEAK_PLATEAU`, the rewrite must follow this structure:

```
consulting-speak original:
"A公司应构建科学的招聘体系，优化招聘流程，提升招聘效率。"

rewrite direction (not consulting-speak):
"A公司的招聘目前有三个具体环节出现积压：简历筛选平均耗时5天、面试安排需要跨3个部门协调、offer审批流程没有时间节点。以下分别讨论每个环节的现状和调整空间。"
```

The rewrite must:
1. **Start with an author-observed problem** — "在访谈中，HR反馈……" or "根据问卷数据，……出现……" or "在流程跟踪中发现……"
2. **Include specific evidence** — a number, a frequency, a person's role, a form name, a duration
3. **Propose limited adjustment, not a full solution** — "可以缩短的环节是……，但需要平衡……" not "应构建科学的体系"
4. **State the boundary** — "这一调整仅适用于……，不适用于……" or "但实施前提是……"

#### 9.4 Consulting-Speak ≠ Protected Term

These are NOT protected terms. They can be deleted, replaced, or restructured freely. The only rule is: if 2+ appear in one paragraph, rewrite.

#### 9.5 Relationship to Hard Evidence Rule

The Hard Evidence Rule (next section) lists a subset of these terms as "unacceptable alone." This section extends that rule: even if evidence is present, a paragraph with 2+ consulting-speak terms must still be rewritten to reduce AIGC signal density.

## Hard Evidence Rule For HR And Management Papers

For human resource management paragraphs about current situation, problems, countermeasures, or conclusions, do not accept a rewrite that only says:

- 构建体系
- 提升效率
- 优化流程
- 强化能力
- 丰富渠道
- 数据驱动
- 智能高效
- 提供参考

Accepted rewrites must, when source evidence exists, connect the statement to at least one concrete anchor:

- which company, department, or post;
- which recruitment, training, performance, incentive, service, or management process;
- which form, system, channel, or table;
- which indicator or review standard;
- who is responsible;
- how often the process is reviewed;
- whether the evidence comes from a questionnaire, interview, process document, or existing rule;
- what the implementation boundary is.

If the source does not provide enough evidence, output `HUMAN_EVIDENCE_REQUEST`. Do not invent company facts, questionnaire results, interviews, forms, systems, owners, indicators, review cycles, or boundaries.
Use `workflow/author_evidence_pack_template.md` for the request.

### Anti-Fabrication Enforcement

If a material gap is detected (data needed but not available in source), output a `material_gap_table` and stop. Do NOT fabricate:

- Industry average data (行业平均水平)
- Budget ratios (预算比例)
- Growth rates (增速)
- Turnover rates (流失率)
- Employee headcount (员工规模)
- System launch years (系统上线年份)
- Competitor case studies (竞品企业案例)

Unless these values already exist in the original thesis, the report, the questionnaire, the interview, the user-provided material, or a cited source. When in doubt, mark the gap and request author input.

## Social-Science Acceptance Gate

A red/orange social-science paragraph fails acceptance when:

- it is only synonym replacement;
- it still follows "definition + meaning + countermeasure";
- it still uses long "一是、二是、三是、四是" enumeration;
- abstract nouns remain dense;
- it lacks the company or local research object;
- it lacks questionnaire, interview, process, post, indicator, responsibility, review-cycle, or boundary evidence when such evidence is needed;
- the rewrite becomes smoother, more formal, or more policy-like.

Any failed item triggers a second-pass rewrite. If second pass still fails, output the author evidence request and mark the paragraph incomplete.

## Stop Conditions

Stop and request author input when:

- No company, department, survey, interview, case, or process evidence is available.
- Further rewriting only produces smoother abstract language — this means the rewrite is INCREASING AIGC risk, not reducing it.
- The paragraph depends on cited theory and cannot be safely localized.
- Character delta would exceed the allowed range.
- The rewritten text has sentence-length σ < 8 (still too uniform).
- The rewritten text still uses "首先...其次...最后" or "一是...二是...三是" structure.
- The rewritten text adds abstract nouns (机制, 体系, 能力, 保障, 路径, 价值) without concrete anchors.

When the rewrite is making text smoother rather than more human-like, STOP and diagnose the cause. If rhythm is uniform, apply `references/burstiness_injection_rules.md`; if rhythm is already varied, switch to report-color targeting, evidence-first reconstruction, or template-skeleton repair.

Use labels:

- `SOCIAL_SCIENCE_TEMPLATE_PLATEAU`
- `CASE_EVIDENCE_MISSING`
- `SURVEY_DATA_UNDERUSED`
- `COUNTERMEASURE_LIST_PLATEAU`
- `POLICY_STYLE_PLATEAU`
- `BURSTINESS_INSUFFICIENT` — sentence-length σ < 10, needs rhythm injection
- `FORMALIZATION_REGRESSION` — rewrite made text more formal/polished than original
- `CONNECTOR_OVERLOAD` — more than 5 connectors per paragraph
- `ENUMERATION_FINGERPRINT` — "第一/第二/第三" or "一是/二是/三是" structure detected

## Output

```markdown
## Social-Science Bottleneck Diagnosis
| section | paragraph_id | template_skeleton | available_evidence | missing_evidence | repair_strategy |
|---|---|---|---|---|---|

## Evidence Request
| section | missing_evidence | question_to_author | why_needed |
|---|---|---|---|
```

## Relation To SKILL.md

Use this file with `DISCIPLINE_AIGC_BOTTLENECK_RULES`, `AIGC_PLATEAU_BREAKER`, and `THREE_MODE_COLOR_BAND_WORKFLOW`.
