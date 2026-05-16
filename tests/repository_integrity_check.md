# Repository Integrity Check

Use this checklist before publishing documentation cleanup releases.

## Markdown Format

- [ ] `README.md` is normal multi-line Markdown.
- [ ] `SKILL.md` is normal multi-line Markdown.
- [ ] `NOTICE` is normal multi-line text/Markdown.
- [ ] `AGENTS.md` is normal multi-line Markdown.
- [ ] Markdown tables have line breaks.
- [ ] Code blocks are closed.

## SKILL.md

- [ ] `SKILL.md` frontmatter is valid YAML.
- [ ] `SKILL.md` remains a concise routing document.
- [ ] `SKILL.md` uses family-based router groups instead of a long duplicate reference index.
- [ ] Files referenced from `SKILL.md` under `references/` exist.
- [ ] Files referenced from `SKILL.md` under `prompts/` exist.
- [ ] Files referenced from `SKILL.md` under `workflow/` exist.
- [ ] v0.6 target-driven routes point to existing files.
- [ ] v0.7 AIGC-focused length-control routes point to existing files.
- [ ] v0.8 AIGC plateau breaker routes point to existing files.
- [ ] v0.8.1 red-orange first-pass routes point to existing files.
- [ ] v0.8.2 slimming keeps detailed rules outside `SKILL.md`.
- [ ] v0.8.3 three-mode file workflow routes point to existing files.
- [ ] v0.8.4 social-science template bottleneck routes point to existing files.

## Repository Docs

- [ ] README is concise and user-facing.
- [ ] Detailed version notes live in `CHANGELOG.md`.
- [ ] `QUICKSTART.md` exists.
- [ ] `THIRD_PARTY_NOTICES.md` exists.
- [ ] NOTICE is concise and points to third-party notices.
- [ ] Third-party notices record links, license observations, referenced ideas, code-copy status, and thanks.

## Safety

- [ ] The project does not promise external detection outcomes.
- [ ] The project does not promote detection evasion.
- [ ] The project does not promise fixed reduction percentages.
- [ ] The project does not support forged reports, data, experiments, citations, sources, or risk levels.
- [ ] Targets such as similarity below 10% and AIGC below 20% are described as goals, not guarantees.
- [ ] AIGC-focused work includes a length budget and does not encourage uncontrolled expansion.
- [ ] AIGC plateau work does not treat red-risk reduction alone as completion.
- [ ] Orange-zone work freezes white/low-risk paragraphs instead of rewriting everything again.
- [ ] First-pass red-orange work does not defer orange/medium-risk paragraphs to later rounds.
- [ ] Whole-thesis character change defaults to `±10%` unless the user specifies another range.
- [ ] File input workflows do not modify the original file directly.
- [ ] Social-science bottleneck workflows request missing evidence instead of fabricating case facts.
