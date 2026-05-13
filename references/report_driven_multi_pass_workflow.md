# Report Driven Multi-Pass Workflow

## Purpose

`REPORT_DRIVEN_MULTI_PASS_WORKFLOW` strengthens report-driven dual optimization by adding mandatory AIGC reshaping after similarity repair.

## Round 0: Report Mapping

- Extract report fragments.
- Map fragments to source text.
- Mark mapping confidence.
- Mark protected zones.

## Round 1: Similarity First

- Process high-contribution repeated fragments.
- Preserve citations.
- Do not modify protected content.

## Round 2: AIGC Deep Rewrite

For paragraphs revised in Round 1:

- Audit AI-like rhythm.
- Delete universal summaries.
- Rebuild sentence relationships.
- Add concrete objects and boundaries from the source.
- Avoid over-smooth prose.

## Round 3: Safety Review

Check:

- Terms.
- Citations.
- Data.
- Formulas.
- Conclusions.
- Whether new unsupported facts were introduced.

## Round 4: Recheck Advice

- Recommend rerunning the user's chosen check.
- Use the new report for local follow-up.
- Do not continue full-thesis rewriting.

## Relation To SKILL.md

Used by report-driven dual optimization and iterative revision.
