# v0.9.5 Slim Forced Chain Cases

Use this checklist to verify that the Skill behaves as a forced execution chain instead of a broad rule library.

## Case 1: Original HR Thesis First Pass

Input:

```text
original_thesis: /path/original.docx
original_aigc_color_report: /path/original_aigc.docx
mode: only_reduce_aigc
color_rule: red/orange/purple/black
scope: red_and_orange_together
character_control: ±10%
major: human_resource_management
```

Expected mandatory chain:

- `FILE_INPUT_COPY_WORKFLOW`
- `DOCX_COLOR_REPORT_EXTRACTION`
- `THREE_MODE_COLOR_BAND_WORKFLOW`
- `FIRST_PASS_RED_ORANGE_ENGINE`
- `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`
- `AIGC_REGRESSION_GUARD`
- `FINAL_ACCEPTANCE_AUDIT`

Any missing step means not complete.

## Case 2: First-Pass Red-Orange Action Types

Input:

```text
red_orange_paragraphs: P1, P2, P3
P1_action: synonym_replacement
P2_action: evidence_reconstruction
P3_action: none
```

Expected:

- P1 fails because synonym replacement is not one of A/B/C/D.
- P2 passes action-type requirement if evidence is real.
- P3 is unprocessed.
- Completion forbidden.

## Case 3: Evidence Missing

Input:

```text
major: human_resource_management
paragraph: 对策段
needed_evidence: recruitment process, owner, indicator, review cycle
source_evidence: missing
```

Expected:

- Use `D_AUTHOR_MATERIAL_REQUEST`.
- Show or reference `workflow/author_evidence_pack_template.md`.
- Do not fabricate company process, questionnaire, interview, owner, metric, or review cycle.
- Do not mark the paragraph complete as rewritten.

## Case 4: Original Test Barely Changes AIGC

Input:

```text
user_report: 用原版测试后 AIGC 几乎不变
```

Expected:

- Mark `FIRST_PASS_FAILURE`, not plateau.
- Check DOCX color extraction.
- Check red/orange coverage.
- Check synonym-only rewrite.
- Check social-science bottleneck activation.
- Check author evidence pack request.
- Output failure-cause table and next repair plan.

## Case 5: SKILL.md Slimness

Expected:

- `SKILL.md` contains no long supporting-reference list.
- `SKILL.md` contains no long alias list.
- Entry modes are the 10 hard-chain modes.
- Deprecated modes such as `AIGC_ONLY`, `REPORT_AIGC_ONLY`, and `SECOND_PASS_REWRITE_REQUIREMENT` are not entry modes.

## Case 6: Final Acceptance Audit

Input:

```text
docx_color_read: yes
red_total: 10
red_processed: 10
orange_total: 25
orange_processed: 24
```

Expected:

- `FINAL_ACCEPTANCE_AUDIT` fails completion.
- Unprocessed orange count is 1.
- Output unprocessed paragraph list.
- Do not mark task as complete.
