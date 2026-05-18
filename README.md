# zh-thesis-risk-optimizer

## 项目简介

`zh-thesis-risk-optimizer` 是面向中文论文的文本质量与风险优化 Skill。它用于辅助处理 AIGC 写作风险、查重相似风险、报告颜色定位、引用完整性保护、文件副本处理和最终验收。

当前版本采用瘦路由设计：`SKILL.md` 包含用户入口模式和内部必经引擎。旧模式和历史提示词只作为内部子规则或兼容资料保留，不再建议用户直接调用。

本项目不承诺任何外部检测平台结果，不破解、模拟、逆向或伪造检测系统，不伪造报告、数据、实验、引用、访谈、案例、代码、接口或运行结果，不删除必要引用，也不把他人观点伪装成原创。

## 核心能力

- 风险率前置门：所有改写任务先进入 `RISK_INTAKE_GATE`，必须收集当前查重率、当前 AIGC 疑似率、目标查重率和目标 AIGC 疑似率。
- Intake 预检：风险率字段完成后进入 `INTAKE_WIZARD_PRECHECK`，避免信息不足时直接改写。
- 文件副本处理：文件输入默认创建副本，不直接改原文件。
- OOXML DOCX 补丁：用 OOXML 方式修改 DOCX，最大限度保留格式，不重建全文。
- 重复插入防护：防止同一段落在 DOCX 中被重复插入。
- DOCX 颜色报告提取：先读取颜色元数据，再做红橙紫黑风险带映射。
- 专业策略路由：根据论文专业选择管理、计算机、工科、医学、法学、教育或人文 profile。
- 颜色分层路由：红、橙、紫、黑从第一次颜色报告解析后全部统计、路由和验收。
- 风险带覆盖率门禁：`RISK_BAND_COVERAGE_GATE` 强制检查红、橙、紫目标是否被处理、轻处理或有效冻结。
- 三任务类型颜色分级：在 `THREE_MODE_COLOR_BAND_WORKFLOW` 内处理只降 AIGC、只降查重、双降三类任务。
- 首轮红橙联合处理：原文和原版 AIGC 报告进入 `FIRST_PASS_RED_ORANGE_ENGINE`，红色和橙色一起作为主处理区。
- 当前报告红橙验收：复检稿进入 `CURRENT_REPORT_RED_ORANGE_ENGINE`，当前红橙必须全部进入任务表。
- 社科/管理类模板瓶颈处理：人力资源管理、工商管理、市场营销、教育管理、行政管理等论文启用 `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`。
- 受控人类化引擎：根据当前 AIGC 疑似率选择保守、受控或局部升级策略；Level 4 只能通过 `LOCAL_ESCALATED_HUMANIZATION` 局部执行。
- 论文语体守卫：`THESIS_REGISTER_GUARD` 按章节限制人化强度，摘要、理论基础和结论禁止聊天化。
- 紫色重平衡：`PURPLE_BAND_REBALANCER` 对紫色段做低强度统计扰动，不能 Level 4、不能聊天化、不能大幅扩写。
- 全文统计风格重平衡：`GLOBAL_STYLE_VARIANCE_ENGINE` 检查章节开头、句长、连接词和段落节奏是否过于统一。
- 改写写回门禁：确认改写文本不只是生成在表格里，而是已经真实写回 DOCX 正文。
- 模板残留检测：检测摘要、理论基础、第五章、结论等高风险章节是否仍保留原 AI 模板句。
- 学术语体守卫：防止受控人类化过度，禁止日记式、自媒体式、聊天式表达。
- AIGC 回归防线：同时防两种回归——更正式更像 AI，或太口语太不像论文。
- 首轮效果门禁：检查颜色迁移、AIGC 阈值、语体质量和格式完整性。
- 最终验收：`FINAL_ACCEPTANCE_AUDIT` 检查链路、红橙紫覆盖率、字数变化、证据缺口、语体质量、格式完整性和交付状态。

## 快速开始

第一步只建议调用 intake：

```text
请使用 zh-thesis-risk-optimizer。先执行 RISK_INTAKE_GATE 和 INTAKE_WIZARD_PRECHECK。
请展示 workflow/intake_request_template.md 的完整模板，等我填写后再继续。
```

如果你已经知道材料，可以直接填写：

```text
【任务目标】只降 AIGC
【当前查重率 current_similarity_rate】11%
【当前 AIGC 疑似率 current_aigc_rate】68.6%
【目标查重率 target_similarity_rate】15%
【目标 AIGC 疑似率 target_aigc_rate】30%
【任务类型 task_type】aigc_only
【论文输入】原文 DOCX：/path/to/original.docx
【处理范围】全文；只处理报告红橙片段
【输出形式】创建副本并回写；同时输出诊断表和验收表
【字数约束】全文 ±10%
【保护项】引用、数据、图表编号、参考文献、学校声明、代码、路径、参数
【AIGC 报告】/path/to/aigc_report.docx
【是否有 AIGC 颜色报告 has_aigc_color_report】true
【红段数量/比例 current_red_count/current_red_ratio】1 / 请自动解析
【橙段数量/比例 current_orange_count/current_orange_ratio】17 / 请自动解析
【紫段数量/比例 current_purple_count/current_purple_ratio】紫段较多 / 请自动解析
【黑段数量/比例 current_black_count/current_black_ratio】请自动解析
【论文专业和题目】人力资源管理，《……》
【查重报告】无
【是否有查重报告 has_similarity_report】false
【报告颜色规则】红色>70%；橙色60%-70%；紫色50%-60%；黑色<50%
【当前状态】原文未改
【阶段 stage】original
【是否要求保持 DOCX 原格式 preserve_docx_format_required】true
【历史版本】无
【用户目标】红橙一起处理；不全文大改；不承诺检测结果
【可用证据】问卷、访谈、流程、岗位、指标等材料；没有则写无
【特殊要求】跳过
```

## 受控人类化：安全吸收老版本降 AIGC 能力

如果想吸收老版本 bff6860 的强降 AIGC 能力，但不想失去学术规范，应使用 `CONTROLLED_HUMANIZATION_ENGINE` level 2 或 level 3，而不是 aggressive 口语化。

```text
请使用新版受控人类化策略：吸收 bff6860 的去模板化、句长变化和作者判断能力，
但必须通过 ACADEMIC_TONE_GUARD，不能出现日记式、自媒体式或聊天式表达；
DOCX 写回必须使用 OOXML patch，只替换确认映射的正文段落，保持原格式。
```

## 工作流组件

以下是当前主工作流组件。旧提示词文件仍可保留，但不得作为用户命令直接调用；模型应按“标准链路”执行，而不是让用户手动挑旧入口。

| 入口模式 | 用途 |
|---|---|
| `RISK_INTAKE_GATE` | 改写前收集当前/目标查重率与 AIGC 疑似率，决定策略、人化上限和局部 Level 4 权限。 |
| `INTAKE_WIZARD_PRECHECK` | 所有匹配任务的入口，先收集必填、强烈建议和可选信息。 |
| `FILE_INPUT_COPY_WORKFLOW` | 用户提供 DOCX/TXT/Markdown/LaTeX 文件时，先创建副本再处理。 |
| `OOXML_DOCX_PATCH_WORKFLOW` | 内部引擎：OOXML 方式修改 DOCX，最大限度保留格式。 |
| `DOCX_COLOR_REPORT_EXTRACTION` | 用户提供 Word/DOCX 颜色标记报告时，先提取颜色元数据。 |
| `THREE_MODE_COLOR_BAND_WORKFLOW` | 按红橙紫黑风险带处理 AIGC、查重或双目标任务。 |
| `DISCIPLINE_STRATEGY_ROUTER` | 根据专业选择 profile、保护项和允许的人化强度。 |
| `COLOR_BAND_ROUTER` | 第一次颜色解析后立即统计和路由红橙紫黑。 |
| `RISK_BAND_COVERAGE_GATE` | 检查红橙紫目标覆盖率、跳过原因、冻结理由和下一批处理计划。 |
| `FIRST_PASS_RED_ORANGE_ENGINE` | 原文加原版 AIGC 报告的首轮红橙联合处理。 |
| `CURRENT_REPORT_RED_ORANGE_ENGINE` | 当前稿加当前 AIGC 报告的红橙覆盖处理。 |
| `AIGC_PLATEAU_BREAKER` | 多轮后红色下降但橙色堆积、AIGC 下降变慢时使用。 |
| `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` | 社科/管理类论文模板骨架和证据不足问题处理。 |
| `CONTROLLED_HUMANIZATION_ENGINE` | 内部引擎：受控去 AIGC 人类化，打破 AI 模板但保持学术语体。 |
| `LOCAL_ESCALATED_HUMANIZATION` | 内部引擎：只对符合条件的红橙残留段局部启用 Level 4，禁止全文 Level 4。 |
| `PURPLE_BAND_REBALANCER` | 内部引擎：对紫色段做低强度统计重平衡，不允许 Level 4。 |
| `GLOBAL_STYLE_VARIANCE_ENGINE` | 内部引擎：检查全文统计风格统一问题并输出局部调整计划。 |
| `REWRITE_APPLICATION_GATE` | 内部门禁：验证改写是否真实写回 DOCX 正文、diff 是否足够。 |
| `TEMPLATE_RESIDUE_DETECTOR` | 内部门禁：检测改写后是否仍残留高风险模板句。 |
| `THESIS_REGISTER_GUARD` | 内部门禁：按章节把人化文本拉回论文语体，严格章节禁止聊天化。 |
| `AIGC_REGRESSION_GUARD` | 防止改写后更正式更像 AI，或太口语太不像论文。 |
| `FIRST_PASS_EFFECTIVENESS_GATE` | 内部必经门禁：检查颜色迁移、AIGC 阈值、语体质量和格式完整性。 |
| `FINAL_ACCEPTANCE_AUDIT` | 每次报告驱动或文件副本任务结束前的最终验收。 |

## 标准链路

原文 + 原版 AIGC 颜色报告 + 只降 AIGC + 控字数 + 红橙一起处理：

```text
RISK_INTAKE_GATE
-> DISCIPLINE_STRATEGY_ROUTER
-> FILE_INPUT_COPY_WORKFLOW
-> OOXML_DOCX_PATCH_WORKFLOW when DOCX format preservation is required
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> COLOR_BAND_ROUTER
-> RISK_BAND_COVERAGE_GATE
-> FIRST_PASS_RED_ORANGE_ENGINE
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable
-> CONTROLLED_HUMANIZATION_ENGINE when applicable
-> LOCAL_ESCALATED_HUMANIZATION when triggered
-> PURPLE_BAND_REBALANCER when triggered
-> GLOBAL_STYLE_VARIANCE_ENGINE
-> REWRITE_APPLICATION_GATE
-> TEMPLATE_RESIDUE_DETECTOR
-> THESIS_REGISTER_GUARD
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> RISK_BAND_COVERAGE_GATE final check
-> FINAL_ACCEPTANCE_AUDIT
```

当前稿 + 当前 AIGC 颜色报告：

```text
RISK_INTAKE_GATE
-> DISCIPLINE_STRATEGY_ROUTER
-> FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> COLOR_BAND_ROUTER
-> RISK_BAND_COVERAGE_GATE
-> CURRENT_REPORT_RED_ORANGE_ENGINE
-> AIGC_PLATEAU_BREAKER when applicable
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable
-> CONTROLLED_HUMANIZATION_ENGINE when applicable
-> LOCAL_ESCALATED_HUMANIZATION when triggered
-> PURPLE_BAND_REBALANCER when triggered
-> GLOBAL_STYLE_VARIANCE_ENGINE
-> REWRITE_APPLICATION_GATE
-> TEMPLATE_RESIDUE_DETECTOR
-> THESIS_REGISTER_GUARD
-> AIGC_REGRESSION_GUARD
-> FIRST_PASS_EFFECTIVENESS_GATE
-> RISK_BAND_COVERAGE_GATE final check
-> FINAL_ACCEPTANCE_AUDIT
```

任一步缺失，都不能标记完成。首轮不是只处理重点章节；只要报告识别出红橙紫风险段，最终必须输出 `red_coverage_rate`、`orange_coverage_rate`、`purple_coverage_rate`、跳过清单、有效冻结理由和 `next_batch_plan`。红色覆盖率低于 100% 或橙色覆盖率不足时，不得标记完成。

Level 4 不是全文模式，只能局部用于符合专业 profile 和 section profile 的高风险残留段。摘要、理论基础、结论禁止聊天化表达。紫色处理用于降低全文统计一致性，不用于大幅改写。

## DOCX 格式保护

DOCX 写回默认使用 OOXML patch：

- 不直接改原文件，先创建副本。
- 只修改 `word/document.xml` 中已确认映射的 `w:t` 文本节点。
- 不重建 styles.xml、numbering.xml、页眉页脚、脚注、尾注、批注、图片、目录。
- 低置信度映射不写回。
- 重复匹配立即停止写回。
- 写回后验证：zip 完整性、无重复插入、资源保留、页数稳定。

## 专业适配说明

本 Skill 支持中文论文通用文本风险优化，但不宣称适合所有专业的一次性自动处理。

- 对社科/管理类论文有专项规则：重点处理模板骨架、管理套话、证据不足、问卷/访谈/流程/岗位/指标缺失。
- 对工科/计算机类论文有专项保护：公式、代码、接口、路径、表名、字段名、参数、实验数据、运行结果默认保护。
- 其他专业必须先填写专业保护项、数据边界和证据来源；信息不足时应输出作者补充清单，而不是编造内容。

## 项目结构

- [SKILL.md](SKILL.md)：瘦路由和强制链路。
- [QUICKSTART.md](QUICKSTART.md)：使用指南。
- [references/](references)：入口模式和内部引擎使用的详细规则。
- [prompts/](prompts)：入口提示词和历史兼容提示词。
- [workflow/](workflow)：intake、作者材料包、OOXML 补丁清单和文件/项目模板。
- [tests/](tests)：结构和安全验收清单。
- [NOTICE](NOTICE) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)：第三方致谢和许可证说明。

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
