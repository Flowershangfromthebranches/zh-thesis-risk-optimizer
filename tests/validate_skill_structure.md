# Validate Skill Structure

Use this check before publishing or syncing the Skill.

## Required Outcome

- Every `prompts/*.md` path declared by `SKILL.md` exists.
- Every `references/*.md` path declared by `SKILL.md` exists.
- Every `workflow/*.md` path declared by `SKILL.md` exists.
- `QUICKSTART.md` recommends only the 10 slim-router entry modes.
- `README.md` recommends only the 10 slim-router entry modes.
- Retired historical modes are not recommended as public-document entry modes.
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
- `SIMILARITY_ONLY`
- `REPORT_AIGC_ONLY`
- `DUAL_OPTIMIZATION`
- `AIGC_DEEP_REWRITE_ENGINE`
- `TARGETED_MULTIPASS_ENGINE`
- `AIGC_FOCUSED_LENGTH_CONTROLLED`
- `REPORT_SIMILARITY_ONLY`
- `SECOND_PASS_REWRITE`
- `FULL_THESIS_PROJECT_MODE`
- `NO_REPORT_FALLBACK_WORKFLOW`

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
readme = (root / 'README.md').read_text(encoding='utf-8')

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
    'SIMILARITY_ONLY',
    'REPORT_AIGC_ONLY',
    'DUAL_OPTIMIZATION',
    'AIGC_DEEP_REWRITE_ENGINE',
    'TARGETED_MULTIPASS_ENGINE',
    'AIGC_FOCUSED_LENGTH_CONTROLLED',
    'REPORT_SIMILARITY_ONLY',
    'SECOND_PASS_REWRITE',
    'FULL_THESIS_PROJECT_MODE',
    'NO_REPORT_FALLBACK_WORKFLOW',
]

archived_prompt_files = [
    'prompts/mode_aigc_only.md',
    'prompts/mode_dual_optimization.md',
    'prompts/mode_report_driven_aigc.md',
    'prompts/mode_report_driven_similarity.md',
    'prompts/mode_second_pass_rewrite.md',
    'prompts/mode_targeted_multipass.md',
    'prompts/mode_aigc_focused_length_controlled.md',
    'prompts/mode_full_thesis_project.md',
    'prompts/mode_no_report_dual_fallback.md',
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
    if mode in readme:
        errors.append(f'README.md still recommends retired entry mode: {mode}')

for mode in expected_modes:
    if f'`{mode}`' not in readme:
        errors.append(f'README.md does not list entry mode: {mode}')

for rel in archived_prompt_files:
    path = root / rel
    if not path.exists():
        errors.append(f'Archived prompt file missing: {rel}')
        continue
    head = path.read_text(encoding='utf-8')[:200]
    if 'ARCHIVED_COMPATIBILITY_ONLY' not in head:
        errors.append(f'Archived prompt lacks compatibility header: {rel}')
    if 'Do not call directly. Route through `SKILL.md` Minimal Mode Router.' not in head:
        errors.append(f'Archived prompt lacks routing warning: {rel}')

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
