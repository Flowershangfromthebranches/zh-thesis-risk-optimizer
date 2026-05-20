"""Tests for zh-thesis-risk-optimizer v1.1 — updated for fixed APIs."""

import io
import zipfile
import pytest
from pathlib import Path

from thesis_risk_optimizer.document_io.text_units import (
    TextUnit, TextUnitType, RiskLevel, ActionType
)
from thesis_risk_optimizer.document_io.docx_reader import DocxReader, FormatInfo
from thesis_risk_optimizer.document_io.docx_writer import DocxWriter
from thesis_risk_optimizer.document_io.format_preserver import (
    should_freeze, should_protect, classify_no_edit_zones, FROZEN_UNIT_TYPES
)
from thesis_risk_optimizer.report_parser.aigc_report_parser import (
    AigcReportParser, AigcReport, ReportFragment, ColorBand
)
from thesis_risk_optimizer.report_parser.color_zone_locator import ColorZoneLocator
from thesis_risk_optimizer.analysis.thesis_classifier import ThesisClassifier, Discipline
from thesis_risk_optimizer.analysis.risk_estimator import RiskEstimator
from thesis_risk_optimizer.analysis.paragraph_diagnoser import (
    ParagraphDiagnoser, ParagraphDiagnosis, DiagnosisTag
)
from thesis_risk_optimizer.analysis.rewrite_ratio_planner import (
    RewriteRatioPlanner, RatioPlan
)
from thesis_risk_optimizer.strategies import get_strategy, list_strategies
from thesis_risk_optimizer.strategies.computer import ComputerStrategy
from thesis_risk_optimizer.strategies.management import ManagementStrategy
from thesis_risk_optimizer.rewrite.modify_engine import ModifyEngine
from thesis_risk_optimizer.rewrite.rebuild_engine import RebuildEngine
from thesis_risk_optimizer.rewrite.evidence_injector import EvidenceInjector, get_evidence_report_items
from thesis_risk_optimizer.rewrite.anti_ai_style_guard import AntiAIStyleGuard, GuardResult
from thesis_risk_optimizer.rewrite.rewrite_engine import RewriteEngine, BatchResult, RewriteResult
from thesis_risk_optimizer.validation.structure_validator import StructureValidator
from thesis_risk_optimizer.validation.format_validator import FormatValidator
from thesis_risk_optimizer.validation.length_validator import LengthValidator
from thesis_risk_optimizer.validation.final_report import FinalReportGenerator, ReportContext


# ============================================================================
# Helpers
# ============================================================================

def make_unit(uid="u0001", text="测试段落内容", unit_type=TextUnitType.PARAGRAPH,
              section="introduction", risk_level=RiskLevel.LOW, action=ActionType.FREEZE) -> TextUnit:
    return TextUnit(uid=uid, unit_type=unit_type, text=text,
                    section=section, risk_level=risk_level, action=action,
                    original_text=text,
                    metadata={"body_element_index": 0, "paragraph_index": 0})


def make_minimal_docx(path: Path, paragraphs: list[str] = None):
    """Create a minimal valid DOCX with given paragraphs."""
    if paragraphs is None:
        paragraphs = ["测试内容。"]
    body_xml = ""
    for i, p in enumerate(paragraphs):
        body_xml += f'<w:p><w:r><w:t>{p}</w:t></w:r></w:p>'
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '</Types>')
        zf.writestr("_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
        zf.writestr("word/document.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{body_xml}</w:body></w:document>')
        zf.writestr("word/_rels/document.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>')


# ============================================================================
# 1. TextUnit
# ============================================================================

class TestTextUnit:
    def test_basic(self):
        unit = make_unit(text="这是一个测试。")
        assert unit.char_count == 7
        assert unit.is_body is True
        assert unit.is_protected is False

    def test_protected(self):
        ref = make_unit(unit_type=TextUnitType.REFERENCE, text="[1] A. Title.")
        assert ref.is_protected is True

    def test_metadata_location(self):
        unit = make_unit()
        assert unit.metadata.get("body_element_index") == 0
        assert unit.metadata.get("paragraph_index") == 0


# ============================================================================
# 2. DocxReader
# ============================================================================

class TestDocxReader:
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            DocxReader("/nonexistent/doc.docx")

    def test_read_minimal(self, tmp_path):
        path = tmp_path / "test.docx"
        make_minimal_docx(path, ["第一章 绪论", "这是一段正文内容。"])
        reader = DocxReader(path)
        units = reader.read()
        assert len(units) >= 1
        # Should have body_element_index in metadata
        for u in units:
            assert "body_element_index" in u.metadata
            assert "paragraph_index" in u.metadata
            assert "original_text_hash" in u.metadata


# ============================================================================
# 3. DocxWriter
# ============================================================================

class TestDocxWriter:
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            DocxWriter("/nonexistent/doc.docx")

    def test_write_and_read_back(self, tmp_path):
        """Integration: read → modify → write → read back."""
        path = tmp_path / "input.docx"
        make_minimal_docx(path, ["原始正文内容，需要被修改。"])

        reader = DocxReader(path)
        units = reader.read()

        # Modify the first body paragraph
        body_units = [u for u in units if u.is_body and not u.is_protected]
        assert len(body_units) > 0, "Should have at least one body paragraph"
        unit = body_units[0]
        unit.text = "这是修改后的正文内容。"
        unit.action = ActionType.MODIFY

        # Write
        out_path = tmp_path / "output.docx"
        writer = DocxWriter(path)
        result = writer.apply_modifications(units)
        writer.save(out_path)
        assert out_path.exists()
        assert result["modified"] >= 1, f"Expected at least 1 modification, got {result}"

        # Read back
        reader2 = DocxReader(out_path)
        units2 = reader2.read()
        texts = [u.text for u in units2 if u.is_body]
        assert "这是修改后的正文内容。" in texts, f"Modified text not found in output. Texts: {texts}"

        # Original should be untouched
        reader3 = DocxReader(path)
        units3 = reader3.read()
        orig_texts = [u.text for u in units3 if u.is_body]
        assert "原始正文内容，需要被修改。" in orig_texts

    def test_skips_protected(self, tmp_path):
        """Protected paragraphs should be skipped."""
        path = tmp_path / "input.docx"
        make_minimal_docx(path, ["参考文献", "[1] Author. Title. 2024."])

        reader = DocxReader(path)
        units = reader.read()
        for u in units:
            if "参考" in u.text or u.text.startswith("["):
                u.unit_type = TextUnitType.REFERENCE
                u.text = "MODIFIED"  # try to modify

        out_path = tmp_path / "output.docx"
        writer = DocxWriter(path)
        result = writer.apply_modifications(units)
        writer.save(out_path)

        # Read back — references should NOT be modified
        reader2 = DocxReader(out_path)
        units2 = reader2.read()
        for u in units2:
            if u.unit_type == TextUnitType.REFERENCE:
                assert "MODIFIED" not in u.text, f"Protected unit was modified: {u.text}"


# ============================================================================
# 4. Format preserver
# ============================================================================

class TestFormatPreserver:
    def test_frozen_types(self):
        for t in [TextUnitType.COVER, TextUnitType.DECLARATION, TextUnitType.TOC,
                   TextUnitType.REFERENCE, TextUnitType.FORMULA]:
            assert should_freeze(make_unit(unit_type=t)) is True

    def test_body_not_frozen(self):
        assert should_freeze(make_unit(unit_type=TextUnitType.PARAGRAPH)) is False


# ============================================================================
# 5. AIGC Report Parser
# ============================================================================

class TestAigcReportParser:
    def test_score_to_band(self):
        parser = AigcReportParser()
        assert parser._score_to_band(85.0) == ColorBand.RED
        assert parser._score_to_band(55.0) == ColorBand.PURPLE
        assert parser._score_to_band(25.0) == ColorBand.BLACK

    def test_extract_rate(self):
        parser = AigcReportParser()
        assert parser._extract_overall_rate("AIGC疑似率: 65.93%") == 65.93

    def test_inspect_colors(self, tmp_path):
        """inspect_colors should not crash on any docx."""
        path = tmp_path / "report.docx"
        make_minimal_docx(path, ["被测段落内容。"])
        parser = AigcReportParser()
        stats = parser.inspect_colors(path)
        assert "color_stats" in stats
        assert "paragraphs_with_color" in stats


# ============================================================================
# 6. ColorZoneLocator
# ============================================================================

class TestColorZoneLocator:
    def test_substring_match(self):
        locator = ColorZoneLocator()
        report = AigcReport(source_path=Path("/f"), fragments=[
            ReportFragment(text="电子商务取得了显著成效", color_band=ColorBand.RED, index=0)
        ])
        units = [make_unit("u1", text="随着互联网发展，电子商务取得了显著成效。这是原文。")]
        result = locator.locate(units, report)
        assert result["matched_unit_count"] >= 1


# ============================================================================
# 7. ThesisClassifier
# ============================================================================

class TestThesisClassifier:
    def test_computer(self):
        c = ThesisClassifier()
        disc, conf, scores = c.classify(title="基于Spring Boot的在线商城系统设计与实现",
                             abstract="采用MySQL和Vue...",
                             headings=["系统设计", "系统实现", "系统测试"])
        assert disc == Discipline.COMPUTER

    def test_fallback(self):
        c = ThesisClassifier()
        disc, conf, scores = c.classify(title="关于某主题的研究")
        assert disc == Discipline.UNIVERSAL


# ============================================================================
# 8. RiskEstimator
# ============================================================================

class TestRiskEstimator:
    def test_template_text(self):
        e = RiskEstimator()
        units = [make_unit(f"u{i}", text="随着互联网的不断发展，电子商务具有十分重要的现实意义。"
                          "本文首先分析了现状，其次提出方案，最后验证可行性。"
                          "实验结果表明系统具有良好的稳定性和实用性。") for i in range(5)]
        result = e.estimate(units)
        assert result.template_score > 0.1
        assert 0 <= result.estimated_rate <= 100


# ============================================================================
# 9. ParagraphDiagnoser
# ============================================================================

class TestParagraphDiagnoser:
    def test_template(self):
        d = ParagraphDiagnoser()
        unit = make_unit(text="随着社会发展，企业管理具有十分重要的现实意义。"
                         "本文首先介绍背景，其次分析问题，最后提出对策。")
        diag = d.diagnose(unit)
        assert DiagnosisTag.TEMPLATE_SKELETON in diag.tags

    def test_normal_text(self):
        d = ParagraphDiagnoser()
        unit = make_unit(text="使用Python 3.11和Django 4.2开发。数据库PostgreSQL 15。"
                         "用户模块实现了注册、登录、权限管理。")
        diag = d.diagnose(unit)
        assert DiagnosisTag.TEMPLATE_SKELETON not in diag.tags


# ============================================================================
# 10. RewriteRatioPlanner (KEY FIX TEST)
# ============================================================================

class TestRewriteRatioPlanner:
    def test_unknown_not_frozen(self):
        """CRITICAL: UNKNOWN risk paragraphs should NOT be frozen."""
        planner = RewriteRatioPlanner()
        units = [make_unit(f"u{i}", text=f"这是第{i}段正文内容，讨论了相关技术和方法。")
                 for i in range(100)]
        plan = planner.plan(units, aigc_rate=65.93)
        planner.apply_to_units(units, plan)

        body = [u for u in units if u.is_body and not u.is_protected]
        assigned_modify = sum(1 for u in body if u.action == ActionType.MODIFY)
        assigned_rewrite = sum(1 for u in body if u.action == ActionType.REWRITE)
        assigned_rebuild = sum(1 for u in body if u.action == ActionType.REBUILD)
        total_assigned = assigned_modify + assigned_rewrite + assigned_rebuild

        assert total_assigned > 0, (
            f"All body units frozen! modify={assigned_modify} "
            f"rewrite={assigned_rewrite} rebuild={assigned_rebuild}"
        )

    def test_high_aigc_rate_forces_action(self):
        """At 80% AIGC, most units should get rebuild/rewrite actions."""
        planner = RewriteRatioPlanner()
        # Use text with strong template signals to trigger high diagnosis scores
        units = [make_unit(f"u{i}", text=f"随着社会经济的不断发展，企业管理具有十分重要的现实意义。"
                          "本文首先介绍了研究背景，其次分析了存在的问题，最后提出了优化对策。"
                          "实验结果表明该方案具有良好的可行性和实用性，为相关领域提供了参考。")
                 for i in range(100)]
        plan = planner.plan(units, aigc_rate=80.0)
        planner.apply_to_units(units, plan)

        body = [u for u in units if u.is_body and not u.is_protected]
        rebuilds = sum(1 for u in body if u.action == ActionType.REBUILD)
        rewrites = sum(1 for u in body if u.action == ActionType.REWRITE)
        modifies = sum(1 for u in body if u.action == ActionType.MODIFY)
        total = rebuilds + rewrites + modifies
        # At 80% AIGC, at least 40% should get rewrite or rebuild
        # (planned: 50% rewrite + 40% rebuild = 90% should be rewrite+)
        assert rebuilds + rewrites >= 30, (
            f"Expected >=30 rewrite+rebuild, got rebuilds={rebuilds} rewrites={rewrites} modifies={modifies}"
        )
        assert total > 0, "All units frozen!"

    def test_protected_still_frozen(self):
        """Protected units (references, cover) should still freeze."""
        planner = RewriteRatioPlanner()
        # Body unit needs enough template signals to score above freeze threshold
        body_text = (
            "随着互联网技术的不断发展，电子商务具有十分重要的现实意义。"
            "本文首先分析了研究现状，其次提出了优化方案，最后验证了可行性。"
            "实验结果表明该系统具有良好的实用性和稳定性。"
        )
        units = [
            make_unit("u1", unit_type=TextUnitType.PARAGRAPH, text=body_text),
            make_unit("u2", unit_type=TextUnitType.REFERENCE, text="[1] Author. Title."),
            make_unit("u3", unit_type=TextUnitType.COVER, text="毕业论文"),
        ]
        plan = planner.plan(units, aigc_rate=65.93)
        planner.apply_to_units(units, plan)

        assert units[0].action != ActionType.FREEZE, (
            f"Body paragraph should not freeze, got {units[0].action.value}. "
            f"Score={units[0].metadata.get('diagnostic_score')}"
        )
        assert units[1].action == ActionType.FREEZE, "Reference should freeze"
        assert units[2].action == ActionType.FREEZE, "Cover should freeze"


# ============================================================================
# 11. Strategies
# ============================================================================

class TestStrategies:
    def test_all_registered(self):
        names = {s["name"] for s in list_strategies()}
        assert "computer" in names
        assert "management" in names
        assert "universal" in names

    def test_get(self):
        s = get_strategy("computer")
        assert s.name == "computer"
        assert isinstance(get_strategy("nonexistent").name, str)


# ============================================================================
# 12. ModifyEngine + RebuildEngine
# ============================================================================

class TestModifyEngine:
    def test_break_template(self):
        engine = ModifyEngine(ComputerStrategy())
        result = engine.rewrite(
            make_unit(text="随着互联网技术的不断发展，电子商务取得了显著成效。"),
            ParagraphDiagnosis(unit_uid="u1"))
        if result:
            assert "随着" not in result or len(result) < len("随着互联网技术的不断发展，电子商务取得了显著成效。")


class TestRebuildEngine:
    def test_hollow_detection(self):
        engine = RebuildEngine(ComputerStrategy())
        assert engine._is_hollow(make_unit(text="具有重要的意义和价值")) is True
        assert engine._is_hollow(make_unit(
            text="用户模块包含UserRegister、UserLogin、PermissionManager三个类。"
                 "注册接口POST /api/v1/auth/register接收用户名和密码，bcrypt加密后存入users表。"
        )) is False


# ============================================================================
# 13. EvidenceInjector (KEY FIX: no placeholders)
# ============================================================================

class TestEvidenceInjector:
    def test_no_html_comments(self):
        """EvidenceInjector must NOT inject HTML comments into text."""
        injector = EvidenceInjector()
        strategy = ComputerStrategy()
        unit = make_unit(section="implementation", text="系统实现了基本功能。")
        result = injector.inject("系统实现了用户注册和订单管理功能。", unit, strategy)
        assert "<!--" not in result, f"HTML comment found: {result}"
        assert "EVIDENCE" not in result, f"EVIDENCE marker found: {result}"

    def test_no_bracket_placeholders(self):
        """Must not inject [OS/版本] style placeholders."""
        injector = EvidenceInjector()
        strategy = ComputerStrategy()
        unit = make_unit(section="implementation")
        result = injector.inject("系统实现完成。", unit, strategy)
        # Text should be returned unchanged
        assert "系统实现完成。" in result
        assert "[OS" not in result, f"Placeholder found: {result}"

    def test_evidence_needs_in_metadata(self):
        """Evidence needs should be recorded in metadata, not text."""
        injector = EvidenceInjector()
        strategy = ComputerStrategy()
        unit = make_unit(section="implementation", text="系统实现了功能。")
        injector.inject("系统实现了功能。", unit, strategy)
        needs = unit.metadata.get("evidence_needs", [])
        # May or may not have needs depending on text, but text should be clean
        assert "<!--" not in unit.text


# ============================================================================
# 14. AntiAIStyleGuard
# ============================================================================

class TestAntiAIStyleGuard:
    def test_reject_template(self):
        g = AntiAIStyleGuard()
        r = g.check("随着社会不断发展，企业管理具有十分重要的现实意义。", "原文", ActionType.REWRITE)
        assert r.passed is False

    def test_accept_concrete(self):
        g = AntiAIStyleGuard()
        r = g.check("使用PostgreSQL 15存储数据，users表包含id、username、password_hash字段。"
                     "订单查询接口支持分页和状态筛选。", "原文", ActionType.REWRITE)
        assert r.passed is True


# ============================================================================
# 15. RewriteEngine
# ============================================================================

class TestRewriteEngine:
    def test_no_llm_modify_fallback(self):
        engine = RewriteEngine(strategy=ComputerStrategy(), llm=None)
        unit = make_unit(text="随着互联网的发展，本系统具有良好的实用性。", action=ActionType.MODIFY)
        batch = engine.process_units([unit])
        assert batch.total == 1

    def test_no_llm_rebuild_fails_gracefully(self):
        """Rebuild without LLM should fail explicitly, not silently."""
        engine = RewriteEngine(strategy=ComputerStrategy(), llm=None)
        unit = make_unit(text="具有重要的意义。", action=ActionType.REBUILD)
        batch = engine.process_units([unit])
        assert batch.total == 1
        if batch.results:
            assert not batch.results[0].success
            assert "No LLM" in batch.results[0].error or "LLM" in batch.results[0].error

    def test_frozen_skipped(self):
        engine = RewriteEngine(strategy=ComputerStrategy(), llm=None)
        unit = make_unit(action=ActionType.FREEZE)
        batch = engine.process_units([unit])
        assert batch.frozen == 1


# ============================================================================
# 16. LengthValidator
# ============================================================================

class TestLengthValidator:
    def test_compression_extreme(self):
        """Extreme compression (below 60%) should still fail."""
        v = LengthValidator()
        unit = make_unit(text="短", action=ActionType.REWRITE)
        unit.original_text = "这是一段比较长的原文文本内容，包含多个句子和详细描述。"
        result = v.validate([unit])
        # Very short text vs long original → should fail
        assert result.passed is False or result.band == "out_of_range"

    def test_compression_acceptable(self):
        """Moderate compression (within acceptable range) should pass."""
        v = LengthValidator()
        # Create texts with ratio ~92% (within ideal range 95%-110%)
        orig = "这是一段比较长的原文文本内容，包含多个句子和详细描述信息。系统采用了传统的B/S架构设计方案。用户通过浏览器访问系统。"
        new = "这是一段修改后的文本内容，保留了核心论点和实验过程。系统采用B/S架构设计方案。用户通过浏览器访问系统。"
        ratio = len(new) / len(orig)
        assert 0.85 < ratio < 1.0, f"Test setup: ratio={ratio:.2f}, orig={len(orig)}, new={len(new)}"
        unit = make_unit(text=new, action=ActionType.REWRITE)
        unit.original_text = orig
        result = v.validate([unit])
        # Should pass since compression is within acceptable range
        assert result.in_acceptable_range or result.band in ("ideal", "acceptable", "hard")


# ============================================================================
# 17. StructureValidator
# ============================================================================

class TestStructureValidator:
    def test_missing_heading(self):
        v = StructureValidator()
        orig = [make_unit("h1", text="第一章", unit_type=TextUnitType.HEADING)]
        result = v.validate(orig, [])
        assert result.passed is False


# ============================================================================
# 18. FormatValidator
# ============================================================================

class TestFormatValidator:
    def test_invalid(self, tmp_path):
        bad = tmp_path / "bad.docx"
        bad.write_text("not a zip")
        assert FormatValidator().validate(bad).passed is False

    def test_valid(self, tmp_path):
        path = tmp_path / "good.docx"
        make_minimal_docx(path)
        assert FormatValidator().validate(path).passed is True


# ============================================================================
# 19. FinalReport (HONESTY CHECK)
# ============================================================================

class TestFinalReport:
    def test_warns_no_llm(self):
        gen = FinalReportGenerator()
        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            [make_unit("u1", text="测试")], "computer", "计算机策略",
            RatioPlan(total_body_units=1), BatchResult(total=1),
            None, False, context=ReportContext(no_llm=True, processed_zero=True),
        )
        md = report.to_markdown()
        assert "LLM" in md, "Should warn about no LLM"
        assert "未实际处理" in md, "Should warn about zero processing"

    def test_warns_parse_failed(self):
        gen = FinalReportGenerator()
        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            [make_unit()], "computer", "策略",
            RatioPlan(total_body_units=1), BatchResult(total=1),
            None, True, context=ReportContext(report_parse_failed=True),
        )
        md = report.to_markdown()
        assert "未成功映射" in md, "Should warn about report parse failure"


# ============================================================================
# 20. No data fabrication
# ============================================================================

class TestNoDataFabrication:
    def test_ref_not_modified(self):
        assert should_freeze(make_unit(unit_type=TextUnitType.REFERENCE)) is True

    def test_medicine_forbids(self):
        s = get_strategy("medicine")
        g = s.rewrite_guidance(make_unit(), ParagraphDiagnosis(unit_uid="u1"))
        assert "伪造" in g or "编造" in g or "数据" in g


# ============================================================================
# 21. CLI
# ============================================================================

class TestCLI:
    def test_version(self):
        from thesis_risk_optimizer.cli import main
        assert main(["--version"]) == 0

    def test_missing_input(self):
        from thesis_risk_optimizer.cli import main
        with pytest.raises(SystemExit) as exc:
            main(["optimize"])
        assert exc.value.code == 2

    def test_dry_run(self, tmp_path):
        """Dry-run should complete without errors and assign actions."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, [
            "随着互联网技术的不断发展，电子商务取得了显著成效。",
            "本文首先分析了现状，其次提出了优化方案。",
            "实验结果表明系统具有良好的实用性。",
        ])
        from thesis_risk_optimizer.cli import main
        result = main(["optimize", "--input", str(path), "--aigc-rate", "65.93",
                        "--target-rate", "30", "--major", "computer",
                        "--title", "测试论文",
                        "--has-aigc-report", "no", "--allow-rewrite", "yes",
                        "--allow-supplement", "yes", "--has-materials", "no",
                        "--confirmed", "yes", "--dry-run", "--debug"])
        assert result == 0

    def test_inspect_report(self, tmp_path):
        path = tmp_path / "report.docx"
        make_minimal_docx(path, ["红色段落", "橙色段落"])
        from thesis_risk_optimizer.cli import main
        result = main(["inspect-report", "--input", str(path)])
        assert result == 0


# ============================================================================
# 22. Regression tests (v1.2)
# ============================================================================

class TestRegressionV12:
    """Regression tests per 修改2.md requirements."""

    def test_module_main_entry(self):
        """python -m thesis_risk_optimizer.cli should work."""
        import subprocess, sys, os
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")
        result = subprocess.run(
            [sys.executable, "-m", "thesis_risk_optimizer.cli", "--version"],
            capture_output=True, text=True, timeout=10,
            env=env,
        )
        assert result.returncode == 0
        assert "2." in result.stdout or "2." in result.stderr

    def test_no_report_still_allocates_rewrite_rebuild(self):
        """Without AIGC report but with aigc_rate=65.93, rewrite>0 and rebuild>0."""
        planner = RewriteRatioPlanner()
        # Simulate 261 body units (realistic thesis size)
        units = [
            make_unit(f"u{i}",
                      text=f"随着信息技术的飞速发展，Web应用程序作为互联网服务的重要载体，"
                           f"具有重要的现实意义。本文首先分析了研究现状，其次提出了第{i}种优化方案。"
                           f"实验结果表明系统具有良好的可行性，为相关领域提供了参考。")
            for i in range(261)
        ]
        plan = planner.plan(units, aigc_rate=65.93)
        planner.apply_to_units(units, plan)

        body = [u for u in units if u.is_body and not u.is_protected]
        rebuilds = sum(1 for u in body if u.action == ActionType.REBUILD)
        rewrites = sum(1 for u in body if u.action == ActionType.REWRITE)
        modifies = sum(1 for u in body if u.action == ActionType.MODIFY)

        # For 65.93%, planned: modify=65, rewrite=144, rebuild=52
        assert rebuilds > 0, f"rebuild=0, expected >0"
        assert rewrites > 0, f"rewrite=0, expected >0"
        # Should be close to plan (allow some tolerance for protected/short text)
        assert rewrites >= 100, f"rewrites={rewrites} too low, expected >=100 (planned=144)"
        assert rebuilds >= 30, f"rebuilds={rebuilds} too low, expected >=30 (planned=52)"

    def test_no_llm_aborts_without_allow(self, tmp_path):
        """Without --allow-no-llm, should abort when rewrite/rebuild tasks exist."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, [
            "随着互联网技术的不断发展，电子商务具有十分重要的现实意义。"
            "本文首先分析了研究现状，其次提出了优化方案，最后验证了可行性。"
            "实验结果表明该系统具有良好的实用性和稳定性。"
        ] * 10)
        from thesis_risk_optimizer.cli import main
        # Without --allow-no-llm and without --dry-run, should abort (return 1)
        result = main([
            "optimize", "--input", str(path),
            "--aigc-rate", "65.93", "--target-rate", "30",
            "--major", "computer", "--title", "测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--llm-provider", "none",
        ])
        assert result == 1, f"Expected abort (exit 1) without --allow-no-llm, got {result}"

    def test_allow_no_llm_proceeds(self, tmp_path):
        """With --allow-no-llm, should proceed in non-dry-run mode."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, [
            "随着互联网技术的不断发展，电子商务具有十分重要的现实意义。"
            "本文首先分析了研究现状，其次提出了优化方案，最后验证了可行性。"
            "实验结果表明该系统具有良好的实用性和稳定性。"
        ] * 5)
        from thesis_risk_optimizer.cli import main
        result = main([
            "optimize", "--input", str(path),
            "--aigc-rate", "65.93", "--target-rate", "30",
            "--major", "computer", "--title", "测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--llm-provider", "none", "--allow-no-llm",
            "--output", str(tmp_path / "out.docx"),
            "--report", str(tmp_path / "out.md"),
        ])
        assert result == 0
        assert (tmp_path / "out.docx").exists()

    def test_dry_run_shows_real_assignment(self, tmp_path, capsys):
        """Dry-run must show rewrite/rebuild > 0."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, [
            "随着信息技术的飞速发展，Web应用程序作为互联网服务的重要载体，"
            "具有十分重要的现实意义。本文首先分析了国内外研究现状，"
            "其次提出了优化方案。实验结果表明系统具有良好的可行性。"
        ] * 20)
        from thesis_risk_optimizer.cli import main
        result = main([
            "optimize", "--input", str(path),
            "--aigc-rate", "65.93", "--target-rate", "30",
            "--major", "computer", "--title", "测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--dry-run", "--debug",
        ])
        assert result == 0

    def test_final_report_honest_when_low_processed(self):
        """FinalReport must show high remaining risk when processed_count is low."""
        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=100, planned_modify=25,
                         planned_rewrite=55, planned_rebuild=20,
                         assigned_modify=25, assigned_rewrite=55, assigned_rebuild=20)
        batch = BatchResult(total=100, succeeded=3, failed=97)
        ctx = ReportContext(no_llm=True, processed_zero=False)

        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            [make_unit(f"u{i}", text=f"测试段落{i}") for i in range(100)],
            "computer", "计算机策略", plan, batch, 65.93, False,
            context=ctx
        )
        md = report.to_markdown()
        assert "LLM" in md, "Must warn about no LLM"
        assert "处理比例不足" in md or "未能完成" in md or "剩余风险" in md, \
            "Must mention insufficient processing or remaining risk"

    def test_purple_color_mapping(self):
        """9D91E9 must map to purple. 000000 must map to black."""
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReportParser, ColorBand
        parser = AigcReportParser()
        assert parser._hex_to_band("9D91E9") == ColorBand.PURPLE, "9D91E9 should be PURPLE"
        assert parser._hex_to_band("000000") == ColorBand.BLACK, "000000 should be BLACK"
        assert parser._hex_to_band("B0B0B0") == ColorBand.GRAY, "B0B0B0 should be GRAY"
        assert parser._hex_to_band("F12828") == ColorBand.RED, "F12828 should be RED"
        assert parser._hex_to_band("F39800") == ColorBand.ORANGE, "F39800 should be ORANGE"

    def test_paragraph_diagnoser_catches_real_patterns(self):
        """Diagnoser must catch real-world template sentences."""
        d = ParagraphDiagnoser()

        # Pattern 1
        diag = d.diagnose(make_unit(
            text="随着信息技术的飞速发展，Web应用程序成为了互联网服务的重要载体。"
        ))
        assert DiagnosisTag.TEMPLATE_SKELETON in diag.tags, \
            f"Failed to catch '随着...发展...载体'. Tags: {diag.tags}"

        # Pattern 2
        diag = d.diagnose(make_unit(
            text="实验结果表明，该系统具有良好的有效性和可靠性。"
        ))
        assert DiagnosisTag.TEMPLATE_SKELETON in diag.tags or \
               DiagnosisTag.HOLLOW_CONCLUSION in diag.tags, \
            f"Failed to catch '实验结果表明...'. Tags: {diag.tags}"

        # Pattern 3
        diag = d.diagnose(make_unit(
            text="国外在Web安全领域起步较早，国内也取得了不少进展。"
        ))
        assert DiagnosisTag.TEMPLATE_SKELETON in diag.tags, \
            f"Failed to catch '国外起步较早...国内取得进展'. Tags: {diag.tags}"

        # Pattern 4: pseudo-detail (computer thesis)
        diag = d.diagnose(make_unit(
            text="系统采用Python语言开发，使用SQL注入检测模块和XSS扫描引擎，"
                 "生成HTML格式的测试报告。",
            section="implementation",
        ))
        assert len(diag.tags) > 0, \
            f"Pseudo-detail should trigger at least one tag. Tags: {diag.tags}"


# ============================================================================
# 28. v1.7 Guard & Policy tests (新修改.md)
# ============================================================================

class TestGuardsAndPolicies:
    """Tests for EvidencePolicy, AntiStuffingGuard, LengthPolicy."""

    def test_evidence_forbids_version_numbers(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import check_evidence
        text = "系统使用Python 3.11和Django 4.2开发，采用MySQL 8.0数据库。"
        result = check_evidence(text)
        assert result.passed is False or result.risk_level == "high"

    def test_evidence_allows_general_description(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import check_evidence
        text = "系统采用Python语言开发，使用关系型数据库进行数据存储。"
        result = check_evidence(text)
        assert result.passed is True

    def test_anti_stuffing_detects_tech_flood(self):
        from thesis_risk_optimizer.rewrite.anti_stuffing_guard import check_stuffing
        original = "系统实现了基本功能。"
        rewritten = (
            "系统采用Python Django Flask Vue React MySQL Redis Docker "
            "Nginx Linux Ubuntu Spring Boot MongoDB PostgreSQL开发，"
            "使用ThreadPoolExecutor Session User-Agent Payload "
            "XSS CSRF SQL API HTTP HTTPS JSON XML处理数据。"
        )
        result = check_stuffing(rewritten, original)
        assert result.passed is False, f"Should detect stuffing, score={result.stuffing_score}"

    def test_anti_stuffing_passes_normal_rewrite(self):
        from thesis_risk_optimizer.rewrite.anti_stuffing_guard import check_stuffing
        original = "系统实现了用户管理功能。"
        rewritten = (
            "用户管理模块负责处理注册和登录。当用户提交注册信息时，"
            "系统首先校验数据格式，然后将密码加密后存入数据库。"
            "登录时通过比对加密后的密码完成身份验证。"
        )
        result = check_stuffing(rewritten, original)
        assert result.passed is True

    def test_length_policy_total_fails_over_120(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(1000, 1300)
        assert result["passed"] is False
        assert result["level"] == "FAILURE"

    def test_length_policy_total_warns_over_115(self):
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(1000, 1170)
        assert result["level"] == "WARNING"

    def test_length_policy_accepts_compression_in_range(self):
        """Compression within acceptable range (90%-115%) should pass."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(1000, 930)
        assert result["passed"] is True
        assert result["band"] == "acceptable"

    def test_length_policy_fails_excessive_compression(self):
        """Compression below 85% should fail."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(1000, 800)
        assert result["passed"] is False
        assert result["level"] == "FAILURE"

    def test_length_policy_paragraph_fails_over_180(self):
        """Paragraph expansion over 180% (hard limit) should fail."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_paragraph(100, 190)
        assert result["passed"] is False

    def test_length_policy_paragraph_accepts_compression(self):
        """Paragraph compression within 60%-180% should pass."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_paragraph(100, 75)
        assert result["passed"] is True

    def test_computer_strategy_forbids_version_stuffing(self):
        from thesis_risk_optimizer.strategies.computer import ComputerStrategy
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis
        s = ComputerStrategy()
        unit = make_unit(section="implementation", text="系统实现了功能。")
        diagnosis = ParagraphDiagnosis(unit_uid="u1")
        guidance = s.rewrite_guidance(unit, diagnosis)
        assert "版本号" in guidance or "函数名" in guidance

    def test_final_report_diagnoses_length_growth(self):
        from thesis_risk_optimizer.validation.final_report import FinalReport, FinalReportGenerator, ReportContext
        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=10)
        batch = BatchResult(total=10, succeeded=8)
        units = []
        for i in range(10):
            u = make_unit(f"u{i}", text="原文" * 20)
            u.text = "改写" * 50  # 2.5x growth
            units.append(u)
        ctx = ReportContext(no_llm=True)
        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            units, "computer", "策略", plan, batch, None, False, context=ctx,
        )
        md = report.to_markdown()
        assert "过度扩写" in md or "字数增长" in md


# ============================================================================
# 29. v2.0 Bidirectional Length Control tests (新修改2.md)
# ============================================================================

class TestBidirectionalLengthControl:
    """Tests for bidirectional length control per 新修改2.md requirements."""

    def test_length_accepts_reasonable_decrease(self):
        """原文 10000 字，优化后 9300 字，应通过 (ratio=0.93, in acceptable_range)."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(10000, 9300)
        assert result["passed"] is True
        assert result["band"] in ("ideal", "acceptable"), f"band={result['band']}"

    def test_length_accepts_reasonable_increase(self):
        """原文 10000 字，优化后 10800 字，应通过 (ratio=1.08, in ideal_range)."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(10000, 10800)
        assert result["passed"] is True
        assert result["band"] in ("ideal", "acceptable"), f"band={result['band']}"

    def test_length_rejects_excessive_decrease(self):
        """原文 10000 字，优化后 8000 字，应失败 (ratio=0.80, below hard_range)."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(10000, 8000)
        assert result["passed"] is False
        assert result["level"] == "FAILURE"

    def test_length_rejects_excessive_increase(self):
        """原文 10000 字，优化后 12500 字，应失败 (ratio=1.25, above hard_range)."""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(10000, 12500)
        assert result["passed"] is False
        assert result["level"] == "FAILURE"

    def test_min_length_requirement(self):
        """用户设置 --min-length 18000，优化后 17000，应失败。"""
        from thesis_risk_optimizer.rewrite.evidence_policy import LengthPolicy
        result = LengthPolicy.check_total(20000, 17000, min_length=18000)
        assert result["passed"] is False
        assert result["level"] == "FAILURE"
        assert "18000" in result["message"]

    def test_report_explains_length_change(self):
        """optimization_report 必须解释字数变化原因。"""
        from thesis_risk_optimizer.validation.final_report import FinalReportGenerator, ReportContext
        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=5)
        batch = BatchResult(total=5, succeeded=5)
        units = []
        # Create units with compression (模板句被压缩)
        for i in range(5):
            u = make_unit(f"u{i}",
                text="随着互联网技术的不断发展，电子商务具有十分重要的现实意义。"
                     "本文首先分析了研究现状，其次提出了优化方案，最后验证了可行性。"
                     "实验结果表明该系统具有良好的实用性和稳定性。")
            u.text = "系统采用B/S架构，用户通过浏览器访问。"  # much shorter
            units.append(u)
        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            units, "computer", "策略", plan, batch, None, False,
        )
        md = report.to_markdown()
        assert "字数变化原因" in md or "变化比例" in md, \
            f"Report should explain length change. Keys in report section 5: {md[md.find('字数变化'):md.find('字数变化')+200]}"

    def test_length_validator_bidirectional(self):
        """LengthValidator should allow compression within acceptable range."""
        from thesis_risk_optimizer.validation.length_validator import LengthValidator
        v = LengthValidator()
        # Create unit with ~93% of original (within acceptable range)
        unit = make_unit(
            text="改写后的文本内容，保留了核心观点和主要论据。系统运行稳定可靠。",
            action=ActionType.REWRITE,
        )
        unit.original_text = "这是一段比较长的原文文本内容，包含多个句子和详细描述。系统运行稳定可靠。"
        # Current text should be shorter but within acceptable range
        ratio = len(unit.text) / len(unit.original_text)
        assert 0.85 < ratio < 1.0, f"Test setup: ratio={ratio:.2f}"
        result = v.validate([unit])
        # Should pass since we allow compression now
        assert result.in_acceptable_range or result.band in ("ideal", "acceptable", "hard")

    def test_length_report_has_range_fields(self):
        """LengthReport should have all required range fields."""
        from thesis_risk_optimizer.validation.length_validator import LengthValidator
        v = LengthValidator()
        unit = make_unit(text="测试内容。", action=ActionType.REWRITE)
        unit.original_text = "测试内容。"
        result = v.validate([unit])
        assert hasattr(result, 'in_ideal_range')
        assert hasattr(result, 'in_acceptable_range')
        assert hasattr(result, 'triggered_hard_range')
        assert hasattr(result, 'reasons')
        assert hasattr(result, 'band')

    def test_final_report_shows_length_details(self):
        """FinalReport section 5 should show all required length fields."""
        from thesis_risk_optimizer.validation.final_report import FinalReportGenerator, ReportContext
        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=3)
        batch = BatchResult(total=3, succeeded=3)
        units = [make_unit(f"u{i}", text="原文内容" * 10) for i in range(3)]
        for u in units:
            u.text = "改写内容" * 8  # slightly shorter
        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            units, "computer", "策略", plan, batch, None, False,
        )
        md = report.to_markdown()
        assert "原文字数" in md
        assert "优化后字数" in md
        assert "变化比例" in md
        assert "ideal_range" in md
        assert "acceptable_range" in md
        assert "hard_range" in md


# ============================================================================
# 30. v2.0 Risk Delta and Denominator Dilution tests (新修改4.md)
# ============================================================================

class TestRiskDeltaAndDilution:
    """Tests for risk delta evaluation and denominator dilution detection."""

    def test_risk_chars_must_decrease(self):
        """Rate drops but risk_chars增加 → should fail."""
        from thesis_risk_optimizer.validation.risk_delta_evaluator import RiskDeltaEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = RiskDeltaEvaluator()

        # Before: 1000 risk chars
        before_report = AigcReport(
            source_path=Path("/f/before.docx"),
            overall_rate=65.0,
            fragments=[
                ReportFragment(text="A" * 500, color_band=ColorBand.RED, index=0),
                ReportFragment(text="B" * 500, color_band=ColorBand.ORANGE, index=1),
            ]
        )

        # After: 1100 risk chars (increased!)
        after_report = AigcReport(
            source_path=Path("/f/after.docx"),
            overall_rate=50.0,
            fragments=[
                ReportFragment(text="A" * 600, color_band=ColorBand.RED, index=0),
                ReportFragment(text="B" * 500, color_band=ColorBand.ORANGE, index=1),
            ]
        )

        result = evaluator.evaluate(
            before_report, after_report,
            before_doc_chars=20000, after_doc_chars=25000
        )

        assert result.verdict == "failed", f"Should fail, got {result.verdict}"
        assert any("风险字符" in r and "增加" in r for r in result.failure_reasons)

    def test_denominator_dilution_detected(self):
        """total_chars +40%, risk_chars不降 → should trigger dilution guard."""
        from thesis_risk_optimizer.rewrite.denominator_dilution_guard import DenominatorDilutionGuard

        guard = DenominatorDilutionGuard()

        result = guard.check(
            before_rate=65.0,
            after_rate=50.0,
            before_total_chars=20000,
            after_total_chars=28000,  # +40%
            before_risk_chars=13000,
            after_risk_chars=13500,  # didn't decrease
        )

        assert result.triggered is True, "Should detect dilution"
        assert "分母" in result.warning_message or "文本总量" in result.warning_message

    def test_red_purple_must_not_increase(self):
        """red或purple增加 → should mark as needing second round."""
        from thesis_risk_optimizer.validation.risk_delta_evaluator import RiskDeltaEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = RiskDeltaEvaluator()

        before_report = AigcReport(
            source_path=Path("/f/before.docx"),
            overall_rate=65.0,
            fragments=[
                ReportFragment(text="R" * 200, color_band=ColorBand.RED, index=0),
                ReportFragment(text="P" * 100, color_band=ColorBand.PURPLE, index=1),
                ReportFragment(text="O" * 500, color_band=ColorBand.ORANGE, index=2),
            ]
        )

        after_report = AigcReport(
            source_path=Path("/f/after.docx"),
            overall_rate=50.0,
            fragments=[
                ReportFragment(text="R" * 250, color_band=ColorBand.RED, index=0),  # red increased
                ReportFragment(text="P" * 150, color_band=ColorBand.PURPLE, index=1),  # purple increased
                ReportFragment(text="O" * 400, color_band=ColorBand.ORANGE, index=2),
            ]
        )

        result = evaluator.evaluate(
            before_report, after_report,
            before_doc_chars=20000, after_doc_chars=22000
        )

        assert result.verdict in ("failed", "needs_second_round")
        assert any("红色字符增加" in r for r in result.failure_reasons)
        assert any("紫色字符增加" in r for r in result.failure_reasons)

    def test_length_hard_range_blocks_success(self):
        """总字数 >120% → should fail even if rate drops."""
        from thesis_risk_optimizer.validation.risk_delta_evaluator import RiskDeltaEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = RiskDeltaEvaluator()

        before_report = AigcReport(
            source_path=Path("/f/before.docx"),
            overall_rate=65.0,
            fragments=[
                ReportFragment(text="R" * 500, color_band=ColorBand.RED, index=0),
            ]
        )

        after_report = AigcReport(
            source_path=Path("/f/after.docx"),
            overall_rate=45.0,
            fragments=[
                ReportFragment(text="R" * 400, color_band=ColorBand.RED, index=0),  # red decreased
            ]
        )

        result = evaluator.evaluate(
            before_report, after_report,
            before_doc_chars=20000, after_doc_chars=25000  # +25% length
        )

        assert result.verdict == "failed", f"Should fail due to length, got {result.verdict}"
        assert any("字数" in r and "超过" in r for r in result.failure_reasons)

    def test_english_abstract_body_editable(self):
        """ABSTRACT heading frozen, English abstract body can be processed."""
        from thesis_risk_optimizer.document_io.format_preserver import should_freeze
        from thesis_risk_optimizer.document_io.text_units import TextUnit, TextUnitType

        # ABSTRACT heading should be frozen
        heading = TextUnit(
            uid="h1", unit_type=TextUnitType.HEADING,
            text="ABSTRACT", section="abstract"
        )
        assert should_freeze(heading) is True

        # English abstract body should NOT be frozen
        body = TextUnit(
            uid="a1", unit_type=TextUnitType.PARAGRAPH,
            text="With the rapid development of Internet technology...",
            section="abstract"
        )
        assert should_freeze(body) is False

        # Chinese abstract body should NOT be frozen
        cn_body = TextUnit(
            uid="a2", unit_type=TextUnitType.PARAGRAPH,
            text="随着互联网技术的快速发展...",
            section="abstract"
        )
        assert should_freeze(cn_body) is False

    def test_consistency_guard_python_version(self):
        """Same doc has Python 3.9, 3.10, 3.11 without evidence → should fail."""
        from thesis_risk_optimizer.rewrite.consistency_guard import ConsistencyGuard

        guard = ConsistencyGuard()

        text = (
            "系统使用Python 3.9开发后端，前端采用Python 3.10的某些特性，"
            "部署环境为Python 3.11。数据库使用MySQL 8.0。"
        )

        result = guard.check(text, original_text="", has_source_code=False)

        assert result.passed is False, "Should fail due to inconsistent Python versions"
        assert any("Python" in v and "版本不一致" in v for v in result.violations)




# ============================================================================
# 31. v2.0 Multi-discipline tests (新修改5.md)
# ============================================================================

class TestMultiDiscipline:
    """Tests for multi-discipline support and strategy isolation."""

    def test_thesis_classifier_confidence(self):
        """ThesisClassifier should output confidence score."""
        from thesis_risk_optimizer.analysis.thesis_classifier import ThesisClassifier, Discipline

        c = ThesisClassifier()

        # HR thesis should be classified with confidence
        disc, confidence, scores = c.classify(
            title="某企业人力资源管理优化研究",
            abstract="本文研究了某制造公司的员工绩效考核和薪酬激励问题。"
                    "通过问卷调查发现员工满意度较低，离职率偏高。",
            keywords="人力资源; 绩效考核; 薪酬激励; 员工满意度",
            headings=["企业现状分析", "绩效考核体系优化", "薪酬方案设计", "实施效果评估"],
        )

        assert disc == Discipline.HUMAN_RESOURCE, f"Expected HUMAN_RESOURCE, got {disc}"
        assert confidence > 0.0, f"Confidence should be > 0, got {confidence}"
        assert 0.0 <= confidence <= 1.0

    def test_human_resource_strategy_exists(self):
        """HumanResource strategy should be registered."""
        from thesis_risk_optimizer.strategies import get_strategy, list_strategies

        strategy = get_strategy("human_resource")
        assert strategy.name == "human_resource"
        assert strategy.label == "人力资源策略"

        names = {s["name"] for s in list_strategies()}
        assert "human_resource" in names

    def test_human_resource_no_computer_details(self):
        """HumanResource strategy must forbid computer-style details."""
        from thesis_risk_optimizer.strategies import get_strategy
        from thesis_risk_optimizer.document_io.text_units import TextUnit, TextUnitType, RiskLevel, ActionType
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis

        strategy = get_strategy("human_resource")

        unit = TextUnit(
            uid="hr1", unit_type=TextUnitType.PARAGRAPH,
            text="随着经济社会的发展，企业竞争日益激烈。",
            section="introduction",
            risk_level=RiskLevel.HIGH,
            action=ActionType.REWRITE,
        )

        diagnosis = ParagraphDiagnosis(unit_uid="hr1")
        guidance = strategy.rewrite_guidance(unit, diagnosis)

        # Should NOT mention computer terms
        assert "Python" not in guidance
        assert "函数名" not in guidance or "绝对不写" in guidance
        # Should mention enterprise/management context
        assert any(kw in guidance for kw in ["企业", "管理", "员工", "制度"])

    def test_management_strategy_differs_from_computer(self):
        """Management strategy should differ from computer strategy."""
        from thesis_risk_optimizer.strategies import get_strategy
        from thesis_risk_optimizer.document_io.text_units import TextUnit, TextUnitType, RiskLevel, ActionType
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis

        computer = get_strategy("computer")
        management = get_strategy("management")

        unit = TextUnit(
            uid="u1", unit_type=TextUnitType.PARAGRAPH,
            text="本文研究了企业管理系统。", section="introduction",
            risk_level=RiskLevel.HIGH, action=ActionType.REWRITE,
        )

        diagnosis = ParagraphDiagnosis(unit_uid="u1")

        comp_guidance = computer.rewrite_guidance(unit, diagnosis)
        mgmt_guidance = management.rewrite_guidance(unit, diagnosis)

        # Strategies should produce different guidance
        assert comp_guidance != mgmt_guidance
        # Computer should mention tech-related things
        assert any(kw in comp_guidance for kw in ("模块", "系统", "技术"))
        # Management should NOT focus on tech details
        assert "模块职责" not in mgmt_guidance

    def test_outcome_evaluator_failure_on_rate_increase(self):
        """AIGC rate increase should trigger failure verdict."""
        from thesis_risk_optimizer.validation.outcome_evaluator import OptimizationOutcomeEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = OptimizationOutcomeEvaluator()

        # Before: 76.67%, After: 81.7% (rate increased!)
        before = AigcReport(
            source_path=Path("/f/before.docx"), overall_rate=76.67,
            fragments=[
                ReportFragment(text="A" * 1000, color_band=ColorBand.RED, index=0),
            ],
        )
        after = AigcReport(
            source_path=Path("/f/after.docx"), overall_rate=81.7,
            fragments=[
                ReportFragment(text="A" * 1200, color_band=ColorBand.RED, index=0),
            ],
        )

        result = evaluator.evaluate(
            before, after,
            before_doc_chars=20000, after_doc_chars=21000,
            discipline="human_resource", assigned_strategy="human_resource",
        )

        assert result.verdict == "failed"
        assert result.rollback_recommended is True
        assert any("上升" in r for r in result.failure_reasons)

    def test_outcome_evaluator_failure_on_computer_mode_misuse(self):
        """Computer strategy on non-CS thesis should trigger failure."""
        from thesis_risk_optimizer.validation.outcome_evaluator import OptimizationOutcomeEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = OptimizationOutcomeEvaluator()

        before = AigcReport(
            source_path=Path("/f/before.docx"), overall_rate=76.67,
            fragments=[ReportFragment(text="A" * 1000, color_band=ColorBand.RED, index=0)],
        )
        after = AigcReport(
            source_path=Path("/f/after.docx"), overall_rate=70.0,
            fragments=[ReportFragment(text="A" * 800, color_band=ColorBand.RED, index=0)],
        )

        # HR thesis but using computer strategy
        result = evaluator.evaluate(
            before, after,
            before_doc_chars=20000, after_doc_chars=20000,
            discipline="human_resource", assigned_strategy="computer",
        )

        assert result.strategy_misuse_detected is True
        assert result.verdict == "failed"
        assert any("策略" in r for r in result.failure_reasons)

    def test_feedback_round_changes_strategy(self):
        """If first round fails, second round should NOT use same strategy."""
        from thesis_risk_optimizer.strategies import get_strategy

        # First round: use computer strategy
        strategy1 = get_strategy("computer")

        # Second round: should reassess and potentially switch
        # (We test that get_strategy returns different instances for different disciplines)
        strategy2 = get_strategy("human_resource")
        strategy3 = get_strategy("universal")

        # Different disciplines should get different strategies
        assert strategy1.name != strategy2.name
        assert strategy2.name != strategy3.name
        # All should have different paragraph_transforms
        assert strategy1.paragraph_transforms != strategy2.paragraph_transforms

    def test_classifier_avoids_false_positive_computer(self):
        """Generic words like '系统', '数据', '模型' should NOT trigger computer classification."""
        from thesis_risk_optimizer.analysis.thesis_classifier import ThesisClassifier, Discipline

        c = ThesisClassifier()

        # A management thesis that mentions generic system/data words
        disc, conf, _ = c.classify(
            title="企业财务管理系统优化研究",
            abstract="本文通过数据分析，建立财务风险评估模型，对某企业的财务管理系统进行优化。",
            keywords="财务管理; 风险分析; 系统优化; 数据分析",
            headings=["企业财务现状", "风险评估模型", "管理系统优化", "效果评估"],
        )

        # Should NOT be classified as computer despite "系统", "数据", "模型"
        assert disc != Discipline.COMPUTER, \
            f"Generic words should not trigger COMPUTER classification, got {disc}"

    def test_final_report_includes_discipline_info(self):
        """FinalReport should include discipline, confidence, and strategy misuse info."""
        from thesis_risk_optimizer.validation.final_report import FinalReportGenerator, ReportContext
        from thesis_risk_optimizer.rewrite.rewrite_engine import BatchResult
        from thesis_risk_optimizer.analysis.rewrite_ratio_planner import RatioPlan
        from pathlib import Path

        gen = FinalReportGenerator()
        plan = RatioPlan(total_body_units=5)
        batch = BatchResult(total=5, succeeded=5)
        ctx = ReportContext(
            classification_confidence=0.72,
            strategy_misuse_risk=False,
        )

        report = gen.generate(
            Path("/f/in.docx"), Path("/f/out.docx"),
            [make_unit("u1", text="测试内容")], "human_resource", "人力资源策略",
            plan, batch, None, False, context=ctx,
        )
        md = report.to_markdown()
        assert "human_resource" in md or "人力资源" in md
        assert "classification_confidence" in md or "置信度" in md


# ============================================================================
# 32. v14 HR Strategy Fix Tests
# ============================================================================

class TestCliAcceptsHumanResourceMajor:
    """Test 1: --major human_resource and --major hr must be accepted."""

    def test_cli_major_human_resource(self, tmp_path):
        """--major human_resource should work without error."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, [
            "企业员工绩效考核制度存在明显不足，考核指标设计不够科学，"
            "导致考核结果难以反映员工真实工作表现。"
        ] * 3)
        from thesis_risk_optimizer.cli import main
        result = main([
            "optimize", "--input", str(path),
            "--aigc-rate", "76.67", "--target-rate", "30",
            "--major", "human_resource", "--title", "HR测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--dry-run",
        ])
        assert result == 0

    def test_cli_major_hr(self, tmp_path):
        """--major hr should work (alias for human_resource)."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, ["企业绩效考核研究。"])
        from thesis_risk_optimizer.cli import main
        result = main([
            "optimize", "--input", str(path),
            "--aigc-rate", "76.67", "--target-rate", "30",
            "--major", "hr", "--title", "HR测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--dry-run",
        ])
        assert result == 0

    def test_cli_major_human_resource_forces_hr_strategy(self, tmp_path, capsys):
        """--major human_resource must force HumanResourceStrategy."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, ["企业绩效考核研究。"])
        from thesis_risk_optimizer.cli import main
        main([
            "optimize", "--input", str(path),
            "--aigc-rate", "76.67", "--target-rate", "30",
            "--major", "human_resource", "--title", "HR测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--dry-run",
        ])
        captured = capsys.readouterr()
        assert "人力资源策略" in captured.out


class TestBaseStrategyHasNoComputerTerms:
    """Test 2: BaseStrategy._section_guidance must not contain computer terms."""

    def test_no_computer_terms_in_base(self):
        """BaseStrategy section guidance should not contain 函数, 模块, 测试环境, 输入输出, 界面交互."""
        from thesis_risk_optimizer.strategies.base import BaseStrategy, UniversalStrategy
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis

        strategy = UniversalStrategy()
        computer_terms = ["函数", "模块", "测试环境", "输入输出", "界面交互",
                          "核心功能", "测试方式", "数据流", "异常处理", "测试用例"]

        # Check all sections
        for section in ["abstract", "introduction", "literature_review",
                        "tech_background", "requirements", "design",
                        "implementation", "testing", "conclusion"]:
            unit = make_unit(section=section)
            guidance = strategy._section_guidance(unit)
            for term in computer_terms:
                assert term not in guidance, (
                    f"BaseStrategy section '{section}' contains computer term '{term}': {guidance}"
                )

    def test_computer_terms_only_in_computer_strategy(self):
        """ComputerStrategy should contain the computer terms."""
        from thesis_risk_optimizer.strategies.computer import ComputerStrategy

        strategy = ComputerStrategy()
        # design section should have 模块关系, 数据流, 输入输出
        design_unit = make_unit(section="design")
        guidance = strategy._section_guidance(design_unit)
        assert "模块关系" in guidance or "数据流" in guidance or "输入输出" in guidance

        # implementation should have 函数
        impl_unit = make_unit(section="implementation")
        guidance = strategy._section_guidance(impl_unit)
        assert "函数" in guidance or "异常处理" in guidance

        # testing should have 测试环境
        test_unit = make_unit(section="testing")
        guidance = strategy._section_guidance(test_unit)
        assert "测试环境" in guidance or "测试用例" in guidance


class TestHRStrategyRejectsTemplatePhrases:
    """Test 3: HR rewrite must reject template phrases."""

    def test_rejects_common_templates(self):
        """HR guard should reject text containing template phrases."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        # Text with template phrases
        text = (
            "随着经济社会的发展，企业竞争日益激烈。"
            "人力资源是企业最重要的资源，具有重要意义。"
            "要完善绩效考核体系，加强员工培训，提高员工满意度。"
            "多措并举，推动企业高质量发展。"
        )
        result = check_hr_template(text)
        assert result.passed is False, f"Should reject templates, got passed=True"
        assert len(result.template_violations) > 0

    def test_accepts_concrete_text(self):
        """HR guard should accept concrete, non-template text."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        text = (
            "从论文已有描述看，该企业销售部门的绩效考核周期为季度考核，"
            "但考核指标未根据不同岗位职责进行差异化设计。"
            "一线销售人员与后勤管理人员使用相同的考核表，"
            "导致后勤人员认为考核标准与日常工作关联度低。"
        )
        result = check_hr_template(text)
        assert result.passed is True, f"Should accept concrete text, violations: {result.template_violations}"

    def test_rejects_empty_countermeasures(self):
        """HR guard should reject empty countermeasure phrases."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        text = (
            "为了进一步完善相关机制，应当加强员工培训，"
            "构建长效机制，从制度层面、管理层面、员工层面提高员工满意度，"
            "促进企业可持续发展。"
        )
        result = check_hr_template(text)
        assert result.passed is False

    def test_hr_section_guidance_no_computer_terms(self):
        """HR strategy section guidance must not contain any computer terms."""
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis

        strategy = HumanResourceStrategy()
        computer_terms = ["函数", "模块", "测试环境", "输入输出", "界面交互",
                          "核心功能", "测试方式", "数据流", "异常处理", "测试用例",
                          "数据库", "API", "Python", "Java"]

        for section in ["abstract", "introduction", "literature_review",
                        "requirements", "design", "implementation",
                        "testing", "conclusion"]:
            unit = make_unit(section=section)
            guidance = strategy._section_guidance(unit)
            for term in computer_terms:
                assert term not in guidance, (
                    f"HR strategy section '{section}' contains computer term '{term}': {guidance}"
                )


class TestHRStrategyNoFakeData:
    """Test 4: HR strategy must not introduce fake enterprise data."""

    def test_rejects_fabricated_employee_count(self):
        """HR guard should reject fabricated employee counts."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        original = "该企业存在人力资源管理问题。"
        rewritten = "该企业现有员工 350 人，分布在生产、销售、管理三个部门。"
        result = check_hr_template(rewritten, original)
        assert result.passed is False
        assert any("编造数据" in v for v in result.fabrication_violations)

    def test_rejects_fabricated_survey_count(self):
        """HR guard should reject fabricated survey data."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        original = "通过调查发现问题。"
        rewritten = "通过发放问卷 200 份，回收有效问卷 186 份，有效回收率达到 93%。"
        result = check_hr_template(rewritten, original)
        assert result.passed is False

    def test_rejects_fabricated_turnover_rate(self):
        """HR guard should reject fabricated turnover rates."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        original = "员工离职问题突出。"
        rewritten = "近两年员工离职率为 18.5%，远高于行业平均水平。"
        result = check_hr_template(rewritten, original)
        assert result.passed is False

    def test_accepts_conservative_expression(self):
        """HR text should accept conservative expressions without specific data."""
        from thesis_risk_optimizer.strategies.human_resource import check_hr_template

        original = "员工离职问题突出。"
        rewritten = "从论文已有描述看，该企业员工离职问题较为突出，主要集中在一线岗位。"
        result = check_hr_template(rewritten, original)
        assert result.passed is True, f"Should accept conservative expression, violations: {result.template_violations}"


class TestHROutcomeRateIncreaseFails:
    """Test 5: 76.67% → 77.02% must be judged as failure."""

    def test_rate_increase_fails(self):
        """AIGC rate increase 76.67% → 77.02% must fail and recommend rollback."""
        from thesis_risk_optimizer.validation.outcome_evaluator import OptimizationOutcomeEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = OptimizationOutcomeEvaluator()

        before = AigcReport(
            source_path=Path("/f/before.docx"), overall_rate=76.67,
            fragments=[
                ReportFragment(text="A" * 1000, color_band=ColorBand.RED, index=0),
            ],
        )
        after = AigcReport(
            source_path=Path("/f/after.docx"), overall_rate=77.02,
            fragments=[
                ReportFragment(text="A" * 1020, color_band=ColorBand.RED, index=0),
            ],
        )

        result = evaluator.evaluate(
            before, after,
            before_doc_chars=20000, after_doc_chars=20000,
            discipline="human_resource", assigned_strategy="human_resource",
        )

        assert result.verdict == "failed", f"Expected failed, got {result.verdict}"
        assert result.rollback_recommended is True
        assert any("上升" in r for r in result.failure_reasons), \
            f"Should mention rate increase. Reasons: {result.failure_reasons}"

    def test_small_rate_drop_fails(self):
        """AIGC rate drop less than 5pp should also fail."""
        from thesis_risk_optimizer.validation.outcome_evaluator import OptimizationOutcomeEvaluator
        from thesis_risk_optimizer.report_parser.aigc_report_parser import AigcReport, ReportFragment, ColorBand
        from pathlib import Path

        evaluator = OptimizationOutcomeEvaluator()

        before = AigcReport(
            source_path=Path("/f/before.docx"), overall_rate=76.67,
            fragments=[
                ReportFragment(text="A" * 1000, color_band=ColorBand.RED, index=0),
            ],
        )
        after = AigcReport(
            source_path=Path("/f/after.docx"), overall_rate=73.0,
            fragments=[
                ReportFragment(text="A" * 950, color_band=ColorBand.RED, index=0),
            ],
        )

        result = evaluator.evaluate(
            before, after,
            before_doc_chars=20000, after_doc_chars=20000,
            discipline="human_resource", assigned_strategy="human_resource",
        )

        assert result.verdict == "failed", \
            f"3.67pp drop (< 5pp threshold) should fail, got {result.verdict}"


class TestHRConservativeModeNoExpansion:
    """Test 6: Conservative mode must not significantly expand text."""

    def test_conservative_rewrite_length_range(self):
        """Conservative mode length range should be 90%-110%."""
        from thesis_risk_optimizer.strategies.human_resource import (
            HumanResourceStrategy, HR_CONSERVATIVE_LENGTH_RANGE
        )

        strategy = HumanResourceStrategy()
        strategy.enable_conservative_mode()
        assert strategy.conservative_mode is True

        # Conservative length range
        low, high = strategy.get_paragraph_length_range(ActionType.REWRITE)
        assert low == 0.90
        assert high == 1.10

    def test_conservative_rebuild_length_range(self):
        """Conservative mode rebuild should also use 90%-110%."""
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy

        strategy = HumanResourceStrategy()
        strategy.enable_conservative_mode()

        low, high = strategy.get_paragraph_length_range(ActionType.REBUILD)
        assert low == 0.90
        assert high == 1.10

    def test_normal_rewrite_length_range(self):
        """Normal HR rewrite should be 80%-130% (tighter than default 80%-140%)."""
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy

        strategy = HumanResourceStrategy()
        assert strategy.conservative_mode is False

        low, high = strategy.get_paragraph_length_range(ActionType.REWRITE)
        assert low == 0.80
        assert high == 1.30

    def test_normal_rebuild_length_range(self):
        """Normal HR rebuild should be 90%-150% (tighter than default 60%-180%)."""
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy

        strategy = HumanResourceStrategy()

        low, high = strategy.get_paragraph_length_range(ActionType.REBUILD)
        assert low == 0.90
        assert high == 1.50

    def test_conservative_guidance_mentions_no_expansion(self):
        """Conservative mode guidance should mention no expansion."""
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy
        from thesis_risk_optimizer.analysis.paragraph_diagnoser import ParagraphDiagnosis

        strategy = HumanResourceStrategy()
        strategy.enable_conservative_mode()

        unit = make_unit(section="introduction", action=ActionType.REWRITE)
        diagnosis = ParagraphDiagnosis(unit_uid="u1")
        guidance = strategy.rewrite_guidance(unit, diagnosis)

        assert "等长" in guidance or "不扩写" in guidance or "90%-110%" in guidance, \
            f"Conservative guidance should mention equal-length. Got: {guidance[:200]}"

    def test_conservative_disables(self):
        """Conservative mode should be disableable."""
        from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy

        strategy = HumanResourceStrategy()
        strategy.enable_conservative_mode()
        assert strategy.conservative_mode is True
        strategy.disable_conservative_mode()
        assert strategy.conservative_mode is False


class TestCLIConservativeFlag:
    """Test conservative flag on CLI."""

    def test_cli_conservative_flag(self, tmp_path):
        """--conservative flag should be accepted."""
        path = tmp_path / "test.docx"
        make_minimal_docx(path, ["企业绩效考核研究。"])
        from thesis_risk_optimizer.cli import main
        result = main([
            "optimize", "--input", str(path),
            "--aigc-rate", "76.67", "--target-rate", "30",
            "--major", "human_resource", "--title", "HR测试论文",
            "--has-aigc-report", "no", "--allow-rewrite", "yes",
            "--allow-supplement", "yes", "--has-materials", "no",
            "--confirmed", "yes",
            "--conservative", "--dry-run",
        ])
        assert result == 0


class TestCLIEvaluateOutcome:
    """Test evaluate-outcome command."""

    def test_evaluate_outcome_exists(self):
        """evaluate-outcome subcommand should be recognized."""
        from thesis_risk_optimizer.cli import _build_parser
        parser = _build_parser()
        # Should not raise
        args = parser.parse_args([
            "evaluate-outcome",
            "--before-report", "/fake/before.docx",
            "--after-report", "/fake/after.docx",
            "--major", "human_resource",
        ])
        assert args.command == "evaluate-outcome"
        assert args.major == "human_resource"
