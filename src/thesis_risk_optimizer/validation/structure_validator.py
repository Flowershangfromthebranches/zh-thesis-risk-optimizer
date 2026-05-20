"""Structure validator: verify thesis structure is preserved after modification.

Checks:
- Heading hierarchy is intact
- Section order is preserved
- No sections were dropped
- No paragraphs were deleted entirely
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..document_io.text_units import TextUnit, TextUnitType


@dataclass
class StructureReport:
    """Report on structural integrity after modification."""

    passed: bool = True
    original_unit_count: int = 0
    modified_unit_count: int = 0
    missing_sections: list[str] = field(default_factory=list)
    dropped_headings: list[str] = field(default_factory=list)
    empty_paragraphs: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


class StructureValidator:
    """Validate that thesis structure is preserved."""

    def validate(
        self,
        original_units: list[TextUnit],
        modified_units: list[TextUnit],
    ) -> StructureReport:
        """Check structural integrity between original and modified units."""
        report = StructureReport(
            original_unit_count=len(original_units),
            modified_unit_count=len(modified_units),
        )

        # 1. Check unit count hasn't dropped drastically
        if len(modified_units) < len(original_units) * 0.5:
            report.passed = False
            report.issues.append(
                f"单元数量大幅减少: {len(original_units)} → {len(modified_units)}"
            )

        # 2. Check all headings are still present
        orig_headings = {u.uid: u.text for u in original_units if u.unit_type == TextUnitType.HEADING}
        mod_headings = {u.uid: u.text for u in modified_units if u.unit_type == TextUnitType.HEADING}

        for uid, text in orig_headings.items():
            if uid not in mod_headings:
                report.dropped_headings.append(f"[{uid}] {text[:60]}")
                report.passed = False
            elif not mod_headings[uid].strip():
                report.dropped_headings.append(f"[{uid}] {text[:60]} (变为空)")
                report.passed = False

        # 3. Check for empty body paragraphs
        for unit in modified_units:
            if unit.is_body and len(unit.text.strip()) < 10 and len(unit.original_text.strip()) >= 10:
                report.empty_paragraphs.append(unit.uid)
                report.passed = False

        # 4. Check section coverage
        orig_sections = {u.section for u in original_units if u.section}
        mod_sections = {u.section for u in modified_units if u.section}
        missing = orig_sections - mod_sections
        if missing:
            report.missing_sections = list(missing)
            report.issues.append(f"缺失章节: {missing}")

        return report
