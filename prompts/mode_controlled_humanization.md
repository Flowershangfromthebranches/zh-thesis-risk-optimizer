# Prompt: CONTROLLED_HUMANIZATION_ENGINE

Use this prompt when social-science or management thesis text needs controlled de-AIGC humanization after template-bottleneck repair.

This is an internal engine, not a user-facing entry mode. Route through `SKILL.md` Mandatory Chain.

## Inputs

- Red/orange paragraph list after `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` processing.
- Discipline type (must be social-science or management).
- Current AIGC risk level.
- `RISK_INTAKE_GATE` output, including `selected_strategy`, `max_humanization_level`, and `level_4_allowed`.
- Author evidence availability.
- Protected items list.

## 1. Intensity Level Selection

```yaml
controlled_humanization:
  discipline: HR_management / business_admin / marketing / education_admin / public_admin
  current_aigc_level: <percentage>
  selected_intensity: 1 / 2 / 3 / 3.5
  level_4_allowed: false / local_only
  reason: <why this level>
```

Selection rules:
- AIGC < 30% → max level 2, conservative repair.
- AIGC 30%-50% → max level 3, controlled humanization.
- AIGC 50%-70% → max level 3.5; local Level 4 may only be handed to `LOCAL_ESCALATED_HUMANIZATION`.
- AIGC >= 70% → max level 4 only through `LOCAL_ESCALATED_HUMANIZATION`; this prompt still uses max 3.5 in strict sections.
- AIGC >= 75% and `stage = second_pass` or `first_pass_failure` → output style risk warning and hand eligible Chapter 4/5 residuals to `LOCAL_ESCALATED_HUMANIZATION`.

This prompt must not self-select Level 4. It can only output `level_4_candidate: yes` and route the paragraph to `LOCAL_ESCALATED_HUMANIZATION`.

## 2. Per-Paragraph Processing

For each red/orange paragraph:

```yaml
paragraph_id:
  original_template_type: four_problem_four_solution / definition_significance_countermeasure / enumeration_chain / policy_style / encyclopedia_theory / other
  humanization_strategy: A / B / C / D / E / F
  intensity_level: 1 / 2 / 3 / 3.5
  level_4_candidate: yes / no
  evidence_anchor: <what evidence supports the rewrite>
  academic_tone_guard_pre_check: pass / fail
  academic_tone_guard_post_check: pass / fail
  thesis_register_guard_required: yes
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
- Also run `THESIS_REGISTER_GUARD` when section is 摘要, 英文摘要, 理论基础, 结论, 第四章, or 第五章.

## 5. Output

```markdown
## Controlled Humanization Report

| paragraph_id | section | original_template_type | strategy | intensity | tone_guard_pre | tone_guard_post | passed |
|---|---|---|---|---|---|---|---|

### Intensity Summary
- level_used: <1/2/3/3.5>
- level_3_warning: yes/no
- level_4_allowed: false/local_only
- level_4_candidates: <paragraph list or none>
- next_route_for_level_4_candidates: LOCAL_ESCALATED_HUMANIZATION / none

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
- Never use Level 4 directly in this prompt.
- Never use chat-like expression in 摘要, 英文摘要, 理论基础, or 结论.
