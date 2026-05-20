"""Rebuild engine: full reconstruction of high-risk paragraphs.

Rebuild operations:
- Determine if the original paragraph is hollow
- If hollow, regenerate from topic + section function + discipline strategy
- Must add real research process or reasonable engineering/case/analysis details
- Must not fabricate non-existent data, references, or experimental results
"""

from __future__ import annotations

import re
from typing import Optional

from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis, DiagnosisTag
from ..strategies.base import BaseStrategy


class RebuildEngine:
    """Full paragraph reconstruction engine.

    Used for high-risk, low-quality paragraphs that need complete
    restructuring rather than editing.
    """

    # -- Indicators that a paragraph is too hollow to salvage ------------------
    HOLLOW_INDICATORS = [
        re.compile(r"^.{0,100}(?:具有|有着|存在|表现).{0,20}(?:意义|价值|作用|影响)$"),
        re.compile(r"^(?:通过|经过|基于).{0,50}(?:分析|研究|调查|实验).{0,50}(?:得出|发现|表明|证明)"),
    ]

    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy

    def rebuild_plan(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> dict:
        """Generate a rebuild plan for a paragraph.

        Returns a dict describing what the new paragraph should contain,
        which can be used to guide an LLM or provide a template.
        """
        is_hollow = self._is_hollow(unit)

        plan = {
            "unit_uid": unit.uid,
            "section": unit.section,
            "original_hollow": is_hollow,
            "new_structure": [],
            "details_to_add": [],
            "evidence_needed": [],
            "forbidden": [],
        }

        # Determine new structure based on section
        plan["new_structure"] = self._section_structure(unit.section)

        # Determine what details to add
        plan["details_to_add"] = self._required_details(unit, diagnosis)

        # What must NOT be done
        plan["forbidden"] = [
            "不得编造不存在的数据、参考文献、实验结果",
            "不得编造具体的数值数据(除非论文已有)",
            "不得编造人名、地名、机构名(除非论文已有)",
        ]

        if is_hollow:
            plan["forbidden"].append("不得保留原段落结构——需要完全重构")

        return plan

    def _is_hollow(self, unit: TextUnit) -> bool:
        """Check if a paragraph is too hollow/empty to be meaningfully modified."""
        text = unit.original_text
        if len(text) < 50:
            return True

        for pattern in self.HOLLOW_INDICATORS:
            if pattern.search(text):
                return True

        # Check substance density: ratio of specific terms to total length
        specific_terms = len(re.findall(r"\d+|[A-Z][a-z]+|[\u4e00-\u9fff]{2,4}(?:系统|模块|接口|函数|方法|数据|测试|实验)", text))
        if len(text) > 100 and specific_terms < 3:
            return True

        return False

    def _section_structure(self, section: str) -> list[str]:
        """Return recommended paragraph structure for a section."""
        structures = {
            "abstract": ["研究对象/系统", "核心功能/方法", "关键发现/测试结果", "实际结论(含局限)"],
            "introduction": ["具体问题描述", "现有方案不足", "本文解决思路", "本文范围与限制"],
            "tech_background": ["技术名称与版本", "在本系统中的角色", "为什么选它(对比替代方案)", "使用方式和配置"],
            "design": ["模块功能", "模块间关系", "数据流/输入输出", "设计取舍理由"],
            "implementation": ["开发环境与依赖", "核心实现逻辑", "关键代码/流程", "遇到的异常与处理"],
            "testing": ["测试环境", "测试步骤", "测试用例与参数", "预期vs实际结果", "不足与改进"],
            "conclusion": ["已完成工作总结", "实际效果/发现", "局限与不足", "后续改进方向"],
        }
        return structures.get(section, ["主题句", "具体内容/证据", "分析/论证", "小结或过渡"])

    def _required_details(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> list[str]:
        """List what details should be added to make the paragraph concrete."""
        details = []
        section = unit.section

        if DiagnosisTag.MISSING_DETAIL in diagnosis.tags:
            if section == "implementation":
                details.extend(["开发环境版本号", "核心函数输入输出", "异常处理方式"])
            elif section == "testing":
                details.extend(["测试用例", "测试参数", "实际运行结果"])
            elif section == "design":
                details.extend(["模块接口定义", "数据流方向", "设计取舍理由"])
            else:
                details.append("具体数据/过程/案例")

        if DiagnosisTag.ABSTRACT_ONLY in diagnosis.tags:
            details.append("该概念/技术在本文系统中的具体应用方式")

        if not details:
            details.append("更具体的研究过程或实现细节")

        return details
