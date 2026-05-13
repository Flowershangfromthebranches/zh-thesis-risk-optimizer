# Sentence-Level AIGC Localizer

## Purpose

This file localizes AIGC risk at sentence level so the Skill revises only the sentences that matter.

## Output Table

| sentence_id | sentence | aigc_pattern | severity | repair_action | length_action | protected_items |
|---|---|---|---|---|---|---|

## Severity

- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

## Repair Action

- `REORDER`
- `REPLACE_OPENING`
- `SPECIFY_OBJECT`
- `ADD_BOUNDARY`
- `USE_EXISTING_EVIDENCE`
- `COMPRESS_GENERIC_CLAIM`
- `REMOVE_EMPTY_VALUE_CLAIM`
- `KEEP_PROTECTED`

## Length Action

- `KEEP_LENGTH`
- `SLIGHT_EXPAND`
- `COMPRESS`
- `REPLACE_WITH_SAME_LENGTH`
- `DO_NOT_TOUCH`

## Mandatory Rules

- Process `HIGH` and `CRITICAL` sentences first.
- Do not force-rewrite `LOW` sentences just because the full-text mode is active.
- If a sentence contains code, parameters, paths, data, or citations, protect it first.
- Process at most 1-3 key sentences per paragraph.
- Prefer replacement, not appending.

## Relation To SKILL.md

Use this file before AIGC-focused paragraph revision and before any L4/L5 rewrite under a length budget.
