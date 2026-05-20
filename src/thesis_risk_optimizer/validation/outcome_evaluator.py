"""Optimization outcome evaluator: determine whether an optimization round succeeded.

Every optimization round must be evaluated against these criteria:
1. AIGC rate must decrease (or at least not increase)
2. Risk characters must decrease
3. Red/purple characters must not increase
4. Total chars within hard_range
5. No discipline strategy misuse detected
6. Second round must not produce same result as first round

If any criterion fails, the round is declared failed and rollback is recommended.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..report_parser.aigc_report_parser import AigcReport, ColorBand


@dataclass
class OutcomeResult:
    """Result of evaluating an optimization round."""

    verdict: str = "unknown"  # "success" | "failed" | "rollback_recommended"
    failure_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollback_recommended: bool = False

    # Per-criterion results
    rate_decreased: Optional[bool] = None
    rate_drop_sufficient: Optional[bool] = None
    risk_chars_decreased: Optional[bool] = None
    red_chars_not_increased: Optional[bool] = None
    purple_chars_not_increased: Optional[bool] = None
    length_in_range: Optional[bool] = None
    strategy_misuse_detected: bool = False
    same_as_previous: bool = False

    # Detailed stats
    before_rate: Optional[float] = None
    after_rate: Optional[float] = None
    rate_delta: float = 0.0


class OptimizationOutcomeEvaluator:
    """Evaluate optimization outcome against success criteria.

    Failure conditions (any ONE = FAILED):
    - AIGC rate increases
    - AIGC rate drops less than 5 percentage points
    - red_chars increases
    - purple_chars increases
    - risk_chars increases
    - total chars exceeds hard_range (outside 85%-120%)
    - computer_mode used on non-computer thesis
    - HR thesis has computer-style details injected
    - Second round produces same result as first round
    """

    MIN_RATE_DROP = 5.0  # minimum percentage points
    HARD_RANGE_LOW = 0.85
    HARD_RANGE_HIGH = 1.20

    def evaluate(
        self,
        before_report: AigcReport,
        after_report: AigcReport,
        before_doc_chars: int = 0,
        after_doc_chars: int = 0,
        discipline: str = "universal",
        assigned_strategy: str = "universal",
        previous_after_rate: Optional[float] = None,
    ) -> OutcomeResult:
        """Evaluate the outcome of one optimization round.

        Args:
            before_report: AIGC report before optimization
            after_report: AIGC report after optimization
            before_doc_chars: Total chars in original document
            after_doc_chars: Total chars in optimized document
            discipline: Detected discipline
            assigned_strategy: Strategy actually used
            previous_after_rate: After-rate from a previous round (for feedback detection)

        Returns:
            OutcomeResult with verdict and failure reasons.
        """
        result = OutcomeResult()

        # Extract statistics
        before_red = self._count_chars(before_report, ColorBand.RED)
        after_red = self._count_chars(after_report, ColorBand.RED)
        before_purple = self._count_chars(before_report, ColorBand.PURPLE)
        after_purple = self._count_chars(after_report, ColorBand.PURPLE)
        before_risk = self._count_risk_chars(before_report)
        after_risk = self._count_risk_chars(after_report)
        before_rate = before_report.overall_rate
        after_rate = after_report.overall_rate

        result.before_rate = before_rate
        result.after_rate = after_rate

        # 1. Rate check
        if before_rate is not None and after_rate is not None:
            result.rate_delta = before_rate - after_rate
            result.rate_decreased = result.rate_delta > 0
            result.rate_drop_sufficient = result.rate_delta >= self.MIN_RATE_DROP

            if not result.rate_decreased:
                result.failure_reasons.append(
                    f"AIGC 疑似率上升 ({before_rate:.1f}% → {after_rate:.1f}%)"
                )
            elif not result.rate_drop_sufficient:
                result.failure_reasons.append(
                    f"AIGC 疑似率降幅不足 (下降仅 {result.rate_delta:.1f} 个百分点，"
                    f"未达到 {self.MIN_RATE_DROP} 个百分点阈值)"
                )

        # 2. Red chars check
        result.red_chars_not_increased = after_red <= before_red
        if not result.red_chars_not_increased:
            result.failure_reasons.append(
                f"红色字符增加 ({before_red} → {after_red})，存在新增高风险内容"
            )

        # 3. Purple chars check
        result.purple_chars_not_increased = after_purple <= before_purple
        if not result.purple_chars_not_increased:
            result.failure_reasons.append(
                f"紫色字符增加 ({before_purple} → {after_purple})，存在新增中高风险内容"
            )

        # 4. Risk chars check
        result.risk_chars_decreased = after_risk < before_risk
        if not result.risk_chars_decreased:
            result.failure_reasons.append(
                f"风险字符总量未减少 ({before_risk} → {after_risk})"
            )

        # 5. Length check
        if before_doc_chars > 0:
            length_ratio = after_doc_chars / before_doc_chars
            result.length_in_range = (
                self.HARD_RANGE_LOW <= length_ratio <= self.HARD_RANGE_HIGH
            )
            if not result.length_in_range:
                if length_ratio > self.HARD_RANGE_HIGH:
                    result.failure_reasons.append(
                        f"总字数增长 {length_ratio:.0%}，超过硬上限 {self.HARD_RANGE_HIGH:.0%}"
                    )
                else:
                    result.failure_reasons.append(
                        f"总字数压缩至 {length_ratio:.0%}，低于硬下限 {self.HARD_RANGE_LOW:.0%}"
                    )

        # 6. Strategy misuse check
        if discipline not in ("computer",) and assigned_strategy == "computer":
            result.strategy_misuse_detected = True
            result.failure_reasons.append(
                f"检测到 computer 策略误用于 {discipline} 专业论文"
            )

        # 7. HR-specific check: no computer-style details in HR thesis
        if discipline in ("human_resource", "management"):
            self._check_hr_no_computer_details(after_report, result)

        # 8. Second round same-as-previous check
        if previous_after_rate is not None and after_rate is not None:
            if abs(after_rate - previous_after_rate) < 0.01:
                result.same_as_previous = True
                result.failure_reasons.append(
                    "二轮优化结果与一轮完全相同，没有进一步改善"
                )

        # Determine verdict
        if result.failure_reasons:
            result.verdict = "failed"
            result.rollback_recommended = True
        else:
            result.verdict = "success"
            result.rollback_recommended = False

        return result

    def _count_chars(self, report: AigcReport, band: str) -> int:
        return sum(len(f.text) for f in report.fragments if f.color_band == band)

    def _count_risk_chars(self, report: AigcReport) -> int:
        """Count red + orange + purple characters."""
        total = 0
        for band in [ColorBand.RED, ColorBand.ORANGE, ColorBand.PURPLE]:
            total += self._count_chars(report, band)
        return total

    def _check_hr_no_computer_details(self, report: AigcReport, result: OutcomeResult):
        """Check that HR/management thesis does not contain computer-style details."""
        computer_patterns = [
            "Python", "Java", "Spring", "Django", "Flask", "MySQL", "Redis",
            "Docker", "API", "HTTP", "JSON", "XML", "SQL", "CSS", "HTML",
            "function", "class", "def ", "import ", "npm ", "pip ",
            "数据库表", "接口文档", "前端", "后端", "服务器部署",
        ]
        found = set()
        for frag in report.fragments:
            for pat in computer_patterns:
                if pat.lower() in frag.text.lower():
                    found.add(pat)

        if found:
            result.strategy_misuse_detected = True
            result.failure_reasons.append(
                f"人力资源/管理论文中出现计算机式细节: {', '.join(sorted(found)[:5])}"
            )

    def format_report(self, result: OutcomeResult) -> str:
        """Format a human-readable evaluation report."""
        lines = []
        lines.append("## 优化结果评估")
        lines.append("")

        if result.verdict == "success":
            lines.append("**本轮优化成功 ✅**")
        else:
            lines.append("**本轮优化失败 ❌**")
            if result.rollback_recommended:
                lines.append("**建议回滚到原文，不建议使用改后版本。**")

        if result.before_rate is not None and result.after_rate is not None:
            lines.append(f"\nAIGC 疑似率: {result.before_rate:.1f}% → {result.after_rate:.1f}% "
                         f"(变动 {result.rate_delta:+.1f} pp)")

        if result.failure_reasons:
            lines.append("\n### 失败原因")
            for reason in result.failure_reasons:
                lines.append(f"- {reason}")

        if result.warnings:
            lines.append("\n### 警告")
            for w in result.warnings:
                lines.append(f"- {w}")

        return "\n".join(lines)
