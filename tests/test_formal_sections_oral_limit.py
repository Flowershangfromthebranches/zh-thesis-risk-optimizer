from thesis_risk_optimizer.validation.oral_style_guard import OralStyleGuard


def test_abstract_warns_on_mild_oral_expression():
    text = "本文以A公司绩效制度为研究对象。问题比较明显。"
    result = OralStyleGuard().check(text, section="abstract")

    assert result.mild_oral_count == 1
    assert result.status == "warning"


def test_conclusion_fails_on_strong_oral_expression():
    result = OralStyleGuard().check("结论部分说白了不能写成口头汇报。", section="conclusion")

    assert result.status == "fail"
    assert result.strong_oral_count == 1
