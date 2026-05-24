from thesis_risk_optimizer.strategies.domain_profiles import (
    get_domain_profile,
    classify_domain,
    list_domain_profiles,
)


def test_builtin_domain_profiles_cover_required_families():
    names = {profile.name for profile in list_domain_profiles()}

    assert "computer_engineering" in names
    assert "management" in names
    assert "education" in names
    assert "literature" in names
    assert "law" in names
    assert "economics" in names
    assert "medicine" in names
    assert "art_design" in names
    assert "engineering_general" in names
    assert "marxism" in names


def test_aliases_resolve_to_canonical_profiles():
    assert get_domain_profile("software_engineering").name == "computer_engineering"
    assert get_domain_profile("information_system").name == "computer_engineering"
    assert get_domain_profile("business_administration").name == "management"
    assert get_domain_profile("finance").name == "economics"
    assert get_domain_profile("nursing").name == "medicine"
    assert get_domain_profile("civil").name == "engineering_general"
    assert get_domain_profile("ideological_political").name == "marxism"


def test_auto_domain_classifier_uses_title_abstract_keywords_and_headings():
    profile, evidence = classify_domain(
        title="某公司绩效考核制度优化研究",
        abstract="本文结合A公司岗位职责、员工访谈和问卷反馈分析绩效流程。",
        keywords="绩效考核;员工反馈;岗位",
        headings=["企业概况", "绩效制度现状", "访谈结果分析"],
    )

    assert profile.name == "management"
    assert any("岗位" in item or "绩效" in item for item in evidence)


def test_auto_domain_classifier_does_not_treat_generic_system_as_computer():
    profile, evidence = classify_domain(
        title="基层公共服务体系建设研究",
        abstract="研究围绕地方政策文本、基层治理场景和公共服务流程展开。",
        keywords="公共服务;治理;政策",
        headings=["政策背景", "地方实践", "现实问题"],
    )

    assert profile.name == "marxism"
    assert not any("数据库" in item for item in evidence)
