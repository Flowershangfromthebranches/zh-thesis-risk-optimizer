"""IntakeGate: validates that all required information is present before optimization.

Step 1 of the 7-step workflow.
If any required field is missing, returns a structured result indicating what's needed.
Optimization MUST NOT proceed when IntakeResult.complete is False.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .required_fields import REQUIRED_FIELDS, format_missing_fields_prompt


@dataclass
class IntakeResult:
    """Result of intake validation."""

    complete: bool = False
    missing_fields: list[str] = field(default_factory=list)
    missing_prompt: str = ""

    # Parsed values (populated when complete)
    major: str = ""
    title: str = ""
    current_rate: Optional[float] = None
    target_rate: Optional[float] = None
    has_report: bool = False
    allow_rewrite: bool = False
    allow_supplement: bool = False
    has_materials: bool = False


class IntakeGate:
    """Validates required intake fields before optimization.

    Usage:
        gate = IntakeGate()
        result = gate.check(
            major="人力资源管理",
            title="某公司招聘管理优化研究",
            current_rate=76.67,
            target_rate=30.0,
            has_report=True,
            allow_rewrite=True,
            allow_supplement=True,
            has_materials=True,
        )
        if not result.complete:
            print(result.missing_prompt)
            return  # DO NOT proceed
    """

    def check(
        self,
        major: Optional[str] = None,
        title: Optional[str] = None,
        current_rate: Optional[float] = None,
        target_rate: Optional[float] = None,
        has_report: Optional[bool] = None,
        allow_rewrite: Optional[bool] = None,
        allow_supplement: Optional[bool] = None,
        has_materials: Optional[bool] = None,
    ) -> IntakeResult:
        """Check if all required fields are provided.

        Args:
            major: User-declared thesis discipline.
            title: Thesis title.
            current_rate: Current AIGC suspicion rate (%).
            target_rate: Target AIGC suspicion rate (%).
            has_report: Whether AIGC color report is available.
            allow_rewrite: Whether rewriting is allowed.
            allow_supplement: Whether content supplementation is allowed.
            has_materials: Whether thesis-writing materials are available.

        Returns:
            IntakeResult indicating completeness and any missing fields.
        """
        result = IntakeResult()
        values = {
            "major": major,
            "title": title,
            "current_rate": current_rate,
            "target_rate": target_rate,
            "has_report": has_report,
            "allow_rewrite": allow_rewrite,
            "allow_supplement": allow_supplement,
            "has_materials": has_materials,
        }

        missing = []
        for f in REQUIRED_FIELDS:
            val = values.get(f.name)
            if val is None or (isinstance(val, str) and not val.strip()):
                missing.append(f.name)

        if missing:
            result.complete = False
            result.missing_fields = missing
            result.missing_prompt = format_missing_fields_prompt(missing)
        else:
            result.complete = True
            result.major = major.strip()
            result.title = title.strip()
            result.current_rate = current_rate
            result.target_rate = target_rate
            result.has_report = has_report
            result.allow_rewrite = allow_rewrite
            result.allow_supplement = allow_supplement
            result.has_materials = has_materials

        return result
