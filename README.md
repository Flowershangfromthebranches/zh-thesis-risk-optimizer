# zh-thesis-risk-optimizer

## 项目简介

`zh-thesis-risk-optimizer` 是面向中文论文的文本质量与风险优化 Skill。它用于辅助诊断并改进 AIGC 写作风险、查重相似风险、引用边界风险、报告片段定位问题和长文一致性问题。

本项目的定位是：中文论文文本质量优化、AIGC 风险诊断、相似表达修复、报告驱动定位、全文项目管理、引用完整性保护和学术规范辅助。

本项目不承诺检测结果，不破解或模拟检测系统，不伪造报告，不删除必要引用，不把他人观点伪装成原创观点。

## 核心能力

- AIGC 风险诊断：识别模板化表达、机械结构、泛化结尾、模糊归因等问题。
- AIGC 深度改写：重构段落逻辑、句间关系、具体对象和表达节奏，避免只换词。
- 查重相似风险诊断：处理定义重复、教材式表述、背景套话、相似源表述过近等问题。
- 评分诊断：输出启发式写作风险评分，用于定位风险和安排优先级。
- 句子级定位：按句标注风险标签、保护标签和处理建议。
- 报告驱动映射：把用户提供的查重/AIGC 报告片段映射回论文原文。
- 目标驱动多轮优化：支持用户设置相似度和 AIGC 目标阈值，并用报告趋势安排下一轮任务。
- AIGC 反升防线：识别正式化润色、抽象名词膨胀、证据稀释等回归问题。
- AIGC 专项控长修复：在查重已基本满足要求后，定点降低 AIGC 风险并控制全文增幅。
- AIGC 平台期突破：识别多轮改写后“红色高风险下降、橙色中风险卡住”的瓶颈。
- 首轮红橙联合处理：原版报告进入首轮时，同时把红色和橙色纳入主处理区。
- 字符变动守卫：默认整篇论文总字符变动控制在 `±10%` 范围内。
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

## v0.6 目标驱动多轮闭环

`v0.6-targeted-multipass-engine` 面向真实多轮双降任务，核心是“目标驱动 + 报告反馈 + 证据注入 + 多轮闭环 + 回归防线”。

新增能力：

- 支持用户设置优化目标，例如相似度 `<10%`、AIGC `<20%`。
- 明确这些目标只表示用户期望和回归测试方向，不是检测结果承诺。
- 支持多版报告反馈闭环：先分析新旧报告差异，再决定下一轮任务。
- 加入 AIGC 反升防线，避免把普通表达改成更正式、更抽象、更像 AI 的润色稿。
- 加入相似度 `<10%` 专项策略和 AIGC `<20%` 专项策略。
- 加入真实内容增量机制，用模块、参数、接口、测试环境、结果数据和边界条件替代空泛模板句。
- 加入 Web 漏洞扫描工具论文回归案例，明确 v0.4 只是历史参考，不是成功标准，v0.5 的形式化润色也不是高质量。

## v0.7 AIGC 专项控长引擎

`v0.7-aigc-focused-length-controlled-engine` 在查重相似风险已经基本满足用户要求时启用。它不再把继续降重作为主目标，而是聚焦 AIGC 高风险段落的定点修复。

新增能力：

- 当查重已达标或接近达标时，进入 AIGC-focused 模式。
- 默认全文增幅控制在 0-2000 中文字；用户指定范围时以用户范围为准。
- 新增长度预算控制和 Compression Pass，处理从约 17000 字扩到约 24000 字这类过度扩写。
- 新增句子级 AIGC 定位，每段优先处理 1-3 个关键句，不做全文无差别重写。
- 新增重复 AI 腔压缩、节奏/突发性控制、人工证据补充清单和保守修复模式。
- 优先替换高风险句，不保留模板句后再追加解释。
- 仍然不承诺任何检测平台结果。

## v0.8 AIGC 平台期突破

`v0.8-aigc-plateau-breaker` 面向多轮降 AIGC 后下降变慢的情况。它把“红色高风险是否下降”和“橙色中风险是否仍然成片存在”分开判断，避免把红色降成橙色误认为真正完成。

新增能力：

- 识别多轮 AIGC 报告中的下降瓶颈，例如 76% -> 65% -> 57% -> 54% 这类边际收益递减。
- 新增 `AIGC_PLATEAU_BREAKER`，先诊断平台期类型，再决定是否继续改写。
- 新增橙色中风险专项策略，处理长枚举、管理类模板、平滑段落、证据摆放不当等问题。
- 新增学科瓶颈规则，区分计算机论文的技术保护平台期和管理类论文的模板结构平台期。
- 强制冻结白色/低风险段落，避免把已经安全的内容反复改坏。
- 对连续多轮无明显进展的段落标记 `NO_PROGRESS_REWRITE_LOOP`、`TECHNICAL_PROTECTED_PLATEAU` 或 `EVIDENCE_LIMITED_PLATEAU`，不继续机械重写。

本版本仍然只做写作风险优化和报告反馈驱动修订，不承诺任何检测平台结果。

## v0.8.1 首轮红橙联合处理

`v0.8.1-red-orange-first-pass` 把橙色中风险从“后置平台期处理”提前到“首轮主处理区”。当用户一开始就提供原版论文和原版 AIGC 报告时，Skill 会同时处理红色和橙色风险片段，避免第一轮只把红色降成橙色。

新增能力：

- 新增 `FIRST_PASS_RED_ORANGE_ENGINE`：红色高风险和橙色中风险同时进入首轮任务表。
- 新增有限内部循环：每个红/橙段落先诊断、再改写、再自检；如果仍像红/橙，再用不同策略做一次有限重试。
- 新增 `CHARACTER_DELTA_GUARD`：默认整篇论文总字符变动不得超过 `±10%`，用户指定范围时以用户范围为准。
- 紫色段落只做低强度清理，黑色/白色/低风险段落默认冻结。
- 如果继续改写会破坏事实、引用、技术实体或超过字符范围，输出停止原因，而不是继续递归。

红橙联合处理的目标是启发式地把可安全处理的红/橙段落压到紫色或黑色水平，但不承诺任何检测平台一定给出对应颜色或百分比。

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

更多示例见 [QUICKSTART.md](QUICKSTART.md)。

## 支持模式

| 模式 | 用途 | 适用输入 |
|---|---|---|
| `AIGC_ONLY` | 只处理 AIGC 风险 | 论文段落、章节 |
| `AIGC_DEEP_REWRITE_ENGINE` | 深度处理高 AIGC 风险 | AIGC 味重、浅层改写无效的段落 |
| `FIRST_PASS_RED_ORANGE_ENGINE` | 首轮红橙联合处理 | 原版论文 + 原版 AIGC 报告 |
| `AIGC_PLATEAU_BREAKER` | 处理多轮 AIGC 下降变慢 | 原文、历史稿、多轮 AIGC 报告 |
| `ORANGE_ZONE_REWRITE_STRATEGY` | 突破橙色中风险平台期 | 中风险成片、枚举/模板结构保留的段落 |
| `DISCIPLINE_AIGC_BOTTLENECK_RULES` | 判断学科瓶颈 | 计算机、管理、商科等不同论文类型 |
| `SIMILARITY_ONLY` | 只处理查重相似风险 | 理论基础、综述、报告片段 |
| `DUAL_OPTIMIZATION` | 同时处理 AIGC 与相似风险 | 高风险段落、章节 |
| `NO_REPORT_FALLBACK_WORKFLOW` | 无报告保底双降 | 无检测报告的正文 |
| `TARGETED_MULTIPASS_ENGINE` | 目标驱动多轮闭环 | 原文、当前稿、历史稿、报告、目标阈值 |
| `AIGC_FOCUSED_LENGTH_CONTROLLED` | AIGC 专项控长修复 | 查重已够用但 AIGC 仍高、字数扩写过多 |
| `CHARACTER_DELTA_GUARD` | 控制全文字符变动 | 完整论文、多章节改写 |
| `LENGTH_BUDGET_CONTROLLER` | 全文字数预算控制 | 完整论文、多章节改写稿 |
| `SENTENCE_LEVEL_AIGC_LOCALIZER` | 句子级 AIGC 定位 | 高风险段落 |
| `BURSTINESS_RHYTHM_CONTROL` | 节奏和突发性控制 | 过度平滑、过度均匀段落 |
| `REPEATED_EXPRESSION_COMPRESSOR` | 重复 AI 腔压缩 | 全文重复表达扫描 |
| `HUMAN_EVIDENCE_REQUEST` | 作者证据补充清单 | 信息不足但 AIGC 风险高 |
| `CONSERVATIVE_AIGC_REPAIR` | 保守 AIGC 修复 | 信息不足且需要控字数 |
| `REPORT_FEEDBACK_LOOP` | 新报告反馈分析 | 多轮查重/AIGC 报告 |
| `AIGC_REGRESSION_GUARD` | AIGC 反升诊断 | 查重下降但 AIGC 上升的稿件 |
| `CONTENT_SUBSTANCE_INJECTION` | 真实内容增量 | 信息密度不足的段落 |
| `SIMILARITY_BELOW_10_STRATEGY` | 相似度目标专项策略 | 用户目标为相似度 <10% |
| `AIGC_BELOW_20_STRATEGY` | AIGC 目标专项策略 | 用户目标为 AIGC <20% |
| `PARAGRAPH_TYPE_STRATEGIES` | 段落类型分流 | 摘要、绪论、技术概述、测试、结论等 |
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
7. 平台期处理：如果多轮 AIGC 下降变慢，先判断红色、橙色、紫色风险带变化，冻结白色段落，再处理橙色平台期。
8. 首轮红橙处理：如果一开始就有原版 AIGC 报告，红色和橙色同时进入主处理区，并用 `±10%` 字符变动守卫约束全文。

## 推荐使用方式（经验参考，非结果承诺）

1. 先基于原版查重一次。
2. 针对检测报告，哪个高先降哪个。
3. 使用查重/AIGC 检测报告中风险更高的一项作为优先输入；双风险段落可以进入双优化流程。
4. 再查重一次，针对不满意的再降低。
5. 不同模型和不同论文的结果差异较大；如果某个模型在你的报告中导致 AIGC 上升，应回退到上一版并更换策略或模型。

## 实测
原版：
<img width="857" height="89" alt="截屏2026-05-14 12 06 40" src="https://github.com/user-attachments/assets/c00f01a5-b603-4d46-b843-9fa94e738324" />
两次降重后：
<img width="857" height="89" alt="截屏2026-05-14 12 06 48" src="https://github.com/user-attachments/assets/765538b5-778e-4bc9-802b-b933e55cbd27" />
mimo-v2.5-pro 示例：
<img width="857" height="89" alt="截屏2026-05-14 12 15 02" src="https://github.com/user-attachments/assets/f8806792-1fc5-4e99-87ad-4169e2d10689" />
以上截图仅是项目维护过程中的个案记录，不代表任何模型或检测平台的稳定结论。

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
