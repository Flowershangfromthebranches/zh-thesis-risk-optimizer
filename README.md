# zh-thesis-risk-optimizer

## 项目简介

`zh-thesis-risk-optimizer` 是面向中文论文的文本质量与风险优化 Skill。它用于辅助处理 AIGC 写作风险、查重相似风险、报告颜色定位、引用完整性保护、文件副本处理和最终验收。

当前版本采用瘦路由设计：`SKILL.md` 只保留 10 个入口模式。旧模式和历史提示词只作为内部子规则或兼容资料保留，不再建议用户直接调用。

本项目不承诺任何外部检测平台结果，不破解、模拟、逆向或伪造检测系统，不伪造报告、数据、实验、引用、访谈、案例、代码、接口或运行结果，不删除必要引用，也不把他人观点伪装成原创。

## 核心能力

- Intake 预检：所有匹配任务先进入 `INTAKE_WIZARD_PRECHECK`，避免信息不足时直接改写。
- 文件副本处理：文件输入默认创建副本，不直接改原文件。
- DOCX 颜色报告提取：先读取颜色元数据，再做红橙紫黑风险带映射。
- 三任务类型颜色分级：在 `THREE_MODE_COLOR_BAND_WORKFLOW` 内处理只降 AIGC、只降查重、双降三类任务。
- 首轮红橙联合处理：原文和原版 AIGC 报告进入 `FIRST_PASS_RED_ORANGE_ENGINE`，红色和橙色一起作为主处理区。
- 当前报告红橙验收：复检稿进入 `CURRENT_REPORT_RED_ORANGE_ENGINE`，当前红橙必须全部进入任务表。
- 社科/管理类模板瓶颈处理：人力资源管理、工商管理、市场营销、教育管理、行政管理等论文启用 `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`。
- AIGC 回归防线：识别更正式、更顺滑、更抽象、更像 AI 的改写回归。
- 最终验收：`FINAL_ACCEPTANCE_AUDIT` 检查链路、红橙覆盖率、字数变化、证据缺口和格式风险。

## 快速开始

第一步只建议调用 intake：

```text
请使用 zh-thesis-risk-optimizer。先执行 INTAKE_WIZARD_PRECHECK。
请展示 workflow/intake_request_template.md 的完整模板，等我填写后再继续。
```

如果你已经知道材料，可以直接填写：

```text
【任务目标】只降 AIGC
【论文输入】原文 DOCX：/path/to/original.docx
【处理范围】全文；只处理报告红橙片段
【输出形式】创建副本并回写；同时输出诊断表和验收表
【字数约束】全文 ±10%
【保护项】引用、数据、图表编号、参考文献、学校声明、代码、路径、参数
【AIGC 报告】/path/to/aigc_report.docx
【论文专业和题目】人力资源管理，《……》
【查重报告】无
【报告颜色规则】红色>70%；橙色60%-70%；紫色50%-60%；黑色<50%
【当前状态】原文未改
【历史版本】无
【用户目标】红橙一起处理；不全文大改；不承诺检测结果
【可用证据】问卷、访谈、流程、岗位、指标等材料；没有则写无
【特殊要求】跳过
```

## 支持模式

用户只需要使用下面 10 个入口。旧提示词文件仍可保留，但不得作为用户命令直接调用。

| 入口模式 | 用途 |
|---|---|
| `INTAKE_WIZARD_PRECHECK` | 所有匹配任务的入口，先收集必填、强烈建议和可选信息。 |
| `FILE_INPUT_COPY_WORKFLOW` | 用户提供 DOCX/TXT/Markdown/LaTeX 文件时，先创建副本再处理。 |
| `DOCX_COLOR_REPORT_EXTRACTION` | 用户提供 Word/DOCX 颜色标记报告时，先提取颜色元数据。 |
| `THREE_MODE_COLOR_BAND_WORKFLOW` | 按红橙紫黑风险带处理 AIGC、查重或双目标任务。 |
| `FIRST_PASS_RED_ORANGE_ENGINE` | 原文加原版 AIGC 报告的首轮红橙联合处理。 |
| `CURRENT_REPORT_RED_ORANGE_ENGINE` | 当前稿加当前 AIGC 报告的红橙覆盖处理。 |
| `AIGC_PLATEAU_BREAKER` | 多轮后红色下降但橙色堆积、AIGC 下降变慢时使用。 |
| `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` | 社科/管理类论文模板骨架和证据不足问题处理。 |
| `AIGC_REGRESSION_GUARD` | 防止改写后更正式、更顺滑、更抽象、更像 AI。 |
| `FINAL_ACCEPTANCE_AUDIT` | 每次报告驱动或文件副本任务结束前的最终验收。 |

## 标准链路

原文 + 原版 AIGC 颜色报告 + 只降 AIGC + 控字数 + 红橙一起处理：

```text
FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> FIRST_PASS_RED_ORANGE_ENGINE
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable
-> AIGC_REGRESSION_GUARD
-> FINAL_ACCEPTANCE_AUDIT
```

当前稿 + 当前 AIGC 颜色报告：

```text
FILE_INPUT_COPY_WORKFLOW
-> DOCX_COLOR_REPORT_EXTRACTION
-> THREE_MODE_COLOR_BAND_WORKFLOW
-> CURRENT_REPORT_RED_ORANGE_ENGINE
-> AIGC_PLATEAU_BREAKER when applicable
-> SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK when applicable
-> AIGC_REGRESSION_GUARD
-> FINAL_ACCEPTANCE_AUDIT
```

任一步缺失，都不能标记完成。

## 专业适配说明

本 Skill 支持中文论文通用文本风险优化，但不宣称适合所有专业的一次性自动处理。

- 对社科/管理类论文有专项规则：重点处理模板骨架、管理套话、证据不足、问卷/访谈/流程/岗位/指标缺失。
- 对工科/计算机类论文有专项保护：公式、代码、接口、路径、表名、字段名、参数、实验数据、运行结果默认保护。
- 其他专业必须先填写专业保护项、数据边界和证据来源；信息不足时应输出作者补充清单，而不是编造内容。

## DOCX 文件格式保护

文件输入默认执行 `FILE_INPUT_COPY_WORKFLOW`：

- 默认创建原文件副本，不直接修改原文件。
- 只替换已经确认映射的目标文本。
- 不重建全文，不重新排版全文。
- 低置信度映射不写回文件，只输出人工确认项。
- 复杂 Word 格式、批注、域、脚注、尾注、表格、图片和公式需要人工复核。
- 本项目不承诺所有 Word 格式 100% 不变。

## 不适用场景

- 编造数据、实验、案例、访谈、问卷或图表。
- 编造引用、参考文献、相似源、报告百分比或风险等级。
- 删除必要引用。
- 伪造检测结果或报告内容。
- 承诺外部检测系统结果。
- 反向工程或攻击检测系统。
- 替作者完成不存在的研究主体内容。

## 项目结构

- [SKILL.md](SKILL.md)：瘦路由和强制链路。
- [QUICKSTART.md](QUICKSTART.md)：只面向 10 个入口的使用指南。
- [references/](references)：入口模式使用的详细规则。
- [prompts/](prompts)：入口提示词和历史兼容提示词。
- [workflow/](workflow)：intake、作者材料包和文件/项目模板。
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
