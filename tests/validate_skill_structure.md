# Validate Skill Structure

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

Use this check before publishing or syncing the Skill.

## Required Outcome

- Every `prompts/*.md` path declared by `SKILL.md` exists.
- Every `references/*.md` path declared by `SKILL.md` exists.
- Every `workflow/*.md` path declared by `SKILL.md` exists.
- `QUICKSTART.md` recommends only the 11 slim-router entry modes (including internal mandatory gate).
- `README.md` recommends only the 11 slim-router entry modes (including internal mandatory gate).
- `QUICKSTART.md` recommends only the slim-router entry modes and internal engines.
- `README.md` recommends only the slim-router entry modes and internal engines.
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

- `SKILL.md` Minimal Mode Router includes `CONTROLLED_HUMANIZATION_ENGINE`.
- `SKILL.md` Minimal Mode Router includes `OOXML_DOCX_PATCH_WORKFLOW`.
- The mandatory first-pass chain in `SKILL.md` places `FIRST_PASS_EFFECTIVENESS_GATE` between `AIGC_REGRESSION_GUARD` and `FINAL_ACCEPTANCE_AUDIT`.
- The mandatory first-pass chain includes `CONTROLLED_HUMANIZATION_ENGINE` between `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` and `AIGC_REGRESSION_GUARD`.
- `references/first_pass_effectiveness_gate.md` exists.
- `references/controlled_humanization_engine.md` exists.
- `references/academic_tone_guard.md` exists.
- `references/ooxml_docx_patch_workflow.md` exists.
- `references/docx_duplicate_insertion_guard.md` exists.
- `workflow/ooxml_patch_checklist.md` exists.
- `references/final_acceptance_audit.md` contains `FIRST_PASS_EFFECTIVENESS_GATE`.
- `references/first_pass_red_orange_engine.md` contains a rule equivalent to "red to orange is not success / 红转橙不算成功".
- `tests/first_pass_failure_color_migration_case.md` exists.

## Expected Entry Modes and Internal Engines

User-facing entry modes:
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

Internal mandatory engines/gates (not user-facing entries):
- `OOXML_DOCX_PATCH_WORKFLOW`
- `CONTROLLED_HUMANIZATION_ENGINE`
- `FIRST_PASS_EFFECTIVENESS_GATE`

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

all_modes = [
    'INTAKE_WIZARD_PRECHECK',
    'FILE_INPUT_COPY_WORKFLOW',
    'OOXML_DOCX_PATCH_WORKFLOW',
    'DOCX_COLOR_REPORT_EXTRACTION',
    'THREE_MODE_COLOR_BAND_WORKFLOW',
    'FIRST_PASS_RED_ORANGE_ENGINE',
    'CURRENT_REPORT_RED_ORANGE_ENGINE',
    'AIGC_PLATEAU_BREAKER',
    'SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK',
    'CONTROLLED_HUMANIZATION_ENGINE',
    'AIGC_REGRESSION_GUARD',
    'FIRST_PASS_EFFECTIVENESS_GATE',
    'FINAL_ACCEPTANCE_AUDIT',
]

internal_engines = [
    'OOXML_DOCX_PATCH_WORKFLOW',
    'CONTROLLED_HUMANIZATION_ENGINE',
    'FIRST_PASS_EFFECTIVENESS_GATE',
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
description: Chinese thesis AIGC and similarity-risk optimization skill with forced intake, DOCX color-report extraction, red-orange coverage, social-science evidence reconstruction, controlled humanization, first-pass effectiveness gate, and final acceptance audit.
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
if router_modes != all_modes:
    errors.append(
        'Minimal Mode Router mismatch: '
        + ', '.join(router_modes)
    )

# Check mandatory chain
chain_section = skill[skill.index('Mandatory First-Pass Chain'):skill.index('Current-Report Chain')]
chain_lines = [l.strip() for l in chain_section.split('\n') if '->' in l]
chain_text = ' '.join(chain_lines)

# Check CONTROLLED_HUMANIZATION_ENGINE is between SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK and AIGC_REGRESSION_GUARD
if 'SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK' in chain_text and 'CONTROLLED_HUMANIZATION_ENGINE' in chain_text and 'AIGC_REGRESSION_GUARD' in chain_text:
    idx_ss = chain_text.index('SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK')
    idx_ch = chain_text.index('CONTROLLED_HUMANIZATION_ENGINE')
    idx_rg = chain_text.index('AIGC_REGRESSION_GUARD')
    if not (idx_ss < idx_ch < idx_rg):
        errors.append('CONTROLLED_HUMANIZATION_ENGINE not between SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK and AIGC_REGRESSION_GUARD')
else:
    errors.append('Mandatory first-pass chain missing one of: SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK, CONTROLLED_HUMANIZATION_ENGINE, AIGC_REGRESSION_GUARD')

# Check FIRST_PASS_EFFECTIVENESS_GATE is between AIGC_REGRESSION_GUARD and FINAL_ACCEPTANCE_AUDIT
if 'AIGC_REGRESSION_GUARD' in chain_text and 'FIRST_PASS_EFFECTIVENESS_GATE' in chain_text and 'FINAL_ACCEPTANCE_AUDIT' in chain_text:
    idx_guard = chain_text.index('AIGC_REGRESSION_GUARD')
    idx_gate = chain_text.index('FIRST_PASS_EFFECTIVENESS_GATE')
    idx_final = chain_text.index('FINAL_ACCEPTANCE_AUDIT')
    if not (idx_guard < idx_gate < idx_final):
        errors.append('FIRST_PASS_EFFECTIVENESS_GATE not between AIGC_REGRESSION_GUARD and FINAL_ACCEPTANCE_AUDIT')
else:
    errors.append('Mandatory first-pass chain missing one of: AIGC_REGRESSION_GUARD, FIRST_PASS_EFFECTIVENESS_GATE, FINAL_ACCEPTANCE_AUDIT')

# Check required files exist
required_files = [
    'references/first_pass_effectiveness_gate.md',
    'references/controlled_humanization_engine.md',
    'references/academic_tone_guard.md',
    'references/ooxml_docx_patch_workflow.md',
    'references/docx_duplicate_insertion_guard.md',
    'workflow/ooxml_patch_checklist.md',
    'tests/first_pass_failure_color_migration_case.md',
]
for f in required_files:
    if not (root / f).exists():
        errors.append(f'Required file missing: {f}')

# Check final_acceptance_audit.md contains FIRST_PASS_EFFECTIVENESS_GATE
faa = (root / 'references/final_acceptance_audit.md').read_text(encoding='utf-8')
if 'FIRST_PASS_EFFECTIVENESS_GATE' not in faa:
    errors.append('final_acceptance_audit.md does not contain FIRST_PASS_EFFECTIVENESS_GATE')
if 'material_gap_table' not in faa:
    errors.append('final_acceptance_audit.md missing material_gap_table requirement')
if 'controlled_humanization_level' not in faa:
    errors.append('final_acceptance_audit.md missing controlled_humanization_level')
if 'academic_tone_guard_result' not in faa:
    errors.append('final_acceptance_audit.md missing academic_tone_guard_result')
if 'duplicate_insertion_guard_result' not in faa:
    errors.append('final_acceptance_audit.md missing duplicate_insertion_guard_result')
if 'final_delivery_status' not in faa:
    errors.append('final_acceptance_audit.md missing final_delivery_status')

# Check first_pass_red_orange_engine.md contains red-to-orange not success rule
fpro = (root / 'references/first_pass_red_orange_engine.md').read_text(encoding='utf-8')
if 'Red→orange' not in fpro and 'red to orange' not in fpro.lower() and '红转橙' not in fpro and 'UNPASSED' not in fpro:
    errors.append('first_pass_red_orange_engine.md missing red-to-orange not success rule')

# Check first_pass_effectiveness_gate.md contains core principle
fpeg = (root / 'references/first_pass_effectiveness_gate.md').read_text(encoding='utf-8')
if 'Red-to-orange migration is NOT success' not in fpeg:
    errors.append('first_pass_effectiveness_gate.md missing core principle')

# Check aigc_regression_guard.md has over-humanization regression
arg = (root / 'references/aigc_regression_guard.md').read_text(encoding='utf-8')
if 'over_humanization' not in arg.lower() and 'over-humanization' not in arg.lower():
    errors.append('aigc_regression_guard.md missing over-humanization regression check')

# Check QUICKSTART chain contains CONTROLLED_HUMANIZATION_ENGINE and FIRST_PASS_EFFECTIVENESS_GATE
if 'CONTROLLED_HUMANIZATION_ENGINE' not in quickstart:
    errors.append('QUICKSTART.md does not mention CONTROLLED_HUMANIZATION_ENGINE')
if 'FIRST_PASS_EFFECTIVENESS_GATE' not in quickstart:
    errors.append('QUICKSTART.md does not mention FIRST_PASS_EFFECTIVENESS_GATE')
if 'OOXML' not in quickstart:
    errors.append('QUICKSTART.md does not mention OOXML')

# Check README contains new engines
if 'CONTROLLED_HUMANIZATION_ENGINE' not in readme:
    errors.append('README.md does not mention CONTROLLED_HUMANIZATION_ENGINE')
if 'OOXML' not in readme:
    errors.append('README.md does not mention OOXML')

# Check no retired modes in QUICKSTART or README
for mode in retired_quickstart_entries:
    if mode in quickstart:
        errors.append(f'QUICKSTART.md still recommends retired entry mode: {mode}')
    if mode in readme:
        errors.append(f'README.md still recommends retired entry mode: {mode}')

# Check intake prompt
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

# Check archived prompt files
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

# Check test path references
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
print(f'Router modes: {len(all_modes)}')
print(f'Internal engines: {len(internal_engines)}')
print(f'Total router entries: {len(router_modes)}')
PY
```

## Manual Checks

- [ ] `SKILL.md` has legal YAML frontmatter.
- [ ] `SKILL.md` stays slim and does not reintroduce a long reference index.
- [ ] Historical mode files may remain for archive/compatibility, but they are not routed as entry modes.
- [ ] `skill_slimming_rules.md` remains a maintenance rule only.
- [ ] Missing author evidence routes to `workflow/author_evidence_pack_template.md`.
- [ ] `FIRST_PASS_EFFECTIVENESS_GATE` is between `AIGC_REGRESSION_GUARD` and `FINAL_ACCEPTANCE_AUDIT` in the mandatory first-pass chain.
- [ ] `CONTROLLED_HUMANIZATION_ENGINE` is between `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK` and `AIGC_REGRESSION_GUARD` in the mandatory first-pass chain.
- [ ] `references/first_pass_effectiveness_gate.md` contains the core principle that red-to-orange migration is NOT success.
- [ ] `references/final_acceptance_audit.md` outputs `material_gap_table` when evidence is missing.
- [ ] `references/social_science_template_bottleneck.md` contains anti-fabrication enforcement for specific data types.
- [ ] `tests/first_pass_failure_color_migration_case.md` exists and uses the real failure case data.
- [ ] `references/controlled_humanization_engine.md` supports 3 intensity levels with no unlimited aggressive mode.
- [ ] `references/academic_tone_guard.md` contains prohibited expressions list.
- [ ] `references/ooxml_docx_patch_workflow.md` preserves all non-document.xml resources.
- [ ] `references/docx_duplicate_insertion_guard.md` checks n-gram repeats and page count.
- [ ] `references/aigc_regression_guard.md` checks both formalization and over-humanization regression.
