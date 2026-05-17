# Prompt: CONTROLLED_HUMANIZATION_ENGINE

Use this prompt when social-science or management thesis text needs controlled de-AIGC humanization after template-bottleneck repair.

This is an internal engine, not a user-facing entry mode. Route through `SKILL.md` Mandatory Chain.

## Inputs

- Red/orange paragraph list after `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` processing.
- Discipline type (must be social-science or management).
- Current AIGC risk level.
- Author evidence availability.
- Protected items list.

## 1. Intensity Level Selection

```yaml
controlled_humanization:
  discipline: HR_management / business_admin / marketing / education_admin / public_admin
  current_aigc_level: <percentage>
  selected_intensity: 1 / 2 / 3
  reason: <why this level>
```

Selection rules:
- AIGC < 50% → level 1
- AIGC 50%-75% → level 2 (default)
- AIGC > 75% → level 3 (with warning)

## 2. Per-Paragraph Processing

For each red/orange paragraph:

```yaml
paragraph_id:
  original_template_type: four_problem_four_solution / definition_significance_countermeasure / enumeration_chain / policy_style / encyclopedia_theory / other
  humanization_strategy: A / B / C / D / E / F
  intensity_level: 1 / 2 / 3
  evidence_anchor: <what evidence supports the rewrite>
  academic_tone_guard_pre_check: pass / fail
  academic_tone_guard_post_check: pass / fail
```

## 3. Strategy Application

Apply one or more strategies from `references/controlled_humanization_engine.md`:

- A: Template skeleton dispersal
- B: Non-uniform sentence length
- C: Author judgment insertion
- D: Anti-consulting-speak
- E: Theory de-encyclopedia
- F: Abstract/conclusion de-template

Each paragraph must use at least one strategy. Strategy D is mandatory when 2+ consulting-speak terms appear.

## 4. Academic Tone Guard Check

After each paragraph revision, run `ACADEMIC_TONE_GUARD`:

- Check for prohibited colloquial expressions.
- Check for diary-like tone.
- Check for social-media style.
- If violation found → correct before proceeding.
- If correction would undo the humanization → try a different strategy.

## 5. Output

```markdown
## Controlled Humanization Report

| paragraph_id | section | original_template_type | strategy | intensity | tone_guard_pre | tone_guard_post | passed |
|---|---|---|---|---|---|---|---|

### Intensity Summary
- level_used: <1/2/3>
- level_3_warning: yes/no

### Tone Guard Summary
- checked: <count>
- violations: <count>
- corrected: <count>

### Paragraphs Needing Manual Review
| paragraph_id | reason |
|---|---|
```

## Safety

- Never promise external detection outcomes.
- Never sacrifice thesis formality for score reduction.
- Never produce diary-like, chat-like, or social-media-like text.
- If evidence is missing, request `workflow/author_evidence_pack_template.md`.
- Level 3 output must include the academic-formality warning.
