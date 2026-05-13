# Prompt: EFFECTIVENESS_AUDIT

## Purpose

Use this mode to decide whether a rewrite is likely to be more effective than shallow polishing.

## Input

- Original paragraph.
- Rewritten paragraph.
- Protected items.

## Checks

- Did information order change?
- Did concrete thesis objects increase?
- Were empty significance sentences removed?
- Did sentence relationships change?
- Were supported boundaries or limitations added?
- Were citations, terms, data, and conclusions preserved?
- Did the rewrite avoid unsupported facts?

## Output

```markdown
## Effectiveness Audit
| Check | Result | Evidence |
|---|---|---|

## Decision
- Accept / second pass required:
```

This is heuristic and not a detection-result prediction.
