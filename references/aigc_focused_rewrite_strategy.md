# AIGC-Focused Rewrite Strategy

## Purpose

This file strengthens AIGC-risk reduction when similarity reduction is no longer the main objective.

## 1. AI Pattern Library

Identify and repair these common AIGC patterns:

### 1. Template Opening

- 随着...发展
- 在...背景下
- 近年来
- 当前...日益突出

### 2. Mechanical Transition

- 然而
- 与此同时
- 因此
- 此外
- 综上所述
- 实验结果表明

### 3. Generic Value Ending

- 具有重要意义
- 提供了便捷的解决方案
- 具有良好的应用前景
- 为...提供参考
- 提升了系统整体能力

### 4. Overly Balanced Sentence Pattern

- 一是...二是...三是...
- 首先...其次...最后...
- 从理论层面...从实践层面...
- 不仅...而且...

### 5. Abstract Noun Stacking

- 体系
- 机制
- 路径
- 维度
- 能力
- 价值
- 支撑
- 保障
- 赋能
- 边界
- 场景
- 生态

### 6. Vague Attribution

- 相关研究表明
- 实践证明
- 这说明
- 可以看出
- 具有一定优势

## 2. Repair Actions

Priority order — report targeting and regression control first:

- **Report color targeting**: if a color-marked DOCX report is provided, extract color metadata first with `references/docx_color_report_extraction.md`.
- **Rhythm gate**: apply `references/burstiness_injection_rules.md` when the paragraph is too uniform. If rhythm is already varied, do not add more short sentences.
- **Connector deletion**: remove all "首先、其次、此外、因此、综上所述、与此同时". Target < 3 per paragraph.
- Template opening: start from the thesis object, module, problem, or test condition. Do not use "随着...发展" or "在...背景下".
- Mechanical transition: delete or replace with concrete cause, condition, limitation, or implementation path.
- Generic value ending: delete entirely. Do not replace with another value claim. End with a concrete detail or boundary.
- Overly balanced pattern: break parallel structures. Convert "一是...二是...三是" to flowing prose.
- Abstract noun: replace with modules, parameters, input/output, or test data. Delete if no concrete replacement exists.
- Vague attribution: use concrete evidence such as tables, test counts, environment, or method. If no evidence exists, delete the attribution.
- **Anti-formalization**: if the rewrite sounds more polished or "academic" than the original, diagnose the failure cause and rewrite with less polish, stronger evidence placement, or template repair.
- **Social-science template repair**: for HR, management, education, public administration, and similar theses, break repeated "现状 -> 问题 -> 原因 -> 对策 -> 保障" skeletons and move source evidence before evaluation.

## 3. High-Impact AIGC Zones

Highest priority:

- Abstract.
- Introduction opening.
- Research background.
- Research significance.
- Generic definitions in technology overview.
- Feasibility analysis.
- Testing-result analysis.
- Conclusion.

Lower priority:

- Code explanation.
- Parameter explanation.
- Figure and table titles.
- References.
- Already concrete implementation process.

## 4. AIGC Repair Without Expansion

Prefer these actions instead of expansion:

1. Change the opening angle.
2. Change information order.
3. Delete empty value claims — do not replace with other value claims.
4. Replace abstract evaluation with concrete objects.
5. Replace "general-summary-general" with "object-process-result".
6. Replace "background-problem-significance" with "this task-object-limit".
7. Replace "实验结果表明" with concrete test-result wording.
8. Replace "具有重要意义" with scope or uncovered area — or just delete.
9. Use rhythm repair only when the paragraph is too uniform; otherwise prioritize evidence-first reconstruction.
10. Break enumeration: convert numbered lists to flowing prose or process-stage grouping.

## 5. Anti-Formalization Guard

AIGC-focused rewriting must NOT increase formality. Check after each rewrite:

| Check | Pass/Fail |
|---|---|
| Text does not sound more polished than original? | |
| No new abstract nouns added (机制, 体系, 能力, 保障, 路径, 价值)? | |
| Sentence rhythm was audited, and rhythm repair was applied only if needed? | |
| Connectors reduced, not increased? | |
| No "首先...其次...最后" structure remains? | |
| Short sentences are formal and not slogan-like or conversational? | |

If 2+ checks fail, the rewrite has increased AIGC risk. Do not automatically add more short sentences; first diagnose whether the failure is rhythm uniformity, formalization, missing evidence, or retained social-science template skeleton.

## Relation To SKILL.md

Use this file in `AIGC_FOCUSED_LENGTH_CONTROLLED` and `AIGC_ONLY` when the goal is AIGC reduction with stable length.
