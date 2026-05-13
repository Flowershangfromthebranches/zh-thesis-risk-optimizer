# CHANGELOG

## v0.7.0-aigc-focused-length-controlled-engine

- Added AIGC-focused length-controlled engine for cases where similarity reduction is already enough.
- Added length budget controller with default whole-thesis growth of 0-2000 Chinese characters.
- Added sentence-level AIGC localization, burstiness/rhythm control, repeated-expression compression, human evidence requests, and conservative AIGC repair.
- Added AIGC-focused execution prompt and length compression pass prompt.
- Added Web vulnerability scanner AIGC-focused length-control example and v0.7 regression tests.
- Updated deep rewrite, evidence injection, arbitration, and quality checklist rules to prevent over-expansion.

## v0.6.0-targeted-multipass-engine

- Added target-driven multi-pass workflow for similarity and AIGC goals.
- Added optimization target interpretation with explicit non-guarantee boundaries.
- Added report feedback loop for multi-round report comparison.
- Added AIGC regression guard for formalization, over-smoothing, abstract noun inflation, and evidence dilution.
- Added content substance injection and evidence-density rules.
- Added paragraph-type strategies for abstract, background, literature review, technology overview, feasibility, design, testing, and conclusion.
- Added similarity below 10 and AIGC below 20 specialty strategies as user-goal workflows.
- Added Web vulnerability scanner regression case and v0.6 targeted multipass tests.

## v0.5.0-effective-rewrite-engine

- Added AIGC deep rewrite engine for structure, rhythm, specificity, and argument rebuilding.
- Added paragraph structure rebuilding rules.
- Added evidence and trace injection rules that only use user-provided facts.
- Added dual-optimization arbitration for conflicts between similarity-risk revision and AIGC-risk revision.
- Added no-report fallback workflow with diagnosis-first, high-editability targeting, and two-pass revision.
- Added report-driven multi-pass workflow: mapping, similarity pass, AIGC deep rewrite pass, safety review, and recheck advice.
- Added L5 rewrite intensity for high-risk, non-protected paragraphs.
- Added anti-shallow-rewrite rules.
- Added mandatory post-rewrite AIGC self-audit and second-pass rewrite trigger.

## v0.4.1-cleanup

- Fixed Markdown structure and kept core documents as normal multi-line Markdown.
- Verified `SKILL.md` YAML frontmatter.
- Audited `SKILL.md` references and ensured referenced resources exist.
- Simplified README for public users.
- Moved detailed version notes into CHANGELOG.
- Added QUICKSTART and THIRD_PARTY_NOTICES.
- Added repository integrity checklist.

## v0.4.0-full-thesis-workflow

- Added full-thesis project management.
- Added thesis master overview, chapter tasks, progress tracking, revision logs, iteration plans, and project handoff templates.
- Added iterative revision workflow for second-pass and third-pass report-driven optimization.
- Slimmed `SKILL.md` into a routing document and moved detailed rules into `references/`, `prompts/`, and `workflow/`.

## v0.3.0-report-driven-mapping

- Added report-driven workflows for similarity reports and AIGC reports.
- Added report-to-source mapping.
- Added similarity source handling.
- Added mapping confidence levels: `HIGH`, `MEDIUM`, `LOW`, and `UNMAPPED`.
- Added report-driven task tables and safety checks.

## v0.2.0-scoring-diagnosis

- Added heuristic scoring diagnosis.
- Added sentence-level risk localization.
- Added risk label system.
- Added risk heatmap table.
- Added before/after heuristic score comparison.
- Added no-edit zone rules.

## v0.1.0-initial

- Added initial AIGC and similarity-risk optimization Skill.
- Added `AIGC_ONLY`, `SIMILARITY_ONLY`, `DUAL_OPTIMIZATION`, `AUTO_DIAGNOSIS`, and `ENGINEERING_SCIENCE_MODE`.
- Added citation integrity, protected terms, long-context consistency, and chapter strategy references.
