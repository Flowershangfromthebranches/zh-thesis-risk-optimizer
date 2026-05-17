# Risk Labels

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Use a unified label system for sentence-level and paragraph-level diagnosis.

## AIGC Labels

- `AI-模板化起笔`
- `AI-机械三段式`
- `AI-四字套话`
- `AI-泛化结尾`
- `AI-模糊归因`
- `AI-绝对化断言`
- `AI-连接词过密`
- `AI-句长过均匀`
- `AI-缺少具体对象`
- `AI-宣传式表达`
- `AI-过度对称`
- `AI-万能意义句`
- `AI-过度干净`
- `AI-段落节奏单一`

## Similarity Labels

- `查重-定义重复`
- `查重-教材式表述`
- `查重-相似源过近`
- `查重-引用转述不足`
- `查重-概念解释冗余`
- `查重-背景套话`
- `查重-常见结论表达`
- `查重-综述堆叠`
- `查重-来源边界不清`
- `查重-通用方法描述重复`

## Protection Labels

- `保护-必要引用`
- `保护-公式`
- `保护-代码`
- `保护-接口路径`
- `保护-数据库表名`
- `保护-字段名`
- `保护-实验参数`
- `保护-法规标准原文`
- `保护-经典定义`
- `保护-参考文献条目`
- `保护-图表编号`
- `保护-模型名称`
- `保护-算法名称`
- `保护-LaTeX命令`

## Report Labels

- `报告-查重片段`
- `报告-AIGC片段`
- `报告-相似源说明`
- `报告-贡献率`
- `报告-风险等级`
- `映射-HIGH`
- `映射-MEDIUM`
- `映射-LOW`
- `映射-UNMAPPED`

## Label Priority

1. Protection labels.
2. Mapping-confidence labels.
3. Citation-boundary labels.
4. Similarity labels.
5. AIGC labels.

If protection labels are present, lower rewrite intensity and explain why.

## Label Output Rules

- Use labels in brackets: `[AI-模板化起笔][查重-背景套话]`.
- A sentence can have multiple labels.
- Do not create platform-specific labels.
- Do not use labels as accusations; describe them as writing-risk signals.
- If no significant risk is found, write `[风险低]`.

## Recommended Actions by Label

| Label Type | Typical Action |
| --- | --- |
| AI-only labels | L1-L2 wording and rhythm adjustment |
| Similarity-only labels | L1-L3 reframing with citation preservation |
| AI + similarity labels | DUAL_OPTIMIZATION, usually L2 |
| Protection labels | Preserve, lightly explain, or ask for confirmation |
| Citation-boundary labels | Keep or request citation before rewriting |
| Mapping LOW or UNMAPPED | Do not rewrite before human confirmation |
