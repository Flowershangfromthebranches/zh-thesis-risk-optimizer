# One-Pass Cross-Discipline Strategy

## Purpose

This reference helps the Skill choose a strong first strategy for different disciplines, current AIGC/similarity rates, and color-band distributions.

It is an optimization guide, not a promise of any external detector result. It must preserve facts, citations, data, formulas, code, reference entries, school-template text, and protected discipline terms.

## Core Principle

Every report-driven pass must consider all color bands at the same time:

- red, orange, and purple are counted, routed, and audited;
- black and gray are explicitly frozen by default;
- gray means non-scored text such as too-short fragments, headings, English text, references, or template text, not a low-risk rewrite target;
- black/gray may only be touched when the user explicitly requests it, or when `GLOBAL_STYLE_VARIANCE_ENGINE` selects a very small number of connector sentences and no protected content is involved.

The default objective is not "rewrite more." The objective is to change the statistical fingerprint of high-risk text with the smallest safe intervention.

## AIGC Rate Strategy Matrix

| current AIGC rate | strategy label | primary work | forbidden default |
|---:|---|---|---|
| `>=70%` | `high_risk_first_pass_reconstruction` | Red and orange 100% planned; purple counted from the start; evidence map before rewriting; local Level 4 only when allowed. | Full-text loose rewriting; black/gray rewriting; synonym-only repair. |
| `50%-69.99%` | `orange_purple_joint_repair` | Red/orange structural repair plus purple light rebalance when volume is non-trivial or target is below 30%. | Treating purple as an afterthought; smoothing management prose. |
| `30%-49.99%` | `plateau_breaker_pass` | Persistent orange paragraphs use skeleton breaking, compression, and evidence-first reconstruction; purple becomes mandatory when target is below 25%. | Expanding for word count before risk is controlled. |
| `20%-29.99%` | `near_threshold_pushdown` | Residual orange/purple and template residue only; compress or replace high-risk paragraphs; freeze black/gray; no broad expansion. | Adding length to satisfy word-count concerns unless user accepts risk. |
| `<20%` | `maintenance_only` | Only repair factual, formatting, or user-requested local issues. | Broad de-AIGC rewriting. |

If the user target is `target_aigc_rate <= 20%` and `current_aigc_rate > target_aigc_rate`, route to `near_threshold_pushdown` or a stronger strategy even when the current rate is already close to 20%.

## Color-Band Strategy

| band | report meaning | default action | first-pass expectation |
|---|---|---|---|
| red | `>=70%`, high suspicion | Deep reconstruction. Change paragraph skeleton, evidence placement, and conclusion path. | 100% handled or validly frozen. |
| orange | `>=60%` and `<70%`, medium suspicion | Structural repair or compression. Remove generic openings, repeated connectors, empty value claims, and parallel lists. | Primary target, not secondary cleanup. |
| purple | `>=50%` and `<60%`, light suspicion | Low-intensity rebalance. Vary openings, transitions, rhythm, and repeated terms without changing facts. | Always counted; mandatory when target is below 25% and current rate remains above target. |
| black | `<50%`, scored low risk | Freeze. | Frozen with reason unless a tiny connector edit is explicitly selected. |
| gray | non-scored or excluded text | Freeze. | Do not count as a rewrite target; protect headings, English, short fragments, references, and template pages. |

## Discipline Moves

| profile | high-value evidence | preferred move | protected boundaries |
|---|---|---|---|
| management / HR / business | company process, department, post, survey, interview, indicator, review cycle | Evidence before conclusion; break "problem-cause-countermeasure-guarantee" skeleton; reduce consulting-speak. | Do not invent company facts, questionnaires, interviews, systems, or indicators. |
| computer science / software | modules, APIs, paths, fields, logs, test cases, screenshots, datasets | Rewrite narrative around actual implementation sequence and test boundary; protect technical identifiers. | Code, API paths, table/field names, parameters, commands, metrics. |
| engineering / natural science | design constraints, parameters, instruments, test conditions, result tables | Keep methods stable; revise discussion and conclusion templates with concrete result interpretation. | Formulas, units, parameters, drawings, experimental data. |
| medicine / nursing / public health | study design, sample, inclusion criteria, outcome indicators, ethics boundary | Conservative de-template in abstract/discussion; keep clinical register and evidence hierarchy. | Diagnosis terms, dosage, clinical data, ethics statements, guidelines. |
| law | statutes, cases, facts, doctrinal dispute, jurisdiction, legal consequence | Replace broad "完善制度" claims with rule-issue-application-boundary reasoning. | Legal quotations, article numbers, case facts, doctrinal terms. |
| education / psychology | classroom scene, learner group, questionnaire item, interview note, intervention step | Put teaching or survey scene before policy value claims; make countermeasures executable. | Policy quotations, scale names, statistics, participant data. |
| humanities / communication / arts | text fragment, corpus, work detail, image/design element, historical context | Use close reading and material detail; reduce empty value claims. | Direct quotations, titles, author names, historical facts, image descriptions. |

## Length Control Lesson

Do not expand high-risk paragraphs merely to restore word count. In multi-round AIGC work, added length can raise the overall rate when the new text is smooth, complete, and template-like.

When word count and AIGC reduction conflict:

1. finish risk-band repair first;
2. only add author-provided evidence in sections with low color risk;
3. prefer replacing high-risk generic claims with concrete evidence over appending new explanation;
4. if the user removes the word-count constraint, use compression freely on red/orange/purple paragraphs.

## One-Pass Output Requirements

When this reference is active, final audit must include:

- selected rate strategy;
- selected discipline profile;
- color legend used;
- red/orange/purple coverage;
- black/gray freeze summary;
- whether length expansion was avoided;
- whether any evidence request remains.

