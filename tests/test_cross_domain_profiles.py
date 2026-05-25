from thesis_risk_optimizer.analysis.material_anchor_detector import MaterialAnchorDetector
from thesis_risk_optimizer.strategies.domain_profiles import get_domain_profile


def test_requested_domain_aliases_resolve_without_new_canonical_pollution():
    assert get_domain_profile("management_business").name == "management"
    assert get_domain_profile("literature_language").name == "literature"
    assert get_domain_profile("economics_finance").name == "economics"
    assert get_domain_profile("medical_nursing").name == "medicine"
    assert get_domain_profile("public_administration_marxism").name == "marxism"


def test_hr_anchor_detector_does_not_treat_computer_terms_as_hr_anchors():
    text = "源码接口字段数据库表构成了系统实现说明。"
    result = MaterialAnchorDetector().detect(text, domain="human_resource")

    assert result.anchor_terms == []
    assert result.domain_matched == "human_resource"


def test_literature_anchor_detector_does_not_import_engineering_anchors():
    text = "《边城》中翠翠的等待与叙事视角变化共同推动情节展开。"
    result = MaterialAnchorDetector().detect(text, domain="literature_language")

    assert any(term in result.anchor_terms for term in ["作品", "人物", "情节", "叙事"])
    assert "字段" not in result.anchor_terms
    assert "数据库表" not in result.anchor_terms
