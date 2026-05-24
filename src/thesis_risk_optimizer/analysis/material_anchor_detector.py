"""Detect discipline-specific material anchors in thesis paragraphs."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..strategies.domain_profiles import DomainProfile, get_domain_profile


@dataclass
class MaterialAnchorResult:
    anchor_score: float = 0.0
    anchor_terms: list[str] = field(default_factory=list)
    missing_anchor_warning: str = ""
    domain_matched: str = "universal"


class MaterialAnchorDetector:
    """Domain-aware detector for concrete thesis material anchors."""

    def detect(self, text: str, domain: str | DomainProfile | None = None) -> MaterialAnchorResult:
        profile = domain if isinstance(domain, DomainProfile) else get_domain_profile(domain)
        matched: list[str] = []

        for label, patterns in profile.material_anchors.items():
            if self._matches_any(text, patterns):
                matched.append(label)

        score = min(100.0, len(matched) * 22.0)
        warning = ""
        if not matched and len(text.strip()) >= 18:
            warning = f"缺少{profile.name}专业材料锚点，不能安全补充不存在的材料"

        return MaterialAnchorResult(
            anchor_score=score,
            anchor_terms=matched,
            missing_anchor_warning=warning,
            domain_matched=profile.name,
        )

    @staticmethod
    def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
        for pattern in patterns:
            if pattern.startswith("re:"):
                if re.search(pattern[3:], text):
                    return True
            elif pattern in text:
                return True
        return False
