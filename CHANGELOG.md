# CHANGELOG

## v0.8.4-social-science-template-bottleneck

- Added social-science template bottleneck rules for HR, business, marketing, education management, public administration, accounting, tourism, logistics, and similar applied theses.
- Added prompt for social-science AIGC plateau diagnosis and evidence-first repair.
- Expanded discipline and paragraph strategies for "status -> problem -> cause -> countermeasure -> guarantee" templates.
- Added regression tests for HR, education management, marketing, public administration, and financial management cases.

## v0.8.3-three-mode-file-workflow

- Added three-mode color-band workflow for similarity-only, AIGC-only, and dual revision.
- Standardized default color meanings: red above 70%, orange 60%-70%, purple 50%-60%, black below 50%.
- Added file input copy workflow: never edit the original file, revise a copied file, and preserve formatting where possible.
- Required all modes to apply whole-thesis character delta guard with default `±10%`.
- Updated report-driven AIGC, report-driven similarity, and dual prompts to analyze color reasons and prioritize red/orange fragments.

## v0.8.2-skill-slimming

- Slimmed `SKILL.md` into a concise family-based router.
- Removed the long duplicate reference index from `SKILL.md`.
- Grouped AIGC, similarity, report-driven, diagnosis/guard, and full-thesis workflows.
- Preserved all existing `references/`, `prompts/`, `workflow/`, examples, and tests.

## v0.8.1-red-orange-first-pass

- Added first-pass red-orange engine for original thesis plus original AIGC report workflows.
- Red/high-risk and orange/medium-risk report bands now both enter the first-pass primary task table.
- Added finite internal red/orange self-audit loop with stop states for protection, evidence limits, character delta failure, and no-progress rewrites.
- Added character delta guard with default whole-thesis `±10%` change range.
- Updated README, SKILL router, quickstart, quality checklist, and tests.

## v0.8.0-aigc-plateau-breaker

- Added AIGC plateau breaker for multi-round cases where AIGC reduction slows after initial improvement.
- Added orange-zone rewrite strategy for persistent medium-risk paragraphs.
- Added discipline-specific AIGC bottleneck rules for computer-science technical plateaus and management/business template plateaus.
- Added plateau-breaker execution prompt, local case example, and v0.8 regression tests.
- Updated Skill routing, quality checklist, quickstart, and repository maintenance rules.

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
