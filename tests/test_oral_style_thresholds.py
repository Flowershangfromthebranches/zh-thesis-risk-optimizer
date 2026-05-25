from thesis_risk_optimizer.validation.oral_style_guard import OralStyleGuard


def test_body_allows_at_most_one_mild_oral_per_ten_sentences():
    guard = OralStyleGuard()
    text = (
        "第一句说明研究对象。第二句说明材料来源。第三句说明分析过程。第四句说明限制。"
        "第五句比较明显地呈现差异。第六句继续讨论原因。第七句回到原文材料。"
        "第八句补充章节关系。第九句说明结论边界。第十句保持论文表达。"
    )

    result = guard.check(text, section="body")

    assert result.total_sentences == 10
    assert result.mild_oral_count == 1
    assert result.status == "pass"


def test_body_fails_when_mild_oral_density_exceeds_fifteen_percent():
    guard = OralStyleGuard()
    text = (
        "第一句说明研究对象。第二句比较明显。第三句说明分析过程。第四句不够及时。"
        "第五句说明限制。第六句继续讨论原因。第七句回到原文材料。"
        "第八句补充章节关系。第九句说明结论边界。第十句保持论文表达。"
    )

    result = guard.check(text, section="body")

    assert result.mild_oral_count == 2
    assert result.status == "fail"
