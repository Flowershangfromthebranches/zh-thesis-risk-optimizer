# Discipline Profile: Engineering

## discipline_scope

机械、土木、电气、自动化、材料、环境、化工等。

## typical_aigc_patterns

实验结论模板、设计说明模板、“结果表明、满足要求、具有可行性”重复、讨论部分机械化。

## protected_elements

公式、参数、单位、图表、实验步骤、测试数据、工艺流程、材料名称。

## allowed_rewrite_moves

讨论、结果解释、结论部分轻度去模板；用已有结果说明边界。

## forbidden_rewrite_moves

强人化、口语化、改变实验方法、改变参数或数据含义。

## max_humanization_by_section

| section | max_level |
|---|---:|
| 实验方法 | 1 |
| 参数/公式 | 0 |
| 结果讨论 | 2.5 |
| 结论 | 2.5 |

## color_band_strategy

红橙只处理解释性文字；紫色仅过渡句轻调；黑色技术数据冻结。

## citation_integrity_rules

保留标准、文献和数据来源。

## format_protection_rules

保护单位、图表、公式、参数和工艺流程。
