"""PlanSummary: generates a summary for user confirmation before optimization.

Must be shown to the user and confirmed before ExecuteOptimize runs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .risk_planner import RiskPlanResult


@dataclass
class PlanSummary:
    """Summary of the optimization plan for user confirmation."""

    major: str = ""
    title: str = ""
    current_rate: float = 0.0
    target_rate: float = 0.0
    has_report: bool = False
    allow_rewrite: bool = False
    allow_supplement: bool = False
    has_materials: bool = False
    strategy_name: str = ""
    route_name: str = ""
    modify_ratio: float = 0.0
    rewrite_ratio: float = 0.0
    rebuild_ratio: float = 0.0
    intensity: str = ""
    risk_warnings: list[str] = field(default_factory=list)
    permission_warnings: list[str] = field(default_factory=list)
    confirmation_needed: list[str] = field(default_factory=list)

    def to_text(self) -> str:
        """Format as user-facing text."""
        lines = [
            "=" * 60,
            "  优化方案确认",
            "=" * 60,
            "",
            f"  论文专业：{self.major}",
            f"  论文题目：{self.title}",
            f"  当前 AIGC 疑似率：{self.current_rate}%",
            f"  目标 AIGC 疑似率：{self.target_rate}%",
            f"  是否有报告：{'有' if self.has_report else '无'}",
            f"  是否允许重写：{'是' if self.allow_rewrite else '否'}",
            f"  是否允许补充内容：{'是' if self.allow_supplement else '否'}",
            f"  是否有材料：{'有' if self.has_materials else '无'}",
            "",
            f"  选择的专业路线：{self.route_name}",
            f"  使用策略：{self.strategy_name}",
            f"  处理强度：{self.intensity}",
            f"  预计比例：modify={self.modify_ratio:.0%} / "
            f"rewrite={self.rewrite_ratio:.0%} / "
            f"rebuild={self.rebuild_ratio:.0%}",
            "",
        ]

        if self.risk_warnings:
            lines.append("  ⚠️ 风险提示：")
            for w in self.risk_warnings:
                lines.append(f"    - {w}")
            lines.append("")

        if self.permission_warnings:
            lines.append("  ⚠️ 权限提示：")
            for w in self.permission_warnings:
                lines.append(f"    - {w}")
            lines.append("")

        if self.confirmation_needed:
            lines.append("  ❓ 需要确认：")
            for q in self.confirmation_needed:
                lines.append(f"    - {q}")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)


class PlanSummaryGenerator:
    """Generates a PlanSummary from intake data and risk plan."""

    def generate(
        self,
        major: str,
        title: str,
        current_rate: float,
        target_rate: float,
        has_report: bool,
        allow_rewrite: bool,
        allow_supplement: bool,
        has_materials: bool,
        strategy_name: str,
        route_name: str,
        risk_plan: RiskPlanResult,
        confirmation_needed: list[str] = None,
    ) -> PlanSummary:
        """Generate a plan summary.

        Args:
            major: User-declared thesis major.
            title: Thesis title.
            current_rate: Current AIGC suspicion rate.
            target_rate: Target AIGC suspicion rate.
            has_report: Whether AIGC report is available.
            allow_rewrite: Whether rewriting is allowed.
            allow_supplement: Whether supplementation is allowed.
            has_materials: Whether materials are available.
            strategy_name: Name of the selected strategy.
            route_name: Name of the route used.
            risk_plan: Result from RiskPlanner.
            confirmation_needed: Prompts needing user confirmation.

        Returns:
            PlanSummary ready for user display.
        """
        return PlanSummary(
            major=major,
            title=title,
            current_rate=current_rate,
            target_rate=target_rate,
            has_report=has_report,
            allow_rewrite=allow_rewrite,
            allow_supplement=allow_supplement,
            has_materials=has_materials,
            strategy_name=strategy_name,
            route_name=route_name,
            modify_ratio=risk_plan.modify_ratio,
            rewrite_ratio=risk_plan.rewrite_ratio,
            rebuild_ratio=risk_plan.rebuild_ratio,
            intensity=risk_plan.intensity,
            risk_warnings=risk_plan.warnings,
            confirmation_needed=confirmation_needed or [],
        )
