"""CLI entry point for zh-thesis-risk-optimizer v2.0.

7-step workflow with mandatory IntakeGate, MajorRouter, PermissionGate.
optimize requires --confirmed yes to execute rewriting.
"""

from __future__ import annotations

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Optional

from . import __version__
from .document_io.docx_reader import DocxReader
from .document_io.docx_writer import DocxWriter
from .document_io.text_units import TextUnit, RiskLevel, ActionType, TextUnitType
from .document_io.format_preserver import classify_no_edit_zones, should_freeze
from .report_parser.aigc_report_parser import AigcReportParser, AigcReport
from .report_parser.color_zone_locator import ColorZoneLocator
from .analysis.thesis_classifier import ThesisClassifier, Discipline
from .analysis.risk_estimator import RiskEstimator
from .analysis.paragraph_diagnoser import ParagraphDiagnoser
from .analysis.rewrite_ratio_planner import RewriteRatioPlanner, RatioPlan
from .strategies import get_strategy
from .strategies.base import BaseStrategy
from .strategies.domain_profiles import DomainProfile, classify_domain, get_domain_profile
from .rewrite.rewrite_engine import RewriteEngine, BatchResult, LLMProvider
from .rewrite.anti_ai_style_guard import AntiAIStyleGuard, GuardResult
from .rewrite.evidence_injector import get_evidence_report_items
from .rewrite.oral_style_rewriter import OralStyleRewriter
from .validation.oral_style_guard import OralStyleGuard
from .validation.structure_validator import StructureValidator
from .validation.format_validator import FormatValidator
from .validation.length_validator import LengthValidator
from .validation.final_report import FinalReportGenerator, FinalReport, ReportContext
from .intake.intake_gate import IntakeGate
from .routing.major_router import MajorRouter
from .planning.risk_planner import RiskPlanner
from .planning.plan_summary import PlanSummaryGenerator
from .intake.confirmation import PermissionGate
from .evidence.evidence_plan import EvidencePlan


# ============================================================================
# Simple LLM Providers
# ============================================================================

class NoOpLLMProvider(LLMProvider):
    """LLMProvider that always returns None (no LLM available)."""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return None


class SimpleLLMProvider(LLMProvider):
    """Simple LLM provider that wraps an external callable."""
    def __init__(self, fn):
        self._fn = fn
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return self._fn(prompt, system_prompt)


# ============================================================================
# Intake helpers
# ============================================================================

def _parse_yes_no(val: str) -> Optional[bool]:
    """Parse yes/no/true/false/是/否 to bool."""
    if val is None:
        return None
    v = val.strip().lower()
    if v in ("yes", "true", "是", "1", "y"):
        return True
    if v in ("no", "false", "否", "0", "n"):
        return False
    return None


def _run_intake_check(args) -> dict:
    """Run IntakeGate from CLI args. Returns intake dict."""
    gate = IntakeGate()

    # Parse boolean flags
    has_report = _parse_yes_no(getattr(args, 'has_aigc_report', None))
    allow_rewrite = _parse_yes_no(getattr(args, 'allow_rewrite', None))
    allow_supplement = _parse_yes_no(getattr(args, 'allow_supplement', None))
    has_materials = _parse_yes_no(getattr(args, 'has_materials', None))

    result = gate.check(
        major=getattr(args, 'major', None),
        title=getattr(args, 'title', None),
        current_rate=getattr(args, 'aigc_rate', None),
        target_rate=getattr(args, 'target_rate', None),
        has_report=has_report,
        allow_rewrite=allow_rewrite,
        allow_supplement=allow_supplement,
        has_materials=has_materials,
    )
    return result


def _run_permission_check(intake_result, args) -> 'PermissionResult':
    """Run PermissionGate from intake result."""
    gate = PermissionGate()
    return gate.check(
        current_rate=intake_result.current_rate,
        target_rate=intake_result.target_rate,
        allow_rewrite=intake_result.allow_rewrite,
        allow_supplement=intake_result.allow_supplement,
        has_report=intake_result.has_report,
        has_materials=intake_result.has_materials,
    )


# ============================================================================
# Protected zones — hardened freeze logic
# ============================================================================

# Patterns in text that indicate identity/admin content
IDENTITY_KEYWORDS = [
    "学号", "姓名", "导师", "指导教师", "学院", "专业", "班级",
    "Student ID", "Name", "Supervisor", "School", "Major",
    "日期", "年  月  日", "年月日",
]

# Section names that should be frozen
FROZEN_SECTIONS = {
    "cover", "declaration", "toc", "references", "appendix",
    "acknowledgement", "questionnaire", "interview_guide",
}

# Keywords in text that indicate frozen content
FROZEN_TEXT_KEYWORDS = [
    "原创性声明", "独创性声明", "学术诚信", "学位论文原创性",
    "调查问卷", "访谈提纲", "附录", "致谢",
]


def _is_frozen_content(unit: TextUnit) -> bool:
    """Extended freeze check beyond format_preserver.should_freeze.

    Catches: identity info, questionnaires, interview guides, acknowledgements.
    """
    # Already frozen by format_preserver
    if should_freeze(unit):
        return True

    # Freeze by section
    if unit.section in FROZEN_SECTIONS:
        return True

    # Freeze appendix/questionnaire/interview content
    if unit.unit_type == TextUnitType.APPENDIX:
        return True

    # Freeze identity-info paragraphs
    text = unit.text.strip()
    if len(text) < 100:  # Short paragraphs that look like form fields
        for kw in IDENTITY_KEYWORDS:
            if kw in text:
                return True

    # Freeze specific content types by text pattern
    for kw in FROZEN_TEXT_KEYWORDS:
        if kw in text:
            return True

    # Freeze heading-only lines for frozen sections
    if unit.unit_type == TextUnitType.HEADING:
        heading_lower = text.lower().strip()
        if heading_lower in ("致谢", "附录", "调查问卷", "访谈提纲",
                             "参考文献", "acknowledgement", "references",
                             "目录", "contents"):
            return True

    return False


# ============================================================================
# CLI
# ============================================================================

def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"zh-thesis-risk-optimizer v{__version__}")
        return 0

    if args.command == "inspect-report":
        return run_inspect_report(args)
    elif args.command == "optimize":
        return run_optimize(args)
    elif args.command == "analyze-intake":
        return run_analyze_intake(args)
    elif args.command == "optimize-confirmed":
        return run_optimize_confirmed(args)
    elif args.command == "feedback-round":
        return run_feedback_round(args)
    elif args.command == "evaluate-outcome":
        return run_evaluate_outcome(args)
    else:
        parser.print_help()
        return 0


def _add_intake_args(parser):
    """Add intake-related arguments to a subparser."""
    parser.add_argument("--input", required=True, help="输入论文 (.docx)")
    parser.add_argument("--major", default=None, help="论文专业 (必填)")
    parser.add_argument("--title", default=None, help="论文题目 (必填)")
    parser.add_argument("--aigc-rate", type=float, default=None, help="当前 AIGC 疑似率 (必填)")
    parser.add_argument("--target-rate", type=float, default=None, help="目标 AIGC 疑似率 (必填)")
    parser.add_argument("--has-aigc-report", default=None, help="是否有 AIGC 标红报告 (yes/no)")
    parser.add_argument("--allow-rewrite", default=None, help="是否允许重写 (yes/no)")
    parser.add_argument("--allow-supplement", default=None, help="是否允许补充内容 (yes/no)")
    parser.add_argument("--has-materials", default=None, help="是否有写论文时用到的材料 (yes/no)")
    parser.add_argument("--confirmed", default=None, help="用户已确认方案 (yes/no)")


def _add_processing_args(parser):
    """Add processing-related arguments to a subparser."""
    parser.add_argument("--aigc-report", help="AIGC 标红报告 (.docx)")
    parser.add_argument("--style", default="low_aigc_humanized",
                         choices=["low_aigc_humanized", "standard"],
                         help="改写风格策略 (默认 low_aigc_humanized)")
    parser.add_argument("--domain", default="auto",
                         help="专业画像: auto/computer_engineering/management/education/literature/law/economics/medicine/art_design/engineering_general/marxism")
    parser.add_argument("--conservative", action="store_true",
                         help="启用保守模式")
    parser.add_argument("--output", help="输出文件")
    parser.add_argument("--report", help="处理报告路径")
    parser.add_argument("--dry-run", action="store_true", help="只分析不写入")
    parser.add_argument("--debug", action="store_true", help="输出中间分析结果")
    parser.add_argument("--llm-provider", default="none",
                         choices=["none", "openai", "anthropic", "custom"],
                         help="LLM 提供商 (默认 none)")
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--api-key-env", help="API Key 环境变量名")
    parser.add_argument("--base-url", help="API Base URL")
    parser.add_argument("--allow-no-llm", action="store_true",
                         help="允许在无 LLM 时执行")
    parser.add_argument("--min-length", type=int, default=None)
    parser.add_argument("--max-length", type=int, default=None)
    parser.add_argument("--target-length-range", default=None)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="thesis-optimize",
        description="中文毕业论文 AIGC 风险降低与论文质量重构工具 v2.0",
    )
    parser.add_argument("--version", action="store_true", help="显示版本号")
    sub = parser.add_subparsers(dest="command")

    # analyze-intake: plan only, no rewrite
    ai = sub.add_parser("analyze-intake", help="分析intake信息，生成优化方案（不执行改写）")
    _add_intake_args(ai)

    # optimize: requires --confirmed yes to execute
    opt = sub.add_parser("optimize", help="优化论文（需要 --confirmed yes）")
    _add_intake_args(opt)
    _add_processing_args(opt)

    # optimize-confirmed: shorthand for optimize with all checks
    oc = sub.add_parser("optimize-confirmed", help="确认后执行优化")
    _add_intake_args(oc)
    _add_processing_args(oc)

    # inspect-report
    insp = sub.add_parser("inspect-report", help="检查 AIGC 报告颜色统计")
    insp.add_argument("--input", required=True, help="AIGC 报告 (.docx)")

    # feedback-round
    fb = sub.add_parser("feedback-round", help="二轮反馈优化")
    fb.add_argument("--input", required=True)
    fb.add_argument("--first-round", required=True)
    fb.add_argument("--before-report", required=True)
    fb.add_argument("--after-report", required=True)
    fb.add_argument("--output", help="输出文件")
    fb.add_argument("--report", help="处理报告路径")
    fb.add_argument("--dry-run", action="store_true")
    fb.add_argument("--debug", action="store_true")
    fb.add_argument("--llm-provider", default="none",
                     choices=["none", "openai", "anthropic", "custom"])
    fb.add_argument("--model", help="模型名称")
    fb.add_argument("--api-key-env", help="API Key 环境变量名")
    fb.add_argument("--base-url", help="API Base URL")
    fb.add_argument("--target-rate", type=float, help="目标 AIGC 疑似率")

    # evaluate-outcome
    eo = sub.add_parser("evaluate-outcome", help="评估优化结果")
    eo.add_argument("--before-report", required=True)
    eo.add_argument("--after-report", required=True)
    eo.add_argument("--before-doc", help="原始论文 (.docx)")
    eo.add_argument("--after-doc", help="优化后论文 (.docx)")
    eo.add_argument("--major", default=None)
    eo.add_argument("--assigned-strategy", default=None)

    return parser


# ============================================================================
# analyze-intake command
# ============================================================================

def run_analyze_intake(args) -> int:
    """Step 1-5 only: check intake, route, plan, permission, evidence. No rewrite."""
    print("=" * 60)
    print("  analyze-intake: 信息检查 + 方案生成")
    print("=" * 60)

    # Step 1: IntakeGate
    intake = _run_intake_check(args)
    if not intake.complete:
        print("\n❌ 信息不完整，无法生成优化方案。\n")
        print(intake.missing_prompt)
        return 2

    # Step 2: MajorRouter
    router = MajorRouter()
    route = router.route(intake.major)
    if not route.strategy_name:
        print(f"\n❌ {route.warning}")
        return 2

    print(f"\n✅ 信息完整")
    print(f"   专业: {intake.major}")
    print(f"   题目: {intake.title}")
    print(f"   当前 AIGC: {intake.current_rate}%")
    print(f"   目标 AIGC: {intake.target_rate}%")
    print(f"   路线: {route.route_name} → 策略: {route.strategy_name}")
    if route.warning:
        print(f"   ⚠️  {route.warning}")

    # Step 3: RiskPlanner
    planner = RiskPlanner()
    risk_plan = planner.plan(
        current_rate=intake.current_rate,
        target_rate=intake.target_rate,
        allow_rewrite=intake.allow_rewrite,
        allow_supplement=intake.allow_supplement,
        has_materials=intake.has_materials,
    )

    print(f"\n📐 风险规划:")
    print(f"   强度: {risk_plan.intensity}")
    print(f"   比例: modify={risk_plan.modify_ratio:.0%} "
          f"rewrite={risk_plan.rewrite_ratio:.0%} "
          f"rebuild={risk_plan.rebuild_ratio:.0%}")
    for w in risk_plan.warnings:
        print(f"   ⚠️  {w}")

    # Step 4: PermissionGate
    perm = _run_permission_check(intake, args)
    if perm.needs_confirmation:
        print(f"\n⚠️  需要用户确认以下事项:")
        for p in perm.confirmation_prompts:
            print(f"   - {p}")
        print(f"\n   请确认后使用 optimize-confirmed 或 optimize --confirmed yes 执行。")

    # Step 5: EvidencePlan
    ep = EvidencePlan()
    evidence = ep.plan(
        has_materials=intake.has_materials,
        allow_supplement=intake.allow_supplement,
    )
    print(f"\n📋 证据规划:")
    print(f"   可用证据源: {', '.join(evidence.available_sources)}")
    for w in evidence.warnings:
        print(f"   ⚠️  {w}")

    # Step 6: PlanSummary
    gen = PlanSummaryGenerator()
    summary = gen.generate(
        major=intake.major,
        title=intake.title,
        current_rate=intake.current_rate,
        target_rate=intake.target_rate,
        has_report=intake.has_report,
        allow_rewrite=intake.allow_rewrite,
        allow_supplement=intake.allow_supplement,
        has_materials=intake.has_materials,
        strategy_name=route.strategy_name,
        route_name=route.route_name,
        risk_plan=risk_plan,
    )
    print(f"\n{'='*60}")
    print(summary.to_text())
    print(f"{'='*60}")

    print(f"\n💡 下一步: 确认方案后执行:")
    print(f"   python -m thesis_risk_optimizer.cli optimize-confirmed \\")
    print(f"     --input <论文.docx> --major {intake.major} \\")
    print(f"     --title \"{intake.title}\" \\")
    print(f"     --aigc-rate {intake.current_rate} --target-rate {intake.target_rate} \\")
    print(f"     --has-aigc-report {'yes' if intake.has_report else 'no'} \\")
    print(f"     --allow-rewrite {'yes' if intake.allow_rewrite else 'no'} \\")
    print(f"     --allow-supplement {'yes' if intake.allow_supplement else 'no'} \\")
    print(f"     --has-materials {'yes' if intake.has_materials else 'no'} \\")
    print(f"     --confirmed yes --llm-provider openai --model gpt-4o")

    return 0


# ============================================================================
# optimize command — requires --confirmed yes
# ============================================================================

def run_optimize(args) -> int:
    """optimize: requires IntakeGate + --confirmed yes to execute.

    Without --confirmed yes, acts like analyze-intake (plan only).
    """
    # Step 1: IntakeGate — MUST check BEFORE reading any file
    intake = _run_intake_check(args)
    if not intake.complete:
        print("\n❌ 信息不完整，无法执行优化。\n")
        print(intake.missing_prompt)
        print("\n请补充缺失信息后重试。")
        return 2

    # Check --confirmed
    confirmed = _parse_yes_no(getattr(args, 'confirmed', None))
    if not confirmed:
        # Act as analyze-intake
        print("\n⚠️  未确认方案 (需要 --confirmed yes)。")
        print("   以下为方案预览:\n")
        return run_analyze_intake(args)

    # Confirmed — proceed to full optimize
    return _execute_optimize(args, intake)


# ============================================================================
# optimize-confirmed command
# ============================================================================

def run_optimize_confirmed(args) -> int:
    """optimize-confirmed: intake check + direct execution."""
    # Step 1: IntakeGate
    intake = _run_intake_check(args)
    if not intake.complete:
        print("\n❌ 信息不完整，无法执行优化。\n")
        print(intake.missing_prompt)
        return 2

    # Force confirmed
    return _execute_optimize(args, intake)


# ============================================================================
# Core optimize execution (internal)
# ============================================================================

def _execute_optimize(args, intake) -> int:
    """Execute the full 7-step optimize after intake is confirmed."""
    input_path = Path(args.input)
    no_llm = getattr(args, 'llm_provider', 'none') == "none"
    report_context = ReportContext()

    # Step 2: MajorRouter
    router = MajorRouter()
    route = router.route(intake.major)
    if not route.strategy_name:
        print(f"\n❌ {route.warning}")
        return 2

    # Step 3: RiskPlanner
    risk_planner = RiskPlanner()
    risk_plan_result = risk_planner.plan(
        current_rate=intake.current_rate,
        target_rate=intake.target_rate,
        allow_rewrite=intake.allow_rewrite,
        allow_supplement=intake.allow_supplement,
        has_materials=intake.has_materials,
    )

    # Step 4: PermissionGate — user already confirmed, so just warn
    perm = _run_permission_check(intake, args)
    if perm.needs_confirmation:
        for p in perm.confirmation_prompts:
            print(f"   ⚠️  {p}")
        for w in perm.warnings:
            print(f"   ⚠️  {w}")

    # Step 5: EvidencePlan
    ep = EvidencePlan()
    evidence = ep.plan(
        has_materials=intake.has_materials,
        allow_supplement=intake.allow_supplement,
    )

    # ---- Now read the thesis ------------------------------------------------
    print(f"\n📄 读取论文: {input_path}")
    reader = DocxReader(input_path)
    units = reader.read()
    print(f"   总单元: {len(units)}, 正文: {sum(1 for u in units if u.is_body)}")

    # Parse AIGC report
    aigc_rate = intake.current_rate
    has_report = intake.has_report
    report_data = None
    report_mapping = None
    report_parse_failed = False

    aigc_report_path = getattr(args, 'aigc_report', None)
    if aigc_report_path:
        rp = Path(aigc_report_path)
        if rp.exists():
            parser = AigcReportParser()
            report_data = parser.parse(rp, debug=getattr(args, 'debug', False))
            if report_data.overall_rate and not aigc_rate:
                aigc_rate = report_data.overall_rate

            locator = ColorZoneLocator()
            report_mapping = locator.locate(units, report_data)

            if report_mapping["matched_fragment_count"] == 0 and report_data.total_scored > 0:
                report_parse_failed = True
                print(f"\n⚠️  AIGC 标红报告未能成功映射到正文段落。")

    # Route to strategy
    strategy = get_strategy(route.strategy_name)
    domain_profile, domain_evidence, domain_user_specified = _resolve_domain_profile(args, intake, units, route)

    # HR conservative default: auto-enable if current_rate >= 70
    is_hr = route.strategy_name == "human_resource"
    conservative_requested = getattr(args, 'conservative', False)
    if is_hr and intake.current_rate >= 70 and not conservative_requested:
        # Auto-enable conservative for high-AIGC HR theses
        conservative_requested = True
        print(f"\n⚠️  人力资源论文 AIGC={intake.current_rate}% >= 70%，自动启用保守模式。")

    if conservative_requested and hasattr(strategy, 'enable_conservative_mode'):
        strategy.enable_conservative_mode()
        print(f"\n✏️  采用策略: {strategy.label} (保守模式)")
    else:
        print(f"\n✏️  采用策略: {strategy.label}")

    print(f"   路线: {route.route_name}")
    print(f"   domain profile: {domain_profile.name}")
    if domain_evidence:
        print(f"   profile 依据: {', '.join(domain_evidence[:8])}")
    print(f"   AIGC 疑似率: {aigc_rate}%")

    # Plan rewrite ratios
    planner = RewriteRatioPlanner()
    plan = planner.plan(units, aigc_rate=aigc_rate)

    planner.apply_to_units(units, plan)

    # For HR conservative: cap rebuild count and rewrite count
    if is_hr and conservative_requested:
        _cap_hr_rebuild(units, plan)

    # Apply hardened freeze logic
    for unit in units:
        if _is_frozen_content(unit):
            unit.action = ActionType.FREEZE
            unit.metadata["freeze_reason"] = f"受保护内容: {unit.unit_type.value}/{unit.section}"

    body_units = [u for u in units if u.is_body]
    assigned = {
        "modify": sum(1 for u in body_units if u.action == ActionType.MODIFY),
        "rewrite": sum(1 for u in body_units if u.action == ActionType.REWRITE),
        "rebuild": sum(1 for u in body_units if u.action == ActionType.REBUILD),
        "freeze": sum(1 for u in body_units if u.action == ActionType.FREEZE),
    }
    print(f"\n📐 规划: modify={plan.planned_modify} rewrite={plan.planned_rewrite} rebuild={plan.planned_rebuild}")
    print(f"   分配: modify={assigned['modify']} rewrite={assigned['rewrite']} "
          f"rebuild={assigned['rebuild']} freeze={assigned['freeze']}")

    # Log context
    report_context.detected_discipline = route.strategy_name
    report_context.selected_strategy = strategy.name
    report_context.classification_confidence = 1.0  # user-declared
    report_context.user_forced_major = True
    report_context.domain_profile_name = domain_profile.name
    report_context.domain_profile_evidence = domain_evidence
    report_context.domain_user_specified = domain_user_specified

    # -- DRY-RUN ---------------------------------------------------------------
    if getattr(args, 'dry_run', False):
        if no_llm:
            print("\n  当前为 dry-run，仅展示分配计划，不执行真实重写；"
                  "正式执行 rewrite/rebuild 需要接入 LLM。")
        _print_dry_run(units, plan, assigned, None, route, strategy,
                       report_data, report_parse_failed, no_llm, evidence)
        return 0

    # Load system prompt with evidence constraints
    prompt_dir = Path(__file__).parent / "prompts"
    system_prompt = ""
    sp_path = prompt_dir / "system_prompt.md"
    if sp_path.exists():
        system_prompt = sp_path.read_text(encoding="utf-8")

    style = getattr(args, "style", "low_aigc_humanized")
    if style == "low_aigc_humanized":
        hp_path = prompt_dir / "low_aigc_humanized_prompt.md"
        if hp_path.exists():
            system_prompt += "\n\n" + hp_path.read_text(encoding="utf-8")
        system_prompt += "\n\n## 当前专业画像\n"
        system_prompt += f"- profile: {domain_profile.name} / {domain_profile.label}\n"
        system_prompt += f"- anchors: {', '.join(domain_profile.material_anchors.keys())}\n"
        system_prompt += f"- style: {'; '.join(domain_profile.style_guidance)}\n"

    # Inject evidence constraints into system prompt
    if not intake.has_materials:
        system_prompt += "\n\n## 重要约束 (has_materials=no)\n"
        system_prompt += "- 不得新增问卷人数\n"
        system_prompt += "- 不得新增访谈人数\n"
        system_prompt += "- 不得新增百分比\n"
        system_prompt += "- 不得新增离职率、满意度\n"
        system_prompt += "- 不得新增企业经营数据\n"
        system_prompt += "- 不得新增 BEI/BES/ROI 等术语，除非原文已有\n"
        system_prompt += "- 只能基于原文已有信息保守重写\n"
        system_prompt += "- 重点删除模板句、调整论证顺序，而不是扩写\n"

    # Set up LLM
    llm = None
    if not no_llm:
        llm = _build_llm_provider(args)
    else:
        has_rewrite_rebuild = assigned["rewrite"] + assigned["rebuild"] > 0
        if has_rewrite_rebuild:
            print("\n⚠️  当前未接入 LLM，只能进行轻度规则修改。")
            allow_no_llm = getattr(args, 'allow_no_llm', False)
            if not allow_no_llm:
                print("  当前任务需要 rewrite/rebuild，但未接入 LLM。")
                print("  可使用 --allow-no-llm 强制仅做规则修改。")
                return 1
            print("  已使用 --allow-no-llm，将仅做规则修改 (效果有限)。")
            report_context.no_llm = True

    engine = RewriteEngine(
        strategy=strategy,
        llm=llm,
        system_prompt=system_prompt,
        style=style,
        domain=domain_profile.name,
    )
    batch_result = engine.process_units(units)
    oral_failures = _apply_final_oral_validation(units, domain_profile.name)
    if oral_failures:
        print(f"\n⚠️  口语化限流复检仍有 {oral_failures} 个段落未通过，报告中会标记 warning。")

    guard_results = [r.guard_result for r in batch_result.results if r.guard_result]
    guard_failures = sum(1 for g in guard_results if g and not g.passed)

    processed = batch_result.succeeded
    frozen = batch_result.frozen
    print(f"   处理: {processed} 成功, {batch_result.failed} 失败, {frozen} 冻结")

    if processed == 0 and frozen < len(units):
        print("\n⚠️  未实际处理任何正文段落。")
        report_context.processed_zero = True

    # Write output
    output_path = Path(args.output) if args.output else input_path.parent / f"{input_path.stem}_optimized.docx"
    report_output = Path(args.report) if args.report else input_path.parent / f"{input_path.stem}_optimization_report.md"

    print(f"\n💾 写入: {output_path}")
    writer = DocxWriter(input_path)
    result = writer.apply_modifications(units)
    writer.save(output_path)
    print(f"   修改: {result['modified']}, 跳过: {result['skipped']}, 错误: {result['errors']}")

    # Validate
    fmt_val = FormatValidator()
    fmt_ok = fmt_val.validate(output_path)
    str_val = StructureValidator()
    str_ok = str_val.validate(units, units)
    len_val = LengthValidator()

    target_range = None
    target_length_range = getattr(args, 'target_length_range', None)
    if target_length_range:
        try:
            parts = target_length_range.split(",")
            target_range = (float(parts[0]), float(parts[1]))
        except (ValueError, IndexError):
            pass

    len_rpt = len_val.validate(
        units,
        min_length=getattr(args, 'min_length', None),
        max_length=getattr(args, 'max_length', None),
        target_range=target_range,
    )

    # Generate report
    report_context.aigc_rate = aigc_rate
    report_context.has_report = has_report
    report_context.report_parse_failed = report_parse_failed
    report_context.processed_zero = processed == 0

    gen = FinalReportGenerator()
    final = gen.generate(
        input_path, output_path, units, route.strategy_name, strategy.label,
        plan, batch_result, aigc_rate, has_report,
        str_ok, len_rpt, guard_results, report_context,
    )

    # Inject honest verdict into report
    _inject_honest_verdict(final, report_context)

    print(f"📝 报告: {report_output}")
    gen.save(final, report_output)

    # Print final verdict
    if final.honest_warnings:
        print("\n⚠️  重要提示:")
        for w in final.honest_warnings:
            print(f"   {w}")

    print(f"\n✅ 完成!")
    return 0


def _cap_hr_rebuild(units, plan):
    """Cap rebuild and rewrite count for HR conservative mode.

    HR theses should not have massive rebuild — cap at max 5 rebuilds.
    Rewrite should be capped at 25% of valid body paragraphs.
    """
    body_units = [u for u in units if u.is_body and not u.action == ActionType.FREEZE]
    total_valid = len(body_units)
    if total_valid == 0:
        return

    # 1. Cap Rebuild at 5
    rebuild_count = sum(1 for u in body_units if u.action == ActionType.REBUILD)
    if rebuild_count > 5:
        excess = rebuild_count - 5
        downgraded = 0
        for u in reversed(body_units):
            if u.action == ActionType.REBUILD and downgraded < excess:
                u.action = ActionType.REWRITE
                downgraded += 1

    # 2. Cap Rewrite at 25% of valid body units
    max_rewrite = max(1, int(total_valid * 0.25))
    rewrite_count = sum(1 for u in body_units if u.action == ActionType.REWRITE)
    if rewrite_count > max_rewrite:
        excess = rewrite_count - max_rewrite
        downgraded = 0
        for u in reversed(body_units):
            if u.action == ActionType.REWRITE and downgraded < excess:
                u.action = ActionType.MODIFY
                downgraded += 1


def _apply_final_oral_validation(units, domain: str = "universal") -> int:
    """Final oral-style recovery before DOCX writing.

    Strong oral expressions are recovered once. If a paragraph still fails the
    guard, we keep the text but record a warning for the final report instead
    of adding more oral language or inventing materials.
    """
    guard = OralStyleGuard()
    rewriter = OralStyleRewriter()
    failures = 0
    for unit in units:
        if not unit.is_body or unit.action == ActionType.FREEZE:
            continue
        rewritten = rewriter.rewrite(unit.text, section=unit.section, domain=domain)
        if rewritten.text != unit.text:
            unit.text = rewritten.text
            unit.metadata.setdefault("oral_rewrite_log", [])
            unit.metadata["oral_rewrite_log"].extend(
                {
                    "original": item.original,
                    "replacement": item.replacement,
                    "section": item.section,
                    "reason": item.reason,
                }
                for item in rewritten.replacements
            )
        result = guard.check(unit.text, section=unit.section, domain=domain)
        unit.metadata["final_oral_style_summary"] = {
            "total_sentences": result.total_sentences,
            "mild_oral_count": result.mild_oral_count,
            "strong_oral_count": result.strong_oral_count,
            "oral_density": result.oral_density,
            "status": result.status,
        }
        if result.status == "fail":
            failures += 1
            unit.metadata["final_oral_style_failed"] = True
            unit.metadata["final_oral_style_warnings"] = result.warnings
    return failures


def _resolve_domain_profile(args, intake, units, route) -> tuple[DomainProfile, list[str], bool]:
    """Resolve explicit or automatic domain profile for low-AIGC mode."""
    requested = getattr(args, "domain", "auto") or "auto"
    if requested != "auto":
        profile = get_domain_profile(requested)
        return profile, [f"--domain {requested}"], True

    headings = [u.text for u in units if u.unit_type == TextUnitType.HEADING]
    abstract = "\n".join(
        u.text for u in units
        if u.section == "abstract" or u.unit_type == TextUnitType.ABSTRACT
    )
    profile, evidence = classify_domain(
        title=intake.title,
        abstract=abstract,
        headings=headings,
        declared_major=intake.major,
    )

    if profile.name == "universal" and route.strategy_name:
        routed_profile = get_domain_profile(route.strategy_name)
        if routed_profile.name != "universal":
            return routed_profile, [f"专业路由: {route.route_name}"], False

    return profile, evidence, False


def _inject_honest_verdict(report: FinalReport, ctx: ReportContext):
    """Inject honest verdict into report based on outcome.

    Rules:
    - If no LLM and nothing processed: say so
    - Never say "修改成功率 100%" as success
    - Never say "部分成功" if rate increased
    - Without after-report: "已生成候选版本，效果未验证"
    """
    # Ban misleading phrases from existing warnings
    banned_phrases = [
        "修改成功率 100%",
        "覆盖全部红橙紫段落",
        "部分成功，待验证",
        "深度重写完成",
        "降 AIGC 版已完成",
        "优化成功",
    ]

    # Check and remove any misleading content
    report.honest_warnings = [
        w for w in report.honest_warnings
        if not any(bp in w for bp in banned_phrases)
    ]

    # If AIGC rate is known and post-rate is known
    if ctx.has_report and ctx.aigc_rate is not None and ctx.post_aigc_rate is not None:
        if ctx.post_aigc_rate >= ctx.aigc_rate:
            # 必须明确判定失败
            report.honest_warnings.append(
                f"本轮优化失败。AIGC 疑似率从 {ctx.aigc_rate:.2f}% 上升至 {ctx.post_aigc_rate:.2f}%，不建议使用改后版本，建议回滚原文。"
            )
    elif not ctx.has_report:
        if not any("效果未验证" in w for w in report.honest_warnings):
            report.honest_warnings.append(
                "已生成候选版本，尚未验证检测结果。"
            )

    # 再次清理确保不含成功字眼
    if ctx.post_aigc_rate is not None and ctx.aigc_rate is not None and ctx.post_aigc_rate >= ctx.aigc_rate:
        report.honest_warnings = [
            w for w in report.honest_warnings
            if "部分成功" not in w and "优化成功" not in w
        ]


# ============================================================================
# Dry-run output — only shows non-frozen content
# ============================================================================

def _print_dry_run(units, plan, assigned, batch_result, route, strategy,
                   report_data, report_parse_failed, no_llm, evidence=None):
    """Print detailed dry-run summary. Only shows non-frozen content."""
    print(f"\n{'='*60}")
    print("  DRY-RUN 分析报告")
    print(f"{'='*60}")
    print(f"  专业: {route.strategy_name}  策略: {strategy.label}")
    print(f"  路线: {route.route_name}")
    print(f"  AIGC 疑似率: {plan.aigc_rate or '未提供'}")
    print()

    # Planned vs assigned
    print(f"  --- 处理比例 ---")
    print(f"  {'':>10} {'计划':>8} {'分配':>8}")
    print(f"  {'modify':>10} {plan.planned_modify:>8} {assigned['modify']:>8}")
    print(f"  {'rewrite':>10} {plan.planned_rewrite:>8} {assigned['rewrite']:>8}")
    print(f"  {'rebuild':>10} {plan.planned_rebuild:>8} {assigned['rebuild']:>8}")
    print(f"  {'freeze':>10} {'':>8} {assigned['freeze']:>8}")

    if assigned["modify"] + assigned["rewrite"] + assigned["rebuild"] == 0:
        print(f"\n  ❌ 实际分配为 0！正文全部被冻结。")
        if no_llm:
            print(f"  提示: 未启用 LLM, 请使用 --llm-provider 参数。")

    # Samples per action — ONLY non-frozen content
    for action_name, label in [("rebuild", "重构"), ("rewrite", "重写"),
                                ("modify", "修改")]:
        samples = [
            u for u in units
            if u.action.value == action_name and not _is_frozen_content(u)
        ]
        if samples:
            print(f"\n  --- {label} 样本 (前{min(5, len(samples))}段) ---")
            for u in samples[:5]:
                print(f"    [{u.uid}] {u.section or '?'}: {u.text[:70]}...")

    # Evidence warnings
    if evidence and evidence.warnings:
        print(f"\n  --- 证据约束 ---")
        for w in evidence.warnings:
            print(f"    ⚠️  {w}")

    # AIGC report status
    if report_data:
        print(f"\n  --- AIGC 报告 ---")
        print(f"    Red={report_data.red_count} Orange={report_data.orange_count} "
              f"Purple={report_data.purple_count} Black={report_data.black_count}")
        if report_parse_failed:
            print(f"    ⚠️  报告映射失败,建议运行 inspect-report。")

    print(f"{'='*60}\n")


# ============================================================================
# inspect-report command
# ============================================================================

def run_inspect_report(args) -> int:
    path = Path(args.input)
    parser = AigcReportParser()
    stats = parser.inspect_colors(path)

    print("=" * 60)
    print("  AIGC 报告颜色统计")
    print("=" * 60)
    print(f"  文件: {path}")
    print(f"  有颜色的段落数: {stats['total_paragraphs_with_color']}")
    print(f"\n  发现的所有颜色值:")
    for color_key, count in stats["color_stats"].items():
        print(f"    {color_key}: {count} 次")
    print(f"\n  前10个有颜色的段落:")
    for p in stats["paragraphs_with_color"][:10]:
        print(f"    段落 {p['index']}: {p['text_preview'][:60]}...")
        for c in p["colors"]:
            print(f"      -> {c['type']}: {c['value']}")
    print("=" * 60)

    report = parser.parse(path, debug=True)
    print(f"\n  解析结果: Red={report.red_count} Orange={report.orange_count} "
          f"Purple={report.purple_count} Black={report.black_count} "
          f"Gray={len(report.fragments) - report.total_scored}")
    if report.overall_rate:
        print(f"  检测到总体 AIGC 疑似率: {report.overall_rate}%")

    return 0


# ============================================================================
# feedback-round command
# ============================================================================

def run_feedback_round(args) -> int:
    """Second-pass optimization."""
    from .validation.risk_delta_evaluator import RiskDeltaEvaluator
    from .rewrite.denominator_dilution_guard import DenominatorDilutionGuard

    input_path = Path(args.input)
    first_round_path = Path(args.first_round)
    before_report_path = Path(args.before_report)
    after_report_path = Path(args.after_report)

    print(f"📄 二轮反馈优化")
    print(f"   原始论文: {input_path}")
    print(f"   一轮优化: {first_round_path}")
    print(f"   原始报告: {before_report_path}")
    print(f"   一轮报告: {after_report_path}")

    parser = AigcReportParser()
    before_report = parser.parse(before_report_path, debug=getattr(args, 'debug', False))
    after_report = parser.parse(after_report_path, debug=getattr(args, 'debug', False))

    reader1 = DocxReader(input_path)
    original_units = reader1.read()
    reader2 = DocxReader(first_round_path)
    optimized_units = reader2.read()

    evaluator = RiskDeltaEvaluator()
    risk_delta = evaluator.evaluate(
        before_report, after_report,
        before_doc_chars=sum(len(u.text) for u in original_units),
        after_doc_chars=sum(len(u.text) for u in optimized_units),
        target_rate=args.target_rate,
    )

    print(f"\n📊 风险变化评估:")
    print(f"   判定: {risk_delta.verdict}")
    print(f"   AIGC 疑似率: {risk_delta.before_rate}% → {risk_delta.after_rate}% "
          f"({risk_delta.rate_delta:+.1f}pp)")

    if risk_delta.verdict == "failed":
        print(f"\n❌ 本轮优化失败。")
        if risk_delta.rate_delta >= 0:
            print(f"   AIGC 疑似率从 {risk_delta.before_rate}% 上升至 {risk_delta.after_rate}%。")
            print(f"   不建议使用改后版本，建议回滚原文。")
            print(f"   请不要继续使用同一策略二次优化。")
        return 1

    if risk_delta.verdict == "success":
        print(f"\n✅ 一轮优化已成功，无需二轮处理。")
        return 0

    print(f"\n   需要进一步处理。")
    if args.dry_run:
        print(f"   当前为 dry-run，不执行。")
        return 0

    return 0


# ============================================================================
# evaluate-outcome command
# ============================================================================

def run_evaluate_outcome(args) -> int:
    """Evaluate optimization outcome by comparing before/after reports."""
    from .validation.outcome_evaluator import OptimizationOutcomeEvaluator

    before_report_path = Path(args.before_report)
    after_report_path = Path(args.after_report)

    if not before_report_path.exists():
        print(f"❌ 原始报告不存在: {before_report_path}")
        return 1
    if not after_report_path.exists():
        print(f"❌ 优化后报告不存在: {after_report_path}")
        return 1

    parser = AigcReportParser()
    before_report = parser.parse(before_report_path)
    after_report = parser.parse(after_report_path)

    before_doc_chars = 0
    after_doc_chars = 0
    if hasattr(args, 'before_doc') and args.before_doc:
        bp = Path(args.before_doc)
        if bp.exists():
            reader = DocxReader(bp)
            units = reader.read()
            before_doc_chars = sum(len(u.text) for u in units)
    if hasattr(args, 'after_doc') and args.after_doc:
        ap = Path(args.after_doc)
        if ap.exists():
            reader = DocxReader(ap)
            units = reader.read()
            after_doc_chars = sum(len(u.text) for u in units)

    discipline = "universal"
    major_input = getattr(args, 'major', None) or "universal"
    if major_input == "hr":
        major_input = "human_resource"
    discipline = major_input

    assigned_strategy = getattr(args, 'assigned_strategy', None) or discipline

    evaluator = OptimizationOutcomeEvaluator()
    result = evaluator.evaluate(
        before_report, after_report,
        before_doc_chars=before_doc_chars,
        after_doc_chars=after_doc_chars,
        discipline=discipline,
        assigned_strategy=assigned_strategy,
    )

    print("=" * 60)
    print("  优化结果评估")
    print("=" * 60)
    print(evaluator.format_report(result))

    if result.verdict == "failed":
        before_rate = before_report.overall_rate or 0
        after_rate = after_report.overall_rate or 0
        if after_rate >= before_rate:
            print(f"\n❌ 本轮优化失败。AIGC 疑似率从 {before_rate}% 上升至 {after_rate}%。")
            print(f"   不建议使用改后版本，建议回滚原文。")
            print(f"   请不要继续使用同一策略二次优化。")

        if discipline in ("human_resource", "hr"):
            print(f"\n### 人力资源论文建议")
            print("- 建议回滚到原文")
            print("- 进入 human_resource conservative mode")
            print("- 优先处理报告中仍为红色的段落")

    print("=" * 60)
    return 0


# ============================================================================
# LLM provider builder
# ============================================================================

def _build_llm_provider(args) -> Optional[LLMProvider]:
    """Build an LLM provider from CLI arguments."""
    provider = getattr(args, 'llm_provider', 'none')
    model = getattr(args, 'model', None) or "gpt-4o"
    api_key_env = getattr(args, 'api_key_env', None)
    base_url = getattr(args, 'base_url', None)

    if provider == "none":
        return None

    api_key = None
    if api_key_env:
        api_key = os.environ.get(api_key_env)
    if not api_key:
        for env_name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "LLM_API_KEY"]:
            api_key = os.environ.get(env_name)
            if api_key:
                break

    if not api_key:
        print(f"⚠️  未找到 API Key。回退到无 LLM 模式。")
        return None

    if provider == "openai" or (provider == "custom" and base_url):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=base_url or None)

            def openai_generate(prompt: str, system_prompt: str = "") -> str:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=4096,
                )
                return resp.choices[0].message.content

            return SimpleLLMProvider(openai_generate)
        except ImportError:
            print("⚠️  需要安装 openai 包: pip install openai")
            return None

    if provider == "anthropic":
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)

            def anthropic_generate(prompt: str, system_prompt: str = "") -> str:
                resp = client.messages.create(
                    model=model,
                    max_tokens=4096,
                    system=system_prompt or "You are a helpful assistant.",
                    messages=[{"role": "user", "content": prompt}],
                )
                return resp.content[0].text

            return SimpleLLMProvider(anthropic_generate)
        except ImportError:
            print("⚠️  需要安装 anthropic 包: pip install anthropic")
            return None

    return None


if __name__ == "__main__":
    raise SystemExit(main())
