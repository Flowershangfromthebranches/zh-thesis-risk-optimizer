from thesis_risk_optimizer.document_io.text_units import ActionType, RiskLevel, TextUnit, TextUnitType
from thesis_risk_optimizer.rewrite.anti_template_rewriter import AntiTemplateRewriter
from thesis_risk_optimizer.cli import _build_parser
from thesis_risk_optimizer.validation.final_report import FinalReportGenerator, ReportContext
from thesis_risk_optimizer.rewrite.rewrite_engine import BatchResult
from thesis_risk_optimizer.analysis.rewrite_ratio_planner import RatioPlan


def make_unit(uid, text, section="analysis", risk_level=RiskLevel.HIGH):
    return TextUnit(
        uid=uid,
        unit_type=TextUnitType.PARAGRAPH,
        text=text,
        original_text=text,
        section=section,
        risk_level=risk_level,
        action=ActionType.MODIFY,
    )


def test_management_rewrite_does_not_force_computer_terms():
    unit = make_unit(
        "m1",
        "A公司招聘流程主要用于满足部门用人需求，能够提升管理效率，便于岗位配置。",
    )

    result = AntiTemplateRewriter().rewrite_unit(unit, domain="management")

    forbidden = {"源码", "字段", "接口", "数据库", "数据表"}
    assert not any(term in result.text for term in forbidden)
    assert "A公司" in result.text
    assert "招聘流程" in result.text
    assert result.action in {"light_edit", "rewrite"}


def test_literature_rewrite_does_not_force_engineering_terms():
    unit = make_unit(
        "l1",
        "《边城》中翠翠形象主要用于展现作品主题，具有重要意义。",
    )

    result = AntiTemplateRewriter().rewrite_unit(unit, domain="literature")

    forbidden = {"系统", "模块", "数据表", "接口"}
    assert not any(term in result.text for term in forbidden)
    assert "《边城》" in result.text
    assert "翠翠" in result.text


def test_rewriter_preserves_existing_domain_materials():
    cases = [
        ("management", "A公司招聘专员在访谈中提到，岗位说明和问卷反馈存在差异。", ["A公司", "岗位", "问卷", "访谈"]),
        ("literature", "《雷雨》中周朴园的台词推动了人物关系和关键情节。", ["《雷雨》", "周朴园", "情节"]),
        ("law", "该案事实显示双方合同履行存在争议，法条适用关系到责任承担。", ["该案", "合同", "法条", "责任承担"]),
        ("computer_engineering", "用户页面提交表单后，接口会校验status字段。", ["页面", "接口", "status字段"]),
    ]

    rewriter = AntiTemplateRewriter()
    for domain, text, terms in cases:
        result = rewriter.rewrite_unit(make_unit(domain, text), domain=domain)
        for term in terms:
            assert term in result.text


def test_rewriter_varies_repeated_mainly_used_openers():
    units = [
        make_unit("u1", "登录模块主要用于完成用户身份校验，能够保障系统运行。"),
        make_unit("u2", "订单模块主要用于完成订单信息维护，能够提升管理效率。"),
        make_unit("u3", "统计模块主要用于完成数据汇总，便于后续分析。"),
    ]

    results = AntiTemplateRewriter().rewrite_units(units, domain="computer_engineering")
    starts = [item.text[:8] for item in results]

    assert len(set(starts)) == len(starts)
    assert not all(item.text.startswith(("登录模块主要用于", "订单模块主要用于", "统计模块主要用于")) for item in results)


def test_rewriter_keeps_default_length_within_90_to_115_percent():
    unit = make_unit(
        "len1",
        "问卷结果主要用于分析员工培训需求，能够为后续培训方案提供支撑，并提升企业管理效率。",
    )

    result = AntiTemplateRewriter().rewrite_unit(unit, domain="management")
    ratio = len(result.text) / len(unit.original_text)

    assert 0.90 <= ratio <= 1.15


def test_rewriter_does_not_fabricate_specific_materials_when_missing():
    unit = make_unit(
        "safe1",
        "该研究主要用于分析管理问题，能够提升管理水平，并为后续发展提供参考。",
    )

    result = AntiTemplateRewriter().rewrite_unit(unit, domain="management")

    forbidden_fragments = ["A公司", "访谈", "问卷", "2023", "员工30人", "部门经理"]
    assert not any(fragment in result.text for fragment in forbidden_fragments)
    assert result.needs_material is True


def test_low_risk_paragraph_only_receives_light_touch():
    unit = make_unit(
        "low1",
        "访谈中，A公司招聘专员提到岗位说明更新不及时，导致初筛标准前后不一致。",
        risk_level=RiskLevel.MINIMAL,
    )

    result = AntiTemplateRewriter().rewrite_unit(unit, domain="management")

    assert result.text == unit.original_text
    assert result.action == "keep"


def test_cli_accepts_low_aigc_humanized_style_and_domain_default_auto():
    parser = _build_parser()
    args = parser.parse_args(["optimize", "--input", "thesis.docx"])

    assert args.style == "low_aigc_humanized"
    assert args.domain == "auto"


def test_cli_accepts_explicit_domain_without_breaking_existing_args():
    parser = _build_parser()
    args = parser.parse_args([
        "optimize",
        "--input", "thesis.docx",
        "--major", "工商管理",
        "--domain", "management",
        "--style", "low_aigc_humanized",
    ])

    assert args.major == "工商管理"
    assert args.domain == "management"
    assert args.style == "low_aigc_humanized"


def test_final_report_includes_domain_template_anchor_and_uncertainty_sections():
    units = [
        make_unit(
            "r1",
            "A公司招聘流程主要用于满足部门用人需求，能够为后续管理提供支撑。",
        ),
        make_unit(
            "r2",
            "该研究主要用于分析管理问题，能够提升管理质量。",
        ),
    ]
    ctx = ReportContext(
        domain_profile_name="management",
        domain_profile_evidence=["工商管理", "招聘", "岗位"],
        domain_user_specified=True,
    )

    report = FinalReportGenerator().generate(
        "in.docx",
        "out.docx",
        units,
        "management",
        "low_aigc_humanized",
        RatioPlan(total_body_units=2, assigned_modify=2),
        BatchResult(total=2, succeeded=1),
        None,
        False,
        context=ctx,
    )
    md = report.to_markdown()

    assert "domain profile 判断结果" in md
    assert "management" in md
    assert "模板化风险报告" in md
    assert "材料锚点报告" in md
    assert "过度润色警告" in md
    assert "不确定性说明" in md
    assert "不承诺任何检测器一定降低" in md
