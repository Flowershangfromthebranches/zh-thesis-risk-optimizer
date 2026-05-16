# Validate Skill Structure

Use this check before publishing or syncing the Skill.

## Required Outcome

- Every `prompts/*.md` path declared by `SKILL.md` exists.
- Every `references/*.md` path declared by `SKILL.md` exists.
- Every `workflow/*.md` path declared by `SKILL.md` exists.
- `QUICKSTART.md` recommends only the 10 slim-router entry modes.
- Retired historical modes are not recommended as QUICKSTART entry modes.
- Path references inside `tests/*.md` resolve to real files.
- Failure on any missing path blocks release.

## Expected Entry Modes

- `INTAKE_WIZARD_PRECHECK`
- `FILE_INPUT_COPY_WORKFLOW`
- `DOCX_COLOR_REPORT_EXTRACTION`
- `THREE_MODE_COLOR_BAND_WORKFLOW`
- `FIRST_PASS_RED_ORANGE_ENGINE`
- `CURRENT_REPORT_RED_ORANGE_ENGINE`
- `AIGC_PLATEAU_BREAKER`
- `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`
- `AIGC_REGRESSION_GUARD`
- `FINAL_ACCEPTANCE_AUDIT`

## Retired Modes Must Not Be QUICKSTART Entries

These names may appear in historical tests or references, but `QUICKSTART.md` must not recommend them as user-facing entry modes:

- `AIGC_ONLY`
- `REPORT_AIGC_ONLY`
- `DUAL_OPTIMIZATION`
- `AIGC_DEEP_REWRITE_ENGINE`
- `TARGETED_MULTIPASS_ENGINE`
- `AIGC_FOCUSED_LENGTH_CONTROLLED`

## Executable Check

Run from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import re
import sys

root = Path('.')
skill = (root / 'SKILL.md').read_text(encoding='utf-8')
quickstart = (root / 'QUICKSTART.md').read_text(encoding='utf-8')

expected_modes = [
    'INTAKE_WIZARD_PRECHECK',
    'FILE_INPUT_COPY_WORKFLOW',
    'DOCX_COLOR_REPORT_EXTRACTION',
    'THREE_MODE_COLOR_BAND_WORKFLOW',
    'FIRST_PASS_RED_ORANGE_ENGINE',
    'CURRENT_REPORT_RED_ORANGE_ENGINE',
    'AIGC_PLATEAU_BREAKER',
    'SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK',
    'AIGC_REGRESSION_GUARD',
    'FINAL_ACCEPTANCE_AUDIT',
]

retired_quickstart_entries = [
    'AIGC_ONLY',
    'REPORT_AIGC_ONLY',
    'DUAL_OPTIMIZATION',
    'AIGC_DEEP_REWRITE_ENGINE',
    'TARGETED_MULTIPASS_ENGINE',
    'AIGC_FOCUSED_LENGTH_CONTROLLED',
]

errors = []

declared_paths = sorted(set(re.findall(
    r'((?:prompts|references|workflow)/[A-Za-z0-9_./-]+\\.md)',
    skill,
)))

for rel in declared_paths:
    if not (root / rel).exists():
        errors.append(f'SKILL.md declares missing path: {rel}')

router_modes = re.findall(r'^\\| `([^`]+)` \\|', skill, flags=re.MULTILINE)
if router_modes != expected_modes:
    errors.append(
        'Minimal Mode Router mismatch: '
        + ', '.join(router_modes)
    )

for mode in expected_modes:
    if f'`{mode}`' not in quickstart:
        errors.append(f'QUICKSTART.md does not list entry mode: {mode}')

for mode in retired_quickstart_entries:
    if mode in quickstart:
        errors.append(f'QUICKSTART.md still recommends retired entry mode: {mode}')

test_paths = []
for test_file in sorted((root / 'tests').glob('*.md')):
    text = test_file.read_text(encoding='utf-8')
    for rel in re.findall(
        r'((?:prompts|references|workflow|tests|examples)/[A-Za-z0-9_./-]+\\.md)',
        text,
    ):
        test_paths.append((test_file, rel))

for test_file, rel in test_paths:
    if not (root / rel).exists():
        errors.append(f'{test_file} references missing path: {rel}')

if errors:
    print('FAIL')
    for error in errors:
        print('-', error)
    sys.exit(1)

print('PASS')
print(f'SKILL declared paths: {len(declared_paths)}')
print(f'Test path references: {len(test_paths)}')
print(f'Entry modes: {len(router_modes)}')
PY
```

## Manual Checks

- [ ] `SKILL.md` has legal YAML frontmatter.
- [ ] `SKILL.md` stays slim and does not reintroduce a long reference index.
- [ ] Historical mode files may remain for archive/compatibility, but they are not routed as entry modes.
- [ ] `skill_slimming_rules.md` remains a maintenance rule only.
- [ ] Missing author evidence routes to `workflow/author_evidence_pack_template.md`.
