# Repeated Expression Compressor

## Purpose

Reduce repeated AI-like expressions across the thesis without diluting risk by expansion.

## Expressions To Scan

- 本文设计并实现
- 具有重要意义
- 提供便捷解决方案
- 提高系统效率
- 增强系统安全性
- 模块化设计思想
- 自动化检测
- 格式化报告
- 方便用户使用
- 具有良好的扩展性
- 能够有效发现
- 为...提供参考

## Handling Rules

1. The first occurrence may be kept or rewritten.
2. The second occurrence must become a more concrete object-based expression.
3. The third and later occurrences should be deleted, merged, or compressed first.
4. Do not solve repetition by adding more explanation.
5. Compression of repeated expressions should create negative delta for the length budget, leaving room for necessary evidence.

## Output Table

| expression | count | locations | action |
|---|---:|---|---|

## Relation To SKILL.md

Use this file in `REPEATED_EXPRESSION_COMPRESSOR` and any full-thesis AIGC-focused pass.
