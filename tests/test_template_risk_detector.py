from thesis_risk_optimizer.analysis.template_risk_detector import TemplateRiskDetector


def test_template_detector_flags_common_high_risk_phrases():
    text = (
        "该模块主要用于学生信息管理，能够提升整体效率，便于后续维护。"
        "从实践角度看，其具有重要意义，并为平台运行提供支撑。"
    )

    result = TemplateRiskDetector().detect_paragraph(text, paragraph_id="p1", domain="computer_engineering")

    assert result.paragraph_id == "p1"
    assert result.template_risk_score >= 60
    assert "主要用于" in result.matched_patterns
    assert "能够.*" in result.matched_patterns
    assert "便于.*" in result.matched_patterns
    assert "具有重要意义" in result.matched_patterns
    assert "提供.*支撑" in result.matched_patterns
    assert result.suggested_action in {"rewrite", "rebuild"}


def test_template_detector_combines_abstract_density_and_missing_anchors():
    text = "系统功能模块流程主要包括数据管理和平台机制优化，能够提升质量和效率。"

    result = TemplateRiskDetector().detect_paragraph(text, paragraph_id="p2", domain="education")

    assert result.abstract_density > 0.12
    assert result.material_anchor_score == 0
    assert result.suggested_action in {"rewrite", "rebuild"}
    assert "抽象词密度偏高" in result.reason


def test_template_detector_finds_repeated_section_skeletons():
    paragraphs = [
        "学生管理模块主要用于完成学生数据维护，包括新增、修改和查询。",
        "课程管理模块主要用于完成课程数据维护，包括新增、修改和查询。",
        "成绩管理模块主要用于完成成绩数据维护，包括新增、修改和查询。",
    ]

    results = TemplateRiskDetector().detect_section(paragraphs, domain="computer_engineering")

    assert len(results) == 3
    assert any("连续段落段首结构重复" in item.reason for item in results)
    assert any(item.suggested_action == "rewrite" for item in results)
