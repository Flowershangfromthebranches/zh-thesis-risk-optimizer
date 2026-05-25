---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC risk reduction and quality reconstruction tool. Reduces AIGC suspicion rates by improving authentic writing quality — not by synonym replacement or academic-polish templating.
license: MIT
---

# zh-thesis-risk-optimizer v2.0

## 1. When to use this skill

Use this skill when:
- The user has a Chinese graduation thesis with high AIGC suspicion rate
- The user wants to reduce AI-like writing patterns while improving academic quality
- The input is a `.docx` thesis file (optionally with an AIGC color-marked report)
- The user needs discipline-specific rewriting (not one-size-fits-all polishing)
- The task needs general low-AIGC humanization across multiple majors without forcing a computer-engineering style
- The user needs low-template, anchor-first revision that stays in thesis register instead of becoming colloquial writing

Do NOT use this skill for:
- Simple synonym replacement or "lowering similarity rate"
- Making text more formal/academic/模板化
- Making text more colloquial/chatty as the main risk-reduction method
- Tasks that require fabricating data, citations, or experimental results
- Turning all majors into software/system-design writing
- Turning theses into chat records, oral reports, essays, or public-account style articles

## 2. Inputs

**Required (IntakeGate enforced):**
- Thesis major/discipline (user-declared, highest priority)
- Thesis title
- Current AIGC suspicion rate (%)
- Target AIGC suspicion rate (%)
- Whether AIGC color report is available
- Whether rewriting is allowed
- Whether content supplementation is allowed
- Whether thesis-writing materials are available

**Optional:**
- `.docx` AIGC color-marked report (`--aigc-report`)
- User-provided reference materials

**If any required field is missing, return the missing list. Do NOT proceed.**

## 3. Core workflow (7 steps)

```
1. IntakeGate       → Validate all required fields. Missing → return prompt, stop.
2. MajorRoute       → User-declared major → route to strategy (8 routes).
3. DomainProfile    → choose `low_aigc_humanized` profile (`--domain auto` or explicit domain).
4. RiskPlan         → current_rate + target_rate → modify/rewrite/rebuild ratios.
5. PermissionGate   → Show plan, get user confirmation. No confirmation → stop.
6. EvidencePlan     → Set material priority order + fabrication prohibitions.
7. ExecuteOptimize  → RewriteEngine + strategy + guards → output .docx copy.
8. OutcomeReport    → Honest evaluation: success / failed / partial / unverifiable.
```

## 4. Major routing (8 routes)

| Route | Strategy | Aliases |
|-------|----------|---------|
| computer_engineering | computer | CS, SE, AI, Web, Python, Java, Django... |
| human_resource | human_resource | HR, 招聘, 绩效, 薪酬, 培训... |
| business_management | management | 工商管理, 财务, 市场, 物流, 会计... |
| education | education | 教育学, 学前, 教学设计, 课程... |
| literature_language | literature | 文学, 语言, 新闻传播, 翻译... |
| law_governance | law | 法学, 法律事务, 社会治理... |
| medical_nursing | medicine | 护理, 临床, 药学, 公卫... |
| universal_light | universal | 其他 (NOT for high-AIGC bulk rewrite) |

**Rule: User declaration has highest priority. System MUST NOT auto-classify and override.**

## 4.1 Domain profiles for low_aigc_humanized

`--style low_aigc_humanized` is the default. `--domain auto` is the default domain profile mode.

Supported domain profiles:
- `computer_engineering` / `software_engineering` / `information_system`: preserve source code, pages, interfaces, fields, database tables, configuration, test cases.
- `management` / `business_administration` / `human_resource`: preserve enterprise cases, departments, posts, systems, processes, interviews, questionnaires, indicators.
- `education`: preserve school, class, students, classroom links, teaching activities, homework, evaluation, teacher feedback.
- `literature` / `chinese_language`: preserve works, characters, plots, narrative perspective, imagery, textual detail.
- `law`: preserve statutes, case facts, dispute focus, judgment result, legal interpretation and responsibility.
- `economics` / `finance`: preserve indicators, years, samples, variables, models, statistical results and trends.
- `medicine` / `nursing`: preserve cases, samples, nursing process, observation indicators, intervention, follow-up and risk control.
- `art_design`: preserve design theme, composition, color, materials, sketches, iteration and work display.
- `engineering_general` / `mechanical` / `electrical` / `civil`: preserve parameters, equipment, structures, conditions, drawings, calculations and standards.
- `marxism` / `ideological_political` / `public_administration`: preserve policy texts, local practice, grassroots cases, theory source and governance scenarios.

The universal rule is:真实、具体、不模板化, not 高级、漂亮、统一. Low-risk paragraphs should not be heavily rewritten.

This skill is not a colloquialization tool. Oral wording is only a very low-frequency natural variation: by default, body text allows at most 1 mild oral expression per 10 sentences; abstracts, theory, methods, data analysis, and conclusions are stricter and should not contain obvious oral wording. Strong oral expressions are recovered automatically into thesis-appropriate wording, without converting them into template phrases such as "具有重要意义", "提供支撑", "完善机制", "提升水平", "优化路径", or "促进发展".

Anchor-first policy is mandatory. Before rewriting, check whether the paragraph has professional material anchors. If anchors exist, preserve and reorganize around them. If anchors are missing, only do light anti-template and rhythm edits, report the material shortage, and do not add colloquial language to fake authenticity.

## 5. Risk planning

| AIGC Rate | Modify | Rewrite | Rebuild | Intensity |
|-----------|--------|---------|---------|-----------|
| < 30%     | 80%    | 20%     | 0%      | low       |
| 30-50%    | 50%    | 40%     | 10%     | medium    |
| 50-70%    | 25%    | 55%     | 20%     | high      |
| ≥ 70%     | 10%    | 50%     | 40%     | critical  |

## 6. Evidence priority (highest to lowest)

1. Thesis original text
2. User-provided real materials
3. References already in the thesis
4. User supplementary data (surveys, interviews, code, screenshots)
5. Web search results (if allowed) — must record source
6. Model knowledge (conservative only) — MUST NOT fabricate specifics

## 7. PermissionGate scenarios

Must get user confirmation before proceeding when:
- A. User disallows rewrite but system needs rewrite/rebuild
- B. User disallows supplement but content is hollow
- C. No AIGC report available
- D. User allows supplement but has no materials
- E. User allows web search (record sources, no fabrication)

## 8. Rewrite rules

Three action types:

- **modify**: Adjust sentence order, reduce templating, add minor qualifiers. Keep original meaning.
- **rewrite**: Keep topic, change argument structure, add discipline details. NOT synonym replacement.
- **rebuild**: Full reconstruction from topic + section function. Must add concrete content.

Critical rules:
- High AIGC → prefer rewrite/rebuild, not light modify
- Different disciplines use DIFFERENT strategies — never force one template on all
- AntiAIStyleGuard rejects: template sentences, overly abstract phrases, synonym-only rewrites
- Avoid over-polished phrases such as "主要用于", "能够", "便于", "提供支撑", "具有重要意义", "形成闭环" when they appear as repeated templates
- Keep discipline-specific material anchors, but never invent missing materials
- Do not reduce AI-like writing traces by adding many oral expressions
- Strong oral expressions must be recovered before final output; if the guard still fails, report a warning instead of adding more naturalized wording

## 9. Format preservation

- Input = `.docx` → Output = `.docx` with same structure
- Modify only `w:t` text nodes via OOXML patching
- Preserve: heading hierarchy, bold/italic/font/size, tables, images, paragraph order
- NEVER modify: cover, declaration, TOC, references, formulas, figure/table numbers, identity info
- Create a working copy first — NEVER edit the original file directly

## 10. OutcomeReport (honest evaluation)

The final report MUST be honest:
- If no LLM was available and nothing was processed → say so
- If AIGC rate increased → verdict = "failed", recommend rollback
- If risk_chars increased → verdict = "failed"
- If rate dropped < 5pp → verdict = "failed"
- If no report available → say "无法验证", not "成功"
- Never write a success-style report when the outcome is unverifiable

## 11. Safety and integrity rules

**NON-NEGOTIABLE:**
1. Never fabricate data, experiments, citations, interviews, case facts, or risk percentages
2. Never promise specific detection outcomes
3. Never delete necessary citations or disguise sourced content as original
4. Medicine: absolutely no clinical data or case fabrication
5. Law: no fabricated legal articles or case facts
6. When evidence is insufficient, mark "需要用户提供资料" — do not invent
7. Do not auto-guess major and proceed with bulk rewrite
8. If information is incomplete, return missing fields — do not proceed
9. When materials are insufficient, ask for real materials instead of adding colloquial style
10. Never promise any detector-specific percentage outcome

**PRIORITY:**
- Goal achievement over code preservation
- Delete over patch
- Simplify over complex routing
- Discipline-specific over one-size-fits-all
- User confirmation over automatic execution
