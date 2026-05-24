"""Base strategy: abstract base class and common utilities for discipline strategies.

All discipline-specific strategies inherit from BaseStrategy and override
the methods that need specialization.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from ..document_io.text_units import TextUnit, TextUnitType, ActionType, RiskLevel
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis, DiagnosisTag


@dataclass
class StrategyResult:
    """Result of applying a strategy to a text unit."""

    unit_uid: str
    original_text: str
    modified_text: str = ""
    action: ActionType = ActionType.FREEZE
    success: bool = False
    notes: str = ""


class BaseStrategy(ABC):
    """Abstract base for discipline-specific rewrite strategies.

    Each subclass defines:
    - discipline name
    - what to prioritize when rewriting
    - what to avoid
    - how to inject evidence for this discipline
    """

    name: str = "base"
    label: str = "Base Strategy"

    # -- What to avoid in output (populated per discipline) -------------------
    FORBIDDEN_PATTERNS: list[str] = []
    # -- What to prioritize adding --------------------------------------------
    PRIORITY_ELEMENTS: list[str] = []
    # -- Paragraph transform template (populated per discipline) --------------
    paragraph_transforms: str = ""

    def rewrite_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """Generate discipline-specific rewrite guidance for a text unit.

        This is the primary method called by the rewrite engine.
        Returns a string that guides the LLM or rule-based rewriter.
        """
        parts = []

        # 1. Section context
        parts.append(self._section_guidance(unit))

        # 2. Action-specific guidance
        if unit.action == ActionType.MODIFY:
            parts.append(self._modify_guidance(unit, diagnosis))
        elif unit.action == ActionType.REWRITE:
            parts.append(self._rewrite_guidance(unit, diagnosis))
        elif unit.action == ActionType.REBUILD:
            parts.append(self._rebuild_guidance(unit, diagnosis))

        # 3. Discipline-specific rules
        discipline_rules = self._discipline_rules(unit, diagnosis)
        if discipline_rules:
            parts.append(discipline_rules)

        # 4. Forbidden patterns
        if self.FORBIDDEN_PATTERNS:
            parts.append(f"【禁止】{'; '.join(self.FORBIDDEN_PATTERNS)}")

        # 5. Priority elements
        if self.PRIORITY_ELEMENTS:
            parts.append(f"【优先】{'; '.join(self.PRIORITY_ELEMENTS)}")

        # 6. Paragraph transform template
        if self.paragraph_transforms:
            parts.append(self.paragraph_transforms)

        return "\n".join(parts)

    def _section_guidance(self, unit: TextUnit) -> str:
        """Return section-specific guidance.

        Base guidance is discipline-neutral. Discipline-specific subclasses
        should override this method to provide their own section guidance.
        Computer-specific terms (模块, 函数, 测试环境, 输入输出, 界面交互, etc.)
        belong in ComputerStrategy, not here.
        """
        section = unit.section
        guidance = {
            "abstract": "摘要应加入具体研究对象、研究方法、主要发现,不要只写背景+方法+结果模板",
            "introduction": "绪论应减少宏大背景,改成'具体问题+本文为什么做+当前做法的不足'",
            "literature_review": "不要用'国外起步较早,国内也取得进展'模板句;调整综述逻辑,避免编造文献",
            "conclusion": "必须写局限和后续改进;结论要和全文实际工作对应;不要写空泛总结",
        }
        return guidance.get(section, "")

    def _modify_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """Light modification guidance."""
        return "【修改模式】调整句序、降低模板化、增加少量限定词,保持原意。不要同义替换。"

    def _rewrite_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """Rewrite guidance."""
        return (
            "【重写模式】保留主题,改变论证顺序,加入专业细节,改变句群结构。"
            "不是同义替换,而是重新组织内容。"
        )

    def _rebuild_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """Rebuild guidance."""
        tags_str = ", ".join(t.value for t in diagnosis.tags) if diagnosis.tags else "高风险"
        return (
            f"【重构模式】原段落检测到: {tags_str}。"
            "按论文题目和章节功能重新生成内容,必须补充具体细节。"
            "不得编造不存在的数据、参考文献、实验结果。"
        )

    @abstractmethod
    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """Discipline-specific rewrite rules — override in subclasses."""
        ...

    # -- Evidence suggestion --------------------------------------------------

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """Suggest what evidence would help rewrite this unit."""
        return ""

    # -- Rebuild planning -----------------------------------------------------

    def rebuild_section_structure(self, section: str) -> list[str]:
        """Discipline-neutral paragraph structure for rebuild planning.

        This base structure must stay free of computer/software terms.  Specific
        disciplines can override it with their own material anchors.
        """
        structures = {
            "abstract": ["研究对象", "材料依据", "分析方法", "主要发现与限制"],
            "introduction": ["具体问题描述", "研究对象来源", "已有处理不足", "本文范围与限制"],
            "literature_review": ["研究对象差异", "方法差异", "已有不足", "本文切入点"],
            "requirements": ["研究对象", "材料依据", "问题表现", "分析边界"],
            "design": ["研究对象", "材料依据", "分析过程", "结论限制"],
            "implementation": ["研究对象", "材料依据", "分析过程", "结论限制"],
            "testing": ["评价对象", "材料依据", "分析过程", "结论限制"],
            "conclusion": ["完成内容", "主要发现", "研究限制", "后续处理方向"],
        }
        return structures.get(section, ["研究对象", "材料依据", "分析过程", "结论限制"])

    def rebuild_required_details(
        self, unit: TextUnit, diagnosis: ParagraphDiagnosis
    ) -> list[str]:
        """Discipline-neutral details needed during rebuild."""
        details: list[str] = []
        if DiagnosisTag.MISSING_DETAIL in diagnosis.tags:
            details.append("原文已有的具体对象、过程或材料")
        if DiagnosisTag.ABSTRACT_ONLY in diagnosis.tags:
            details.append("该概念在本文研究对象中的具体对应关系")
        if DiagnosisTag.HOLLOW_CONCLUSION in diagnosis.tags:
            details.append("结论对应的材料依据和限制")
        if not details:
            details.append("更具体的研究过程或材料依据")
        return details


class UniversalStrategy(BaseStrategy):
    """Default strategy for unclassified disciplines."""

    name = "universal"
    label = "通用策略"

    FORBIDDEN_PATTERNS = [
        "不要使用模板句(随着...发展、具有重要意义等)",
        "不要做同义替换式改写",
        "不要把普通表达改成更正式的书面语",
        "不要编造数据、文献、实验",
    ]

    PRIORITY_ELEMENTS = [
        "增加研究对象、过程、材料、限制、案例",
        "将空泛结论改成具体分析",
        "保持学术规范",
    ]

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return "通用策略: 减少模板句,增加具体细节,保持学术规范。"
