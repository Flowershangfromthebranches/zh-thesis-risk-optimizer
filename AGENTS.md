# AGENTS.md

## Project Rules

- Treat this repository as an academic-integrity-first Skill project.
- Keep `SKILL.md` frontmatter valid YAML and keep `name`, `description`, and `license` aligned with README.
- Do not add claims that promise detection outcomes or platform-specific results.
- Preserve the distinction between AIGC risk optimization and similarity risk optimization.
- Always protect citations, data, conclusions, formulas, code, interfaces, table names, field names, parameters, and technical terms.
- For upstream-inspired content, keep attribution in `README.md` and `NOTICE`.
- If a source license is unclear, only use design ideas and avoid copying substantial text.

## v0.2 Scoring Diagnosis Rules

- Scoring must always be described as heuristic writing-risk scoring.
- Never state or imply that scores equal any real detection system result.
- Sentence-level localization must protect formulas, code, citations, experiment data, and technical entities.
- Before/after score comparison is only a writing-risk reference.
- Do not add promises that a score will drop to a specific percentage or external threshold.
- Citation and technical protection outrank AIGC-risk reduction and similarity-risk reduction.
- Risk labels should be descriptive, not verdict-like. Use them to guide revision priority.
- Protected or no-edit zones should be preserved unless the user explicitly confirms a targeted change.

## v0.3 Report-Driven Mapping Rules

- Report-driven mode must not fabricate report content.
- Do not invent detection-system names, percentages, similarity sources, or risk levels.
- If a report fragment cannot be mapped to the source text, mark it `UNMAPPED`.
- Low-confidence mappings must not be directly rewritten.
- Citation integrity outranks similarity-risk reduction.
- Necessary citations must not be deleted.
- Similarity-source content must not be disguised as uncited original writing.
- Protect formulas, code, interfaces, table names, fields, experiment data, and reference entries.
- Do not implement commercial detection-system cracking or reverse engineering.
- Do not promote detection evasion.
- Separate user-provided report facts from the Skill's heuristic diagnosis.

## v0.4 Full-Thesis Workflow Rules

- `SKILL.md` must stay slim and function as a router, not a full rule library.
- New complex rules should go in `references/`, not in `SKILL.md`.
- Templates go in `workflow/`.
- Execution prompts go in `prompts/`.
- Examples go in `examples/`.
- Do not promise specific AI-rate, similarity-rate, or detection-rate targets.
- Do not promise external detection outcomes.
- Full-thesis mode must not rewrite the whole thesis in one pass.
- Always create an overview first, then chapter tasks, then prioritized paragraph work.
- Low-confidence report mappings, citation-heavy paragraphs, and experiment-data-heavy paragraphs must enter human-review status.
- Iterative optimization must not repeatedly overhaul completed chapters.
- Progress tracking must record protected items and human review items.

## Repository Documentation Rules

- README is user-facing and should stay concise.
- CHANGELOG records version history.
- THIRD_PARTY_NOTICES records upstream sources, license observations, referenced ideas, and attribution.
- NOTICE stays short and points to THIRD_PARTY_NOTICES for details.
- `SKILL.md` remains a high-level routing document.
- New rules go in `references/`.
- New templates go in `workflow/`.
- New prompts go in `prompts/`.
- New examples go in `examples/`.
- Do not promise detection outcomes.
- Do not promote detection evasion.
- Do not fabricate reports, data, experiments, citations, percentages, sources, or risk levels.
- Audit every path referenced from `SKILL.md`; referenced files must exist.

## v0.5 Effective Rewrite Engine Rules

- Do not keep adding new modes when the problem is weak execution; prioritize rewrite effectiveness.
- AIGC-risk reduction must not rely on synonym replacement.
- Dual optimization must state the order of operations.
- No-report mode must state its limits and remain heuristic.
- Report-driven mode must use multi-pass processing.
- Every substantial rewrite must run a post-rewrite self-audit.
- If the self-audit hits three or more AI-risk items, run a second-pass rewrite.
- Technical facts, citation boundaries, data, conclusions, formulas, code, interfaces, table names, fields, and parameters still outrank rewrite aggressiveness.

## v0.6 Targeted Multipass Rules

- User targets such as similarity below 10% and AIGC below 20% are goals, not guarantees.
- If a new report shows similarity improved but AIGC worsened, mark `PARTIAL_SUCCESS_SIMILARITY_ONLY_AIGC_FAILED`.
- Do not treat v0.4 historical improvement as a success standard.
- Do not treat v0.5-style formalization as quality improvement.
- Run report difference diagnosis before another rewrite when historical reports are available.
- Use existing evidence before rewriting; ask for author supplementation when evidence is missing.
- AIGC regression guard must run when a rewrite becomes more formal, smoother, or less concrete.
- Completion requires report trend improvement plus no factual, citation, data, or technical damage.

## v0.7 AIGC-Focused Length-Control Rules

- When similarity is already acceptable, do not keep similarity reduction as the main objective.
- AIGC-focused work must use a whole-thesis length budget, default 0-2000 added Chinese characters.
- Prefer replacement-based reconstruction over append-based expansion.
- Sentence-level AIGC localization should precede high-risk paragraph rewriting.
- Process only key high-risk sentences when possible; do not rewrite every sentence by default.
- If the draft exceeds the budget, run Compression Pass before marking completion.
- Missing evidence should trigger author questions or conservative repair, not invented detail.
- Repeated AI-like expressions should be compressed to create budget for necessary evidence.

## v0.8 AIGC Plateau Breaker Rules

- Do not treat red/high-risk reduction alone as AIGC success.
- If red risk decreases but orange/medium-risk text remains high, enter `AIGC_PLATEAU_BREAKER`.
- Orange-zone paragraphs need structural repair, not another light synonym or connector pass.
- Freeze white/low-risk paragraphs and do not spend rewrite budget on them.
- After two or more weak-improvement rounds, mark `NO_PROGRESS_REWRITE_LOOP` before trying another normal rewrite.
- Distinguish computer-science technical protected plateaus from management/business template plateaus.
- For computer-science plateaus, protect code, paths, APIs, parameters, table names, fields, formulas, and data; revise only surrounding explanations.
- For management/business plateaus, break list structures and anchor paragraphs in survey, interview, company, or case-specific evidence.
- If remaining risk is protected or evidence-limited, label it instead of inventing details or repeatedly rewriting.

## v0.8.1 Red-Orange First-Pass Rules

- When the original thesis and original AIGC report are available, do not wait for orange plateau; use `FIRST_PASS_RED_ORANGE_ENGINE`.
- Red/high-risk and orange/medium-risk fragments both belong in the first-pass primary task table.
- Purple/light-risk fragments are secondary cleanup; black/white/low-risk fragments are frozen by default.
- Internal retry loops must be finite and must use a different repair move on retry.
- Do not mark a paragraph complete just because red became orange; the heuristic target is purple/black-like when safe.
- Whole-thesis character change must stay within `±10%` by default unless the user provides another range.
- If character delta exceeds the allowed range, mark `CHARACTER_DELTA_FAIL` and run compression before completion.
- Stop rather than continue recursion when facts, citations, technical identifiers, protected text, or evidence limits block safe revision.

## v0.8.2 Skill Slimming Rules

- Keep `SKILL.md` as a concise family-based router.
- Do not re-add a long reference index that duplicates the mode router.
- Keep detailed rules in `references/`, executable prompts in `prompts/`, and project templates in `workflow/`.
- When adding new modes, add one concise router row and put implementation detail in a separate file.
- After slimming, audit all paths referenced from `SKILL.md`.

## v0.8.3 Three-Mode File Workflow Rules

- Default user-facing modes are similarity-only, AIGC-only, and dual revision.
- Report color legend defaults to red above 70%, orange 60%-70%, purple 50%-60%, and black below 50% unless the report says otherwise.
- Red and orange are primary targets in both similarity and AIGC reports.
- Purple is light cleanup only; black, gray, and white are frozen unless needed for context.
- All modes must apply whole-thesis character delta guard, default `±10%`.
- If input is a file, never edit the original file directly.
- File workflows must create a copy, extract target text, write safe revisions back to the copy, and deliver the copy.
- Low-confidence or unmapped file fragments must not be written back automatically.

## v0.8.4 Social-Science Template Bottleneck Rules

- HR, business administration, marketing, education management, public administration, accounting/financial management, tourism, logistics, and similar applied theses can plateau even with reports.
- Do not solve these papers with smoother management language.
- Detect repeated "status -> problem -> cause -> countermeasure -> guarantee" skeletons.
- Use organization, survey, interview, process, department, post,制度, indicator, or case evidence to rebuild paragraphs.
- If evidence is missing, output `HUMAN_EVIDENCE_REQUEST`; do not invent company facts, survey data, interview feedback,制度, or指标.
- Preserve policy, theory, citation, and data boundaries.

## v0.8.5 Intake Wizard Rules

- Run `INTAKE_WIZARD_PRECHECK` whenever a task is routed to this Skill.
- Use `INTAKE_WIZARD` when the precheck finds that goal, input type, report availability, scope, output format, or protection rules are unclear.
- Do not run the wizard when enough context is already present; route directly and state the chosen mode.
- Ask only for missing information, preferably 4 to 7 compact fields.
- Provide selectable options plus "自动判断 / 其他补充".
- Default to whole-thesis character change `±10%`, default AIGC color legend red above 70%, orange 60%-70%, purple 50%-60%, black below 50%, and file-copy handling for file input.
- Keep protection defaults visible: citations, formulas, code, APIs, paths, table names, field names, parameters, experiment data, and reference entries.
- Never ask the user to invent reports, data, experiments, citations, interviews, case facts, or risk percentages.

## v0.8.6 DOCX Color Report And Social-Science Failure Rules

- For Word / DOCX reports with color-marked AIGC or similarity risk, parse color metadata before plain-text extraction.
- If a DOCX report looks like another copy of the thesis after text extraction, assume color metadata may have been lost and stop report-driven rewriting until colors are recovered or supplied.
- Do not treat burstiness as a universal cure. If rhythm is already varied and red/orange risk remains, use template-skeleton repair and evidence-first reconstruction.
- For HR and management theses, do not convert paragraphs into slogan-like short sentences just to vary rhythm.
- Diagnose failures from upstream-inspired workflows as workflow limitations, such as color metadata loss, formalization regression, template skeleton retention, or evidence underuse.
- Preserve respectful attribution to upstream projects; do not claim that an upstream project is defective based on one thesis.

## v0.9.2 Intake Precheck Template Rules

- Any task that matches this Skill starts with `INTAKE_WIZARD_PRECHECK`, even if the user does not explicitly say "use this Skill".
- If enough context is present, output an `Intake Confirmation` block and continue; do not force the user through the full template.
- If required fields are missing, show or reference `workflow/intake_request_template.md` and ask only for the missing fields.
- Keep intake fields grouped as required, strongly recommended, and optional so users know what is mandatory.
- Required fields are task goal, thesis input, processing scope, output form, character constraint, and protection items.
- Strongly recommended fields are AIGC report, similarity report, report color legend, thesis major/title, and current state.
- README and QUICKSTART should point users to the template instead of asking them to memorize the full mode router.
- All new mode routes, templates, and tests must preserve the rule that citations, facts, reports, and protected technical content are not fabricated or damaged.

## Validation Checklist

- `SKILL.md` contains the required frontmatter.
- README explains positioning, core capabilities, quick start, modes, recommended workflow, limitations, upstream relationship, and license.
- CHANGELOG records version changes.
- NOTICE is concise and points to THIRD_PARTY_NOTICES.
- THIRD_PARTY_NOTICES thanks upstream authors and records observed license status.
- Prompts cover AIGC_ONLY, SIMILARITY_ONLY, DUAL_OPTIMIZATION, scoring diagnosis, sentence-level diagnosis, report-driven mapping, full-thesis project management, progress tracking, handoff, engineering/science mode, general academic mode, heatmap use, and checklist use.
- Examples cover AIGC-only, similarity-only, dual optimization, engineering thesis, citation-heavy text, long-thesis workflow, scoring diagnosis, sentence-level localization, before/after comparison, report mapping, report-driven revision, full-thesis project setup, chapter tasks, progress tracking, iterative revision, project handoff, and Skill slimming.
- Tests document structure checks, safety checks, scoring-output checks, report-mapping checks, report-driven safety checks, workflow-template checks, full-thesis project checks, and Skill slimming checks.
