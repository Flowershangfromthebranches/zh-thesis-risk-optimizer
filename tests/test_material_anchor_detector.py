import pytest

from thesis_risk_optimizer.analysis.material_anchor_detector import MaterialAnchorDetector


@pytest.mark.parametrize(
    ("domain", "text", "expected_terms"),
    [
        ("computer_engineering", "登录页面提交后会调用用户接口，user_id字段写入数据库表。", ["页面", "接口", "字段"]),
        ("management", "A公司招聘流程中，部门负责人访谈和员工问卷都反映岗位说明不清。", ["公司", "流程", "访谈", "问卷", "岗位"]),
        ("education", "三年级二班课堂上，学生在小组活动和作业展示中表现出差异。", ["班级", "课堂", "学生", "教学活动", "作业"]),
        ("literature", "《边城》中翠翠的等待情节和渡船意象改变了叙事节奏。", ["作品", "人物", "情节", "意象", "叙事"]),
        ("law", "该案争议焦点在于民法典相关法条的适用条件和责任承担。", ["案例", "争议焦点", "法条", "适用条件", "责任承担"]),
        ("economics", "2019年至2023年样本企业资产负债率指标呈上升趋势，变量回归结果显示融资约束影响明显。", ["年份", "样本", "指标", "变量", "统计结果", "趋势"]),
        ("medicine", "护理干预后记录患者临床表现、观察指标和随访情况，避免并发症风险。", ["护理流程", "干预措施", "临床表现", "观察指标", "随访", "并发症"]),
        ("art_design", "海报方案在构图、色彩和材料选择上经过两轮草图迭代。", ["方案", "构图", "色彩", "材料", "草图", "方案迭代"]),
    ],
)
def test_detector_recognizes_domain_specific_material_anchors(domain, text, expected_terms):
    result = MaterialAnchorDetector().detect(text, domain)

    assert result.domain_matched == domain
    assert result.anchor_score > 0
    for term in expected_terms:
        assert term in result.anchor_terms
    assert result.missing_anchor_warning == ""


def test_detector_warns_when_abstract_paragraph_has_no_domain_anchor():
    text = "该研究能够提升管理质量，完善运行机制，并为后续发展提供支撑。"
    result = MaterialAnchorDetector().detect(text, "management")

    assert result.anchor_score == 0
    assert "缺少management专业材料锚点" in result.missing_anchor_warning
