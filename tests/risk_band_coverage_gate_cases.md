# Risk Band Coverage Gate Cases

## Case 1: First Pass Only Handles 34 Of 90 Risk Targets

Input:

- red targets: 50
- orange targets: 36
- purple targets: 4
- actually rewritten: 34
- appendix frozen: 16
- no complete handling record for remaining body red/orange/purple targets

Expected:

- `risk_band_coverage_gate_result = failed`
- `final_delivery_status = RISK_BAND_COVERAGE_FAILURE`
- failure reason includes `red/orange/purple coverage insufficient`
- output includes skipped red/orange/purple target lists
- output includes `next_batch_plan`
- task must not be `COMPLETED`

## Case 2: Full Red/Orange Coverage And Purple Light Rebalance

Input:

- red targets: 50, all handled or valid-frozen
- orange targets: 36, all handled or valid-frozen
- purple targets: 4, all present in task table and assigned `purple_light_rebalance`
- invalid skips: none

Expected:

- `red_coverage_rate = 100%`
- `orange_coverage_rate = 100%`
- `purple_coverage_rate = 100%`
- `risk_band_coverage_gate_result = passed`

## Case 3: Appendix Freeze Does Not Count As Body Rewrite

Input:

- appendix targets: 16
- freeze reason: appendix
- body red/orange targets remain unhandled

Expected:

- appendix freeze reason is valid
- appendix targets are counted as valid frozen targets
- appendix freeze does not increase body rewrite coverage
- body skipped targets remain in `skipped_red_targets` or `skipped_orange_targets`
- if body red/orange coverage is insufficient, gate fails
