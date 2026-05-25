from thesis_risk_optimizer.validation.oral_style_guard import OralStyleGuard


def test_strong_oral_fails_in_body():
    result = OralStyleGuard().check("说白了，这一问题在正文中不能这样表达。", section="body")

    assert result.status == "fail"
    assert result.strong_oral_count == 1
    assert "说白了" in result.strong_oral_terms


def test_quoted_strong_oral_is_not_counted_as_direct_style():
    result = OralStyleGuard().check("访谈对象提到：“说白了，流程反馈不够及时。”", section="analysis")

    assert result.strong_oral_count == 0
    assert result.status in {"pass", "warning"}
