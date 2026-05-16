# Post-Rewrite AIGC Self-Audit

## Purpose

Every substantial rewrite should be checked for remaining AIGC-style risk.

## Audit Questions

### Burstiness and Rhythm (highest priority)

1. Does the paragraph have at least one sentence shorter than 15 characters?
2. Are there 3+ consecutive sentences in the 25-35 character range? (FAIL if yes)
3. Is the sentence-length standard deviation below 10? (FAIL if yes)
4. Are there more than 3 mechanical connectors (首先/其次/此外/因此/综上所述) in the paragraph? (FAIL if yes)
5. If sentence rhythm is already varied, did the rewrite avoid adding unnecessary short, slogan-like, or conversational sentences?

### Structure and Pattern

6. Is there still a universal opening ("随着...发展", "在...背景下")?
7. Is there still a mechanical three-part structure ("首先...其次...最后" or "一是...二是...三是")?
8. Is every sentence still overly complete and balanced?
9. Does it still follow "background -> action -> significance"?
10. For HR, management, education, or similar theses, does it still follow "现状 -> 问题 -> 原因 -> 对策 -> 保障"?

### Specificity and Evidence

11. Does the paragraph still lack the thesis object?
12. Is there still a generalized ending ("具有重要意义", "提供了参考")?
13. Is it only synonym replacement without structural change?
14. Does it include real process, boundary, or limitation from the source?
15. Did the rewrite use report color metadata when the report was a color-marked DOCX?

### Anti-Regression

16. Does the rewritten version sound more AI-like than the original?
17. Did it damage citations, terms, data, or conclusions?
18. Did it replace concrete objects with abstract nouns?
19. Did it create formalization regression after similarity repair?
20. Did it add more abstract nouns (机制, 体系, 能力, 保障, 路径, 价值) than the original?

## Second-Pass Trigger

If 3 or more questions are answered "yes", run `SECOND_PASS_REWRITE_REQUIREMENT`.

Burstiness-specific triggers (questions 1-5): if uniformity checks fail, apply `references/burstiness_injection_rules.md`. If the paragraph already has varied rhythm but still looks red/orange, switch to template-skeleton repair or evidence-first reconstruction instead of adding more rhythm variation.

Anti-regression triggers (questions 16-20): if 2 or more of these are "yes", mark `AIGC_REGRESSION_FAIL` and rewrite with less polish, stronger evidence placement, and less abstract management language.

If the paragraph also matches three or more categories in `references/aigc_regression_guard.md`, mark `AIGC_REGRESSION_FAIL` and do not accept it as final text.

## Priority Order for Second Pass

1. Fix burstiness failures first (questions 1-4) — highest impact
2. Fix structure/pattern issues (questions 5-8)
3. Fix specificity/evidence issues (questions 9-12)
4. Fix anti-regression issues (questions 13-17)

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
