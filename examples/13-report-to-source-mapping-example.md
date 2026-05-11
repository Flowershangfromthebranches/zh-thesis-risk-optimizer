# Example 13: Report-to-Source Mapping

## Mapping Examples

| 类型 | 报告片段 | 原文情况 | 映射置信度 | 处理 |
|---|---|---|---|---|
| 精确匹配 | 数据预处理包括缺失值处理和异常值剔除 | 原文完全一致 | HIGH | 可进入风险判断 |
| 规范化匹配 | 数据预处理包括缺失值处理、异常值剔除 | 原文标点略不同 | MEDIUM | 说明标点差异后处理 |
| 关键词匹配 | 缺失值、异常值、预处理 | 只能推断在方法章节 P5 | LOW | 不直接改写，需人工确认 |
| 无法映射 | 该方法提升了系统性能 | 原文多处无对应上下文 | UNMAPPED | 请求用户提供原文上下文 |

## Notes

- LOW does not permit direct rewriting.
- UNMAPPED must not be forced into a source paragraph.
- Multiple matches must be listed together.
