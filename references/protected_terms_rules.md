# Protected Terms Rules

Build a protected list before revision. When uncertain, preserve the item and mark it for human review.

## Always Protect

- Professional terms and standard names.
- Abbreviations and their first-use definitions.
- Mathematical formulas, variables, units, equation numbers, and notation.
- Code blocks, inline code, commands, paths, file names, and configuration keys.
- API names, class names, function names, parameters, and protocol names.
- Database names, table names, field names, indexes, enum values, and constants.
- Figure names, table names, captions, labels, and cross-references.
- Experimental values, device names, thresholds, datasets, and metrics.
- Laws, standards, policies, classic definitions, and required direct quotations.
- Detection report text supplied for diagnosis.
- Report metadata, report percentages, source titles, URLs, risk levels, and color-mark explanations supplied by the user.

## Protection Labels

Use protection labels during sentence-level diagnosis:

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

Protection labels override rewrite pressure. If a sentence has both risk labels and protection labels, lower the rewrite intensity or restrict editing to surrounding explanatory prose.

## Plain Text

- Preserve quoted terms and identifiers.
- Preserve numbers, units, and named methods.
- Do not normalize all terms if the thesis uses a deliberate naming convention.

## Word-Style Text

- Treat copied captions, table titles, and figure references as protected.
- Do not change numbered headings unless asked.
- Keep reference markers and footnote markers attached to the same claim.

## LaTeX

Do not modify LaTeX command names or keys:

- `\cite{}`, `\ref{}`, `\label{}`, `\autoref{}`, `\eqref{}`.
- `\begin{}` and `\end{}` environment names.
- Equation, align, gather, table, figure, algorithm, and listing environments.
- File paths in `\input{}`, `\include{}`, `\includegraphics{}`.
- Bibliography commands and keys.

Editable parts:

- Chinese prose outside commands and math environments.
- Explanatory text around equations, if it does not change variable meaning.

## Code and Data Identifiers

Do not rename:

- Function names.
- Variable names.
- JSON keys.
- SQL table names and field names.
- API endpoints.
- Configuration values.

If prose around code is unclear, revise explanation only.

## Safe No-Edit Escalation

If a protected item appears inside a risky sentence:

1. Keep the protected item unchanged.
2. Mark the reason.
3. Rewrite only non-protected prose around it.
4. If the protected item itself seems wrong, ask for human confirmation instead of editing.

## Report-Driven Protection

In report-driven mode, also protect:

- Report fragments quoted as evidence.
- Similarity-source names and source descriptions.
- Contribution rates and risk levels as report facts.
- Color mark meanings copied from the report.

Never alter these fields to make a task table look cleaner. If a report field is missing, mark it as missing instead of inventing it.

## Full-Thesis Protection

In full-thesis projects, maintain protected items at two levels:

- Global list in `THESIS_MASTER_OVERVIEW`.
- Chapter-specific list in each chapter task.

If a term, symbol, API, table, field, citation key, or experiment value appears in several chapters, use the global form consistently.

## Term Consistency Table

Use this table during long tasks:

| Term | First Form | Later Form | Protected? | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
