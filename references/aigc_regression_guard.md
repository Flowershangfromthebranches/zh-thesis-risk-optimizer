# AIGC Regression Guard

## Purpose

`AIGC_REGRESSION_GUARD` detects cases where a rewrite lowers similarity risk but makes the text more AI-like.

## 1. Formalization Regression

Ordinary expression is rewritten into overly formal, abstract, and balanced prose.

High-risk phrases include:

- 持续演进
- 深度嵌入
- 不断升级
- 构成
- 实施
- 呈现
- 赋能
- 支撑
- 体系
- 机制
- 路径
- 维度
- 边界
- 价值
- 能力
- 保障
- 显著提升
- 具有重要意义
- 提供便捷解决方案

## 2. Smoothness Regression

All sentences become too complete, smooth, symmetric, and standard-answer-like.

## 3. Abstract Noun Inflation

Abstract nouns increase without adding modules, parameters, test results, or implementation objects.

## 4. Similarity-First Damage

Common wording is replaced with rarer but more AI-like formal phrases only to avoid source similarity.

## 5. Evidence Dilution

Concrete class names, function names, parameters, test data, or running results are diluted into broad words such as "system capability", "detection mechanism", or "practical value".

## Mandatory Rules

- If a paragraph has three or more regression categories, mark `AIGC_REGRESSION_FAIL`.
- `AIGC_REGRESSION_FAIL` must not be accepted as final text.
- The paragraph must enter Evidence-Based Reconstruction.
- Do not repair regression by adding more formal words.
- Prefer concrete objects already present in the source.
- If there is not enough concrete information, output `建议作者补充：...`.

## Relation To SKILL.md

Use this guard after any dual optimization, report-driven rewrite, or target-driven rewrite when AIGC risk rises or the text becomes more formalized.
