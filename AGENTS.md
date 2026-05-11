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

## Validation Checklist

- `SKILL.md` contains the required frontmatter.
- README explains positioning, modes, limitations, upstream relationship, license, scoring disclaimer, and academic integrity.
- NOTICE thanks upstream authors and records observed license status.
- Prompts cover AIGC_ONLY, SIMILARITY_ONLY, DUAL_OPTIMIZATION, scoring diagnosis, sentence-level diagnosis, report-driven mapping, engineering/science mode, general academic mode, heatmap use, and checklist use.
- Examples cover AIGC-only, similarity-only, dual optimization, engineering thesis, citation-heavy text, long-thesis workflow, scoring diagnosis, sentence-level localization, before/after comparison, report mapping, and report-driven revision.
- Tests document structure checks, safety checks, scoring-output checks, report-mapping checks, and report-driven safety checks.
