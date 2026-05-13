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

- Template opening: start from the thesis object, module, problem, or test condition.
- Mechanical transition: replace with concrete cause, condition, limitation, or implementation path.
- Generic value ending: replace with scope, test result, limitation, or next step.
- Overly balanced pattern: vary sentence length and break fixed parallel structures.
- Abstract noun: replace with modules, parameters, input/output, or test data.
- Vague attribution: use concrete evidence such as tables, test counts, vulnerability counts, environment, or method.

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
3. Delete empty value claims.
4. Replace abstract evaluation with concrete objects.
5. Replace "general-summary-general" with "object-process-result".
6. Replace "background-problem-significance" with "this task-object-limit".
7. Replace "实验结果表明" with concrete test-result wording.
8. Replace "具有重要意义" with scope or uncovered area.

## Relation To SKILL.md

Use this file in `AIGC_FOCUSED_LENGTH_CONTROLLED` and `AIGC_ONLY` when the goal is AIGC reduction with stable length.
