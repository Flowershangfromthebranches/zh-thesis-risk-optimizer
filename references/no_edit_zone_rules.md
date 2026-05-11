# No-Edit Zone Rules

No-edit zones are areas where automatic rewriting can damage academic integrity, technical correctness, or legal/source fidelity.

## Default No-Edit Zones

The following content should not be automatically rewritten:

1. 数学公式。
2. 代码块。
3. API 路径。
4. 数据库表名和字段名。
5. 实验数据。
6. 图表编号。
7. 参考文献条目。
8. LaTeX 命令。
9. 法规、标准、政策原文。
10. 经典定义。
11. 必须逐字引用的材料。
12. 检测报告原文。
13. 用户明确要求保留的内容。

## Required Output for No-Edit Zones

For each no-edit zone, output:

- 保留原文。
- 标注原因。
- 如需修改，要求人工确认。
- 只允许修改其前后解释性文字。

## No-Edit Zone Table

```markdown
| 位置 | 内容类型 | 保护标签 | 处理方式 | 原因 |
| --- | --- | --- | --- | --- |
| P4-S2 | 公式 | 保护-公式 | 保留原文 | 改写会改变变量关系 |
| P6-S1 | API 路径 | 保护-接口路径 | 只改解释文字 | 路径是系统接口标识 |
```

## Allowed Surrounding Edits

You may revise explanatory text around protected material when:

- The protected item itself remains unchanged.
- Citation boundary remains clear.
- Data and conclusions are not changed.
- The revision improves clarity without changing meaning.

## Human Confirmation Required

Ask for confirmation before changing:

- Legal or standard wording.
- Classic definitions that must match an authoritative source.
- Experimental values.
- Reference entries.
- User-marked protected material.
- Any sentence where the rewrite may change the conclusion.
