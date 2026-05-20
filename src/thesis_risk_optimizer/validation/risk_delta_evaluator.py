"""Risk delta evaluator: compare before/after AIGC reports to determine optimization success.

This module prevents "denominator dilution" — the strategy of expanding text to lower
AIGC percentage without actually reducing risk characters.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..report_parser.aigc_report_parser import AigcReportParser, AigcReport, ColorBand


@dataclass
class RiskDeltaResult:
    """Result of comparing before/after AIGC reports."""

    # Before report stats
    before_total_chars: int = 0
    before_red_chars: int = 0
    before_orange_chars: int = 0
    before_purple_chars: int = 0
    before_risk_chars: int = 0  # red + orange + purple
    before_rate: Optional[float] = None

    # After report stats
    after_total_chars: int = 0
    after_red_chars: int = 0
    after_orange_chars: int = 0
    after_purple_chars: int = 0
    after_risk_chars: int = 0  # red + orange + purple
    after_rate: Optional[float] = None

    # Deltas
    risk_char_delta: int = 0  # positive = increase (bad)
    risk_char_delta_ratio: float = 0.0
    rate_delta: float = 0.0  # positive = decrease (good)
    length_delta_ratio: float = 0.0  # after/before

    # Verdict
    verdict: str = "unknown"  # "success" | "failed" | "needs_second_round"
    failure_reasons: list[str] = None

    def __post_init__(self):
        if self.failure_reasons is None:
            self.failure_reasons = []


class RiskDeltaEvaluator:
    """Evaluate optimization success by comparing before/after AIGC reports.

    Success requires ALL of:
    1. AIGC rate drops >= 15 points OR below user target
    2. risk_chars (red+orange+purple) must decrease
    3. red_chars must not increase
    4. purple_chars must not increase
    5. Total chars within hard_range (85%-120%)
    """

    RATE_DROP_THRESHOLD = 15.0  # minimum percentage points drop
    HARD_RANGE_LOW = 0.85
    HARD_RANGE_HIGH = 1.20

    def evaluate(
        self,
        before_report: AigcReport,
        after_report: AigcReport,
        before_doc_chars: int = 0,
        after_doc_chars: int = 0,
        target_rate: Optional[float] = None,
    ) -> RiskDeltaResult:
        """Evaluate optimization success.

        Args:
            before_report: Parsed AIGC report before optimization
            after_report: Parsed AIGC report after optimization
            before_doc_chars: Total characters in original document
            after_doc_chars: Total characters in optimized document
            target_rate: User-specified target AIGC rate (optional)

        Returns:
            RiskDeltaResult with verdict and failure reasons
        """
        result = RiskDeltaResult()

        # Extract char counts from reports
        result.before_red_chars = self._count_chars(before_report, ColorBand.RED)
        result.before_orange_chars = self._count_chars(before_report, ColorBand.ORANGE)
        result.before_purple_chars = self._count_chars(before_report, ColorBand.PURPLE)
        result.before_risk_chars = result.before_red_chars + result.before_orange_chars + result.before_purple_chars
        result.before_total_chars = before_doc_chars or self._count_total_chars(before_report)
        result.before_rate = before_report.overall_rate

        result.after_red_chars = self._count_chars(after_report, ColorBand.RED)
        result.after_orange_chars = self._count_chars(after_report, ColorBand.ORANGE)
        result.after_purple_chars = self._count_chars(after_report, ColorBand.PURPLE)
        result.after_risk_chars = result.after_red_chars + result.after_orange_chars + result.after_purple_chars
        result.after_total_chars = after_doc_chars or self._count_total_chars(after_report)
        result.after_rate = after_report.overall_rate

        # Compute deltas
        result.risk_char_delta = result.after_risk_chars - result.before_risk_chars
        if result.before_risk_chars > 0:
            result.risk_char_delta_ratio = result.risk_char_delta / result.before_risk_chars

        if result.before_rate is not None and result.after_rate is not None:
            result.rate_delta = result.before_rate - result.after_rate

        if result.before_total_chars > 0:
            result.length_delta_ratio = result.after_total_chars / result.before_total_chars

        # Evaluate verdict
        result.verdict, result.failure_reasons = self._evaluate_verdict(
            result, target_rate
        )

        return result

    def _count_chars(self, report: AigcReport, band: str) -> int:
        """Count total characters in fragments of a specific band."""
        return sum(len(f.text) for f in report.fragments if f.color_band == band)

    def _count_total_chars(self, report: AigcReport) -> int:
        """Count total characters in all fragments."""
        return sum(len(f.text) for f in report.fragments)

    def _evaluate_verdict(
        self, result: RiskDeltaResult, target_rate: Optional[float]
    ) -> tuple[str, list[str]]:
        """Determine verdict based on all criteria.

        Returns (verdict, failure_reasons)
        """
        reasons = []

        # Check rate drop
        rate_dropped_enough = False
        if result.rate_delta >= self.RATE_DROP_THRESHOLD:
            rate_dropped_enough = True
        elif target_rate is not None and result.after_rate is not None:
            if result.after_rate <= target_rate:
                rate_dropped_enough = True

        if not rate_dropped_enough:
            reasons.append(
                f"AIGC 疑似率下降不足 (下降 {result.rate_delta:.1f} 个百分点，"
                f"未达到 {self.RATE_DROP_THRESHOLD} 个百分点阈值)"
            )

        # Check risk_chars must decrease
        if result.risk_char_delta > 0:
            reasons.append(
                f"风险字符绝对数量增加 ({result.before_risk_chars} → {result.after_risk_chars}，"
                f"+{result.risk_char_delta} 字符)"
            )
        elif result.risk_char_delta == 0:
            reasons.append("风险字符数量未减少")

        # Check red_chars must not increase
        if result.after_red_chars > result.before_red_chars:
            reasons.append(
                f"红色字符增加 ({result.before_red_chars} → {result.after_red_chars})，"
                "存在新增高风险内容"
            )

        # Check purple_chars must not increase
        if result.after_purple_chars > result.before_purple_chars:
            reasons.append(
                f"紫色字符增加 ({result.before_purple_chars} → {result.after_purple_chars})，"
                "存在新增中高风险内容"
            )

        # Check length within hard_range
        if result.length_delta_ratio > self.HARD_RANGE_HIGH:
            reasons.append(
                f"总字数增长 {result.length_delta_ratio:.0%}，超过硬上限 {self.HARD_RANGE_HIGH:.0%}"
            )
        elif result.length_delta_ratio < self.HARD_RANGE_LOW and result.length_delta_ratio > 0:
            reasons.append(
                f"总字数压缩至 {result.length_delta_ratio:.0%}，低于硬下限 {self.HARD_RANGE_LOW:.0%}"
            )

        # Determine verdict
        if not reasons:
            return "success", []

        # Check if it's a complete failure or needs second round
        has_critical = any(
            "风险字符" in r and "增加" in r
            or "红色字符增加" in r
            or "总字数增长" in r and "超过" in r
            for r in reasons
        )

        if has_critical:
            return "failed", reasons
        else:
            return "needs_second_round", reasons

    def format_report(self, result: RiskDeltaResult) -> str:
        """Format a human-readable report of the evaluation."""
        lines = []
        lines.append("## 风险变化评估报告")
        lines.append("")

        lines.append("### 字符统计")
        lines.append(f"| 指标 | 优化前 | 优化后 | 变化 |")
        lines.append(f"|------|--------|--------|------|")
        lines.append(f"| 总字符数 | {result.before_total_chars} | {result.after_total_chars} "
                     f"| {result.length_delta_ratio:.1%} |")
        lines.append(f"| 红色字符 | {result.before_red_chars} | {result.after_red_chars} "
                     f"| {result.after_red_chars - result.before_red_chars:+d} |")
        lines.append(f"| 橙色字符 | {result.before_orange_chars} | {result.after_orange_chars} "
                     f"| {result.after_orange_chars - result.before_orange_chars:+d} |")
        lines.append(f"| 紫色字符 | {result.before_purple_chars} | {result.after_purple_chars} "
                     f"| {result.after_purple_chars - result.before_purple_chars:+d} |")
        lines.append(f"| 风险字符合计 | {result.before_risk_chars} | {result.after_risk_chars} "
                     f"| {result.risk_char_delta:+d} |")

        lines.append("")
        lines.append("### AIGC 疑似率")
        if result.before_rate is not None and result.after_rate is not None:
            lines.append(f"- 优化前: {result.before_rate:.2f}%")
            lines.append(f"- 优化后: {result.after_rate:.2f}%")
            lines.append(f"- 下降: {result.rate_delta:.1f} 个百分点")

        lines.append("")
        lines.append("### 判定结果")

        if result.verdict == "success":
            lines.append("**本轮优化成功**")
            lines.append("- AIGC 疑似率显著下降")
            lines.append("- 风险字符绝对数量减少")
            lines.append("- 字数控制在合理范围内")
        elif result.verdict == "failed":
            lines.append("**本轮优化失败**")
            for reason in result.failure_reasons:
                lines.append(f"- {reason}")
            lines.append("")
            lines.append("**建议**: 不应将此版本作为最终优化结果。")
        else:
            lines.append("**需要二轮处理**")
            for reason in result.failure_reasons:
                lines.append(f"- {reason}")
            lines.append("")
            lines.append("**建议**: 运行 feedback-round 命令进行针对性二次优化。")

        return "\n".join(lines)
