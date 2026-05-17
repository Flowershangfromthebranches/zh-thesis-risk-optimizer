# Prompt: PURPLE_BAND_REBALANCER

Use when `COLOR_BAND_ROUTER` sets `purple_action = light_rebalance` or `mandatory_rebalance`. Purple-band text is considered from the first color report, not only after red/orange is cleared.

## Inputs

- purple target list from `COLOR_BAND_ROUTER`;
- `purple_action`;
- discipline profile;
- section profile;
- protected elements;
- global variance findings.

## Rules

- Use low-intensity edits only.
- Do not use Level 4.
- Do not make text conversational.
- Do not modify data, citations, terms, code, formulas, or identifiers.
- Do not rewrite black or protected content.

## Output

| field | value |
|---|---|
| purple_targets_count |  |
| purple_rebalanced_count |  |
| purple_rewrite_intensity | low |
| purple_action | skip / observe / light_rebalance / mandatory_rebalance |
| purple_deferred_reason |  |
| next_purple_action_trigger |  |
| global_distribution_effect |  |
| protected_items_preserved | yes/no |
| thesis_register_guard_result |  |
