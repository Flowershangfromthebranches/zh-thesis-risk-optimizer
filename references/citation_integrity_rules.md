# Citation Integrity Rules

Citation integrity is mandatory in every mode.

## Protected Citation Forms

Do not modify:

- Numeric references such as `[1]`, `[2-4]`.
- Author-year citations such as `(Wang, 2024)` or `王某（2024）`.
- Footnote markers.
- LaTeX commands such as `\cite{}`, `\parencite{}`, `\textcite{}`.
- Bibliography keys, DOI strings, URLs, report numbers, and standard numbers.

## Source Boundary Rules

- If a claim comes from a cited source, the rewrite must keep that source boundary.
- If several cited claims are compared, do not merge them into one uncited conclusion.
- If the author is making their own conclusion, make the evidence basis visible.
- If the source is missing, request or mark a citation rather than inventing one.

## Safe Rewriting Patterns

Source-dependent sentence:

```text
已有研究指出，城市热岛效应会影响居民健康[3]。
```

Safe revision:

```text
文献[3]将城市热岛效应与居民健康风险联系起来，本文后续讨论的重点则放在社区尺度的温度暴露差异。
```

Unsafe revision:

```text
城市热岛效应会影响居民健康，本文对此进行了系统验证。
```

The unsafe version removes source boundary and adds unsupported verification.

## Missing Citation Handling

When a statement appears source-dependent but has no citation:

```text
建议补充来源：该句涉及外部研究结论，当前文本未给出文献依据。
```

Do not fabricate author names, years, reference numbers, or DOI.

## Final Check

Before output, confirm:

- Necessary citations remain.
- Citation markers still point to the same claims.
- No cited claim became an uncited original claim.
- No new unsupported source was introduced.
