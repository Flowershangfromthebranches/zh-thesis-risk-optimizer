from thesis_risk_optimizer.validation.oral_style_guard import OralStyleGuard


def test_law_uses_stricter_mild_oral_threshold():
    text = (
        "第一句说明案例事实。第二句说明法条适用。第三句比较明显。第四句说明争议焦点。"
        "第五句说明裁判逻辑。第六句说明责任承担。第七句说明权利义务。第八句说明适用边界。"
        "第九句说明结论限制。第十句保持法学表达。"
    )
    result = OralStyleGuard().check(text, section="body", domain="law")

    assert result.mild_oral_count == 1
    assert result.status == "warning"


def test_medicine_fails_strong_oral_and_warns_mild_oral():
    guard = OralStyleGuard()

    assert guard.check("护理结论说白了不能生活化。", section="body", domain="medical_nursing").status == "fail"
    assert guard.check(
        "第一句说明病例资料。第二句比较明显。第三句说明护理流程。第四句说明观察指标。"
        "第五句说明风险控制。第六句说明伦理限制。第七句说明随访记录。第八句说明操作规范。"
        "第九句说明结论边界。第十句保持医学表达。",
        section="body",
        domain="medical_nursing",
    ).status == "warning"
