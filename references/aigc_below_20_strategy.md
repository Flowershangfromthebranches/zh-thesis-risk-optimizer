# AIGC Below 20 Strategy

## Purpose

This strategy supports user goals such as AIGC below 20%. It is an optimization target, not a promised result.

AIGC below 20 usually cannot be approached through synonym replacement. It requires structure rebuilding and evidence-based writing.

## 1. Template Removal

Delete or rebuild patterns such as:

- 随着...发展
- 然而...
- 本文设计并实现...
- 实验结果表明...
- 具有重要意义
- 提供便捷解决方案

## 2. Local Specificity

Each high-risk paragraph should try to include one paper-specific object, such as:

- 本系统
- Crawler
- Detector
- Reporter
- Helpers
- URL 队列
- GET 参数
- Payload
- HTML 报告
- 本地测试环境

## 3. Uneven but Formal Rhythm

- Avoid identical three-part, parallel, or summary-heavy structures.
- Keep the style formal but not mechanical.
- Do not turn the thesis into conversational prose.

## 4. Boundary and Limitation

Use real boundaries when supported:

- The current tool only checks SQL injection and reflected XSS.
- Detection mainly uses GET parameters.
- XSS detection depends on whether Payload is reflected unchanged.
- SQL injection detection depends on error keyword matching.
- Local target testing cannot fully represent complex production environments.

## 5. Evidence Density

High-risk paragraphs must improve evidence density: the number of concrete objects, parameters, results, modules, and test conditions per 100 Chinese characters.

If evidence density cannot be improved from available sources, output `建议作者补充：...`.

## Relation To SKILL.md

Use this file when the user target includes AIGC below 20% or when a new draft shows AIGC regression.
