from thesis_risk_optimizer.rewrite.anchor_first_policy import AnchorFirstPolicy
from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer


def test_missing_domain_anchor_disallows_oralization_as_humanization():
    result = AnchorFirstPolicy().evaluate(
        "该问题具有重要意义，应当进一步优化路径。",
        domain="human_resource",
    )

    assert not result.has_anchor
    assert not result.allow_naturalization
    assert result.suggested_action == "light_edit"
    assert "材料锚点不足" in result.missing_anchor_warning


def test_anchor_first_rewriter_does_not_add_oral_terms_when_anchor_missing():
    original = "该问题主要用于说明研究价值，具有重要意义。"
    rewritten = HumanVariationLayer(domain="human_resource").apply_text(original)

    assert "说白了" not in rewritten
    assert "没人管" not in rewritten
    assert "比较明显" not in rewritten
