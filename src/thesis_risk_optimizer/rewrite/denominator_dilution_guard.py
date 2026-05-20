"""Denominator dilution guard: detect when AIGC rate drops from text expansion, not risk reduction.

This guard triggers when:
1. AIGC rate decreased
2. total_chars increased > 15%
3. risk_chars did not decrease OR decreased < 10%
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DilutionResult:
    """Result of denominator dilution check."""
    triggered: bool = False
    reasons: list[str] = field(default_factory=list)
    warning_message: str = ""


class DenominatorDilutionGuard:
    """Detect 'denominator dilution' — lowering AIGC rate by expanding text."""

    # Thresholds
    LENGTH_GROWTH_THRESHOLD = 0.15  # 15% growth triggers check
    RISK_DECREASE_MIN = 0.10  # risk_chars must decrease by at least 10%

    def check(
        self,
        before_rate: float,
        after_rate: float,
        before_total_chars: int,
        after_total_chars: int,
        before_risk_chars: int,
        after_risk_chars: int,
    ) -> DilutionResult:
        """Check if rate drop comes from denominator dilution.

        Args:
            before_rate: AIGC rate before optimization
            after_rate: AIGC rate after optimization
            before_total_chars: Total chars before optimization
            after_total_chars: Total chars after optimization
            before_risk_chars: Risk chars (red+orange+purple) before
            after_risk_chars: Risk chars (red+orange+purple) after

        Returns:
            DilutionResult with triggered flag and warning message
        """
        result = DilutionResult()

        # Only check if rate actually decreased
        rate_decreased = after_rate < before_rate
        if not rate_decreased:
            return result

        # Check if text expanded significantly
        if before_total_chars <= 0:
            return result

        length_growth = (after_total_chars - before_total_chars) / before_total_chars
        if length_growth <= self.LENGTH_GROWTH_THRESHOLD:
            return result

        # Check if risk_chars didn't decrease enough
        risk_decreased = after_risk_chars < before_risk_chars
        if risk_decreased:
            risk_decrease_ratio = (before_risk_chars - after_risk_chars) / max(1, before_risk_chars)
            if risk_decrease_ratio >= self.RISK_DECREASE_MIN:
                # Risk decreased enough, not dilution
                return result

        # Triggered: rate drop from expansion, not risk reduction
        result.triggered = True
        result.reasons = [
            f"AIGC 疑似率下降 ({before_rate:.1f}% → {after_rate:.1f}%)",
            f"但总字数增长 {length_growth:.0%}，超过 {self.LENGTH_GROWTH_THRESHOLD:.0%} 阈值",
            f"风险字符未显著减少 ({before_risk_chars} → {after_risk_chars})",
        ]
        result.warning_message = (
            "本轮疑似率下降主要来自文本总量增加，而非风险内容减少，"
            "不建议作为有效优化结果。"
        )

        return result
