"""Section-aware low-AIGC rewrite guidance."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SectionProfile:
    name: str
    guidance: str
    avoid: tuple[str, ...] = ()
    prefer: tuple[str, ...] = ()


SECTION_PROFILES: dict[str, SectionProfile] = {
    "abstract": SectionProfile(
        name="abstract",
        guidance="摘要保持简洁，写清研究对象、方法和结果，避免随着发展和本文从...展开。",
        avoid=("随着.*发展", "本文从.*展开"),
        prefer=("研究对象", "方法", "结果"),
    ),
    "introduction": SectionProfile(
        name="introduction",
        guidance="绪论/背景少写宏大时代背景，多写选题来源、现实问题和研究对象。",
        avoid=("在.*背景下", "具有重要意义"),
        prefer=("选题来源", "现实问题", "研究对象"),
    ),
    "literature_review": SectionProfile(
        name="literature_review",
        guidance="文献综述写研究对象、方法差异和已有不足，不伪造文献观点。",
        avoid=("国内外学者认为", "相关研究表明"),
        prefer=("对象差异", "方法差异", "已有不足"),
    ),
    "methodology": SectionProfile(
        name="methodology",
        guidance="方法/设计/实现多写具体步骤、对象、工具、字段、样本或流程，少写抽象意义。",
        avoid=("提供支撑", "形成闭环"),
        prefer=("步骤", "对象", "流程"),
    ),
    "data_analysis": SectionProfile(
        name="data_analysis",
        guidance="数据/案例分析多写材料本身，分析要对应数据、访谈、案例或文本。",
        avoid=("由此可见", "具有重要意义"),
        prefer=("数据", "访谈", "案例", "文本"),
    ),
    "countermeasure": SectionProfile(
        name="countermeasure",
        guidance="对策建议必须对应前文问题，避免万能建议堆砌。",
        avoid=("加强重视", "完善机制", "提升水平"),
        prefer=("对应问题", "执行对象", "操作步骤"),
    ),
    "conclusion": SectionProfile(
        name="conclusion",
        guidance="结论写完成了什么、发现了什么、限制是什么，少写宏大展望。",
        avoid=("综上所述", "展望未来"),
        prefer=("完成内容", "发现", "限制"),
    ),
    "acknowledgement": SectionProfile(
        name="acknowledgement",
        guidance="致谢通常不参与低AIGC重写。",
    ),
}

SECTION_ALIASES = {
    "research_background": "introduction",
    "requirement_analysis": "methodology",
    "system_design": "methodology",
    "implementation": "methodology",
    "experiment": "methodology",
    "test": "methodology",
    "testing": "methodology",
    "case_analysis": "data_analysis",
}


def get_section_profile(section: str | None) -> SectionProfile:
    key = (section or "").strip().lower()
    if key in SECTION_ALIASES:
        key = SECTION_ALIASES[key]
    if key in SECTION_PROFILES:
        return SECTION_PROFILES[key]
    return SectionProfile(name=key or "general", guidance="保持具体、真实、不模板化，保留原文事实和材料边界。")


def classify_section(heading_or_section: str | None) -> str:
    text = (heading_or_section or "").strip().lower()
    rules = [
        ("abstract", r"摘要|abstract"),
        ("introduction", r"绪论|引言|背景"),
        ("literature_review", r"文献|研究现状|综述"),
        ("methodology", r"方法|设计|实现|实验|测试|需求"),
        ("data_analysis", r"数据分析|案例分析|文本分析|结果分析"),
        ("countermeasure", r"对策|建议"),
        ("conclusion", r"结论|总结"),
        ("acknowledgement", r"致谢"),
    ]
    for name, pattern in rules:
        if re.search(pattern, text):
            return name
    return text or "general"
