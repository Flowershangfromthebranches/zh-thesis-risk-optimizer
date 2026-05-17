#!/usr/bin/env python3
"""
Repository structure validation for zh-thesis-risk-optimizer.

Run from the repository root:

    python tests/validate_skill_structure.md
"""

from pathlib import Path
import re
import sys


ROOT = Path(".")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def section_between(text: str, start: str, end: str) -> str:
    try:
        return text[text.index(start): text.index(end)]
    except ValueError:
        return ""


def ordered(text: str, tokens: list[str]) -> bool:
    pos = -1
    for token in tokens:
        idx = text.find(token, pos + 1)
        if idx == -1:
            return False
        pos = idx
    return True


errors: list[str] = []

skill = read("SKILL.md")
quickstart = read("QUICKSTART.md")
readme = read("README.md")
final_audit = read("references/final_acceptance_audit.md")
intake_prompt = read("prompts/mode_intake_wizard.md")

expected_frontmatter = """---
name: zh-thesis-risk-optimizer
description: Chinese thesis AIGC and similarity-risk optimization skill with forced risk intake, DOCX color-report extraction, red-orange coverage, social-science evidence reconstruction, controlled/local humanization, thesis-register guard, and final acceptance audit.
license: MIT
---"""

if not skill.startswith(expected_frontmatter + "\n\n# zh-thesis-risk-optimizer"):
    fail(errors, "SKILL.md frontmatter is not the expected legal YAML block")

if len(skill.splitlines()) < 80:
    fail(errors, "SKILL.md appears compressed; expected normal multi-line Markdown")

expected_router_modes = [
    "RISK_INTAKE_GATE",
    "INTAKE_WIZARD_PRECHECK",
    "FILE_INPUT_COPY_WORKFLOW",
    "OOXML_DOCX_PATCH_WORKFLOW",
    "DOCX_COLOR_REPORT_EXTRACTION",
    "THREE_MODE_COLOR_BAND_WORKFLOW",
    "FIRST_PASS_RED_ORANGE_ENGINE",
    "CURRENT_REPORT_RED_ORANGE_ENGINE",
    "AIGC_PLATEAU_BREAKER",
    "SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK",
    "CONTROLLED_HUMANIZATION_ENGINE",
    "LOCAL_ESCALATED_HUMANIZATION",
    "REWRITE_APPLICATION_GATE",
    "TEMPLATE_RESIDUE_DETECTOR",
    "THESIS_REGISTER_GUARD",
    "AIGC_REGRESSION_GUARD",
    "FIRST_PASS_EFFECTIVENESS_GATE",
    "FINAL_ACCEPTANCE_AUDIT",
]

router_modes = re.findall(r"^\| `([^`]+)` \|", skill, flags=re.MULTILINE)
if router_modes != expected_router_modes:
    fail(errors, "Minimal Mode Router mismatch: " + ", ".join(router_modes))

declared_paths = sorted(set(re.findall(
    r"((?:prompts|references|workflow)/[A-Za-z0-9_./-]+\.md)",
    skill,
)))
for rel in declared_paths:
    if not (ROOT / rel).exists():
        fail(errors, f"SKILL.md declares missing path: {rel}")

required_files = [
    "references/risk_intake_gate.md",
    "prompts/mode_risk_intake_gate.md",
    "tests/risk_intake_gate_cases.md",
    "references/local_escalated_humanization.md",
    "tests/local_escalated_humanization_cases.md",
    "references/thesis_register_guard.md",
    "references/first_pass_effectiveness_gate.md",
    "references/controlled_humanization_engine.md",
    "references/academic_tone_guard.md",
    "references/ooxml_docx_patch_workflow.md",
    "references/rewrite_application_gate.md",
    "references/template_residue_detector.md",
    "references/docx_duplicate_insertion_guard.md",
    "workflow/ooxml_patch_checklist.md",
    "workflow/intake_request_template.md",
    "tests/first_pass_failure_color_migration_case.md",
    "tests/rewrite_application_gate_cases.md",
    "tests/template_residue_detector_cases.md",
]
for rel in required_files:
    if not (ROOT / rel).exists():
        fail(errors, f"Required file missing: {rel}")

first_chain = section_between(skill, "Mandatory First-Pass Chain", "Current-Report Chain")
current_chain = section_between(skill, "Current-Report Chain", "Social-Science Hard Rule")
quick_first_chain = section_between(quickstart, "First-Pass AIGC", "Controlled Humanization")
quick_current_chain = section_between(quickstart, "Current-Report Workflow", "DOCX Format Protection")

required_chain_tokens = [
    "RISK_INTAKE_GATE",
    "INTAKE_WIZARD_PRECHECK",
    "FILE_INPUT_COPY_WORKFLOW",
    "DOCX_COLOR_REPORT_EXTRACTION",
    "THREE_MODE_COLOR_BAND_WORKFLOW",
    "CONTROLLED_HUMANIZATION_ENGINE",
    "LOCAL_ESCALATED_HUMANIZATION",
    "REWRITE_APPLICATION_GATE",
    "TEMPLATE_RESIDUE_DETECTOR",
    "THESIS_REGISTER_GUARD",
    "AIGC_REGRESSION_GUARD",
    "FIRST_PASS_EFFECTIVENESS_GATE",
    "FINAL_ACCEPTANCE_AUDIT",
]

for token in required_chain_tokens:
    if token not in first_chain:
        fail(errors, f"SKILL.md mandatory first-pass chain missing {token}")
    if token not in current_chain:
        fail(errors, f"SKILL.md current-report chain missing {token}")
    if token not in quickstart:
        fail(errors, f"QUICKSTART.md missing {token}")

critical_order = [
    "CONTROLLED_HUMANIZATION_ENGINE",
    "LOCAL_ESCALATED_HUMANIZATION",
    "REWRITE_APPLICATION_GATE",
    "TEMPLATE_RESIDUE_DETECTOR",
    "THESIS_REGISTER_GUARD",
    "AIGC_REGRESSION_GUARD",
]
if not ordered(first_chain, critical_order):
    fail(errors, "SKILL.md mandatory chain does not order controlled/local/gates before AIGC regression guard")
if not ordered(quick_first_chain, critical_order):
    fail(errors, "QUICKSTART.md first-pass Required chain does not order controlled/local/gates before AIGC regression guard")

requested_order = [
    "CONTROLLED_HUMANIZATION_ENGINE",
    "REWRITE_APPLICATION_GATE",
    "TEMPLATE_RESIDUE_DETECTOR",
    "AIGC_REGRESSION_GUARD",
]
if not ordered(first_chain, requested_order):
    fail(errors, "SKILL.md mandatory chain must contain CONTROLLED_HUMANIZATION_ENGINE -> REWRITE_APPLICATION_GATE -> TEMPLATE_RESIDUE_DETECTOR -> AIGC_REGRESSION_GUARD")
if not ordered(quick_first_chain, requested_order):
    fail(errors, "QUICKSTART.md Required chain must contain CONTROLLED_HUMANIZATION_ENGINE -> REWRITE_APPLICATION_GATE -> TEMPLATE_RESIDUE_DETECTOR -> AIGC_REGRESSION_GUARD")

for token in ["current_similarity_rate", "current_aigc_rate"]:
    if token not in quickstart:
        fail(errors, f"QUICKSTART.md does not explicitly require {token}")
    if token not in intake_prompt:
        fail(errors, f"mode_intake_wizard.md does not include {token}")

for token in [
    "selected_strategy",
    "max_humanization_level",
    "level_4_allowed",
    "local_escalation_applied",
    "local_escalation_sections",
    "thesis_register_guard_result",
    "current_similarity_rate",
    "current_aigc_rate",
    "target_similarity_rate",
    "target_aigc_rate",
]:
    if token not in final_audit:
        fail(errors, f"FINAL_ACCEPTANCE_AUDIT missing {token}")

risk_gate = read("references/risk_intake_gate.md")
for token in [
    "current_aigc_rate < 30",
    "30-49.99",
    "50-69.99",
    ">=70",
    "aggressive_but_localized_repair",
    "similarity_status",
    "already_passed",
    "needs_similarity_reduction",
    "minimal_repair_only",
]:
    if token not in risk_gate:
        fail(errors, f"risk_intake_gate.md missing {token}")

local_escalation = read("references/local_escalated_humanization.md")
for token in ["LOCAL_ESCALATED_HUMANIZATION", "Level 4", "摘要", "理论基础", "结论", "第四章问题分析", "第五章对策分析"]:
    if token not in local_escalation:
        fail(errors, f"local_escalated_humanization.md missing {token}")

controlled = read("references/controlled_humanization_engine.md")
for token in ["must not decide Level 4", "LOCAL_ESCALATED_HUMANIZATION", "Full-text Level 4 is blocked", "THESIS_REGISTER_GUARD"]:
    if token not in controlled:
        fail(errors, f"controlled_humanization_engine.md missing {token}")

thesis_guard = read("references/thesis_register_guard.md")
for token in ["Strict Sections", "Moderate Sections", "Flexible Sections", "一圈查下来", "说白了"]:
    if token not in thesis_guard:
        fail(errors, f"thesis_register_guard.md missing {token}")

effectiveness_gate = read("references/first_pass_effectiveness_gate.md")
for token in ["Condition 14", "Condition 15", "LOCAL_ESCALATED_HUMANIZATION", "orange_count > 25", "red_count + orange_count > 40"]:
    if token not in effectiveness_gate:
        fail(errors, f"first_pass_effectiveness_gate.md missing {token}")

retired_quickstart_entries = [
    "AIGC_ONLY",
    "SIMILARITY_ONLY",
    "REPORT_AIGC_ONLY",
    "DUAL_OPTIMIZATION",
    "AIGC_DEEP_REWRITE_ENGINE",
    "TARGETED_MULTIPASS_ENGINE",
    "AIGC_FOCUSED_LENGTH_CONTROLLED",
    "REPORT_SIMILARITY_ONLY",
    "SECOND_PASS_REWRITE",
    "FULL_THESIS_PROJECT_MODE",
    "NO_REPORT_FALLBACK_WORKFLOW",
]
for mode in retired_quickstart_entries:
    if mode in quickstart:
        fail(errors, f"QUICKSTART.md still recommends retired entry mode: {mode}")
    if mode in readme:
        fail(errors, f"README.md still recommends retired entry mode: {mode}")

if "Completed intake template without report | `NO_REPORT_FALLBACK_WORKFLOW`" in intake_prompt:
    fail(errors, "mode_intake_wizard.md still routes no-report intake to retired NO_REPORT_FALLBACK_WORKFLOW")

archived_prompt_files = [
    "prompts/mode_aigc_only.md",
    "prompts/mode_dual_optimization.md",
    "prompts/mode_report_driven_aigc.md",
    "prompts/mode_report_driven_similarity.md",
    "prompts/mode_second_pass_rewrite.md",
    "prompts/mode_targeted_multipass.md",
    "prompts/mode_aigc_focused_length_controlled.md",
    "prompts/mode_full_thesis_project.md",
    "prompts/mode_no_report_dual_fallback.md",
]
for rel in archived_prompt_files:
    path = ROOT / rel
    if not path.exists():
        fail(errors, f"Archived prompt file missing: {rel}")
        continue
    head = path.read_text(encoding="utf-8")[:220]
    if "ARCHIVED_COMPATIBILITY_ONLY" not in head:
        fail(errors, f"Archived prompt lacks compatibility header: {rel}")
    if "Do not call directly. Route through `SKILL.md` Minimal Mode Router." not in head:
        fail(errors, f"Archived prompt lacks routing warning: {rel}")

test_paths = []
for test_file in sorted((ROOT / "tests").glob("*.md")):
    text = test_file.read_text(encoding="utf-8")
    for rel in re.findall(
        r"((?:prompts|references|workflow|tests|examples)/[A-Za-z0-9_./-]+\.md)",
        text,
    ):
        test_paths.append((test_file, rel))

for test_file, rel in test_paths:
    if not (ROOT / rel).exists():
        fail(errors, f"{test_file} references missing path: {rel}")

if errors:
    print("FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("PASS")
print(f"SKILL declared paths: {len(declared_paths)}")
print(f"Test path references: {len(test_paths)}")
print(f"Router modes: {len(router_modes)}")
