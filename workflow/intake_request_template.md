# Intake Request Template

Copy this template when starting any `zh-thesis-risk-optimizer` task. Replace the example values with your own materials.

All sections should be returned to the model before processing starts. Required fields must be filled. Strongly recommended and optional fields may be filled, or explicitly marked as `无`, `跳过`, or `请自动判断`.

Important: `current_similarity_rate` and `current_aigc_rate` are required before rewriting. If either is unknown, the Skill may read files or parse reports to complete intake, but it must not enter the rewrite chain.

## Required

```text
【任务目标】
只降 AIGC / 只降查重 / 双降 / 只诊断不改写 / 报告映射 / 文件副本处理 / 全文项目管理 / 请自动判断

【当前查重率 current_similarity_rate】
例如：11% / 未检测

【当前 AIGC 疑似率 current_aigc_rate】
例如：68.6% / 未检测

【目标查重率 target_similarity_rate】
例如：15% / 10% / 请自动判断

【目标 AIGC 疑似率 target_aigc_rate】
例如：30% / 20% / 请自动判断

【任务类型 task_type】
aigc_only / similarity_only / dual_optimization

【论文输入】
粘贴正文 / 单章文本 / 原文 DOCX 路径 / Markdown 或 TXT 路径 / LaTeX 路径
示例：/path/to/original.docx

【处理范围】
单段 / 单章 / 全文 / 只处理报告红橙片段 / 只输出任务表

【输出形式】
诊断表 / 修改后文本 / 报告驱动任务表 / 创建副本并回写 / 作者补充证据清单 / 全文项目总览

【字数约束】
默认全文总字符数浮动 ±10%，或写明你的范围

【保护项】
默认保护：引用、公式、代码、接口、路径、表名、字段名、参数、实验数据、参考文献条目、学校声明。
请补充其他必须保留内容：
```

## Strongly Recommended

```text
【AIGC 报告】
无 / AIGC 报告 DOCX 路径 / PDF 复制文本 / 截图 OCR 文本 / 手动复制红橙片段
示例：/path/to/aigc_report.docx

【是否有 AIGC 颜色报告 has_aigc_color_report】
true / false

【红段数量/比例 current_red_count/current_red_ratio】
例如：红段 1 / 红色 2% / 有报告请自动解析

【橙段数量/比例 current_orange_count/current_orange_ratio】
例如：橙段 17 / 橙色 18% / 有报告请自动解析

【紫段数量/比例 current_purple_count/current_purple_ratio】
例如：紫段较多 / 紫色 20% / 有报告请自动解析

【黑段数量/比例 current_black_count/current_black_ratio】
例如：黑色 60% / 有报告请自动解析

【查重报告】
无 / 查重报告 DOCX 路径 / HTML 报告 / PDF 复制文本 / 手动复制标红片段

【是否有查重报告 has_similarity_report】
true / false

【报告颜色规则】
默认：红色 >70%，橙色 60%-70%，紫色 50%-60%，黑色 <50%
如果报告规则不同，请写明：

【论文专业和题目】
示例：人力资源管理，《数智化时代A电商公司招聘管理优化研究》

【当前状态】
原文未改 / 第一次改写后 / 第二次改写后 / AIGC 反升 / 查重已够用但 AIGC 仍高

【阶段 stage】
original / first_pass / second_pass / current_report_pass / first_pass_failure

【是否要求保持 DOCX 原格式 preserve_docx_format_required】
true / false
```

If a strongly recommended item is unavailable, write `无`, `跳过`, or `请自动判断`. Do not leave it implicit.

## Optional

```text
【历史版本】
原文路径：
上一版改写稿路径：
历史 AIGC 报告路径：
历史查重报告路径：

【用户目标】
示例：希望向 AIGC <20%、查重 <10% 靠近。
说明：这是优化目标，不是检测结果承诺。

【可用证据】
计算机论文：模块名、函数名、接口、参数、测试环境、测试次数、结果数据。
管理/社科论文：公司背景、部门/岗位、问卷样本、百分比、访谈摘要、流程节点、制度、指标。
其他：

【特殊要求】
例如：不要改摘要 / 只改第五章 / 保留学校模板 / 不改变图表编号 / 不扩写。
```

If an optional item is unavailable, write `无`, `跳过`, or `请自动判断`. Do not leave it implicit.

## Do Not Provide Or Request

- 伪造数据、实验、访谈、案例、日志或截图。
- 伪造引用、参考文献、相似源、检测百分比或报告结论。
- 删除必要引用。
- 把他人观点改成无来源原创观点。
- 让模型破解、模拟、逆向或伪造任何检测系统。

## Minimal Example

```text
【任务目标】
只降 AIGC

【当前查重率 current_similarity_rate】
11%

【当前 AIGC 疑似率 current_aigc_rate】
68.6%

【目标查重率 target_similarity_rate】
15%

【目标 AIGC 疑似率 target_aigc_rate】
30%

【任务类型 task_type】
aigc_only

【论文输入】
原文 DOCX：/Users/leaf/Desktop/论文/原版.docx

【处理范围】
全文，只处理报告红橙片段

【输出形式】
创建副本并回写，同时输出诊断表

【字数约束】
全文 ±10%

【保护项】
引用、问卷数据、图表编号、参考文献、学校声明

【AIGC 报告】
/Users/leaf/Desktop/论文/原版查AIGC.docx

【是否有 AIGC 颜色报告 has_aigc_color_report】
true

【红段数量/比例 current_red_count/current_red_ratio】
请自动解析

【橙段数量/比例 current_orange_count/current_orange_ratio】
请自动解析

【紫段数量/比例 current_purple_count/current_purple_ratio】
请自动解析

【黑段数量/比例 current_black_count/current_black_ratio】
请自动解析

【查重报告】
无

【是否有查重报告 has_similarity_report】
false

【报告颜色规则】
红色 >70%，橙色 60%-70%，紫色 50%-60%，黑色 <50%

【论文专业和题目】
人力资源管理，《数智化时代A电商公司招聘管理优化研究》

【当前状态】
原文未改

【阶段 stage】
original

【是否要求保持 DOCX 原格式 preserve_docx_format_required】
true

【历史版本】
无

【用户目标】
请自动判断

【可用证据】
无

【特殊要求】
跳过
```
