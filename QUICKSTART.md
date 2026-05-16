# QUICKSTART

## 1. Who This Skill Is For

Use this Skill if you are revising a Chinese thesis and need help with:

- AIGC-style writing risk.
- Similarity-risk and repeated expression.
- Report fragment mapping.
- Citation and source-boundary protection.
- Engineering, science, or computer-science technical entities.
- Full-thesis project planning and progress tracking.

## 2. Using It With Coding Agents

For Codex, Claude Code, Copilot, or similar agents:

1. Put this repository where the agent can read it.
2. Ask the agent to load `SKILL.md`.
3. Start with `INTAKE_WIZARD_PRECHECK`.
4. Fill in the required fields from `workflow/intake_request_template.md`.
5. Provide the thesis text, chapter, report fragment, file path, or project state.
6. Ask the agent to preserve citations, data, conclusions, formulas, code, and technical identifiers.

Every use of this Skill should start with intake precheck. If the required fields are already present, the agent should output an `Intake Confirmation` block and continue without asking the full template.

```text
当前任务需要使用 zh-thesis-risk-optimizer。请先执行 INTAKE_WIZARD_PRECHECK。
如果信息不足，请让我复制填写 workflow/intake_request_template.md；
如果信息足够，请输出 Intake Confirmation 后继续。
```

## 3. Common Commands

```text
请使用 zh-thesis-risk-optimizer。下面是我的 intake 模板：
【任务目标】只降 AIGC
【论文输入】原文 DOCX：/path/to/original.docx
【处理范围】全文，只处理报告红橙片段
【输出形式】创建副本并回写，同时输出诊断表
【字数约束】全文 ±10%
【保护项】引用、数据、图表编号、参考文献、学校声明
【AIGC 报告】/path/to/aigc_report.docx
【论文专业和题目】人力资源管理，《……》
```

```text
请对我的完整论文建立全文双降项目总览，不要先改写。
```

```text
这是论文原文和查重报告片段，请先映射回原文，再输出报告驱动任务表。
```

```text
请用 AIGC_ONLY 处理下面段落，不要改变术语和引用。
```

```text
请用 SIMILARITY_ONLY 处理这段理论基础，保留必要引用。
```

```text
请用 DUAL_OPTIMIZATION 处理这一节，先处理相似风险，再检查 AI 味。
```

```text
请用 AIGC_DEEP_REWRITE_ENGINE 深度改写下面段落，先列出保留事实和禁止改动项。
```

```text
我的目标是查重相似度 <10%、AIGC <20%。请读取原文、当前稿、历史报告和新报告，先做报告差异诊断，再生成 TARGETED_MULTIPASS_ENGINE 下一轮任务表。
```

```text
查重已经基本达标，当前稿比原文扩写太多。请进入 AIGC_FOCUSED_LENGTH_CONTROLLED，把全文增幅控制在 0-2000 中文字内，先输出 AIGC 热点句表和长度预算表。
```

```text
我有原文、三轮改写稿和对应 AIGC 报告。AIGC 下降到 54% 后变慢，请进入 AIGC_PLATEAU_BREAKER，先分析红色/橙色/紫色风险带趋势，再输出橙色平台期任务表。
```

```text
这是原版论文和原版 AIGC 报告。请进入 FIRST_PASS_RED_ORANGE_ENGINE，首轮同时处理红色和橙色片段，黑色/低风险段落冻结，整篇论文总字符变动控制在 ±10% 内。
```

```text
这是原文 DOCX 和 Word 颜色标记 AIGC 报告 DOCX。请先进入 DOCX_COLOR_REPORT_EXTRACTION，提取红/橙/紫/黑颜色片段，再进入 REPORT_AIGC_ONLY 或 FIRST_PASS_RED_ORANGE_ENGINE。
```

```text
请进入 THREE_MODE_COLOR_BAND_WORKFLOW。模式：双降。输入是论文 DOCX 文件、查重报告和 AIGC 报告。请先创建原文件副本，不改原文件；按红色>70%、橙色60%-70%、紫色50%-60%、黑色<50%处理，红橙为主处理区，全文字符变动控制在±10%。
```

```text
改写后 AIGC 率反而上升了，请进入 AIGC_REGRESSION_GUARD，分析哪些段落改写后变得更精致/更平衡/更抽象，然后用 BURSTINESS_INJECTION 做节奏审计，只对确实过度均整的段落做自然节奏修复。
```

## 4. Intake Template

The full copyable template is in [workflow/intake_request_template.md](workflow/intake_request_template.md).

Required fields:

- Task goal.
- Thesis input.
- Processing scope.
- Output format.
- Character constraint.
- Protected items.

Strongly recommended fields:

- AIGC report if reducing AIGC risk.
- Similarity report if revising similarity risk.
- Report color legend if color-marked reports are used.
- Thesis major and title.
- Current state, such as original draft, rewritten draft, AIGC regression, or plateau.

## 5. Full Thesis Workflow

1. Provide the full thesis or chaptered text.
2. Ask for `FULL_THESIS_PROJECT_MODE`.
3. Generate `THESIS_MASTER_OVERVIEW`.
4. Split chapters into `CHAPTER_TASK_MODE` tasks.
5. Build protected term and citation lists.
6. Process high-priority chapters first.
7. Update progress and revision logs after each pass.
8. Use `PROJECT_HANDOFF_MODE` before pausing.

## 6. No-Report Dual Fallback Workflow

When no report is available, do not ask the Skill to promise actual detection changes.

1. Use `NO_REPORT_FALLBACK_WORKFLOW`.
2. Build chapter structure and protected-item lists.
3. Score AIGC and similarity risk heuristically by paragraph.
4. Select only high-editability paragraphs first.
5. Run pass one for structure rebuilding and similarity-expression cleanup.
6. Run pass two for AIGC deep rewrite and self-audit.
7. Mark remaining uncertainty as needing report-based localization.

## 7. Targeted Multipass Workflow

Use this when the user provides targets and multi-round reports.

1. Use `TARGETED_MULTIPASS_ENGINE`.
2. Record only user-provided metrics.
3. Compare original, current, and historical drafts.
4. If AIGC rises after similarity revision, run `AIGC_REGRESSION_GUARD`.
5. Increase evidence density using existing thesis facts.
6. Output next-pass task table.
7. Treat targets as goals, not guaranteed results.

## 8. AIGC-Focused Length-Control Workflow

Use this when similarity reduction is already enough but AIGC risk remains high.

1. Use `AIGC_FOCUSED_LENGTH_CONTROLLED`.
2. Downgrade similarity handling to stability check.
3. Run sentence-level AIGC localization.
4. Compress repeated AI-like expressions.
5. Use replacement-based repair instead of appending explanations.
6. Keep the total growth within the user's budget, default 0-2000 Chinese characters.
7. If the draft exceeds budget, run `LENGTH_COMPRESSION_PASS`.
8. If evidence is missing, output `HUMAN_EVIDENCE_REQUEST` or use conservative repair.

## 9. AIGC Plateau Breaker Workflow

Use this when several AIGC rounds improve slowly or report colors show red text falling while orange text remains high.

1. Use `AIGC_PLATEAU_BREAKER`.
2. Compare the original and each rewrite report by risk band.
3. If red risk decreased but orange stayed high, enter `ORANGE_PLATEAU_PASS`.
4. Freeze white/low-risk paragraphs.
5. Identify whether the plateau is technical-protected, management-template, evidence-limited, or likely a report-model floor.
6. For orange management-style paragraphs, break enumeration, start from local evidence, and compress repeated value claims.
7. For computer-science plateaus, protect code, APIs, parameters, paths, formulas, table names, fields, and data.
8. If a paragraph has been rewritten repeatedly without report improvement, mark `NO_PROGRESS_REWRITE_LOOP` and request missing evidence or human review.

## 10. First-Pass Red-Orange Workflow

Use this when the user provides the original thesis and original AIGC report before any rewrite.

1. Use `FIRST_PASS_RED_ORANGE_ENGINE`.
2. Parse report color or risk-band meaning.
3. Put red/high-risk and orange/medium-risk paragraphs into the primary task table.
4. Use sentence-level localization inside each red/orange paragraph.
5. Run a finite internal self-audit loop, default at most two internal passes.
6. Use a different repair move on retry.
7. Freeze black/white/low-risk paragraphs.
8. Apply `CHARACTER_DELTA_GUARD`; default whole-thesis character change is `±10%`.
9. If safe revision cannot reach the heuristic purple/black target, mark protected, evidence-limited, character-delta, or no-progress status.

## 11. Three-Mode Color-Band Workflow

Use this as the default work mode for similarity-only, AIGC-only, or dual revision.

1. Choose one mode: `SIMILARITY_ONLY`, `AIGC_ONLY`, or `DUAL_OPTIMIZATION`.
2. If the matching report exists, use report-driven processing.
3. If no report exists, use heuristic diagnosis and state that report-based localization is better.
4. Use the default color legend: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
5. Treat red and orange as primary targets.
6. Treat purple as light cleanup only.
7. Freeze black, gray, and white unless needed for context.
8. Apply whole-thesis character delta guard, default `±10%`.
9. For file input, create a copy and write revisions back to the copy only.

## 12. Similarity Report Workflow

1. Provide thesis source text and report fragments.
2. Use `REPORT_SIMILARITY_ONLY`.
3. Map fragments back to source paragraphs.
4. Assign mapping confidence.
5. Classify source type.
6. Preserve or supplement citations.
7. Revise only confirmed and safe mappings.
8. In dual-risk cases, run `REPORT_DRIVEN_MULTI_PASS_WORKFLOW`.
9. After similarity revision, run AIGC deep rewrite and safety review before rechecking.

## 13. AIGC Report Workflow

1. Provide thesis source text and AIGC report fragments.
2. Use `REPORT_AIGC_ONLY`.
3. Map high-risk fragments back to the thesis.
4. Diagnose AI writing patterns.
5. Protect terms, data, citations, and technical entities.
6. Revise locally and compare heuristic writing-risk scores.
7. If self-audit still finds three or more AI-like risks, run the second-pass rewrite prompt.

## 14. Engineering / Science / CS Notes

Always protect:

- Formulas and variables.
- Code and commands.
- API paths.
- Database table names and fields.
- Function names, class names, and parameters.
- Experiment data, metrics, and chart numbers.
- Model, algorithm, dataset, and protocol names.

## 15. Common Misuse

Do not use this Skill to:

- Fabricate data, experiments, citations, reports, or sources.
- Remove necessary citations.
- Promise external detection outcomes.
- Attack or reverse engineer detection systems.
- Rewrite formulas, code, identifiers, or experiment values for style.
- Repeatedly rewrite already completed low-risk chapters.
- Expand every paragraph to reduce AIGC risk.
- Edit the original file directly when the user provided a file.

## 16. Academic Integrity Reminder

If a sentence depends on a source, keep the citation boundary visible. If a report fragment cannot be mapped confidently, ask for more context before revising. If technical facts are unclear, flag them for human review instead of inventing a fix.
