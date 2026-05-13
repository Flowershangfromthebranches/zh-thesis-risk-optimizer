# Post-Rewrite AIGC Self-Audit

## Purpose

Every substantial rewrite should be checked for remaining AIGC-style risk.

## Audit Questions

1. Is there still a universal opening?
2. Is there still a mechanical three-part structure?
3. Is every sentence still overly complete and balanced?
4. Does the paragraph still lack the thesis object?
5. Is there still a generalized ending?
6. Does it still follow "background -> action -> significance"?
7. Is it only synonym replacement?
8. Does it include real process, boundary, or limitation from the source?
9. Does the rewritten version sound more AI-like than the original?
10. Did it damage citations, terms, data, or conclusions?

## Second-Pass Trigger

If 3 or more questions are answered "yes", run `SECOND_PASS_REWRITE_REQUIREMENT`.

## Output

```markdown
## AIGC Self-Audit
| Item | Result | Evidence |
|---|---|---|

## Decision
- Pass / Second pass required:
```

## Relation To SKILL.md

Used after AIGC, dual, report-driven, and no-report fallback rewrites.
