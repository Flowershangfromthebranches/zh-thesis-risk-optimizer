"""Risk estimator: estimate AIGC risk level when no report is provided.

When the user doesn't provide an AIGC report, this module estimates
risk based on heuristic analysis of the text: template sentences,
lack of detail, uniform sentence structure, and shallow content.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from ..document_io.text_units import TextUnit, RiskLevel


# -- Template sentence patterns (high-risk indicators) ------------------------
TEMPLATE_PATTERNS = [
    re.compile(r"随着.*?(?:发展|进步|提高|深入)"),
    re.compile(r"具有(?:(?:十分|非常|极其)?重要的)?(?:现实|理论|实践)?意义"),
    re.compile(r"本文首先.*其次.*最后"),
    re.compile(r"实验结果表明.{0,20}(?:具有|有着|表现).{0,10}(?:良好|优秀|较高)"),
    re.compile(r"为.*?提供(?:了)?(?:参考|借鉴|依据)"),
    re.compile(r"具有(?:良好的|较高的)(?:可行性|实用性|稳定性)"),
    re.compile(r"在(?:新|当前|信息|大数据|互联网|人工智能).{0,10}(?:时代|背景|环境)下"),
    re.compile(r"有效(?:提升|提高|增强|改善|促进)了"),
    re.compile(r"实现了.*?(?:高效|智能|自动)化"),
    re.compile(r"对于.*?具有(?:重要|深远|积极)的?(?:影响|作用|意义)"),
    re.compile(r"国内外.*?(?:起步|发展|研究|现状)"),
    re.compile(r"通过.*?(?:验证|证明|表明).{0,20}(?:了.*?)(?:可行|有效|正确)"),
]

# -- Missing-detail indicators ------------------------------------------------
MISSING_DETAIL_PATTERNS = [
    re.compile(r"做了.*?处理"),  # vague "did processing"
    re.compile(r"进行了.*?分析"),  # vague "conducted analysis"
    re.compile(r"采用了.*?方法"),  # vague "used methods"
    re.compile(r"取得了.*?效果"),  # vague "achieved results"
]

# -- Uniform-sentence indicators ----------------------------------------------
# Check if paragraphs have similar lengths (low variance = AI-like)
# Check if most sentences are complete written-form sentences


@dataclass
class RiskEstimate:
    """Estimated risk for a thesis without a formal AIGC report."""

    overall_risk: RiskLevel = RiskLevel.UNKNOWN
    estimated_rate: float = 0.0
    template_score: float = 0.0
    detail_score: float = 0.0
    uniformity_score: float = 0.0
    shallowness_score: float = 0.0
    breakdown: dict = field(default_factory=dict)


class RiskEstimator:
    """Estimate AIGC risk heuristically from text characteristics.

    Usage:
        estimator = RiskEstimator()
        estimate = estimator.estimate(units)
    """

    def estimate(self, units: list[TextUnit]) -> RiskEstimate:
        """Estimate risk for a set of text units."""
        body_units = [u for u in units if u.is_body]
        if not body_units:
            return RiskEstimate()

        full_text = "\n".join(u.text for u in body_units)

        # 1. Template sentence density
        template_score = self._score_templates(full_text)

        # 2. Missing detail
        detail_score = self._score_missing_detail(body_units)

        # 3. Uniformity
        uniformity_score = self._score_uniformity(body_units)

        # 4. Content shallowness
        shallowness_score = self._score_shallowness(body_units)

        # Combine scores (weighted)
        estimated_rate = (
            template_score * 0.35
            + detail_score * 0.30
            + uniformity_score * 0.20
            + shallowness_score * 0.15
        ) * 100

        estimated_rate = min(95.0, max(5.0, estimated_rate))

        overall = (
            RiskLevel.HIGH if estimated_rate >= 70
            else RiskLevel.MEDIUM if estimated_rate >= 50
            else RiskLevel.LOW if estimated_rate >= 30
            else RiskLevel.MINIMAL
        )

        return RiskEstimate(
            overall_risk=overall,
            estimated_rate=round(estimated_rate, 1),
            template_score=round(template_score, 3),
            detail_score=round(detail_score, 3),
            uniformity_score=round(uniformity_score, 3),
            shallowness_score=round(shallowness_score, 3),
            breakdown={
                "template_weight": 0.35,
                "detail_weight": 0.30,
                "uniformity_weight": 0.20,
                "shallowness_weight": 0.15,
            },
        )

    def _score_templates(self, text: str) -> float:
        """Score template sentence density (0-1, higher = more template-like)."""
        if not text:
            return 0.0

        # Count characters that are part of template matches
        matched_chars = 0
        for pattern in TEMPLATE_PATTERNS:
            for m in pattern.finditer(text):
                matched_chars += len(m.group())

        # Normalize by text length, cap at 1.0
        ratio = min(1.0, matched_chars / max(1, len(text)) * 3)
        return ratio

    def _score_missing_detail(self, units: list[TextUnit]) -> float:
        """Score lack of concrete detail (0-1, higher = less detail)."""
        if not units:
            return 0.0

        vague_count = 0
        for unit in units:
            for pattern in MISSING_DETAIL_PATTERNS:
                if pattern.search(unit.text):
                    vague_count += 1
                    break

        ratio = vague_count / len(units)
        return min(1.0, ratio * 2)

    def _score_uniformity(self, units: list[TextUnit]) -> float:
        """Score sentence/paragraph uniformity (0-1, higher = more uniform/AI-like).

        Checks:
        - Paragraph length variance
        - Average sentence length consistency
        """
        if len(units) < 3:
            return 0.3

        lengths = [len(u.text) for u in units]
        if not lengths:
            return 0.0

        avg = sum(lengths) / len(lengths)
        if avg < 10:
            return 0.0

        # Coefficient of variation (lower = more uniform = higher score)
        variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
        std = variance ** 0.5
        cv = std / avg if avg > 0 else 1.0

        # Low CV = high uniformity = AI-like
        # CV < 0.3 → score near 1.0, CV > 1.0 → score near 0.0
        score = max(0.0, min(1.0, 1.0 - cv))
        return score

    def _score_shallowness(self, units: list[TextUnit]) -> float:
        """Score content shallowness (0-1, higher = more shallow).

        Checks if body text is mostly concept introductions without
        specific application, design rationale, or problem discussion.
        """
        if not units:
            return 0.0

        # Look for indicators of depth: concrete numbers, comparisons,
        # problem descriptions, limitations, specific tools/versions
        depth_patterns = [
            re.compile(r"\d+\.?\d*"),  # numbers
            re.compile(r"(?:因为|由于|原因|问题|不足|局限|缺点|错误|失败)"),
            re.compile(r"(?:版本|参数|配置|环境|接口|函数|方法)"),
            re.compile(r"(?:然而|但是|不过|尽管|虽然|实际上)"),
        ]

        shallow_count = 0
        for unit in units:
            depth_signals = sum(
                1 for p in depth_patterns if p.search(unit.text)
            )
            if depth_signals < 2 and len(unit.text) > 100:
                shallow_count += 1

        return min(1.0, shallow_count / max(1, len(units)))
