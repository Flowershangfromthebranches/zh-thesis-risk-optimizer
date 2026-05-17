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

## 6. Management Thesis Regression

For human resource management, business administration, marketing, education management, public administration, and similar social-science theses, run these extra checks:

- Did the rewrite turn ordinary expressions into more abstract management words such as 机制, 体系, 路径, 赋能, 支撑, 协同?
- Did it add empty value claims such as "提升效率", "优化流程", "强化能力", "提供参考", or "具有重要意义"?
- Did it replace concrete posts, recruitment steps, questionnaire items, interview feedback, forms, review cycles, or responsible roles with broad summary language?
- Did it lower similarity risk by sacrificing evidence density?
- Did it keep the "现状 -> 问题 -> 原因 -> 对策" or "定义 -> 意义 -> 对策" skeleton while only polishing words?

If any management red/orange paragraph fails these checks, do not continue with generic polishing. Route back to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`. If the needed company, questionnaire, interview, process, post, indicator, form, or cycle evidence is missing, request `workflow/author_evidence_pack_template.md`.

## 7. Over-Humanization Regression

The opposite of formalization regression: the rewrite makes text too colloquial, too diary-like, too casual, or too social-media-like in order to reduce AIGC score.

Signals:

- Text reads like a student diary or chat log rather than a thesis.
- Prohibited colloquial expressions appear (see `ACADEMIC_TONE_GUARD`).
- Sentence fragmentation is extreme (all sentences under 10 chars).
- Author judgment is not anchored to evidence.
- Casual connectors replace analytical transitions ("说白了", "其实吧", "我觉得吧").
- Emotional or exaggerated language appears ("一塌糊涂", "彻底失败", "惨不忍睹").
- Social-media style enters the text ("家人们", "格局打开", "干货").

If any over-humanization signal is found:

1. Mark `OVER_HUMANIZATION_FAIL`.
2. Route to `THESIS_REGISTER_GUARD` and `ACADEMIC_TONE_GUARD` for correction.
3. Preserve the sentence-length variation and evidence anchoring from the humanization.
4. Remove only the diary-feel, chat-feel, or social-media-feel words.
5. Restore to undergraduate-thesis acceptable formality.

## 8. Dual Regression Model

`AIGC_REGRESSION_GUARD` now checks for both directions:

| regression type | direction | detection | correction |
|---|---|---|---|
| `FORMAL_AI_REGRESSION` | Too formal, too abstract, too AI-like | Abstract noun inflation, smoothness, template retention | Route to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` or evidence injection |
| `OVER_HUMANIZATION_REGRESSION` | Too colloquial, too casual, too diary-like | Prohibited expressions, extreme fragmentation, emotional language | Route to `THESIS_REGISTER_GUARD` and `ACADEMIC_TONE_GUARD` for correction |

Both regressions must be absent for the text to pass this guard.

## Mandatory Rules

- If a paragraph has three or more regression categories, mark `AIGC_REGRESSION_FAIL`.
- `AIGC_REGRESSION_FAIL` must not be accepted as final text.
- The paragraph must return to the appropriate reconstruction path in the slim router. For management/social-science papers, return to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` or request the author evidence pack.
- If `LOCAL_ESCALATED_HUMANIZATION` caused the regression, lower the local level or rerun `THESIS_REGISTER_GUARD`; do not continue Level 4 in strict sections.
- Do not repair regression by adding more formal words.
- Prefer concrete objects already present in the source.
- If there is not enough concrete information, output `建议作者补充：...`.

## Relation To SKILL.md

Use this guard after `TEMPLATE_RESIDUE_DETECTOR` and `THESIS_REGISTER_GUARD`, especially when `LOCAL_ESCALATED_HUMANIZATION` was used or the text becomes more formalized.
