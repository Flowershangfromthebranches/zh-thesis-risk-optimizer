from thesis_risk_optimizer.rewrite.human_variation import HumanVariationLayer
from thesis_risk_optimizer.rewrite.anchor_first_policy import AnchorFirstPolicy


def test_computer_anchor_first_keeps_software_materials():
    text = "登录页面通过接口提交账号字段，源码中根据状态字段返回测试结果。"
    policy = AnchorFirstPolicy().evaluate(text, domain="computer_engineering")

    assert policy.has_anchor
    assert {"页面", "接口", "字段", "源码", "测试用例"} & set(policy.anchor_terms)


def test_computer_human_variation_preserves_core_anchors():
    text = "登录页面主要用于提交账号字段，接口能够返回测试结果。"
    rewritten = HumanVariationLayer(domain="computer_engineering").apply_text(text)

    for anchor in ["登录页面", "账号字段", "接口", "测试结果"]:
        assert anchor in rewritten
