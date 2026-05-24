"""Shared human-variation layer for all domain profiles.

This layer is intentionally domain-aware but not discipline-specific strategy
code.  It reduces common template residue, varies repeated openers, and keeps
low-risk text from being over-polished into a more formal template.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..document_io.text_units import RiskLevel, TextUnit
from ..strategies.domain_profiles import DomainProfile, get_domain_profile


@dataclass
class HumanVariationResult:
    unit_uid: str
    text: str
    action: str = "keep"
    warnings: list[str] = field(default_factory=list)


class HumanVariationLayer:
    """Apply low-risk, domain-aware human variation to text."""

    COMMON_REPLACEMENTS: tuple[tuple[str, str], ...] = (
        (r"主要用于", "用于"),
        (r"主要包括", "包括"),
        (r"能够", "可以"),
        (r"便于", "方便"),
        (r"有助于", "有利于"),
        (r"通过(.{1,20})实现", r"借助\1完成"),
        (r"具有重要意义", "需要回到具体材料中说明"),
        (r"具有一定的理论意义和实践意义", "仍需结合具体材料判断其价值"),
        (r"提供支撑", "作为依据"),
        (r"形成闭环", "衔接前后环节"),
        (r"提升水平", "把执行情况落到具体环节"),
        (r"综上所述[，,]?", ""),
        (r"由此可见[，,]?", ""),
    )

    HR_REPLACEMENTS: tuple[tuple[str, str], ...] = (
        (r"完善机制", "明确制度执行中容易脱节的环节"),
        (r"进一步完善相关机制", "把责任分工和检查方式写清楚"),
        (r"加强培训", "把培训内容和岗位任务对应起来"),
        (r"提升员工满意度", "回应员工反馈中反复出现的问题"),
        (r"提高员工满意度", "回应员工反馈中反复出现的问题"),
        (r"增强企业凝聚力", "减少员工对制度执行不一致的疑虑"),
        (r"推动企业高质量发展", "回到企业当前的人力资源问题本身"),
        (r"促进企业可持续发展", "回到企业当前的人力资源问题本身"),
        (r"构建长效机制", "把后续跟踪和复盘责任固定下来"),
        (r"多措并举", "分别处理前文提到的几个问题"),
        (r"从制度层面、管理层面、员工层面", "围绕制度执行、管理沟通和员工反馈"),
    )

    COMPUTER_TERMS = ("源码", "接口", "字段", "数据库", "数据表", "版本号", "Python", "Java", "API")

    def __init__(self, domain: str | DomainProfile | None = None):
        self.profile = domain if isinstance(domain, DomainProfile) else get_domain_profile(domain)

    def apply_units(self, units: list[TextUnit]) -> list[HumanVariationResult]:
        results: list[HumanVariationResult] = []
        for index, unit in enumerate(units):
            results.append(self.apply_unit(unit, sequence_index=index))
        return results

    def apply_unit(self, unit: TextUnit, sequence_index: int = 0) -> HumanVariationResult:
        if unit.risk_level in (RiskLevel.MINIMAL, RiskLevel.LOW) and not self._has_template(unit.original_text):
            return HumanVariationResult(unit.uid, unit.original_text, action="keep")

        text = self.apply_text(unit.original_text, sequence_index=sequence_index)
        action = "light_edit" if text != unit.original_text else "keep"
        return HumanVariationResult(unit.uid, text, action=action)

    def apply_text(self, text: str, sequence_index: int = 0) -> str:
        original = text
        text = self._vary_opener(text, sequence_index)
        text = self._apply_replacements(text, self.COMMON_REPLACEMENTS)

        if self.profile.name in {"human_resource", "management"}:
            text = self._apply_replacements(text, self.HR_REPLACEMENTS)

        if self.profile.name not in {"computer_engineering", "engineering_general"}:
            text = self._avoid_computer_insertions(text, original)

        text = self._vary_sentence_length(text)
        return self._tidy(text)

    @classmethod
    def _has_template(cls, text: str) -> bool:
        patterns = [
            r"主要用于", r"能够", r"便于", r"通过.{1,20}实现",
            r"具有重要意义", r"完善机制", r"提升水平",
            r"提升员工满意度", r"增强企业凝聚力", r"推动企业高质量发展",
        ]
        return any(re.search(pattern, text) for pattern in patterns)

    def _vary_opener(self, text: str, index: int) -> str:
        match = re.match(r"^(.{2,16}?)(?:主要用于|用于)完成(.+)", text)
        if not match:
            return text
        subject, rest = match.groups()
        variants = [
            f"在{subject}中，重点是{rest}",
            f"{subject}处理的是{rest}",
            f"围绕{subject}，原文讨论的是{rest}",
        ]
        return variants[index % len(variants)]

    @staticmethod
    def _apply_replacements(text: str, replacements: tuple[tuple[str, str], ...]) -> str:
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)
        return text

    def _avoid_computer_insertions(self, text: str, original: str) -> str:
        for term in self.COMPUTER_TERMS:
            if term in text and term not in original:
                text = text.replace(term, "")
        return text

    @staticmethod
    def _vary_sentence_length(text: str) -> str:
        text = re.sub(r"，并且", "。同时，", text, count=1)
        text = re.sub(r"，同时，", "。同时，", text, count=1)
        return text

    @staticmethod
    def _tidy(text: str) -> str:
        text = re.sub(r"[，,]{2,}", "，", text)
        text = text.replace("，。", "。").replace("。。", "。")
        text = re.sub(r"\s+", "", text)
        return text.strip()
