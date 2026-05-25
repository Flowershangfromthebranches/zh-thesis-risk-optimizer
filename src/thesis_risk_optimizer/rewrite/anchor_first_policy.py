"""Anchor-first policy for low-AIGC thesis rewriting.

The low-AIGC strategy should start from professional materials, not from
oralization.  This policy decides how much a paragraph may be changed based on
the anchors already present in the source text.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..analysis.material_anchor_detector import MaterialAnchorDetector
from ..strategies.domain_profiles import DomainProfile, get_domain_profile


@dataclass(frozen=True)
class AnchorFirstResult:
    domain_name: str
    anchor_score: float
    anchor_terms: list[str] = field(default_factory=list)
    has_anchor: bool = False
    allow_naturalization: bool = False
    suggested_action: str = "light_edit"
    missing_anchor_warning: str = ""
    policy_notes: list[str] = field(default_factory=list)


class AnchorFirstPolicy:
    """Prefer concrete domain anchors before any naturalization."""

    def __init__(self):
        self.detector = MaterialAnchorDetector()

    def evaluate(
        self,
        text: str,
        domain: str | DomainProfile | None = None,
        section: str = "body",
    ) -> AnchorFirstResult:
        profile = domain if isinstance(domain, DomainProfile) else get_domain_profile(domain)
        anchor = self.detector.detect(text, profile)
        has_anchor = anchor.anchor_score > 0
        notes: list[str] = []

        if has_anchor:
            notes.append("优先保留并围绕原文已有专业锚点重组表达")
            action = "rewrite" if anchor.anchor_score >= 44 else "light_edit"
            allow_naturalization = True
            warning = ""
        else:
            notes.append("材料锚点不足，只允许轻度句式调整和反模板处理")
            notes.append("不得通过增加口语化表达强行制造人类化")
            action = "light_edit"
            allow_naturalization = False
            warning = anchor.missing_anchor_warning or "材料锚点不足，建议补充真实材料"
            if "材料锚点不足" not in warning:
                warning = f"材料锚点不足：{warning}"

        return AnchorFirstResult(
            domain_name=profile.name,
            anchor_score=anchor.anchor_score,
            anchor_terms=anchor.anchor_terms,
            has_anchor=has_anchor,
            allow_naturalization=allow_naturalization,
            suggested_action=action,
            missing_anchor_warning=warning,
            policy_notes=notes,
        )
