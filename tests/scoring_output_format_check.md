# Scoring Output Format Check

Use this manual checklist before publishing v0.2-scoring-diagnosis.

## Mode Coverage

- [ ] `SCORING_DIAGNOSIS_MODE` exists.
- [ ] `SENTENCE_LEVEL_DIAGNOSIS_MODE` exists.
- [ ] `BEFORE_AFTER_SCORE_COMPARISON` exists.
- [ ] `RISK_LABEL_SYSTEM` exists.
- [ ] `SAFE_NO_EDIT_ZONE` exists.

## Reference Coverage

- [ ] `references/scoring_framework.md` exists.
- [ ] `references/sentence_level_diagnosis.md` exists.
- [ ] `references/risk_labels.md` exists.
- [ ] `references/no_edit_zone_rules.md` exists.

## Disclaimer and Safety

- [ ] Scoring disclaimer exists.
- [ ] Scores are described as heuristic writing-risk scores.
- [ ] Scores are not described as equivalent to any real detection system.
- [ ] README thanks `openclaw/humanize-chinese`.
- [ ] NOTICE records `openclaw/humanize-chinese`.
- [ ] No promotional language that promises external detection outcomes or encourages detection evasion appears.
- [ ] `SKILL.md` frontmatter is valid YAML.
- [ ] Markdown raw files keep normal line breaks.

## Output Format

- [ ] Risk heatmap table is present.
- [ ] Sentence-level localization example is present.
- [ ] Before/after score comparison example is present.
- [ ] No-edit zone table is present.
- [ ] Code blocks are closed.
- [ ] Markdown tables have normal line breaks.
