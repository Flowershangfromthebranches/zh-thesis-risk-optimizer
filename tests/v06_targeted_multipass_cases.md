# v0.6 Targeted Multipass Cases

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Case 1: Similarity Down But AIGC Up

Input trend:

- Similarity improves.
- AIGC worsens.

Expected status:

- `PARTIAL_SUCCESS_SIMILARITY_ONLY_AIGC_FAILED`
- Enter `AIGC_REGRESSION_GUARD`.

## Case 2: v0.5 Formalization Regression

Input contains:

- 持续演进
- 深度嵌入
- 实施自动化识别

Expected:

- `AIGC_REGRESSION_FAIL` when three or more regression categories are present.
- Do not accept as final text.
- Enter Evidence-Based Reconstruction.

## Case 3: Target Below 10/20

Input target:

- Similarity <10%.
- AIGC <20%.

Expected:

- Enter `TARGETED_MULTIPASS_ENGINE`.
- Do not run a single-pass full-text rewrite.
- State that targets are not guaranteed results.

## Case 4: Evidence Missing

Input:

- Paragraph has generic claims but no module, parameter, test, or result evidence.

Expected:

- Output author supplementation list.
- Do not fabricate details.

## Case 5: Protected Data

Input contains:

- Code.
- URL.
- Payload.
- Test result.

Expected:

- Preserve exact technical data.
- Rewrite only surrounding explanatory prose when safe.
