from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer
from thesis_risk_optimizer.rewrite.oral_style_rewriter import OralStyleRewriter


TEMPLATE_PHRASES = ["具有重要意义", "提供支撑", "完善机制", "提升水平", "优化路径"]


def test_oral_recovery_does_not_create_template_language():
    text = OralStyleRewriter().rewrite("这帮人不是不想干活，只是流程对不上。").text

    assert not any(phrase in text for phrase in TEMPLATE_PHRASES)


def test_human_variation_removes_template_language_without_oralizing():
    text = "该制度主要用于完善机制，能够提升水平，并提供支撑。"
    rewritten = HumanVariationLayer(domain="management_business").apply_text(text)

    assert not any(phrase in rewritten for phrase in TEMPLATE_PHRASES)
    assert "说白了" not in rewritten
    assert "没人管" not in rewritten
