"""Evidence injector: provide evidence suggestions for the optimization report.

KEY FIX v1.1: Does NOT inject HTML comments, placeholders, or bracket templates
into the thesis body text. Instead, evidence suggestions are returned separately
for inclusion in the optimization report or LLM prompts.

The inject() method now only returns the text unchanged, with evidence needs
recorded in unit metadata for the final report.
"""

from __future__ import annotations

import re
from typing import Optional

from ..document_io.text_units import TextUnit
from ..strategies.base import BaseStrategy


# -- Evidence suggestions per discipline --------------------------------------
DISCIPLINE_EVIDENCE: dict[str, dict[str, list[str]]] = {
    "computer": {
        "implementation": [
            "开发环境: 操作系统、IDE、语言及版本",
            "核心依赖库: 名称及版本号",
            "关键模块的输入、处理流程、输出",
            "数据库表结构及关键字段",
            "核心接口路径及参数",
        ],
        "testing": [
            "测试环境配置: 硬件、OS",
            "测试用例及参数",
            "实际运行结果、发现的问题及修复",
        ],
        "design": [
            "模块间通信方式",
            "数据库表设计",
            "设计取舍理由",
        ],
    },
    "management": {
        "requirements": [
            "企业背景: 行业、规模、类型",
            "业务流程中的具体问题表现",
            "涉及的具体岗位和职责",
        ],
        "conclusion": [
            "每个对策的责任部门、衡量指标、实施周期",
        ],
    },
    "education": {
        "design": [
            "教学对象: 年级、班级、人数",
            "具体教学环节设计",
        ],
        "testing": [
            "前后测对比数据",
            "学生具体反馈和变化表现",
        ],
    },
}


class EvidenceInjector:
    """Provides evidence suggestions WITHOUT writing them into thesis body.

    All suggestions go to unit metadata for the final report.
    The inject() method is a no-op that returns text unchanged.
    """

    def inject(
        self, text: str, unit: TextUnit, strategy: BaseStrategy
    ) -> str:
        """Returns text UNCHANGED. Evidence needs go to metadata.

        This method exists for backward compatibility with the rewrite engine
        but no longer modifies text. Use get_evidence_needs() for suggestions.
        """
        # Record what evidence would help, but DON'T modify the text
        needs = self.get_evidence_needs(unit, strategy)
        if needs:
            existing = unit.metadata.get("evidence_needs", [])
            unit.metadata["evidence_needs"] = list(set(existing + needs))
        return text

    def get_evidence_needs(
        self, unit: TextUnit, strategy: BaseStrategy
    ) -> list[str]:
        """Return a list of evidence suggestions for the optimization report.

        These are HUMAN-READABLE suggestions, not text to inject.
        """
        section = unit.section
        disc_evidence = DISCIPLINE_EVIDENCE.get(strategy.name, {})

        # Section-specific suggestions
        suggestions = disc_evidence.get(section, [])

        # Generic suggestions based on text characteristics
        if not suggestions:
            suggestions = self._generic_suggestions(unit, strategy)

        return suggestions

    def _generic_suggestions(
        self, unit: TextUnit, strategy: BaseStrategy
    ) -> list[str]:
        """Generic evidence suggestions when no section-specific ones exist."""
        text = unit.text

        suggestions = []

        # Check for missing detail indicators
        if len(text) > 100:
            has_numbers = bool(re.search(r"\d+\.?\d*", text))
            has_specific = bool(re.search(
                r"(?:系统|模块|接口|函数|参数|配置|版本|测试|数据|流程|岗位|指标|案例|班级|学生|教师|课堂|患者|护理|药品)",
                text
            ))

            if not has_numbers and not has_specific:
                suggestions.append("建议补充具体数据、研究过程或操作细节")

        # Check for template patterns
        if re.search(r"(?:随着|具有.*意义|本文首先|实验结果表明.*良好)", text):
            suggestions.append("当前段落存在模板句式,建议根据实际研究内容重写")

        if not suggestions:
            suggestions.append("建议根据实际研究过程补充更多具体细节")

        return suggestions

    def has_sufficient_detail(self, text: str) -> bool:
        """Check if text already has enough concrete detail."""
        numbers = len(re.findall(r"\d+\.?\d*", text))
        proper_nouns = len(re.findall(r"[A-Z][a-z]+|[A-Z]{2,}", text))
        technical_terms = len(re.findall(
            r"(?:系统|模块|接口|函数|方法|参数|配置|版本|测试|数据|流程|岗位|指标|案例)",
            text
        ))

        if len(text) > 200:
            return numbers + proper_nouns + technical_terms >= 5
        elif len(text) > 100:
            return numbers + proper_nouns + technical_terms >= 3
        return True


def get_evidence_report_items(units: list[TextUnit]) -> list[str]:
    """Collect all evidence needs from processed units for the final report.

    Returns deduplicated, human-readable list of suggested materials.
    """
    all_needs: set[str] = set()
    for unit in units:
        needs = unit.metadata.get("evidence_needs", [])
        for need in needs:
            all_needs.add(need)
    return sorted(all_needs)
