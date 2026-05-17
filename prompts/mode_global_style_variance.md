# Prompt: GLOBAL_STYLE_VARIANCE_ENGINE

Use after red/orange/purple routing to detect full-thesis style uniformity.

## Inputs

- color-band plan;
- section profiles;
- discipline profile;
- repeated term list;
- protected elements.

## Output

| field | value |
|---|---|
| style_uniformity_score |  |
| repeated_transition_terms |  |
| uniform_section_openings |  |
| sentence_length_distribution_issue | yes/no |
| paragraph_length_distribution_issue | yes/no |
| global_variance_plan |  |
| sections_needing_variance |  |

Do not rewrite the full thesis directly. Route local actions to `PURPLE_BAND_REBALANCER`, `COLOR_BAND_ROUTER`, and section profiles.
