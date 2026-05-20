"""Paragraph diagnoser: diagnose why a paragraph reads like AI-generated text.

For each text unit, produces a diagnosis explaining the specific AI-like
characteristics and what kind of rewrite is needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..document_io.text_units import TextUnit, RiskLevel, ActionType


class DiagnosisTag(str, Enum):
    """Specific AI-like characteristics detected in a paragraph."""

    TEMPLATE_SKELETON = "template_skeleton"        # 随着...发展, 具有...意义
    GRAND_NARRATIVE = "grand_narrative"            # 宏大叙事 without specifics
    ENCYCLOPEDIA_STYLE = "encyclopedia_style"      # 百科式概念介绍
    MISSING_DETAIL = "missing_detail"              # 缺少具体数据/过程/参数
    UNIFORM_SENTENCE = "uniform_sentence"           # 句式过于统一
    OVERLY_SMOOTH = "overly_smooth"                # 过于顺滑,缺少转折
    HOLLOW_CONCLUSION = "hollow_conclusion"        # 空泛结论(良好的可行性等)
    VAGUE_ACTION = "vague_action"                  # 模糊动作(进行了处理等)
    POLICY_SPEAK = "policy_speak"                   # 政策套话
    NO_LIMITATIONS = "no_limitations"               # 没有局限/不足描述
    ABSTRACT_ONLY = "abstract_only"                 # 只写抽象概念,不写具体应用
    FLOWCHART_PROSE = "flowchart_prose"            # 把代码/流程写成散文
    PSEUDO_ANALYSIS = "pseudo_analysis"            # 伪分析(没有真正因果推理)


@dataclass
class ParagraphDiagnosis:
    """Diagnosis for a single paragraph."""

    unit_uid: str
    tags: list[DiagnosisTag] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    recommended_action: ActionType = ActionType.FREEZE
    reasoning: str = ""
    needs_evidence: bool = False
    evidence_suggestion: str = ""


class ParagraphDiagnoser:
    """Diagnose individual paragraphs for AI-like characteristics.

    Usage:
        diagnoser = ParagraphDiagnoser()
        diagnosis = diagnoser.diagnose(unit)
    """

    # -- Detection patterns for each diagnosis tag ----------------------------
    DETECTION_RULES: dict[DiagnosisTag, list[re.Pattern]] = {
        DiagnosisTag.TEMPLATE_SKELETON: [
            re.compile(r"随着.{0,20}(?:发展|进步|提高|深入|完善|加快)"),
            re.compile(r"具有(?:(?:十分|非常|极其)?重要的)?(?:现实|理论|实践)?意义"),
            re.compile(r"本文首先.{0,30}其次.{0,30}最后"),
            re.compile(r"在(?:新|当前|信息|大数据|互联网|人工智能|新时代).{0,10}(?:时代|背景|环境)下"),
            re.compile(r"国内外.{0,10}(?:起步|发展|研究|现状|进展)"),
            re.compile(r"日益(?:突出|严重|重要|增长|加剧)"),
            re.compile(r"不可替代的(?:作用|地位|价值)"),
            re.compile(r"提供(?:了)?(?:便捷|有效|可行)的(?:解决方案|途径|方法|手段)"),
            re.compile(r"实验结果表明.{0,30}(?:具有|有着|表现|取得)"),
            re.compile(r"有效性和可靠性"),
            re.compile(r"(?:国外|国内).{0,10}起步较早"),
            re.compile(r"国内也.{0,10}(?:取得|获得|有)(?:了)?(?:不少|很大|显著|一定)(?:进展|成果|成就)"),
            re.compile(r"为.{0,20}提供(?:了)?(?:参考|借鉴|依据|指导)"),
            re.compile(r"作为.{0,15}的(?:重要|主要|核心)(?:载体|平台|工具|手段)"),
        ],
        DiagnosisTag.GRAND_NARRATIVE: [
            re.compile(r"推动.{0,10}(?:发展|进步|高质量)"),
            re.compile(r"促进.{0,10}(?:经济|社会|产业)发展"),
            re.compile(r"构建.{0,10}(?:体系|机制|模式|格局|框架)"),
            re.compile(r"实现.{0,10}(?:现代化|智能化|信息化|数字化)"),
        ],
        DiagnosisTag.ENCYCLOPEDIA_STYLE: [
            re.compile(r"是指.{10,60}(?:技术|方法|理论|概念|模型|架构)"),
            re.compile(r"(?:技术|方法|理论|概念|模型)是.{10,60}(?:一种|一个)"),
        ],
        DiagnosisTag.MISSING_DETAIL: [
            re.compile(r"做(?:了|出).{0,10}处理"),
            re.compile(r"进行(?:了|过).{0,10}(?:分析|研究|调查|实验|测试|优化)"),
            re.compile(r"采用(?:了|过).{0,10}(?:方法|方式|手段|技术|工具)"),
            re.compile(r"取得(?:了|过).{0,10}(?:效果|成果|成效|进展)"),
            re.compile(r"实现(?:了|过).{0,5}(?:模块|功能|系统)"),  # 只说实现了模块
            re.compile(r"采用模块化设计"),
            re.compile(r"提高(?:了)?效率"),  # 只说提高效率，没有具体数据
            re.compile(r"进行(?:了)?测试"),  # 只说进行了测试，没有测试细节
        ],
        DiagnosisTag.HOLLOW_CONCLUSION: [
            re.compile(r"具有(?:良好的|较高的|显著的)(?:可行性|实用性|稳定性|可靠性|有效性)"),
            re.compile(r"实验结果表明.{0,20}(?:具有|有着|表现|取得).{0,10}(?:良好|优秀|较高|显著)"),
            re.compile(r"为.{0,20}提供(?:了)?(?:参考|借鉴|依据)"),
            re.compile(r"有效(?:提升|提高|增强|改善|促进|降低)了"),
        ],
        DiagnosisTag.VAGUE_ACTION: [
            re.compile(r"通过.{0,10}(?:手段|方式|途径|方法)"),
            re.compile(r"运用.{0,10}(?:方式|方法|手段)"),
        ],
        DiagnosisTag.POLICY_SPEAK: [
            re.compile(r"贯彻落实"),
            re.compile(r"坚持.{0,10}(?:方针|原则|路线)"),
            re.compile(r"以.{0,10}为(?:指导|核心|导向|目标|抓手)"),
        ],
        DiagnosisTag.PSEUDO_ANALYSIS: [
            # Pseudo-detail: has tech terms but no real implementation description
            re.compile(r"(?:Python|Java|Spring|Vue|Django|Flask|MySQL|Redis|Docker|Linux).{0,50}"
                       r"(?:注入|漏洞|扫描|爬虫|测试).{0,50}(?:模块|报告|系统)"),
        ],
        DiagnosisTag.NO_LIMITATIONS: [],
        DiagnosisTag.ABSTRACT_ONLY: [],
        DiagnosisTag.FLOWCHART_PROSE: [],
    }

    def diagnose(self, unit: TextUnit) -> ParagraphDiagnosis:
        """Diagnose a single text unit.

        Returns:
            ParagraphDiagnosis with detected tags and recommended action.
        """
        diagnosis = ParagraphDiagnosis(unit_uid=unit.uid)

        text = unit.text
        if not text.strip():
            return diagnosis

        # Detect AI-like patterns
        for tag, patterns in self.DETECTION_RULES.items():
            if self._check_patterns(text, patterns):
                diagnosis.tags.append(tag)

        # Special checks that need more context
        if self._check_no_limitations(text, unit):
            diagnosis.tags.append(DiagnosisTag.NO_LIMITATIONS)

        if self._check_abstract_only(text, unit):
            diagnosis.tags.append(DiagnosisTag.ABSTRACT_ONLY)

        if self._check_flowchart_prose(text, unit):
            diagnosis.tags.append(DiagnosisTag.FLOWCHART_PROSE)

        # Determine risk and action
        diagnosis.risk_level = self._assess_risk(diagnosis.tags, unit)
        diagnosis.recommended_action = self._recommend_action(
            diagnosis.tags, diagnosis.risk_level, unit
        )

        # Build reasoning
        diagnosis.reasoning = self._build_reasoning(diagnosis)

        # Evidence needs
        if diagnosis.recommended_action in (ActionType.REWRITE, ActionType.REBUILD):
            diagnosis.needs_evidence = True
            diagnosis.evidence_suggestion = self._suggest_evidence(diagnosis.tags, unit)

        return diagnosis

    @staticmethod
    def _check_patterns(text: str, patterns: list[re.Pattern]) -> bool:
        """Check if any pattern matches the text (at least 1 match needed for broad coverage)."""
        count = sum(1 for p in patterns if p.search(text))
        return count >= 1

    @staticmethod
    def _check_no_limitations(text: str, unit: TextUnit) -> bool:
        """Check if this is a conclusion-like paragraph without limitations."""
        if unit.section not in ("conclusion", "testing", ""):
            return False
        if len(text) > 100 and not re.search(r"(?:不足|局限|缺点|问题|改进|后续)", text):
            return True
        return False

    @staticmethod
    def _check_abstract_only(text: str, unit: TextUnit) -> bool:
        """Check if paragraph only discusses abstract concepts without application."""
        if len(text) < 50:
            return False
        # Count concrete indicators
        concrete = len(re.findall(r"\d+", text))
        has_specific = bool(re.search(r"(?:本文|本系统|我们|项目中|开发中)", text))
        if concrete < 1 and not has_specific and unit.section in ("tech_background", "design", ""):
            return True
        return False

    @staticmethod
    def _check_flowchart_prose(text: str, unit: TextUnit) -> bool:
        """Check if technical content is described as prose instead of specifics."""
        if unit.section not in ("implementation", "design", ""):
            return False
        if len(text) > 80 and re.search(r"(?:首先|然后|接着|最后).{0,30}(?:模块|功能|步骤)", text):
            if not re.search(r"(?:def |function|class |@|api|接口|参数|返回)", text):
                return True
        return False

    def _assess_risk(self, tags: list[DiagnosisTag], unit: TextUnit) -> RiskLevel:
        """Assess risk level from diagnosis tags."""
        if unit.risk_level != RiskLevel.UNKNOWN:
            return unit.risk_level  # respect report-driven level

        high_tags = {DiagnosisTag.TEMPLATE_SKELETON, DiagnosisTag.HOLLOW_CONCLUSION,
                     DiagnosisTag.GRAND_NARRATIVE}
        medium_tags = {DiagnosisTag.ENCYCLOPEDIA_STYLE, DiagnosisTag.MISSING_DETAIL,
                       DiagnosisTag.PSEUDO_ANALYSIS}

        tag_set = set(tags)
        if tag_set & high_tags:
            return RiskLevel.HIGH
        if tag_set & medium_tags:
            return RiskLevel.MEDIUM
        if tags:
            return RiskLevel.LOW
        return RiskLevel.MINIMAL

    def _recommend_action(
        self, tags: list[DiagnosisTag], risk: RiskLevel, unit: TextUnit
    ) -> ActionType:
        """Recommend rewrite action based on diagnosis."""
        if unit.is_protected:
            return ActionType.FREEZE

        if risk == RiskLevel.HIGH:
            # High risk + template skeleton or hollow = rebuild
            if DiagnosisTag.TEMPLATE_SKELETON in tags or DiagnosisTag.HOLLOW_CONCLUSION in tags:
                return ActionType.REBUILD
            return ActionType.REWRITE
        elif risk == RiskLevel.MEDIUM:
            return ActionType.REWRITE
        elif risk == RiskLevel.LOW:
            return ActionType.MODIFY
        else:
            return ActionType.FREEZE

    def _build_reasoning(self, d: ParagraphDiagnosis) -> str:
        """Build a human-readable reasoning string."""
        if not d.tags:
            return "无明显AI特征"

        tag_descriptions = {
            DiagnosisTag.TEMPLATE_SKELETON: "存在模板句式(如'随着...发展')",
            DiagnosisTag.GRAND_NARRATIVE: "存在宏大叙事,缺少具体内容",
            DiagnosisTag.ENCYCLOPEDIA_STYLE: "百科式概念介绍,未联系本文实际",
            DiagnosisTag.MISSING_DETAIL: "缺少具体数据/过程/参数",
            DiagnosisTag.UNIFORM_SENTENCE: "句式过于统一",
            DiagnosisTag.OVERLY_SMOOTH: "文本过于顺滑,缺少自然转折",
            DiagnosisTag.HOLLOW_CONCLUSION: "空泛结论(如'具有良好的可行性')",
            DiagnosisTag.VAGUE_ACTION: "模糊动作描述(如'进行了处理')",
            DiagnosisTag.POLICY_SPEAK: "政策套话",
            DiagnosisTag.NO_LIMITATIONS: "缺少局限/不足分析",
            DiagnosisTag.ABSTRACT_ONLY: "只写抽象概念,缺少具体应用",
            DiagnosisTag.FLOWCHART_PROSE: "将技术流程写成散文,缺少具体实现细节",
            DiagnosisTag.PSEUDO_ANALYSIS: "伪分析,缺少真正的因果推理",
        }
        parts = [tag_descriptions.get(t, t.value) for t in d.tags]
        return "; ".join(parts)

    def _suggest_evidence(self, tags: list[DiagnosisTag], unit: TextUnit) -> str:
        """Suggest what kind of evidence/information would help."""
        suggestions = []
        section = unit.section

        if DiagnosisTag.MISSING_DETAIL in tags:
            if section in ("implementation", "design"):
                suggestions.append("开发环境、模块输入输出、接口参数、测试数据")
            elif section == "testing":
                suggestions.append("测试步骤、测试用例、预期结果、实际结果")
            else:
                suggestions.append("具体数据、研究过程、案例细节")

        if DiagnosisTag.ABSTRACT_ONLY in tags:
            suggestions.append("本文系统中的具体应用方式")

        if DiagnosisTag.TEMPLATE_SKELETON in tags or DiagnosisTag.HOLLOW_CONCLUSION in tags:
            suggestions.append("真实研究过程、实际遇到的问题、局限性分析")

        if DiagnosisTag.PSEUDO_ANALYSIS in tags:
            suggestions.append("因果推理链、对比分析、实际案例")

        return "; ".join(suggestions) if suggestions else "建议补充具体研究过程和细节"
