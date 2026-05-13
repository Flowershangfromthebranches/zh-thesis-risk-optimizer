# zh-thesis-risk-optimizer

## 项目简介

`zh-thesis-risk-optimizer` 是面向中文论文的文本质量与风险优化 Skill。它用于辅助诊断并改进 AIGC 写作风险、查重相似风险、引用边界风险、报告片段定位问题和长文一致性问题。

本项目的定位是：中文论文文本质量优化、AIGC 风险诊断、相似表达修复、报告驱动定位、全文项目管理、引用完整性保护和学术规范辅助。

本项目不承诺检测结果，不规避检测系统，不伪造报告，不删除必要引用，不把他人观点伪装成原创观点。

## 核心能力

- AIGC 风险诊断：识别模板化表达、机械结构、泛化结尾、模糊归因等问题。
- AIGC 深度改写：重构段落逻辑、句间关系、具体对象和表达节奏，避免只换词。
- 查重相似风险诊断：处理定义重复、教材式表述、背景套话、相似源表述过近等问题。
- 评分诊断：输出启发式写作风险评分，用于定位风险和安排优先级。
- 句子级定位：按句标注风险标签、保护标签和处理建议。
- 报告驱动映射：把用户提供的查重/AIGC 报告片段映射回论文原文。
- 工科/理科/计算机论文保护：保护公式、代码、接口、表名、字段名、参数和实验数据。
- 全文项目管理：生成论文总览、章节任务、进度追踪、修改日志和项目交接摘要。
- 迭代优化：根据新报告进行第二轮、第三轮定点处理，不反复大改低风险章节。

## v0.5 有效改写增强

`v0.5-effective-rewrite-engine` 聚焦实际改写效果，不继续堆叠新外部功能：

- AIGC 深度改写引擎；
- 禁止浅层改写规则；
- 无报告保底双降流程；
- 有报告多轮双降流程；
- L5 深度重写强度；
- 改写后二次 AIGC 自检；
- 第二轮强制重写机制。

无报告模式只能做启发式优化，不能承诺检测结果。有报告模式通常更有效，因为报告提供了明确定位。即使有报告，也必须复测并人工核对引用、数据、术语和结论。

## 快速开始

### 1. 完整论文自分析

```text
请对我的完整论文建立全文双降项目总览，不要先改写。
```

### 2. 报告驱动处理

```text
这是论文原文和查重报告片段，请先映射回原文，再输出报告驱动任务表。
```

### 3. 指定模式处理

```text
请用 AIGC_ONLY / SIMILARITY_ONLY / DUAL_OPTIMIZATION 处理下面段落。
```

更多示例见 [QUICKSTART.md](QUICKSTART.md)。

## 支持模式

| 模式 | 用途 | 适用输入 |
|---|---|---|
| `AIGC_ONLY` | 只处理 AIGC 风险 | 论文段落、章节 |
| `AIGC_DEEP_REWRITE_ENGINE` | 深度处理高 AIGC 风险 | AIGC 味重、浅层改写无效的段落 |
| `SIMILARITY_ONLY` | 只处理查重相似风险 | 理论基础、综述、报告片段 |
| `DUAL_OPTIMIZATION` | 同时处理 AIGC 与相似风险 | 高风险段落、章节 |
| `NO_REPORT_FALLBACK_WORKFLOW` | 无报告保底双降 | 无检测报告的正文 |
| `AUTO_DIAGNOSIS` | 自动诊断并推荐模式 | 未指定模式的正文 |
| `ENGINEERING_SCIENCE_MODE` | 保护技术实体 | 工科、理科、计算机论文 |
| `SCORING_DIAGNOSIS_MODE` | 只评分和定位 | 章节、长段落 |
| `SENTENCE_LEVEL_DIAGNOSIS_MODE` | 句子级风险定位 | 单段或多段文本 |
| `BEFORE_AFTER_SCORE_COMPARISON` | 改写前后启发式评分对比 | 原文与改写稿 |
| `RISK_HEATMAP_TABLE` | 风险热区排序 | 长文、多章节 |
| `REPORT_DRIVEN_MODE` | 报告驱动总流程 | 查重/AIGC 报告 |
| `REPORT_AIGC_ONLY` | AIGC 报告定点处理 | AIGC 报告片段 |
| `REPORT_SIMILARITY_ONLY` | 查重报告定点处理 | 标红片段、相似源说明 |
| `REPORT_DUAL_OPTIMIZATION` | 双报告或重叠风险处理 | 查重 + AIGC 报告 |
| `REPORT_DRIVEN_MULTI_PASS_WORKFLOW` | 有报告多轮双降 | 报告片段 + 原文 |
| `REPORT_TO_SOURCE_MAPPING` | 报告片段映射原文 | 报告片段 + 原文 |
| `FULL_THESIS_PROJECT_MODE` | 完整论文项目管理 | 完整论文、多章节论文 |
| `CHAPTER_TASK_MODE` | 单章任务拆分 | 指定章节 |
| `PROGRESS_TRACKING_MODE` | 查看和维护进度 | 项目总览、章节任务 |
| `REVISION_LOG_MODE` | 记录修改历史 | 已修改章节或段落 |
| `ITERATIVE_REVISION_MODE` | 二轮/三轮定点优化 | 新报告、残留风险 |
| `PROJECT_HANDOFF_MODE` | 项目交接与恢复 | 总览、进度表、任务表 |

## 推荐工作流

1. 先诊断：识别章节结构、风险类型和输入材料。
2. 建立保护清单：保护引用、术语、公式、代码、接口、字段和实验数据。
3. 生成风险热区：按风险、报告贡献率和可安全改写程度排序。
4. 分章处理：完整论文先建总览，再拆分章节任务，不一次性重写全文。
5. 人工核对：引用密集、低置信度映射、实验数据密集段落进入人工核对。
6. 根据新报告迭代：只处理残留高风险片段，不反复大改已完成章节。

## 不适用场景

- 编造数据、实验、案例、访谈、问卷或图表。
- 编造引用、参考文献、相似源、报告百分比或风险等级。
- 删除必要引用。
- 伪造检测结果或报告内容。
- 承诺外部检测系统结果。
- 反向工程或攻击检测系统。
- 替作者完成研究主体内容。

## 项目结构

- [SKILL.md](SKILL.md)：Skill 总纲和模式路由。
- [references/](references)：详细规则与领域说明。
- [prompts/](prompts)：具体模式提示词。
- [workflow/](workflow)：全文项目管理模板。
- [examples/](examples)：模式示例。
- [tests/](tests)：人工验收清单。
- [CHANGELOG.md](CHANGELOG.md)：版本历史。
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)：第三方项目致谢与许可证说明。

## 上游致谢

本项目受到以下项目启发，并对原作者和贡献者表示感谢：

- [houlaisan/deai-academic-zh](https://github.com/houlaisan/deai-academic-zh)
- [Yezery/aigc-down-skill](https://github.com/Yezery/aigc-down-skill)
- [zczjyq/de-AIGC-skill](https://github.com/zczjyq/de-AIGC-skill)
- [openclaw/humanize-chinese](https://github.com/openclaw/skills/tree/main/skills/swaylq/humanize-chinese)
- [lengsukq/ParaphrasingToolClient](https://github.com/lengsukq/ParaphrasingToolClient)
- [Abnerla/AI_paper](https://github.com/Abnerla/AI_paper)
- [Haimbeau1o/thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer)

详细第三方说明见 [NOTICE](NOTICE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## License

MIT License. See [LICENSE](LICENSE).
