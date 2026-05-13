# Effectiveness Evaluation

## Purpose

This file helps evaluate whether revisions are likely to be more effective than shallow polishing.

## Known Weaknesses Fixed In v0.5

Current dual-optimization weakness can come from:

1. Shallow polishing without paragraph-logic rebuilding.
2. Label-heavy diagnosis without forced rewrite actions.
3. Similarity and AIGC goals constraining each other.
4. No-report mode lacking concrete targets.
5. Report mode reducing similarity but skipping AIGC reshaping.
6. Missing second self-audit and rewrite pass.
7. Strong protection rules without editable-zone identification.

## Evaluation Signals

An effective rewrite should show:

- Changed paragraph structure.
- More concrete thesis objects.
- Fewer universal significance sentences.
- Clearer sentence relationships.
- Preserved citations and data.
- No fabricated facts.
- AIGC self-audit below second-pass threshold.
- No formalization regression after similarity reduction.
- Evidence density increased when source evidence exists.

## v0.6 Regression Lesson

The Web vulnerability scanner regression case shows that similarity improvement alone is not enough. A draft can reduce repeated expressions while increasing AIGC risk if it replaces concrete thesis content with smoother and more abstract wording.

Treat v0.4 historical improvement as a partial reference only, not a success standard. Treat v0.5-style formalization as a failure signal when AIGC rises.

Use `references/report_feedback_loop.md` and `references/aigc_regression_guard.md` before accepting another rewrite round.

## Boundary

This evaluation is heuristic. It does not predict or promise external detection results.
