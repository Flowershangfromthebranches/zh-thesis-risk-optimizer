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
3. Provide the thesis text, chapter, report fragment, or project state.
4. Specify a mode when you know what you want.
5. Ask the agent to preserve citations, data, conclusions, formulas, code, and technical identifiers.

## 3. Common Commands

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

## 4. Full Thesis Workflow

1. Provide the full thesis or chaptered text.
2. Ask for `FULL_THESIS_PROJECT_MODE`.
3. Generate `THESIS_MASTER_OVERVIEW`.
4. Split chapters into `CHAPTER_TASK_MODE` tasks.
5. Build protected term and citation lists.
6. Process high-priority chapters first.
7. Update progress and revision logs after each pass.
8. Use `PROJECT_HANDOFF_MODE` before pausing.

## 5. No-Report Dual Fallback Workflow

When no report is available, do not ask the Skill to promise actual detection changes.

1. Use `NO_REPORT_FALLBACK_WORKFLOW`.
2. Build chapter structure and protected-item lists.
3. Score AIGC and similarity risk heuristically by paragraph.
4. Select only high-editability paragraphs first.
5. Run pass one for structure rebuilding and similarity-expression cleanup.
6. Run pass two for AIGC deep rewrite and self-audit.
7. Mark remaining uncertainty as needing report-based localization.

## 6. Targeted Multipass Workflow

Use this when the user provides targets and multi-round reports.

1. Use `TARGETED_MULTIPASS_ENGINE`.
2. Record only user-provided metrics.
3. Compare original, current, and historical drafts.
4. If AIGC rises after similarity revision, run `AIGC_REGRESSION_GUARD`.
5. Increase evidence density using existing thesis facts.
6. Output next-pass task table.
7. Treat targets as goals, not guaranteed results.

## 7. AIGC-Focused Length-Control Workflow

Use this when similarity reduction is already enough but AIGC risk remains high.

1. Use `AIGC_FOCUSED_LENGTH_CONTROLLED`.
2. Downgrade similarity handling to stability check.
3. Run sentence-level AIGC localization.
4. Compress repeated AI-like expressions.
5. Use replacement-based repair instead of appending explanations.
6. Keep the total growth within the user's budget, default 0-2000 Chinese characters.
7. If the draft exceeds budget, run `LENGTH_COMPRESSION_PASS`.
8. If evidence is missing, output `HUMAN_EVIDENCE_REQUEST` or use conservative repair.

## 8. Similarity Report Workflow

1. Provide thesis source text and report fragments.
2. Use `REPORT_SIMILARITY_ONLY`.
3. Map fragments back to source paragraphs.
4. Assign mapping confidence.
5. Classify source type.
6. Preserve or supplement citations.
7. Revise only confirmed and safe mappings.
8. In dual-risk cases, run `REPORT_DRIVEN_MULTI_PASS_WORKFLOW`.
9. After similarity revision, run AIGC deep rewrite and safety review before rechecking.

## 9. AIGC Report Workflow

1. Provide thesis source text and AIGC report fragments.
2. Use `REPORT_AIGC_ONLY`.
3. Map high-risk fragments back to the thesis.
4. Diagnose AI writing patterns.
5. Protect terms, data, citations, and technical entities.
6. Revise locally and compare heuristic writing-risk scores.
7. If self-audit still finds three or more AI-like risks, run the second-pass rewrite prompt.

## 10. Engineering / Science / CS Notes

Always protect:

- Formulas and variables.
- Code and commands.
- API paths.
- Database table names and fields.
- Function names, class names, and parameters.
- Experiment data, metrics, and chart numbers.
- Model, algorithm, dataset, and protocol names.

## 11. Common Misuse

Do not use this Skill to:

- Fabricate data, experiments, citations, reports, or sources.
- Remove necessary citations.
- Promise external detection outcomes.
- Attack or reverse engineer detection systems.
- Rewrite formulas, code, identifiers, or experiment values for style.
- Repeatedly rewrite already completed low-risk chapters.
- Expand every paragraph to reduce AIGC risk.

## 12. Academic Integrity Reminder

If a sentence depends on a source, keep the citation boundary visible. If a report fragment cannot be mapped confidently, ask for more context before revising. If technical facts are unclear, flag them for human review instead of inventing a fix.
