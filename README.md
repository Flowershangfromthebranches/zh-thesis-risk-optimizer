# zh-thesis-risk-optimizer

## 项目简介

`zh-thesis-risk-optimizer` 是面向中文论文的文本质量与风险优化 Skill。它用于辅助诊断并改进 AIGC 写作风险、查重相似风险、引用边界风险、报告片段定位问题和长文一致性问题。

本项目的定位是：中文论文文本质量优化、AIGC 风险诊断、相似表达修复、报告驱动定位、全文项目管理、引用完整性保护和学术规范辅助。

本项目不承诺检测结果，不破解或模拟检测系统，不伪造报告，不删除必要引用，不把他人观点伪装成原创观点。

## 核心能力

- **节奏与突发度审计**：检查句长过均匀、连接词过密和枚举结构过强的问题；仅在确有必要时做节奏修复，避免把论文改成口号式短句。
- AIGC 风险诊断：识别模板化表达、机械结构、泛化结尾、模糊归因等问题。
- AIGC 深度改写：重构段落逻辑、句间关系、具体对象和表达节奏，避免只换词。
- **反形式化防线**：识别并阻止改写后文本变得更精致、更平衡、更抽象的回归问题。
- 查重相似风险诊断：处理定义重复、教材式表述、背景套话、相似源表述过近等问题。
- 评分诊断：输出启发式写作风险评分，用于定位风险和安排优先级。
- 句子级定位：按句标注风险标签、保护标签和处理建议。
- 报告驱动映射：把用户提供的查重/AIGC 报告片段映射回论文原文。
- DOCX 颜色报告解析：对 Word 颜色标记报告先提取颜色元数据，避免普通文本抽取丢失红橙紫黑风险带。
- 目标驱动多轮优化：支持用户设置相似度和 AIGC 目标阈值，并用报告趋势安排下一轮任务。
- AIGC 反升防线：识别正式化润色、抽象名词膨胀、证据稀释等回归问题。
- AIGC 专项控长修复：在查重已基本满足要求后，定点降低 AIGC 风险并控制全文增幅。
- AIGC 平台期突破：识别多轮改写后“红色高风险下降、橙色中风险卡住”的瓶颈。
- 首轮红橙联合处理：原版报告进入首轮时，同时把红色和橙色纳入主处理区。
- 字符变动守卫：默认整篇论文总字符变动控制在 `±10%` 范围内。
- 三模式颜色分级工作流：只降重、只降 AIGC、双降统一使用红/橙/紫/黑处理规则。
- 文件副本处理：文件输入时不改原件，创建副本、提取目标文本、回写副本并交付副本。
- 社科/管理类模板瓶颈处理：针对人力资源、工商管理、市场营销、行政管理、教育管理等论文的标准化表达平台期。
- 工科/理科/计算机论文保护：保护公式、代码、接口、表名、字段名、参数和实验数据。
- 全文项目管理：生成论文总览、章节任务、进度追踪、修改日志和项目交接摘要。
- 迭代优化：根据新报告进行第二轮、第三轮定点处理，不反复大改低风险章节。
- 启动预检：任何匹配本 Skill 的任务都先做 `INTAKE_WIZARD_PRECHECK`；信息足够时直接继续，信息不足时给出可复制模板。

## 快速开始

### 0. 推荐入口：复制模板

```text
当前任务需要使用 zh-thesis-risk-optimizer。请先执行 INTAKE_WIZARD_PRECHECK。
请先展示 workflow/intake_request_template.md 中的完整模板，等我填写后再处理。
必填项必须填写；强烈建议和可选项也要展示，我会填写、写无、写跳过或写请自动判断。
```

可复制模板见 [workflow/intake_request_template.md](workflow/intake_request_template.md)。

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

### 4. 目标驱动多轮处理

```text
我的目标是查重相似度 <10%、AIGC <20%。下面是原文、当前稿、历史报告和新报告，请先做报告差异诊断，再进入 TARGETED_MULTIPASS_ENGINE，不要直接全文改写。
```

### 5. AIGC 专项控长处理

```text
查重已经基本达标，下一步只重点降 AIGC。原文约 17000 字，当前稿约 24000 字，请进入 AIGC_FOCUSED_LENGTH_CONTROLLED，并把全文增幅控制在 0-2000 中文字内。
```

### 6. AIGC 平台期处理

```text
我有原文、三轮改写稿和三轮 AIGC 报告。AIGC 从 76% 降到 65%、57%、54% 后卡住，请进入 AIGC_PLATEAU_BREAKER，先判断红色/橙色/紫色风险带变化，再只处理橙色平台期段落。
```

### 7. 首轮红橙联合处理

```text
这是原版论文和原版 AIGC 报告。请进入 FIRST_PASS_RED_ORANGE_ENGINE，把红色和橙色都纳入首轮主处理区，目标是启发式压到紫色/黑色水平；整篇论文总字符变动控制在 ±10% 内，黑色/低风险段落冻结。
```

### 8. 三模式颜色分级处理

```text
请进入 THREE_MODE_COLOR_BAND_WORKFLOW。模式选择：只降AIGC。输入是论文文件和AIGC报告；红色为70%以上，橙色为60%-70%，紫色为50%-60%，黑色为50%以下。请创建原文件副本，不改原文件，只处理红色和橙色，内部自评是否接近紫/黑水平，全文字符数控制在原文±10%。
```

### 9. 社科/管理类模板瓶颈处理

```text
这是一篇人力资源管理/工商管理/教育管理/市场营销类论文，AIGC报告红橙段落主要集中在现状、问题、原因、对策和保障措施。请进入 SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK，先判断是否存在“现状-问题-原因-对策”模板骨架，再用企业/问卷/访谈/流程/指标证据重构；证据不足时输出作者补充清单，不要编造。
```

更多示例见 [QUICKSTART.md](QUICKSTART.md)。

## 支持模式

日常使用不需要记住全部模式。一般先走 `INTAKE_WIZARD_PRECHECK`，用户填写 intake 模板后，再由 Skill 自动路由到下列常用工作流。

| 常见需求 | 推荐路由 | 需要材料 |
|---|---|---|
| 不知道怎么开始 | `INTAKE_WIZARD_PRECHECK` | 按模板补充必填、强烈建议和可选项 |
| 只降 AIGC | `AIGC_ONLY` / `REPORT_AIGC_ONLY` | 原文，最好有 AIGC 报告 |
| 只降查重 | `SIMILARITY_ONLY` / `REPORT_SIMILARITY_ONLY` | 原文，最好有查重报告 |
| 双降 | `THREE_MODE_COLOR_BAND_WORKFLOW` / `DUAL_OPTIMIZATION` | 原文，最好有两类报告 |
| Word 颜色报告 | `DOCX_COLOR_REPORT_EXTRACTION` | DOCX 报告和颜色规则 |
| 原版 + 原版 AIGC 报告 | `FIRST_PASS_RED_ORANGE_ENGINE` | 原文和原版报告 |
| 多轮后 AIGC 卡住 | `AIGC_PLATEAU_BREAKER` | 历史稿和多轮报告 |
| 查重够用，只降 AIGC | `AIGC_FOCUSED_LENGTH_CONTROLLED` | 原文、当前稿、AIGC 报告 |
| 人力资源/管理类论文效果差 | `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` | 原文、报告、问卷/访谈/流程证据 |
| 文件交付 | `FILE_INPUT_COPY_WORKFLOW` | 原文件路径和输出要求 |
| 完整论文长期任务 | `FULL_THESIS_PROJECT_MODE` | 完整论文或章节目录 |

完整模式路由见 [SKILL.md](SKILL.md)。维护人员检查项见 [tests/](tests)。

## 推荐工作流

1. 先预检：任何匹配本 Skill 的任务先进入 `INTAKE_WIZARD_PRECHECK`；先展示 `workflow/intake_request_template.md`，等待用户填写必填项，并对强烈建议/可选项写明内容、无、跳过或请自动判断。
2. 先诊断：识别章节结构、风险类型和输入材料。
3. 建立保护清单：保护引用、术语、公式、代码、接口、字段和实验数据。
4. 生成风险热区：按风险、报告贡献率和可安全改写程度排序。
5. 分章处理：完整论文先建总览，再拆分章节任务，不一次性重写全文。
6. 人工核对：引用密集、低置信度映射、实验数据密集段落进入人工核对。
7. 根据新报告迭代：只处理残留高风险片段，不反复大改已完成章节。
8. 平台期处理：如果多轮 AIGC 下降变慢，先判断红色、橙色、紫色风险带变化，冻结白色段落，再处理橙色平台期。
9. 首轮红橙处理：如果一开始就有原版 AIGC 报告，红色和橙色同时进入主处理区，并用 `±10%` 字符变动守卫约束全文。
10. 文件处理：如果输入是文件，先创建副本，不直接修改原文件；从副本提取要改的文本，改完回写副本并交付副本文件。

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
- [workflow/](workflow)：入口引导、文件处理和全文项目管理模板。
- [examples/](examples)：模式示例。
- [tests/](tests)：人工验收清单。
- [CHANGELOG.md](CHANGELOG.md)：版本历史。
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)：第三方项目致谢与许可证说明。

## 上游致谢

本项目受到以下项目启发，并对原作者和贡献者表示感谢：

- [houlaisan/deai-academic-zh](https://github.com/houlaisan/deai-academic-zh) — 启发点包括扫描诊断、分轮迭代、报告优先和文本节奏相关分析思路。本项目在尊重原作者的前提下重新组织，不复制其代码或长文本。
- [Yezery/aigc-down-skill](https://github.com/Yezery/aigc-down-skill) — AI写作模式识别（16种模式），保量润色原则，会话记忆库
- [zczjyq/de-AIGC-skill](https://github.com/zczjyq/de-AIGC-skill) — 长度保持编辑，术语一致性，滚动段落摘要
- [openclaw/humanize-chinese](https://github.com/openclaw/skills/tree/main/skills/swaylq/humanize-chinese) — 困惑度、突发度、段落熵作为分析信号
- [lengsukq/ParaphrasingToolClient](https://github.com/lengsukq/ParaphrasingToolClient) — 报告解析工作流
- [Abnerla/AI_paper](https://github.com/Abnerla/AI_paper) — AI痕迹自检，报告导入，标记片段映射
- [Haimbeau1o/thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) — 两层文档架构，迭代优化闭环

详细第三方说明见 [NOTICE](NOTICE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## License

MIT License. See [LICENSE](LICENSE).
