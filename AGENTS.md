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

## Validation Checklist

- `SKILL.md` contains the required frontmatter.
- README explains positioning, core capabilities, quick start, modes, recommended workflow, limitations, upstream relationship, and license.
- CHANGELOG records version changes.
- NOTICE is concise and points to THIRD_PARTY_NOTICES.
- THIRD_PARTY_NOTICES thanks upstream authors and records observed license status.
- Prompts cover AIGC_ONLY, SIMILARITY_ONLY, DUAL_OPTIMIZATION, scoring diagnosis, sentence-level diagnosis, report-driven mapping, full-thesis project management, progress tracking, handoff, engineering/science mode, general academic mode, heatmap use, and checklist use.
- Examples cover AIGC-only, similarity-only, dual optimization, engineering thesis, citation-heavy text, long-thesis workflow, scoring diagnosis, sentence-level localization, before/after comparison, report mapping, report-driven revision, full-thesis project setup, chapter tasks, progress tracking, iterative revision, project handoff, and Skill slimming.
- Tests document structure checks, safety checks, scoring-output checks, report-mapping checks, report-driven safety checks, workflow-template checks, full-thesis project checks, and Skill slimming checks.
