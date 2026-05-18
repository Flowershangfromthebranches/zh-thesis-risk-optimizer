# Discipline Strategy Router

## Purpose

`DISCIPLINE_STRATEGY_ROUTER` selects a discipline profile before any color-band rewrite. It prevents management-style humanization from being applied to computer-science, engineering, medical, law, education, or humanities theses.

It does not promise detector outcomes and must not weaken citation, data, terminology, or format protection.

## Supported Profiles

| selected_profile | discipline_scope | core risks | strategy summary |
|---|---|---|---|
| `management_profile` | 人力资源管理、工商管理、市场营销、行政管理、旅游管理、财务管理、会计管理、物流管理 | 咨询腔、对策模板、体系/机制/赋能/闭环、摘要固定结构、理论百科化、第五章套话 | 反咨询腔、证据前置、作者判断、局部自然解释感；第四章/第五章可较强自然化；摘要/理论/结论禁止聊天化 |
| `computer_science_profile` | 计算机科学、软件工程、信息管理、网络工程、数据科学、人工智能 | 需求分析模板、系统功能模板、模块设计重复、测试结果套话、总结展望 AI 腔 | 保持技术文档风格；只修需求/概述/测试分析/总结模板句；代码、接口、表字段不人化 |
| `engineering_profile` | 机械、土木、电气、自动化、材料、环境、化工 | 实验结论模板、设计说明模板、结果表明/满足要求/具有可行性重复 | 方法和参数基本不动；讨论、结果解释、结论轻度去模板；禁止强人化 |
| `medicine_profile` | 医学、护理、药学、公共卫生 | 摘要/讨论模板、临床价值/推广价值套话、综述 AI 化 | 严格医学规范语体；轻度模板拆解；禁止口语化和主观替代医学表达 |
| `law_profile` | 法学、知识产权、行政法、民商法、刑法 | 法理论述模板、完善制度/健全机制/加强监管、结论宏观化 | 保留法条严谨；制度完善类具体化；禁止口语化 |
| `education_profile` | 教育学、学前教育、小学教育、心理健康教育 | 政策背景套话、促进学生全面发展/提升教学质量、对策模板 | 压缩政策背景；教学场景具体化；调查结果前置；对策落到课堂/教师/学生/评价 |
| `humanities_profile` | 文学、语言学、新闻传播、历史、艺术设计 | 赏析套话、价值意义空泛、丰富内涵/增强感染力 | 文本细读、语料依据、作品细节；不随意替换引用；避免管理类对策化 |

## Output

```yaml
discipline_strategy_router:
  detected_discipline: <discipline>
  discipline_confidence: high | medium | low
  selected_profile: management_profile | computer_science_profile | engineering_profile | medicine_profile | law_profile | education_profile | humanities_profile | unknown_profile
  protected_elements: <list>
  allowed_humanization_level: <section-aware level>
  forbidden_rewrite_actions: <list>
  preferred_rewrite_moves: <list>
  profile_file: discipline_profiles/<profile>.md
```

## Routing Rules

- If confidence is `low`, ask the user to confirm discipline before strong humanization.
- If discipline is unknown, use conservative academic rewrite and request protected elements.
- `LOCAL_ESCALATED_HUMANIZATION` may only run if the selected profile and section profile both allow it.
- Medical, law, and engineering experimental sections default to conservative handling even when AIGC is high.
- For one-pass handling, target AIGC `<=20%`, or cross-discipline tasks, load `references/one_pass_cross_discipline_strategy.md` after selecting the profile.
- Do not force management-style evidence moves onto other profiles. Each profile must use its own evidence type and protected boundaries.
- If a color report includes black or gray text, pass the freeze categories to `COLOR_BAND_ROUTER`; black/gray are not discipline-specific rewrite targets.

## Relation To SKILL.md

Runs after `RISK_INTAKE_GATE` and before `FILE_INPUT_COPY_WORKFLOW`. Its output constrains `COLOR_BAND_ROUTER`, `CONTROLLED_HUMANIZATION_ENGINE`, `LOCAL_ESCALATED_HUMANIZATION`, `PURPLE_BAND_REBALANCER`, and `FINAL_ACCEPTANCE_AUDIT`.
