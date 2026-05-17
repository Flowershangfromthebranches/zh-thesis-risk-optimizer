# v0.7 AIGC-Focused Length-Controlled Engine

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Core Idea

When similarity risk is already acceptable or close to the user's target, the Skill should stop increasing similarity-rewrite intensity and enter AIGC-focused mode. This mode repairs only high-AIGC-risk paragraphs and controls the whole-thesis length budget so the draft does not become much longer only for risk reduction.

This engine learns from scan-first, sentence-level localization, length-preserving editing, rolling consistency, report feedback, and chapter-task workflow ideas, but it does not copy upstream code, configuration, templates, or long text.

## 1. Activation Conditions

Enter `AIGC_FOCUSED_LENGTH_CONTROLLED` when any condition applies:

- The user says similarity is already acceptable or similarity reduction is enough.
- The user asks to continue reducing AIGC risk.
- The new draft grew too much.
- The user requires a whole-thesis growth range such as 0-2000 Chinese characters.
- Reports show `similarity improved but AIGC still high`.
- Multi-round AIGC reports show red/high-risk text decreasing but orange/medium-risk text remaining high.
- The rewrite shows over-expansion.

## 2. Primary Objective

Primary objective:

- Reduce AIGC writing risk.

Secondary objective:

- Keep similarity risk stable and avoid rebound.

Hard constraint:

- Control total character growth.

## 3. Length Budget Rule

Default variables:

- `original_chars`: original thesis Chinese character count.
- `target_chars`: final draft Chinese character count.
- `max_added_chars = 2000`.
- `min_added_chars = 0`.

Default final-draft requirement:

```text
target_chars >= original_chars
target_chars <= original_chars + 2000
```

If the user specifies a different range, use the user's range.

## 4. Expansion Priority

Allowed growth areas:

1. High-AIGC paragraphs that lack enough information.
2. Abstract positions that need existing test results.
3. Conclusion positions that need real limitations.
4. Technology overview positions that should move from encyclopedia definitions to this-thesis usage.
5. Testing analysis positions that need to explain existing result values.

Forbidden or restricted growth areas:

1. References.
2. School statements.
3. Table of contents.
4. Figure and table numbers.
5. Code, paths, interfaces, Payload, parameters.
6. Low-risk implementation chapters.
7. Paragraphs whose similarity repair is complete and AIGC risk is not high.
8. Pure background paragraphs; do not reduce AIGC by adding more background.

## 5. Rewrite-by-Replacement Principle

v0.7 prioritizes replacement-based reconstruction, not append-based expansion.

Bad strategy:

```text
随着互联网技术的快速发展，Web 应用越来越重要。本文还结合 Crawler 和 Detector 模块进行了设计。
```

Good strategy:

```text
本文围绕一个轻量级 Web 漏洞扫描工具展开，重点处理两个环节：一是由 Crawler 收集目标站点 URL，二是由 Detector 对带参数的页面执行 SQL 注入和反射型 XSS 探测。
```

## 6. Completion Criteria

Mark the task complete only when all conditions hold:

- Heuristic AIGC risk decreases.
- No obvious formalization regression appears.
- The draft is not substantially expanded.
- The whole-thesis delta stays within the user's length budget.
- Similarity-protection items are not damaged.
- Technical facts, citations, data, and terms remain intact.

## 7. Plateau Handoff

If AIGC-focused repair improves the report only slightly across two or more rounds, do not keep running the same prompt.

Switch to `AIGC_PLATEAU_BREAKER` when:

- Red/high-risk text is already much lower.
- Orange/medium-risk text remains the main residual band.
- The same paragraphs keep appearing in reports.
- The next likely edit would repeat synonym replacement, connector changes, or append-based explanation.

In plateau mode, freeze white/low-risk text and treat orange paragraphs as the primary target.

## Relation To SKILL.md

`SKILL.md` routes AIGC-focused and length-controlled requests here through `AIGC_FOCUSED_LENGTH_CONTROLLED`.
