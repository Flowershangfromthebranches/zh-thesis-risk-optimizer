# Validate Skill Structure

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Use this check before publishing or syncing the Skill.

## Required Outcome

- Every `prompts/*.md` path declared by `SKILL.md` exists.
- Every `references/*.md` path declared by `SKILL.md` exists.
- Every `workflow/*.md` path declared by `SKILL.md` exists.
- `QUICKSTART.md` recommends only the 11 slim-router entry modes (including internal mandatory gate).
- `README.md` recommends only the 11 slim-router entry modes (including internal mandatory gate).
- Retired historical modes are not recommended as public-document entry modes.
- `SKILL.md` has the expected legal YAML frontmatter.
- `prompts/mode_intake_wizard.md` does not route no-report work to a retired entry mode.
- Path references inside `tests/*.md` resolve to real files.
- Failure on any missing path blocks release.
- `SKILL.md` Minimal Mode Router includes `FIRST_PASS_EFFECTIVENESS_GATE`.
- The mandatory first-pass chain in `SKILL.md` places `FIRST_PASS_EFFECTIVENESS_GATE` between `AIGC_REGRESSION_GUARD` and `FINAL_ACCEPTANCE_AUDIT`.
- `references/first_pass_effectiveness_gate.md` exists.
- `references/final_acceptance_audit.md` contains `FIRST_PASS_EFFECTIVENESS_GATE`.
- `references/first_pass_red_orange_engine.md` contains a rule equivalent to "red to orange is not success / 红转橙不算成功".

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
- `FIRST_PASS_EFFECTIVENESS_GATE`
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
intake_prompt = (root / 'prompts/mode_intake_wizard.md').read_text(encoding='utf-8')

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
    'FIRST_PASS_EFFECTIVENESS_GATE',
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

expected_frontmatter = """---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with forced intake, DOCX color-report extraction, red-orange coverage, social-science evidence reconstruction, first-pass effectiveness gate, and final acceptance audit.
license: MIT
---"""

if not skill.startswith(expected_frontmatter + "\n\n# zh-thesis-risk-optimizer"):
    errors.append('SKILL.md frontmatter is not the expected legal YAML block')

declared_paths = sorted(set(re.findall(
    r'((?:prompts|references|workflow)/[A-Za-z0-9_./-]+\.md)',
    skill,
)))

for rel in declared_paths:
    if not (root / rel).exists():
        errors.append(f'SKILL.md declares missing path: {rel}')

router_modes = re.findall(r'^\| `([^`]+)` \|', skill, flags=re.MULTILINE)
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

if 'Completed intake template without report | `NO_REPORT_FALLBACK_WORKFLOW`' in intake_prompt:
    errors.append('mode_intake_wizard.md still routes no-report intake to retired NO_REPORT_FALLBACK_WORKFLOW')

# Check QUICKSTART first-pass chain contains FIRST_PASS_EFFECTIVENESS_GATE
first_pass_chain_section = quickstart[quickstart.index('First-Pass AIGC'):quickstart.index('Current-Report')]
if 'FIRST_PASS_EFFECTIVENESS_GATE' not in first_pass_chain_section:
    errors.append('QUICKSTART.md first-pass Required chain does not contain FIRST_PASS_EFFECTIVENESS_GATE')

# Check mode_first_pass_red_orange.md contains red-to-orange not success rule
fpro_prompt = (root / 'prompts/mode_first_pass_red_orange.md').read_text(encoding='utf-8')
fpro_ref = (root / 'references/first_pass_red_orange_engine.md').read_text(encoding='utf-8')
combined_fpro = fpro_prompt + fpro_ref
if 'Red→orange' not in combined_fpro and 'red to orange' not in combined_fpro.lower() and '红转橙' not in combined_fpro and 'UNPASSED' not in combined_fpro:
    errors.append('prompts/mode_first_pass_red_orange.md or references/first_pass_red_orange_engine.md missing red-to-orange not success rule')

# Check first_pass_effectiveness_gate.md contains core principle
fpeg = (root / 'references/first_pass_effectiveness_gate.md').read_text(encoding='utf-8')
if 'Red-to-orange migration is NOT success' not in fpeg:
    errors.append('references/first_pass_effectiveness_gate.md missing core principle: Red-to-orange migration is NOT success')

# Check final_acceptance_audit.md has material_gap_table requirement
faa = (root / 'references/final_acceptance_audit.md').read_text(encoding='utf-8')
if 'material_gap_table' not in faa:
    errors.append('references/final_acceptance_audit.md missing material_gap_table requirement')

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
        r'((?:prompts|references|workflow|tests|examples)/[A-Za-z0-9_./-]+\.md)',
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
- [ ] `FIRST_PASS_EFFECTIVENESS_GATE` is between `AIGC_REGRESSION_GUARD` and `FINAL_ACCEPTANCE_AUDIT` in the mandatory first-pass chain.
- [ ] `references/first_pass_effectiveness_gate.md` contains the core principle that red-to-orange migration is NOT success.
- [ ] `references/final_acceptance_audit.md` outputs `material_gap_table` when evidence is missing.
- [ ] `references/social_science_template_bottleneck.md` contains anti-fabrication enforcement for specific data types.
- [ ] `tests/first_pass_failure_color_migration_case.md` exists and uses the real failure case data.
