from thesis_risk_optimizer.rewrite.oral_style_rewriter import (
    OralStyleRewriter,
    TEMPLATE_REGRESSION_PHRASES,
)


def test_strong_oral_is_rewritten_to_natural_thesis_expression():
    result = OralStyleRewriter().rewrite("说白了，A公司绩效反馈没人管。", section="analysis")

    assert "说白了" not in result.text
    assert "没人管" not in result.text
    assert "换言之" in result.text
    assert "缺少记录、反馈或管理" in result.text
    assert result.guard_result.status == "pass"


def test_oral_rewriter_does_not_regress_to_template_phrases():
    result = OralStyleRewriter().rewrite("没人管导致流程对不上。", section="analysis")

    assert not any(phrase in result.text for phrase in TEMPLATE_REGRESSION_PHRASES)
