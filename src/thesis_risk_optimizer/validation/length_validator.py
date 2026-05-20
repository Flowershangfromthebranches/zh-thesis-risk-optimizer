"""Length validator: enforce bidirectional character count constraints.

Rules (v2.0 — bidirectional):
1. Modified output may be shorter than original (down to 85% hard floor).
2. ideal_range: 95%-110% of original length.
3. acceptable_range: 90%-115%.
4. hard_range: 85%-120%.
5. Below 85% or above 120% → FAILURE.
6. Per-paragraph: ideal 80%-140%, acceptable 70%-160%, hard 60%-180%.
7. User-specified --min-length / --max-length override ratio-based bounds.
8. Section-specific rules for abstract, conclusion, technical sections.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..document_io.text_units import TextUnit, ActionType
from ..rewrite.evidence_policy import (
    LengthPolicy, LengthRanges, TOTAL_RANGES, PARAGRAPH_RANGES,
    _classify_length, _detect_length_reasons,
)


@dataclass
class LengthReport:
    """Report on length compliance (bidirectional)."""

    passed: bool = True
    original_total_chars: int = 0
    modified_total_chars: int = 0
    delta: int = 0
    delta_pct: float = 0.0
    band: str = ""  # ideal / acceptable / hard / out_of_range
    compressed_paragraphs: list[str] = field(default_factory=list)
    excessive_expansion: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)  # why length changed
    in_ideal_range: bool = False
    in_acceptable_range: bool = False
    triggered_hard_range: bool = False


class LengthValidator:
    """Validate character count constraints after modification (bidirectional)."""

    def validate(
        self,
        units: list[TextUnit],
        min_length: int | None = None,
        max_length: int | None = None,
        target_range: tuple[float, float] | None = None,
    ) -> LengthReport:
        """Check length compliance across all modified units.

        Args:
            units: Text units with both original and modified text.
            min_length: User-specified minimum total chars (e.g. school requirement).
            max_length: User-specified maximum total chars.
            target_range: User-specified (low, high) ratio range override.

        Returns:
            LengthReport with pass/fail and details.
        """
        report = LengthReport()
        ranges = TOTAL_RANGES.clamp_to_hard(min_length, max_length, target_range)

        body_units = [u for u in units if u.is_body and u.action != ActionType.FREEZE]

        # Collect per-paragraph details for reason analysis
        all_orig_text = ""
        all_new_text = ""

        for unit in body_units:
            orig_len = len(unit.original_text)
            new_len = len(unit.text)
            report.original_total_chars += orig_len
            report.modified_total_chars += new_len

            all_orig_text += unit.original_text
            all_new_text += unit.text

            ratio = new_len / max(1, orig_len)

            # Per-paragraph check
            para_result = LengthPolicy.check_paragraph(orig_len, new_len, section=unit.section)

            # Track compressed paragraphs (below 90% of original)
            if ratio < 0.90 and unit.action != ActionType.FREEZE:
                report.compressed_paragraphs.append(
                    f"[{unit.uid}] {orig_len}→{new_len} chars ({ratio:.0%})"
                )

            # Track excessive expansion (above 140%)
            if ratio > 1.40:
                report.excessive_expansion.append(
                    f"[{unit.uid}] {orig_len}→{new_len} chars ({ratio:.0%})"
                )

            # Per-paragraph failure
            if not para_result["passed"]:
                report.issues.append(para_result["message"])

        # Overall totals
        report.delta = report.modified_total_chars - report.original_total_chars
        if report.original_total_chars > 0:
            report.delta_pct = report.delta / report.original_total_chars

        # Total document check using LengthPolicy
        total_result = LengthPolicy.check_total(
            report.original_total_chars, report.modified_total_chars,
            ranges=ranges, min_length=min_length, max_length=max_length,
        )
        report.band = total_result["band"]
        report.in_ideal_range = total_result["band"] == "ideal"
        report.in_acceptable_range = total_result["band"] in ("ideal", "acceptable")
        report.triggered_hard_range = total_result["band"] == "hard"

        if not total_result["passed"]:
            report.passed = False
            report.issues.append(total_result["message"])
        elif total_result["level"] == "WARNING":
            report.issues.append(total_result["message"])

        # Detect reasons for length change
        report.reasons = _detect_length_reasons(all_orig_text, all_new_text)

        # Failure condition: >10% decrease without reasons
        if report.delta_pct < -0.10 and not report.reasons:
            report.issues.append(
                f"字数下降超过 10% ({report.delta_pct:.1%})，但未检测到删减原因，建议人工复查。"
            )

        return report
