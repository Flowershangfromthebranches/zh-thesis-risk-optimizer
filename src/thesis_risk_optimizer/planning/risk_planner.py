"""RiskPlanner: plans modify/rewrite/rebuild proportions based on AIGC rates.

Step 3 of the 7-step workflow.
Uses current_rate, target_rate, and gap to determine processing intensity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RiskPlanResult:
    """Result of risk-based planning."""

    current_rate: float = 0.0
    target_rate: float = 0.0
    gap: float = 0.0
    modify_ratio: float = 0.0
    rewrite_ratio: float = 0.0
    rebuild_ratio: float = 0.0
    intensity: str = ""  # low / medium / high / critical
    warnings: list[str] = field(default_factory=list)


class RiskPlanner:
    """Plans processing intensity based on AIGC rates.

    Rules:
    - current_rate < 30: modify-dominant
    - 30 <= current_rate < 50: modify + rewrite
    - 50 <= current_rate < 70: rewrite-dominant
    - current_rate >= 70: rewrite/rebuild dominant
    - gap > 30: large gap warning
    """

    def plan(
        self,
        current_rate: float,
        target_rate: float,
        allow_rewrite: bool = True,
        allow_supplement: bool = True,
        has_materials: bool = False,
    ) -> RiskPlanResult:
        """Plan the modify/rewrite/rebuild ratios.

        Args:
            current_rate: Current AIGC suspicion rate (0-100).
            target_rate: Target AIGC suspicion rate (0-100).
            allow_rewrite: Whether user allows rewriting.
            allow_supplement: Whether user allows content supplementation.
            has_materials: Whether user has provided materials.

        Returns:
            RiskPlanResult with planned ratios and warnings.
        """
        result = RiskPlanResult(
            current_rate=current_rate,
            target_rate=target_rate,
            gap=current_rate - target_rate,
        )

        # Base ratios from current rate
        if current_rate < 30:
            result.modify_ratio = 0.80
            result.rewrite_ratio = 0.20
            result.rebuild_ratio = 0.00
            result.intensity = "low"
        elif current_rate < 50:
            result.modify_ratio = 0.50
            result.rewrite_ratio = 0.40
            result.rebuild_ratio = 0.10
            result.intensity = "medium"
        elif current_rate < 70:
            result.modify_ratio = 0.25
            result.rewrite_ratio = 0.55
            result.rebuild_ratio = 0.20
            result.intensity = "high"
        else:
            result.modify_ratio = 0.10
            result.rewrite_ratio = 0.50
            result.rebuild_ratio = 0.40
            result.intensity = "critical"

        # Adjust based on permissions
        if not allow_rewrite:
            # Can only modify
            result.modify_ratio = 1.0
            result.rewrite_ratio = 0.0
            result.rebuild_ratio = 0.0
            result.warnings.append(
                "用户不允许重写，只能做轻度修改，效果可能有限。"
            )

        if not allow_supplement and result.intensity in ("high", "critical"):
            result.warnings.append(
                "用户不允许补充内容，系统只能在原文范围内调整表达，"
                "可能难以显著降低 AIGC 疑似率。"
            )

        # Large gap warning
        if result.gap > 30:
            result.warnings.append(
                f"目标降幅较大（{result.gap:.1f} 个百分点），"
                "可能需要较高比例重写和内容重构。"
                "如果不允许重写或不允许补充材料，实际效果可能无法达到目标。"
            )

        # No materials warning for high intensity
        if not has_materials and result.intensity in ("high", "critical"):
            result.warnings.append(
                "未提供写论文时用到的材料，重写/重构时只能基于原文和模型常识，"
                "可能影响改写质量和真实感。"
            )

        return result
