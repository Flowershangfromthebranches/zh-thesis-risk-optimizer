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

## Term Consistency Table

Use this table during long tasks:

| Term | First Form | Later Form | Protected? | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
