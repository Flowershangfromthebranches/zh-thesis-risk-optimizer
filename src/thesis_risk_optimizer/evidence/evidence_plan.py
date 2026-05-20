"""EvidencePlan: defines material priority and fabrication prohibitions.

Step 5 of the 7-step workflow.
Controls what sources can be used during rewrite/rebuild.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# -- Evidence priority (highest to lowest) ------------------------------------

class EvidencePriority:
    """Priority levels for evidence sources (1 = highest)."""

    THESIS_ORIGINAL = 1          # Information already in the thesis
    USER_MATERIALS = 2           # User-provided real materials
    THESIS_REFERENCES = 3        # References cited in the thesis
    USER_SUPPLEMENTARY = 4       # User-provided surveys, interviews, experiments, etc.
    WEB_SEARCH = 5               # Public resources via web search (if allowed)
    MODEL_KNOWLEDGE = 6          # Conservative expressions from model knowledge


# -- Fabrication prohibitions -------------------------------------------------

FABRICATION_FORBIDDEN: list[str] = [
    "具体问卷人数",
    "具体访谈人数",
    "具体百分比",
    "具体企业经营数据",
    "具体实验数值",
    "具体系统版本",
    "具体函数名",
    "具体数据库表",
    "具体价格",
    "具体案例判决",
    "具体医学病例",
    "具体课堂人数或成绩变化",
]


@dataclass
class EvidencePlanResult:
    """Result of evidence planning."""

    available_sources: list[str] = field(default_factory=list)
    max_priority: int = 6  # Lowest priority usable
    can_use_web: bool = False
    can_use_model_knowledge: bool = False
    needs_material_request: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class EvidencePlan:
    """Plans what evidence sources are available and their priority.

    During rewrite/rebuild, must use evidence in priority order:
    1. Thesis original text
    2. User-provided real materials
    3. References already in the thesis
    4. User supplementary data (surveys, interviews, experiments, code, screenshots)
    5. Web search results (if allowed) — must record source
    6. Model knowledge (conservative only) — must not fabricate specifics
    """

    def plan(
        self,
        has_materials: bool,
        allow_supplement: bool,
        allow_web_search: bool = False,
        has_web_access: bool = False,
    ) -> EvidencePlanResult:
        """Plan available evidence sources.

        Args:
            has_materials: Whether user has provided materials.
            allow_supplement: Whether supplementation is allowed.
            allow_web_search: Whether web search is allowed.
            has_web_access: Whether the system can access the web.

        Returns:
            EvidencePlanResult with available sources and limitations.
        """
        result = EvidencePlanResult()

        # Priority 1: Always available
        result.available_sources.append("论文原文已有信息")

        if has_materials:
            result.available_sources.append("用户提供的真实材料")
            result.available_sources.append("论文参考文献中已有的资料")
            result.available_sources.append("用户补充的问卷/访谈/实验/项目/案例/源码/截图/数据表")
            result.max_priority = EvidencePriority.USER_SUPPLEMENTARY

        if allow_web_search and has_web_access:
            result.can_use_web = True
            result.available_sources.append("公开资料（联网搜索，需记录来源）")
            result.max_priority = EvidencePriority.WEB_SEARCH

        if allow_supplement and not has_materials:
            result.can_use_model_knowledge = True
            result.available_sources.append("模型常识（保守表达，不编造具体数据）")
            result.max_priority = EvidencePriority.MODEL_KNOWLEDGE
            result.warnings.append(
                "未提供真实材料，只能使用模型常识进行保守补充。"
                "不会编造具体数据、人数、百分比、企业经营数据等。"
            )

        if not allow_supplement:
            result.max_priority = EvidencePriority.THESIS_REFERENCES
            result.warnings.append(
                "不允许补充内容，只能在原文和已有引用范围内调整表达。"
            )

        # Determine what materials would be useful
        if not has_materials:
            result.needs_material_request = list(FABRICATION_FORBIDDEN)

        return result
