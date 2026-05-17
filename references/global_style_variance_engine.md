# Global Style Variance Engine

## Purpose

`GLOBAL_STYLE_VARIANCE_ENGINE` checks why a thesis still feels AI-like after red/orange repair. It works at the document level and produces a local adjustment plan. It must not perform full-text rewriting by itself.

## Detection Metrics

1. Highly similar section openings.
2. Over-uniform paragraph length.
3. Over-stable sentence length distribution.
4. Repeated connectors.
5. High-frequency `本研究`, `本文`, `通过`, `同时`, `因此`, `首先`, `其次`, `最后`.
6. Abstract still follows fixed object-method-problem-countermeasure-significance structure.
7. Conclusion only repeats the thesis.
8. Theory section remains encyclopedia-style.
9. Countermeasure section is overly parallel.
10. Lack of local author judgment.

## Handling

- Do not directly rewrite the whole thesis.
- Output `global_variance_plan`.
- Call `PURPLE_BAND_REBALANCER`, `SECTION_STYLE_PROFILES`, and `COLOR_BAND_ROUTER` to implement local adjustment.
- Preserve DOCX format.
- Do not change facts, data, citations, terminology, formulas, code, or identifiers.

## Output

```yaml
global_style_variance:
  style_uniformity_score: <0-100>
  repeated_transition_terms: <list>
  uniform_section_openings: <list>
  sentence_length_distribution_issue: yes | no
  paragraph_length_distribution_issue: yes | no
  global_variance_plan: <plan>
  sections_needing_variance: <list>
```
