# Prompt: DISCIPLINE_STRATEGY_ROUTER

Use after `RISK_INTAKE_GATE` and before report/color processing.

## Inputs

- discipline from intake;
- thesis title;
- abstract or table of contents if available;
- protected items;
- risk intake metrics.

## Steps

1. Detect discipline and confidence.
2. Select exactly one discipline profile.
3. Load the matching file in `discipline_profiles/`.
4. Output protected elements and forbidden rewrite actions.
5. Set section-aware humanization ceiling.
6. If confidence is low, ask for confirmation before strong rewrite.

## Output

| field | value |
|---|---|
| detected_discipline |  |
| discipline_confidence | high / medium / low |
| selected_profile |  |
| protected_elements |  |
| allowed_humanization_level |  |
| forbidden_rewrite_actions |  |
| preferred_rewrite_moves |  |
| profile_file |  |

Do not rewrite text in this mode.
