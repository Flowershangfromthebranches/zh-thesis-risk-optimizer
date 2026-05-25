from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer
from thesis_risk_optimizer.rewrite.anchor_first_policy import AnchorFirstPolicy


def test_management_anchors_are_preserved():
    text = "A公司招聘流程中，岗位职责、问卷数据和访谈案例反映出制度执行不一致。"
    policy = AnchorFirstPolicy().evaluate(text, domain="management_business")
    rewritten = HumanVariationLayer(domain="management_business").apply_text(text)

    assert policy.has_anchor
    for anchor in ["A公司", "招聘流程", "岗位职责", "问卷数据", "访谈案例", "制度"]:
        assert anchor in rewritten


def test_management_output_does_not_gain_computer_terms():
    text = "A公司招聘流程主要用于提升管理效率，岗位职责和访谈反馈需要对应。"
    rewritten = HumanVariationLayer(domain="management_business").apply_text(text)

    assert not any(term in rewritten for term in ["源码", "接口", "字段", "数据库", "版本号"])
