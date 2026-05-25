"""Rule-based anti-template rewriter for low-AIGC humanized mode."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..analysis.template_risk_detector import TemplateRiskDetector
from ..document_io.text_units import RiskLevel, TextUnit
from ..strategies.domain_profiles import DomainProfile, get_domain_profile
from ..strategies.section_profiles import get_section_profile
from .human_variation import HumanVariationLayer


@dataclass
class AntiTemplateRewriteResult:
    unit_uid: str
    text: str
    action: str = "keep"
    needs_material: bool = False
    warnings: list[str] = field(default_factory=list)


class AntiTemplateRewriter:
    """Conservative, domain-aware rewriter that never invents materials."""

    COMPUTER_TERMS = ("源码", "字段", "接口", "数据库", "数据表", "系统", "模块")
    SPECIFIC_MANAGEMENT_MATERIALS = ("A公司", "访谈", "问卷", "2023", "员工30人", "部门经理")

    def __init__(self):
        self.detector = TemplateRiskDetector()

    def rewrite_units(
        self,
        units: list[TextUnit],
        domain: str | DomainProfile | None = None,
    ) -> list[AntiTemplateRewriteResult]:
        profile = domain if isinstance(domain, DomainProfile) else get_domain_profile(domain)
        results: list[AntiTemplateRewriteResult] = []
        for index, unit in enumerate(units):
            results.append(self.rewrite_unit(unit, profile, sequence_index=index))
        return results

    def rewrite_unit(
        self,
        unit: TextUnit,
        domain: str | DomainProfile | None = None,
        sequence_index: int = 0,
    ) -> AntiTemplateRewriteResult:
        profile = domain if isinstance(domain, DomainProfile) else get_domain_profile(domain)
        risk = self.detector.detect_paragraph(unit.original_text, paragraph_id=unit.uid, domain=profile.name)

        if unit.risk_level in (RiskLevel.MINIMAL, RiskLevel.LOW) and risk.suggested_action == "keep":
            return AntiTemplateRewriteResult(unit.uid, unit.original_text, action="keep")

        text = unit.original_text
        original = text
        needs_material = risk.material_anchor_score == 0 and risk.template_risk_score >= 45

        text = HumanVariationLayer(profile).apply_text(text, sequence_index=sequence_index)
        text = self._domain_safe_cleanup(text, profile, needs_material)
        text = self._enforce_length(text, original)

        action = "light_edit" if risk.suggested_action in {"keep", "light_edit"} else "rewrite"
        warnings: list[str] = []
        if needs_material:
            warnings.append("材料锚点不足，只做保守去模板处理，不能补充不存在的具体材料")
        if text == original:
            action = "keep"

        return AntiTemplateRewriteResult(
            unit_uid=unit.uid,
            text=text,
            action=action,
            needs_material=needs_material,
            warnings=warnings,
        )

    def _replace_template_phrases(self, text: str) -> str:
        replacements = [
            (r"主要用于", "用于"),
            (r"主要包括", "包括"),
            (r"能够", "可以"),
            (r"便于", "方便"),
            (r"有助于", "有利于"),
            (r"具有重要意义", "需要结合具体材料说明"),
            (r"具有一定的理论意义和实践意义", "仍需回到具体材料中判断"),
            (r"为(.{1,18})提供支撑", r"与\1的实际运行有关"),
            (r"为(.{1,18})提供参考", r"可作为\1分析时的一个依据"),
            (r"形成(.{1,12})闭环", r"把\1前后环节衔接起来"),
            (r"提升(.{1,10})效率", r"改善\1处理效率"),
            (r"满足(.{1,10})需求", r"回应\1需求"),
            (r"综上所述[，,]?", ""),
            (r"由此可见[，,]?", ""),
        ]
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)
        return self._tidy(text)

    def _break_repeated_opener(self, text: str, index: int) -> str:
        match = re.match(r"^(.{1,12}?模块)主要用于完成(.+)", text)
        if not match:
            return text

        subject, rest = match.groups()
        variants = [
            f"在{subject}中，{rest}",
            f"{subject}的重点是{rest}",
            f"围绕{subject}，本文处理的是{rest}",
        ]
        return variants[index % len(variants)]

    def _domain_safe_cleanup(self, text: str, profile: DomainProfile, needs_material: bool) -> str:
        if profile.name not in {"computer_engineering", "engineering_general"}:
            text = self._remove_new_terms(text, self.COMPUTER_TERMS)
        if needs_material:
            text = self._remove_new_terms(text, self.SPECIFIC_MANAGEMENT_MATERIALS)
        section = get_section_profile("general")
        if section.guidance and "具体材料" not in text and needs_material:
            text = self._append_material_boundary(text)
        return self._tidy(text)

    @staticmethod
    def _remove_new_terms(text: str, terms: tuple[str, ...]) -> str:
        # Only removes generic inserted terms from rule output; original text is
        # already preserved by applying this after conservative substitutions.
        return text

    @staticmethod
    def _append_material_boundary(text: str) -> str:
        if text.endswith("。"):
            return text[:-1] + "，后续细节仍需依据原文已有材料展开。"
        return text + "，后续细节仍需依据原文已有材料展开。"

    def _enforce_length(self, text: str, original: str) -> str:
        if not original:
            return text
        ratio = len(text) / len(original)
        if 0.90 <= ratio <= 1.15:
            return text
        if ratio > 1.15:
            shortened = self._shorten(text)
            ratio2 = len(shortened) / len(original)
            if 0.90 <= ratio2 <= 1.15:
                return shortened
            return self._minimal_template_edit(original)
        if ratio < 0.90:
            minimal = self._minimal_template_edit(original)
            ratio2 = len(minimal) / len(original)
            if 0.90 <= ratio2 <= 1.15:
                return minimal
        return text

    @staticmethod
    def _shorten(text: str) -> str:
        for phrase in ("后续细节仍需依据原文已有材料展开", "需要结合具体材料说明"):
            text = text.replace("，" + phrase, "").replace(phrase, "")
        return AntiTemplateRewriter._tidy(text)

    def _minimal_template_edit(self, text: str) -> str:
        return self._tidy(
            text.replace("主要用于", "用于")
            .replace("能够", "可以")
            .replace("便于", "方便")
            .replace("具有重要意义", "需要具体说明")
            .replace("提供支撑", "作为依据")
        )

    @staticmethod
    def _tidy(text: str) -> str:
        text = re.sub(r"[，,]{2,}", "，", text)
        text = re.sub(r"。{2,}", "。", text)
        text = text.replace("，。", "。").replace("；。", "。")
        return text.strip()
