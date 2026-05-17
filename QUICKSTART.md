# QUICKSTART

## 1. Who This Skill Is For

Use `zh-thesis-risk-optimizer` when you need a Chinese thesis revision workflow for:

- AIGC color-report targeting.
- Red/orange paragraph coverage.
- DOCX/file-copy handling without editing the original file.
- Character-change control.
- Social-science and management-template bottleneck repair.
- Controlled humanization that preserves academic register.
- OOXML-based DOCX format preservation.
- Final acceptance auditing before delivery.

The Skill does not promise any external detection-platform result. It does not crack, simulate, reverse engineer, or forge detection systems or reports.

## 2. Start With Intake

Every matching task starts with `INTAKE_WIZARD_PRECHECK`.

Copy this instruction when you want to use the Skill:

```text
请使用 zh-thesis-risk-optimizer。先执行 INTAKE_WIZARD_PRECHECK。
请展示 workflow/intake_request_template.md 的完整模板，等我填写后再继续。
```

If you already know the inputs, fill the template directly:

```text
【任务目标】只降 AIGC
【论文输入】原文 DOCX：/path/to/original.docx
【处理范围】全文；只处理报告红橙片段
【输出形式】创建副本并回写；同时输出诊断表和验收表
【字数约束】全文 ±10%
【保护项】引用、数据、图表编号、参考文献、学校声明、代码、路径、参数
【AIGC 报告】/path/to/aigc_report.docx
【论文专业和题目】人力资源管理，《……》
【查重报告】无
【报告颜色规则】红色>70%；橙色60%-70%；紫色50%-60%；黑色<50%
【当前状态】原文未改
【历史版本】无
【用户目标】红橙一起处理；不全文大改；不承诺检测结果
【可用证据】问卷、访谈、流程、岗位、指标等材料；没有则写无
【特殊要求】跳过
```

## 3. Entry Modes and Internal Engines

The current slim router exposes these entry modes and internal mandatory engines:

| mode | use when |
|---|---|
| `INTAKE_WIZARD_PRECHECK` | Start every matching task and collect required, recommended, and optional fields. |
| `FILE_INPUT_COPY_WORKFLOW` | The user provides DOCX/TXT/Markdown/LaTeX files; create a copy before editing. |
| `OOXML_DOCX_PATCH_WORKFLOW` | DOCX format preservation required; default writeback method. Internal, not a user entry. |
| `DOCX_COLOR_REPORT_EXTRACTION` | The user provides a Word/DOCX color-marked AIGC report. |
| `THREE_MODE_COLOR_BAND_WORKFLOW` | A task uses red/orange/purple/black color bands for AIGC, similarity, or dual-risk handling. |
| `FIRST_PASS_RED_ORANGE_ENGINE` | Original thesis plus original AIGC report before any rewrite. |
| `CURRENT_REPORT_RED_ORANGE_ENGINE` | Revised/current draft plus its current AIGC report. |
| `AIGC_PLATEAU_BREAKER` | Multiple rounds slow down, red decreases but orange remains, or user reports a plateau after revision. |
| `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` | Human resource management, business administration, marketing, education management, public administration, or similar template-heavy papers. |
| `CONTROLLED_HUMANIZATION_ENGINE` | Internal engine for controlled de-AIGC humanization; breaks AI templates while preserving academic register. Not a user entry. |
| `AIGC_REGRESSION_GUARD` | A rewrite becomes smoother/more AI-like OR too colloquial/casual. |
| `FIRST_PASS_EFFECTIVENESS_GATE` | Internal mandatory gate after first-pass rewrite; checks color migration, AIGC thresholds, tone, and format. Not a user entry. |
| `FINAL_ACCEPTANCE_AUDIT` | End every report-driven or file-copy task with coverage, evidence, regression, tone, format, and character-change checks. |

Other historical rules are internal sub-rules only. Do not invoke them as user-facing entry modes.

## 4. First-Pass AIGC Color Report Workflow

Use this when you have the original paper and original AIGC color report.

```text
请使用 zh-thesis-risk-optimizer。我的任务是只降 AIGC。
输入包括原文 DOCX 和原版 AIGC 颜色报告 DOCX。
颜色规则：红色>70%，橙色60%-70%，紫色50%-60%，黑色<50%。
请同时处理红色和橙色，黑色/低风险/封面/目录/承诺书/参考文献/附录冻结。
全文字符数控制在 ±10%。
DOCX 写回使用 OOXML patch，只替换确认映射的正文段落，保持原格式。
请按强制链路执行，并在最后输出 FINAL_ACCEPTANCE_AUDIT。
```

Required chain:

```text
FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> FIRST_PASS_RED_ORANGE_ENGINE
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable
-> CONTROLLED_HUMANIZATION_ENGINE when applicable
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> FINAL_ACCEPTANCE_AUDIT
```

If any required step is skipped, the task is not complete.

## 5. Controlled Humanization: Absorbing Old Version Strength Safely

If you want to absorb the strong de-AIGC ability of older Skill versions (template-breaking, varied rhythm, author judgment) without losing academic standards, use the controlled humanization strategy:

```text
请使用新版受控人类化策略：吸收 bff6860 的去模板化、句长变化和作者判断能力，
但必须通过 ACADEMIC_TONE_GUARD，不能出现日记式、自媒体式或聊天式表达；
DOCX 写回必须使用 OOXML patch，只替换确认映射的正文段落，保持原格式。
```

The engine supports 3 intensity levels:

| level | AIGC range | behavior |
|---|---|---|
| 1 (light) | < 50% | Only reduce template sentences; strong academic register |
| 2 (medium, default) | 50%-75% | Break templates, add author judgment, vary sentence length, maintain thesis register |
| 3 (strong) | > 75% | Significantly increase human-interpretation feel; constrained by academic tone guard; requires manual review |

There is NO unlimited aggressive colloquialization mode. Level 3 always includes a warning that academic formality may be reduced.

## 6. Current-Report Workflow

Use this when the paper has already been revised once or more and you provide the current draft plus current AIGC report.

```text
请使用 zh-thesis-risk-optimizer。这里是当前稿和当前 AIGC 颜色报告。
请进入 CURRENT_REPORT_RED_ORANGE_ENGINE：
当前报告红色全部处理，橙色全部处理；
紫色只在与红橙同段或必要衔接时处理；
黑色、低风险、封面、目录、承诺书、参考文献、附录冻结。
完成时必须输出红橙覆盖率验收表和 FINAL_ACCEPTANCE_AUDIT。
```

Required chain:

```text
FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> CURRENT_REPORT_RED_ORANGE_ENGINE
-> AIGC_PLATEAU_BREAKER when applicable
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable
-> CONTROLLED_HUMANIZATION_ENGINE when applicable
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> FINAL_ACCEPTANCE_AUDIT
```

## 7. DOCX Format Protection

For DOCX file input, the default writeback method is OOXML patch:

- Copy the original DOCX; never modify the original.
- Unzip the copy; only modify `word/document.xml`.
- Replace only confirmed `w:t` text nodes.
- Preserve styles, numbering, headers, footers, footnotes, endnotes, comments, media, and rels.
- Low-confidence mappings are NOT written back.
- Duplicate matches stop writeback immediately.
- After patching, verify: zip integrity, no duplicate insertion, resource preservation, page count stability.

Do NOT rebuild the entire DOCX unless the user explicitly requests it and accepts format risk.

## 8. Social-Science Evidence Pack

For human resource management and similar management papers, red/orange paragraphs must not be repaired by polished management jargon alone.

If the paragraph lacks company, questionnaire, interview, process, post, form, indicator, owner, review-cycle, or boundary evidence, ask the user to fill:

```text
workflow/author_evidence_pack_template.md
```

Do not fabricate missing interviews, questionnaire results, company systems, indicators, forms, or operational facts.

## 9. Professional Fit

This Skill supports general Chinese thesis text-risk optimization, but it does not claim to fit every discipline automatically.

- Social-science and management papers have special handling for template skeletons, management jargon, questionnaire/interview evidence, posts, processes, forms, indicators, owners, and review cycles.
- Engineering and computer-science papers have special protection for formulas, code, API paths, table names, field names, parameters, experiment data, and running results.
- Other disciplines should provide discipline-specific protected terms, data boundaries, and evidence sources before revision.

## 10. Final Acceptance

Every delivery should include:

- Whether DOCX color metadata was read.
- Red total / processed.
- Orange total / processed.
- Whether social-science bottleneck handling was enabled when applicable.
- Whether synonym-only rewriting appeared.
- Whether the rewrite became more formal, smoother, or more AI-like.
- Character-change result.
- Unprocessed red/orange paragraphs.
- Author evidence still needed.
- Color migration assessment.
- First-pass effectiveness gate result.
- Controlled humanization level used.
- Academic tone guard result.
- OOXML patch result.
- Duplicate insertion guard result.
- Format preservation result.
- Final delivery status.

If red/orange unprocessed count is not zero, or a required chain step is missing, the task must not be marked complete.
