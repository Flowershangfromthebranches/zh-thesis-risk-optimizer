"""Tests for zh-thesis-risk-optimizer v2.0 final workflow.

14 required test cases per the refactoring specification.
"""

import pytest
from pathlib import Path

from thesis_risk_optimizer.intake.intake_gate import IntakeGate, IntakeResult
from thesis_risk_optimizer.intake.confirmation import PermissionGate, PermissionResult
from thesis_risk_optimizer.routing.major_router import MajorRouter, RouteResult
from thesis_risk_optimizer.planning.risk_planner import RiskPlanner, RiskPlanResult
from thesis_risk_optimizer.planning.plan_summary import PlanSummaryGenerator, PlanSummary
from thesis_risk_optimizer.evidence.evidence_plan import EvidencePlan, FABRICATION_FORBIDDEN
from thesis_risk_optimizer.strategies import get_strategy
from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy
from thesis_risk_optimizer.strategies.computer import ComputerStrategy
from thesis_risk_optimizer.document_io.text_units import TextUnit, TextUnitType, RiskLevel, ActionType
from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis


def make_unit(uid="u0001", text="测试段落内容", unit_type=TextUnitType.PARAGRAPH,
              section="introduction", risk_level=RiskLevel.LOW, action=ActionType.FREEZE):
    return TextUnit(uid=uid, unit_type=unit_type, text=text,
                    section=section, risk_level=risk_level, action=action,
                    original_text=text,
                    metadata={"body_element_index": 0, "paragraph_index": 0})


# ============================================================================
# 1. test_intake_missing_fields
# ============================================================================

class TestIntakeMissingFields:
    """缺少必填信息时，不执行优化，返回缺失项。"""

    def test_missing_all_fields(self):
        gate = IntakeGate()
        result = gate.check()
        assert result.complete is False
        assert len(result.missing_fields) == 8
        assert "major" in result.missing_fields
        assert "title" in result.missing_fields
        assert "当前无法开始优化" in result.missing_prompt

    def test_missing_some_fields(self):
        gate = IntakeGate()
        result = gate.check(
            major="计算机科学与技术",
            title="基于Django的在线商城系统",
        )
        assert result.complete is False
        assert "current_rate" in result.missing_fields
        assert "target_rate" in result.missing_fields
        assert "major" not in result.missing_fields
        assert "title" not in result.missing_fields

    def test_missing_major_only(self):
        gate = IntakeGate()
        result = gate.check(
            title="某公司招聘管理优化研究",
            current_rate=76.67,
            target_rate=30.0,
            has_report=True,
            allow_rewrite=True,
            allow_supplement=True,
            has_materials=True,
        )
        assert result.complete is False
        assert result.missing_fields == ["major"]

    def test_empty_major_treated_as_missing(self):
        gate = IntakeGate()
        result = gate.check(
            major="  ",
            title="某研究",
            current_rate=50.0,
            target_rate=30.0,
            has_report=False,
            allow_rewrite=True,
            allow_supplement=True,
            has_materials=False,
        )
        assert result.complete is False
        assert "major" in result.missing_fields


# ============================================================================
# 2. test_intake_complete_generates_plan
# ============================================================================

class TestIntakeCompleteGeneratesPlan:
    """信息完整时，生成 PlanSummary。"""

    def test_complete_intake_generates_plan(self):
        gate = IntakeGate()
        result = gate.check(
            major="人力资源管理",
            title="数智化时代A电商公司招聘管理优化研究",
            current_rate=76.67,
            target_rate=30.0,
            has_report=True,
            allow_rewrite=True,
            allow_supplement=True,
            has_materials=True,
        )
        assert result.complete is True
        assert result.major == "人力资源管理"
        assert result.current_rate == 76.67
        assert result.target_rate == 30.0

        # Now generate plan
        router = MajorRouter()
        route = router.route(result.major)
        assert route.strategy_name == "human_resource"

        planner = RiskPlanner()
        risk_plan = planner.plan(
            current_rate=result.current_rate,
            target_rate=result.target_rate,
            allow_rewrite=result.allow_rewrite,
            allow_supplement=result.allow_supplement,
            has_materials=result.has_materials,
        )

        gen = PlanSummaryGenerator()
        summary = gen.generate(
            major=result.major,
            title=result.title,
            current_rate=result.current_rate,
            target_rate=result.target_rate,
            has_report=result.has_report,
            allow_rewrite=result.allow_rewrite,
            allow_supplement=result.allow_supplement,
            has_materials=result.has_materials,
            strategy_name=route.strategy_name,
            route_name=route.route_name,
            risk_plan=risk_plan,
        )
        assert isinstance(summary, PlanSummary)
        assert summary.major == "人力资源管理"
        assert summary.strategy_name == "human_resource"
        text = summary.to_text()
        assert "人力资源管理" in text
        assert "76.67" in text


# ============================================================================
# 3. test_major_user_declared_priority
# ============================================================================

class TestMajorUserDeclaredPriority:
    """用户声明专业优先级最高。"""

    def test_user_declared_overrides_everything(self):
        router = MajorRouter()
        # User says HR — must use HR strategy
        route = router.route("人力资源管理")
        assert route.strategy_name == "human_resource"
        assert route.user_declared is True

    def test_explicit_computer_is_respected(self):
        router = MajorRouter()
        route = router.route("计算机科学与技术")
        assert route.strategy_name == "computer"
        assert route.user_declared is True

    def test_no_major_returns_error(self):
        router = MajorRouter()
        route = router.route("")
        assert route.strategy_name == ""
        assert route.user_declared is False
        assert "未提供" in route.warning

    def test_none_major_returns_error(self):
        router = MajorRouter()
        route = router.route(None)
        assert route.strategy_name == ""
        assert route.user_declared is False


# ============================================================================
# 4. test_major_human_resource_route
# ============================================================================

class TestMajorHumanResourceRoute:
    """论文专业=人力资源管理时，进入 HumanResourceStrategy。"""

    def test_hr_route(self):
        router = MajorRouter()
        for major in ["人力资源管理", "人力资源", "招聘管理", "绩效考核",
                       "薪酬管理", "员工培训", "hr", "human_resource"]:
            route = router.route(major)
            assert route.strategy_name == "human_resource", \
                f"Major '{major}' should route to human_resource, got {route.strategy_name}"

    def test_hr_strategy_loaded(self):
        strategy = get_strategy("human_resource")
        assert isinstance(strategy, HumanResourceStrategy)
        assert strategy.name == "human_resource"


# ============================================================================
# 5. test_major_computer_route
# ============================================================================

class TestMajorComputerRoute:
    """论文专业=计算机科学与技术时，进入 ComputerEngineeringStrategy。"""

    def test_computer_route(self):
        router = MajorRouter()
        for major in ["计算机科学与技术", "软件工程", "网络工程", "人工智能",
                       "数据科学", "Web", "computer", "cs"]:
            route = router.route(major)
            assert route.strategy_name == "computer", \
                f"Major '{major}' should route to computer, got {route.strategy_name}"

    def test_computer_strategy_loaded(self):
        strategy = get_strategy("computer")
        assert isinstance(strategy, ComputerStrategy)
        assert strategy.name == "computer"


# ============================================================================
# 6. test_no_report_requires_confirmation
# ============================================================================

class TestNoReportRequiresConfirmation:
    """没有 AIGC 报告时，需要用户确认继续。"""

    def test_no_report_needs_confirmation(self):
        gate = PermissionGate()
        result = gate.check(
            current_rate=76.67,
            target_rate=30.0,
            allow_rewrite=True,
            allow_supplement=True,
            has_report=False,
            has_materials=True,
        )
        assert result.needs_confirmation is True
        assert result.can_proceed is False
        assert any("未提供 AIGC 标红报告" in p for p in result.confirmation_prompts)

    def test_with_report_no_confirmation_needed(self):
        gate = PermissionGate()
        result = gate.check(
            current_rate=30.0,
            target_rate=20.0,
            allow_rewrite=True,
            allow_supplement=True,
            has_report=True,
            has_materials=True,
        )
        # With report and low rate, should not need confirmation
        assert result.can_proceed is True or not result.needs_confirmation


# ============================================================================
# 7. test_rewrite_not_allowed_warning
# ============================================================================

class TestRewriteNotAllowedWarning:
    """需要重写但用户不允许时，提示效果受限。"""

    def test_rewrite_forbidden_with_high_rate(self):
        gate = PermissionGate()
        result = gate.check(
            current_rate=76.67,
            target_rate=30.0,
            allow_rewrite=False,
            allow_supplement=True,
            has_report=True,
            has_materials=True,
        )
        assert result.needs_confirmation is True
        assert any("不允许重写" in p or "禁止重写" in p
                    for p in result.confirmation_prompts)

    def test_risk_planner_warns_no_rewrite(self):
        planner = RiskPlanner()
        result = planner.plan(
            current_rate=76.67,
            target_rate=30.0,
            allow_rewrite=False,
        )
        assert result.modify_ratio == 1.0
        assert result.rewrite_ratio == 0.0
        assert result.rebuild_ratio == 0.0
        assert any("不允许重写" in w for w in result.warnings)


# ============================================================================
# 8. test_supplement_not_allowed_warning
# ============================================================================

class TestSupplementNotAllowedWarning:
    """需要补充但用户不允许时，提示效果受限。"""

    def test_supplement_forbidden_with_high_rate(self):
        gate = PermissionGate()
        result = gate.check(
            current_rate=65.0,
            target_rate=30.0,
            allow_rewrite=True,
            allow_supplement=False,
            has_report=True,
            has_materials=False,
        )
        assert result.needs_confirmation is True
        assert any("不允许补充内容" in p for p in result.confirmation_prompts)


# ============================================================================
# 9. test_no_material_with_supplement_requires_confirmation
# ============================================================================

class TestNoMaterialWithSupplementRequiresConfirmation:
    """允许补充但无材料时，必须询问是否允许使用模型常识或联网资料。"""

    def test_no_material_with_supplement_needs_confirmation(self):
        gate = PermissionGate()
        result = gate.check(
            current_rate=60.0,
            target_rate=30.0,
            allow_rewrite=True,
            allow_supplement=True,
            has_report=True,
            has_materials=False,
        )
        assert result.needs_confirmation is True
        assert any("未提供" in p and "材料" in p
                    for p in result.confirmation_prompts)

    def test_evidence_plan_warns_no_material(self):
        ep = EvidencePlan()
        result = ep.plan(
            has_materials=False,
            allow_supplement=True,
        )
        assert result.can_use_model_knowledge is True
        assert any("保守补充" in w for w in result.warnings)
        assert len(result.needs_material_request) > 0


# ============================================================================
# 10. test_strategy_isolated
# ============================================================================

class TestStrategyIsolated:
    """计算机策略不得污染人力资源策略；人力资源策略不得包含计算机词。"""

    def test_hr_strategy_no_computer_terms(self):
        strategy = get_strategy("human_resource")
        computer_terms = [
            "Python", "Java", "Spring", "Django", "MySQL", "Redis",
            "Docker", "API", "HTTP", "JSON", "数据库表", "接口文档",
            "前端", "后端", "服务器部署",
        ]

        for section in ["abstract", "introduction", "literature_review",
                        "requirements", "design", "implementation",
                        "testing", "conclusion"]:
            unit = make_unit(section=section, action=ActionType.REWRITE)
            diagnosis = ParagraphDiagnosis(unit_uid="u1")
            guidance = strategy.rewrite_guidance(unit, diagnosis)
            for term in computer_terms:
                # Allow term only if it appears in a prohibition/warning context
                if term in guidance:
                    # Check that it's in a prohibition context (wider window)
                    idx = guidance.index(term)
                    context_start = max(0, idx - 60)
                    context = guidance[context_start:idx]
                    prohibition_markers = [
                        "不写", "禁止", "绝对", "不得", "避免",
                        "不要", "不加", "不插入", "不编造",
                    ]
                    assert any(p in context for p in prohibition_markers), \
                        f"HR section '{section}' uses computer term '{term}' " \
                        f"outside prohibition context: ...{guidance[max(0,idx-40):idx+20]}..."

    def test_computer_strategy_no_hr_exclusive_terms(self):
        strategy = get_strategy("computer")
        hr_exclusive_terms = [
            "绩效考核", "薪酬激励", "员工培训", "离职率",
            "人岗匹配", "胜任力素质", "招聘管理",
        ]

        for section in ["abstract", "introduction", "design",
                        "implementation", "testing", "conclusion"]:
            unit = make_unit(section=section, action=ActionType.REWRITE)
            diagnosis = ParagraphDiagnosis(unit_uid="u1")
            guidance = strategy.rewrite_guidance(unit, diagnosis)
            for term in hr_exclusive_terms:
                assert term not in guidance, \
                    f"Computer section '{section}' contains HR term '{term}'"


# ============================================================================
# 11. test_length_bidirectional_range
# ============================================================================

class TestLengthBidirectionalRange:
    """字数支持上下浮动。"""

    def test_default_ranges(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import TOTAL_RANGES
        # ideal: 95%-110%
        assert TOTAL_RANGES.ideal_low == 0.95
        assert TOTAL_RANGES.ideal_high == 1.10
        # acceptable: 90%-115%
        assert TOTAL_RANGES.acceptable_low == 0.90
        assert TOTAL_RANGES.acceptable_high == 1.15
        # hard: 85%-120%
        assert TOTAL_RANGES.hard_low == 0.85
        assert TOTAL_RANGES.hard_high == 1.20

    def test_compression_within_ideal(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        # 97% of original → ideal
        result = LengthPolicy.check_total(10000, 9700)
        assert result["passed"] is True
        assert result["band"] == "ideal"

    def test_compression_within_acceptable(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        # 92% of original → acceptable
        result = LengthPolicy.check_total(10000, 9200)
        assert result["passed"] is True
        assert result["band"] == "acceptable"

    def test_compression_below_hard_fails(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        # 80% → out of range
        result = LengthPolicy.check_total(10000, 8000)
        assert result["passed"] is False

    def test_expansion_above_hard_fails(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        # 125% → out of range
        result = LengthPolicy.check_total(10000, 12500)
        assert result["passed"] is False


# ============================================================================
# 12. test_outcome_failure_on_rate_increase
# ============================================================================

class TestOutcomeFailureOnRateIncrease:
    """AIGC 上升时判定失败。"""

    def test_rate_increase_fails(self):
        from thesis_risk_optimizer.validation.outcome_evaluator import OptimizationOutcomeEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import (
            AigcReport, ReportFragment, ColorBand
        )

        evaluator = OptimizationOutcomeEvaluator()
        before = AigcReport(
            source_path=Path("/f/before.docx"), overall_rate=76.67,
            fragments=[
                ReportFragment(text="A" * 1000, color_band=ColorBand.RED, index=0),
            ],
        )
        after = AigcReport(
            source_path=Path("/f/after.docx"), overall_rate=81.0,
            fragments=[
                ReportFragment(text="A" * 1200, color_band=ColorBand.RED, index=0),
            ],
        )

        result = evaluator.evaluate(
            before, after,
            before_doc_chars=20000, after_doc_chars=21000,
        )
        assert result.verdict == "failed"
        assert result.rollback_recommended is True
        assert any("上升" in r for r in result.failure_reasons)


# ============================================================================
# 13. test_outcome_failure_on_risk_chars_increase
# ============================================================================

class TestOutcomeFailureOnRiskCharsIncrease:
    """risk_chars 增加时判定失败。"""

    def test_risk_chars_increase_fails(self):
        from thesis_risk_optimizer.validation.risk_delta_evaluator import RiskDeltaEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import (
            AigcReport, ReportFragment, ColorBand
        )

        evaluator = RiskDeltaEvaluator()
        before = AigcReport(
            source_path=Path("/f/before.docx"), overall_rate=65.0,
            fragments=[
                ReportFragment(text="A" * 500, color_band=ColorBand.RED, index=0),
                ReportFragment(text="B" * 500, color_band=ColorBand.ORANGE, index=1),
            ],
        )
        after = AigcReport(
            source_path=Path("/f/after.docx"), overall_rate=50.0,
            fragments=[
                ReportFragment(text="A" * 600, color_band=ColorBand.RED, index=0),
                ReportFragment(text="B" * 600, color_band=ColorBand.ORANGE, index=1),
            ],
        )

        result = evaluator.evaluate(
            before, after,
            before_doc_chars=20000, after_doc_chars=25000,
        )
        assert result.verdict == "failed"
        assert any("风险字符" in r for r in result.failure_reasons)


# ============================================================================
# 14. test_final_report_not_success_when_unverified
# ============================================================================

class TestFinalReportNotSuccessWhenUnverified:
    """无法验证结果时，不得写成功式报告。"""

    def test_no_llm_warns(self):
        from thesis_risk_optimizer.validation.final_report import (
            FinalReportGenerator, ReportContext
        )
        from thesis_risk_optimizer.rewrite.rewrite_engine import BatchResult
        from thesis_risk_optimizer.analysis.rewrite_ratio_planner import RatioPlan

        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=10, planned_rewrite=8, planned_rebuild=2)
        batch = BatchResult(total=10, succeeded=0, failed=10)
        ctx = ReportContext(no_llm=True, processed_zero=True)

        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            [make_unit(f"u{i}", text="测试") for i in range(10)],
            "computer", "计算机策略", plan, batch, 65.0, False,
            context=ctx,
        )
        md = report.to_markdown()
        # Must NOT say "优化成功" or "优化完成" without qualification
        assert "优化成功" not in md
        assert "未实际处理" in md or "本轮处理了什么\n- 处理策略" in md
        # Must have warnings
        assert len(report.honest_warnings) > 0

    def test_no_report_warns_unverifiable(self):
        from thesis_risk_optimizer.validation.final_report import (
            FinalReportGenerator, ReportContext
        )
        from thesis_risk_optimizer.rewrite.rewrite_engine import BatchResult
        from thesis_risk_optimizer.analysis.rewrite_ratio_planner import RatioPlan

        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=5)
        batch = BatchResult(total=5, succeeded=5)
        ctx = ReportContext(has_report=False)

        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            [make_unit(f"u{i}", text="改写内容" * 10) for i in range(5)],
            "computer", "策略", plan, batch, None, False,
            context=ctx,
        )
        md = report.to_markdown()
        assert "无 AIGC 报告，无法判断" in md


# ============================================================================
# Extra: Integration test for the full workflow chain
# ============================================================================

class TestFullWorkflowChain:
    """Test that the 7-step workflow chain works end-to-end."""

    def test_intake_to_plan(self):
        """Complete flow from intake check to plan summary generation."""
        # Step 1: IntakeGate
        gate = IntakeGate()
        intake = gate.check(
            major="计算机科学与技术",
            title="基于Django的在线商城系统设计与实现",
            current_rate=65.93,
            target_rate=30.0,
            has_report=True,
            allow_rewrite=True,
            allow_supplement=True,
            has_materials=True,
        )
        assert intake.complete is True

        # Step 2: MajorRouter
        router = MajorRouter()
        route = router.route(intake.major)
        assert route.strategy_name == "computer"

        # Step 3: RiskPlanner
        planner = RiskPlanner()
        risk_plan = planner.plan(
            current_rate=intake.current_rate,
            target_rate=intake.target_rate,
            allow_rewrite=intake.allow_rewrite,
            allow_supplement=intake.allow_supplement,
            has_materials=intake.has_materials,
        )
        assert risk_plan.intensity == "high"
        assert risk_plan.rewrite_ratio > 0

        # Step 4: PermissionGate
        perm_gate = PermissionGate()
        perm = perm_gate.check(
            current_rate=intake.current_rate,
            target_rate=intake.target_rate,
            allow_rewrite=intake.allow_rewrite,
            allow_supplement=intake.allow_supplement,
            has_report=intake.has_report,
            has_materials=intake.has_materials,
        )
        # With all permissions and report, should be OK
        assert perm.can_proceed is True

        # Step 5: EvidencePlan
        ep = EvidencePlan()
        evidence = ep.plan(
            has_materials=intake.has_materials,
            allow_supplement=intake.allow_supplement,
        )
        assert len(evidence.available_sources) >= 3

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
        assert summary.strategy_name == "computer"
        text = summary.to_text()
        assert "65.93" in text
        assert "computer" in text

    def test_universal_light_warning_for_high_aigc(self):
        """Universal mode should warn when used for high-AIGC thesis."""
        router = MajorRouter()
        route = router.route("通用")
        assert route.strategy_name == "universal"
        assert "通用模式" in route.warning


# ============================================================================
# 15. New HR Conservative Mode & Reporting Tests
# ============================================================================

class TestHRConservativeModeAndReporting:
    def test_hr_conservative_caps_rebuild_after_assignment(self):
        from thesis_risk_optimizer.cli import _cap_hr_rebuild
        from thesis_risk_optimizer.document_io.text_units import TextUnit, ActionType, TextUnitType
        
        # Create 20 units all assigned to REBUILD
        units = []
        for i in range(20):
            unit = TextUnit(uid=str(i), unit_type=TextUnitType.PARAGRAPH, text="test", section="introduction", action=ActionType.REBUILD)
            units.append(unit)
            
        _cap_hr_rebuild(units, None)
        
        rebuild_count = sum(1 for u in units if u.action == ActionType.REBUILD)
        rewrite_count = sum(1 for u in units if u.action == ActionType.REWRITE)
        modify_count = sum(1 for u in units if u.action == ActionType.MODIFY)
        
        assert rebuild_count <= 5
        assert rewrite_count <= int(20 * 0.25)  # 5
        assert modify_count == 10

    def test_hr_conservative_does_not_process_all_red(self):
        from thesis_risk_optimizer.cli import _cap_hr_rebuild
        from thesis_risk_optimizer.document_io.text_units import TextUnit, ActionType, RiskLevel, TextUnitType
        
        # Suppose we have 50 red units
        units = []
        for i in range(50):
            unit = TextUnit(uid=str(i), unit_type=TextUnitType.PARAGRAPH, text="red", section="body", 
                            risk_level=RiskLevel.HIGH, action=ActionType.REBUILD)
            units.append(unit)
            
        _cap_hr_rebuild(units, None)
        
        rebuilds = sum(1 for u in units if u.action == ActionType.REBUILD)
        # Even if all are HIGH risk (red), they must not all be rebuilt
        assert rebuilds <= 5

    def test_hr_no_material_blocks_hr_term_injection(self):
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy
        from thesis_risk_optimizer.document_io.text_units import TextUnit, ActionType, TextUnitType
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis
        
        strategy = HumanResourceStrategy()
        assert "ROI、BEI、BES" in strategy.paragraph_transforms
        assert any("招聘漏斗" in fp for fp in strategy.FORBIDDEN_PATTERNS)
        
        # Test that conservative mode returns strict restrictions
        strategy.enable_conservative_mode()
        unit = TextUnit(uid="1", unit_type=TextUnitType.PARAGRAPH, text="test", section="introduction", action=ActionType.REWRITE)
        guidance = strategy.rewrite_guidance(unit, ParagraphDiagnosis("1"))
        assert "新增数据" in guidance and "不扩写" in guidance

    def test_hr_rate_increase_final_report_failed(self):
        from thesis_risk_optimizer.validation.final_report import FinalReport, ReportContext
        from thesis_risk_optimizer.cli import _inject_honest_verdict
        
        report = FinalReport(has_aigc_report=True)
        report.honest_warnings = []
        ctx = ReportContext(has_report=True, aigc_rate=76.67, post_aigc_rate=79.02)
        
        _inject_honest_verdict(report, ctx)
        
        assert len(report.honest_warnings) == 1
        assert "本轮优化失败" in report.honest_warnings[0]
        assert "76.67" in report.honest_warnings[0]
        assert "79.02" in report.honest_warnings[0]
        assert "建议回滚" in report.honest_warnings[0]
        
        md = report.to_markdown()
        assert "- 否 ❌" in md  # 是否达到目标
        assert "是 ❌ (AIGC 疑似率反升)" in md
        assert "不建议 ❌" in md
        assert "强烈建议回滚 ⚠️" in md

    def test_summary_does_not_use_processed_count_as_success(self):
        from thesis_risk_optimizer.validation.final_report import FinalReport
        
        report = FinalReport(processed_count=73)
        # Assuming has_aigc_report is false by default
        md = report.to_markdown()
        
        assert "未知 (无 AIGC 报告，无法判断是否达到降重目标)" in md
        # It must output processed count under '本轮处理了什么'
        assert "- 处理总段落数: 73" in md
        # It must not use 73 as success
        assert "修改成功率" not in md
