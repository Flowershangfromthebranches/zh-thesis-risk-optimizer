# First-Pass Red-Orange Engine

## Purpose

`FIRST_PASS_RED_ORANGE_ENGINE` is used when the user provides the original thesis and the original AIGC report. It prevents the common failure mode where the first pass only reduces red/high-risk text and leaves orange/medium-risk text as the next bottleneck.

This engine treats red and orange report bands as the first-pass main work area. It does not promise that any external system will mark the result as purple, black, or low risk.

## Activation Conditions

Enter this mode when:

- The user provides the original thesis plus the original AIGC report.
- The report has color bands or risk bands such as red, orange, purple, and black/white.
- The user wants AIGC reduction in the first pass.
- The user asks to avoid repeated second/third rounds caused by orange plateau.

Do not use this mode when the user provides a revised/current draft and the current report after a prior rewrite. Use `references/current_report_red_orange_engine.md` instead.

## Band Policy

| report_band | role in first pass | action |
|---|---|---|
| red/high | primary target | strong reconstruction with protection checks |
| orange/medium | primary target | structural repair, rhythm repair, evidence placement |
| purple/light | secondary target | local cleanup only when safe |
| black/white/low | frozen | do not rewrite unless user explicitly asks |
| protected | no-edit or surrounding-edit only | preserve exact data, code, citations, terms, formulas, paths, parameters |

Red and orange paragraphs must both enter the first-pass task table. Orange is not deferred to a later plateau stage.

## First-Pass Workflow

1. Parse the user-provided report and record the meaning of each color/risk band.
2. Map red and orange fragments back to the thesis source.
3. Build a protected list before any rewrite.
4. Create a red-orange task table.
5. Run sentence-level localization inside each red/orange paragraph.
6. Select only the 1-3 highest-impact sentences per paragraph unless the whole paragraph skeleton is the risk.
7. Apply replacement-based reconstruction, not append-based expansion.
8. Run band-target self-audit.
9. If red/orange risk remains in the heuristic self-audit, run one limited internal retry with a different repair move.
10. Stop when the paragraph is heuristically reduced to purple/black, protected, evidence-limited, or no-progress.

## Internal Recursive Loop

The loop is finite and must not become uncontrolled rewriting.

```text
for each red/orange task:
  diagnose sentence risks
  revise using at least two valid repair moves
  run self-audit
  if target_band is purple_or_black_like:
    mark PASS
  else if protected_or_evidence_limited:
    mark STOP_WITH_REASON
  else if retry_count < max_internal_passes:
    retry with a different repair move
  else:
    mark NEEDS_REPORT_RECHECK_OR_HUMAN_EVIDENCE
```

Default:

- `max_internal_passes = 2`.
- Do not run a third internal rewrite unless the user explicitly asks and the paragraph has enough evidence.
- Do not use the same repair move twice.

## Allowed Repair Moves

Use moves from:

- `references/aigc_focused_rewrite_strategy.md`.
- `references/orange_zone_rewrite_strategy.md`.
- `references/burstiness_rhythm_control.md`.
- `references/content_substance_injection.md`.

At least two of the following must change:

- paragraph opening angle,
- information order,
- sentence relationship,
- local evidence placement,
- repeated expression,
- paragraph rhythm,
- generic conclusion,
- discipline-template skeleton.

## Character Change Control

First-pass red-orange work must obey `references/character_delta_guard.md`.

Default whole-thesis range:

- `allowed_total_delta_ratio = ±10%`.

If red/orange repair would exceed this range:

- compress generic transitions first,
- delete repeated value claims,
- preserve technical facts and citations,
- stop expansion and ask for author evidence if needed.

## Exit States

- `RED_ORANGE_FIRST_PASS_COMPLETED`: red/orange tasks were safely handled and self-audit passed.
- `PURPLE_BLACK_HEURISTIC_TARGET_REACHED`: the paragraph is heuristically reduced to light/low risk.
- `PROTECTED_STOP`: risk remains but protected content prevents deeper rewriting.
- `EVIDENCE_LIMITED_STOP`: risk remains because the paragraph lacks author-provided evidence.
- `CHARACTER_DELTA_FAIL`: revision exceeds the allowed whole-thesis character-change range.
- `NO_PROGRESS_INTERNAL_LOOP`: internal retries did not materially change the risk pattern.

## Safety

Do not fabricate data, experiments, citations, interviews, code, APIs, logs, screenshots, report percentages, or external detection outcomes. The color-band target is a heuristic writing goal only.

## Relation To SKILL.md

Use this file before `AIGC_PLATEAU_BREAKER` when the user provides the original AIGC report at the start of the task.
