from thesis_risk_optimizer.analysis.paragraph_diagnoser import (
    DiagnosisTag,
    ParagraphDiagnosis,
)
from thesis_risk_optimizer.document_io.text_units import (
    ActionType,
    RiskLevel,
    TextUnit,
    TextUnitType,
)
from thesis_risk_optimizer.rewrite.rebuild_engine import RebuildEngine
from thesis_risk_optimizer.strategies.computer import ComputerStrategy
from thesis_risk_optimizer.strategies.human_resource import HumanResourceStrategy
from thesis_risk_optimizer.strategies.management import ManagementStrategy


def make_unit(uid="hr1", text="测试段落", section="implementation", risk_level=RiskLevel.HIGH):
    return TextUnit(
        uid=uid,
        unit_type=TextUnitType.PARAGRAPH,
        text=text,
        original_text=text,
        section=section,
        risk_level=risk_level,
        action=ActionType.REBUILD,
    )


def diagnosis(*tags):
    return ParagraphDiagnosis(unit_uid="hr1", tags=list(tags), risk_level=RiskLevel.HIGH)


def test_hr_rebuild_plan_does_not_use_computer_structure_or_details():
    unit = make_unit(
        text="A公司招聘制度主要用于满足用人需求，能够提升员工满意度。",
        section="implementation",
    )
    plan = RebuildEngine(HumanResourceStrategy()).rebuild_plan(
        unit, diagnosis(DiagnosisTag.MISSING_DETAIL)
    )
    combined = " ".join(plan["new_structure"] + plan["details_to_add"])

    forbidden = ["技术名称", "版本", "开发环境", "依赖", "核心函数", "输入输出", "测试参数", "模块接口", "数据流"]
    assert not any(term in combined for term in forbidden)
    assert any(term in combined for term in ["企业", "岗位", "制度", "员工", "访谈", "问卷", "对策"])


def test_computer_rebuild_plan_keeps_computer_structure():
    unit = make_unit(text="用户模块主要用于完成登录。", section="implementation")
    plan = RebuildEngine(ComputerStrategy()).rebuild_plan(
        unit, diagnosis(DiagnosisTag.MISSING_DETAIL)
    )
    combined = " ".join(plan["new_structure"] + plan["details_to_add"])

    assert any(term in combined for term in ["开发环境", "核心实现", "函数", "输入输出", "异常处理"])


def test_management_rebuild_plan_uses_generic_or_case_structure_not_computer():
    unit = make_unit(text="企业流程主要用于提升管理水平。", section="implementation")
    plan = RebuildEngine(ManagementStrategy()).rebuild_plan(
        unit, diagnosis(DiagnosisTag.MISSING_DETAIL)
    )
    combined = " ".join(plan["new_structure"] + plan["details_to_add"])

    forbidden = ["开发环境", "核心函数", "测试用例", "模块接口", "数据库", "API"]
    assert not any(term in combined for term in forbidden)
    assert any(term in combined for term in ["研究对象", "材料依据", "分析过程", "结论限制", "具体过程"])


def test_human_variation_removes_hr_cliches_and_preserves_anchors():
    from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer

    text = (
        "A公司招聘岗位制度主要用于完善机制，能够提升员工满意度，"
        "并增强企业凝聚力，推动企业高质量发展。"
    )
    result = HumanVariationLayer(domain="human_resource").apply_text(text)

    forbidden = ["完善机制", "提升员工满意度", "增强企业凝聚力", "推动企业高质量发展"]
    assert not any(term in result for term in forbidden)
    for anchor in ["A公司", "招聘", "岗位", "制度", "员工"]:
        assert anchor in result
    assert not any(term in result for term in ["源码", "接口", "字段", "数据库", "版本号"])


def test_human_variation_breaks_repeated_openers_for_all_domains():
    from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer

    units = [
        make_unit("u1", "招聘制度主要用于完成人员筛选。"),
        make_unit("u2", "培训制度主要用于完成能力提升。"),
        make_unit("u3", "绩效制度主要用于完成考核管理。"),
    ]
    results = HumanVariationLayer(domain="human_resource").apply_units(units)
    starts = [item.text[:8] for item in results]

    assert len(set(starts)) == len(starts)
    assert not all("主要用于" in item.text for item in results)


def test_hr_low_risk_paragraph_is_not_rewritten_into_management_template():
    from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer

    unit = make_unit(
        text="访谈中，A公司招聘专员提到岗位说明更新不及时，导致初筛标准前后不一致。",
        risk_level=RiskLevel.MINIMAL,
    )
    result = HumanVariationLayer(domain="human_resource").apply_unit(unit)

    assert result.text == unit.original_text
    assert result.action == "keep"
    assert "完善机制" not in result.text
    assert "提升水平" not in result.text


def test_hr_rewrite_engine_prompt_does_not_include_computer_rebuild_defaults():
    from thesis_risk_optimizer.rewrite.rewrite_engine import RewriteEngine

    unit = make_unit(
        text="A公司绩效制度主要用于管理员工表现，具有重要意义。",
        section="testing",
    )
    engine = RewriteEngine(
        strategy=HumanResourceStrategy(),
        style="low_aigc_humanized",
        domain="human_resource",
    )
    prompt = engine._build_prompt(unit, "HR guidance")

    forbidden = ["源码", "接口", "字段", "数据库", "版本号", "软件测试", "测试用例与参数"]
    assert not any(term in prompt for term in forbidden)
    assert any(term in prompt for term in ["企业", "岗位", "制度", "访谈", "问卷", "员工"])
