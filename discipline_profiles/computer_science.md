# Discipline Profile: Computer Science

## discipline_scope

计算机科学、软件工程、信息管理、网络工程、数据科学、人工智能相关论文。

## typical_aigc_patterns

需求分析模板化、系统功能描述模板化、模块设计重复、测试章节“测试结果表明”套话、总结展望 AI 腔。

## protected_elements

代码、接口名、表名、字段名、函数名、模块名、数据库结构、技术术语、参数、路径、图表编号、测试数据。

## allowed_rewrite_moves

重写需求分析、系统概述、测试分析、总结展望中的模板句；保持技术文档风格；轻微句式变化。

## forbidden_rewrite_moves

不得把“本模块负责……”改成“这个模块主要就是……”。不得人化代码、表结构、字段名、函数名。不得降低技术准确性。

## max_humanization_by_section

| section | max_level |
|---|---:|
| 摘要 | 3 |
| 需求分析 | 3 |
| 系统设计 | 2 |
| 系统实现 | 2 |
| 测试分析 | 3 |
| 结论 | 3 |

## color_band_strategy

红橙只处理模板句和解释性文字；紫色只调节连接和句式；黑色技术实体冻结。

## citation_integrity_rules

保留技术来源、框架说明和引用边界。

## format_protection_rules

保护代码块、路径、接口、数据库结构和图表编号。
