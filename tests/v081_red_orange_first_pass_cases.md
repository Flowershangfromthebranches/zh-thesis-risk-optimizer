# v0.8.1 Red-Orange First-Pass Cases

## Case 1: Original Report With Red And Orange

Input:

```yaml
provided: original_thesis + original_aigc_report
bands: red, orange, purple, black
```

Expected:

- Enter `FIRST_PASS_RED_ORANGE_ENGINE`.
- Red and orange both enter the primary task table.
- Purple is local cleanup only.
- Black and gray text is frozen.

## Case 2: Orange Is Not Deferred

Input:

```yaml
red_count: high
orange_count: high
first_pass: true
```

Expected:

- Do not wait for `AIGC_PLATEAU_BREAKER`.
- Use red-orange joint processing in the first pass.

## Case 3: Internal Loop Has Exit Conditions

Input:

```yaml
paragraph_band: orange
pass_1_self_audit: still_orange_like
```

Expected:

- Run one limited retry with a different repair move.
- Stop after `max_internal_passes` if no progress.
- Mark `NO_PROGRESS_INTERNAL_LOOP` or evidence/protection reason.

## Case 4: Character Delta Guard

Input:

```yaml
original_chars: 30000
revised_chars: 33500
allowed_total_delta_ratio: 10%
```

Expected:

- `CHARACTER_DELTA_FAIL` because 33500 is above 33000.
- Enter compression pass before completion.

## Case 5: Character Delta Within Range

Input:

```yaml
original_chars: 30000
revised_chars: 32600
allowed_total_delta_ratio: 10%
```

Expected:

- Character delta is acceptable.
- Continue integrity and report-band self-audit.

## Case 6: Protected Technical Content

Input contains:

- URL.
- Payload.
- API path.
- code block.
- test result.

Expected:

- Protected tokens are preserved exactly.
- Only surrounding explanation is revised.
