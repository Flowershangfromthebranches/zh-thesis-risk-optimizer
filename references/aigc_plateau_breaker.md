# AIGC Plateau Breaker

## Purpose

`AIGC_PLATEAU_BREAKER` handles the common bottleneck where early rounds reduce red/high-risk AIGC text, but later rounds remain stuck in orange/medium-risk bands.

This mode is based on report feedback and local case regression analysis. It does not promise any external detection result.

For original thesis plus original AIGC report workflows, use `references/first_pass_red_orange_engine.md` first. The plateau breaker is a fallback when the first pass was not available, was incomplete, or later reports still show orange/medium-risk concentration.

## Plateau Signal

Enter this mode when one or more signals appear:

- AIGC score falls in the first round but then decreases slowly.
- Red/high-risk text is much lower, but orange/medium-risk text remains high.
- Repeated rounds keep rewriting the same paragraphs without a clear report trend.
- The remaining risky text is mostly enumerated, smooth, generic, or discipline-template prose.
- The current method only demotes red to orange instead of reducing orange to low risk.

## Case-Derived Observation

In the A-commerce recruitment-management thesis sample, local report-color analysis showed:

| round | red text | orange text | purple text | observed bottleneck |
|---|---:|---:|---:|---|
| original | about 39.4% | about 24.4% | about 3.2% | many high-risk template paragraphs |
| first pass | about 7.1% | about 36.3% | about 8.1% | red was demoted to orange |
| second pass | about 5.8% | about 40.7% | about 1.6% | orange plateau formed |
| third pass | about 1.9% | about 37.6% | about 6.1% | remaining risk concentrated in orange paragraphs |

The failure was not lack of rewriting. The failure was that the strategy kept treating medium-risk orange paragraphs as if they only needed light wording changes.

## Why Plateau Happens

1. Red-to-orange demotion is mistaken for success.
2. Medium-risk orange paragraphs keep the same paragraph skeleton.
3. Enumerated structures such as "第一、第二、第三" remain intact.
4. Generic discipline terms remain dense.
5. Protected facts and numerical survey data make the model too conservative.
6. The rewrite changes words but not paragraph rhythm, evidence placement, or local perspective.
7. Low-risk/white paragraphs are not frozen consistently, causing wasted edits.

## Required State Labels

- `RED_HIGH_RISK_PASS`: first remove high-risk formulaic expression.
- `ORANGE_PLATEAU_PASS`: specifically break persistent medium-risk paragraphs.
- `PURPLE_CLEANUP_PASS`: local cleanup only.
- `WHITE_FREEZE`: do not rewrite.
- `NO_PROGRESS_REWRITE_LOOP`: stop repeating the same strategy.

## No-Progress Rule

If a round produces less than a small visible report improvement, or if orange text remains the main risk band, do not run another normal rewrite. Switch to `ORANGE_PLATEAU_PASS`.

## Completion Rule

Do not mark completed when only red risk decreases. Completion requires the residual orange plateau to be addressed or explicitly marked as protected, evidence-limited, or low return.

## Relation To SKILL.md

Use this file when new reports show decreasing but plateauing AIGC scores, especially after two or more rounds.
