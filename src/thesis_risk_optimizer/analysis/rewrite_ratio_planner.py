"""Rewrite ratio planner: decide the proportion of modify / rewrite / rebuild.

Based on AIGC risk level (from report or estimation), plans how many
text units should be modified, rewritten, or rebuilt.

KEY FIX v1.1: UNKNOWN risk paragraphs are NOT frozen. They are diagnosed
via ParagraphDiagnoser, scored, and allocated actions based on the ratio plan.
Only truly protected units (cover, declaration, TOC, references, formulas) are frozen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..document_io.text_units import TextUnit, RiskLevel, ActionType
from .paragraph_diagnoser import ParagraphDiagnoser, ParagraphDiagnosis, DiagnosisTag


# Section priority: higher number = process first
SECTION_PRIORITY = {
    "implementation": 10,
    "testing": 9,
    "design": 8,
    "requirements": 7,
    "abstract": 6,
    "conclusion": 6,
    "introduction": 5,
    "tech_background": 5,
    "literature_review": 4,
    "acknowledgement": 0,
    "references": 0,
    "appendix": 0,
}


@dataclass
class RatioPlan:
    """Planned distribution of rewrite actions."""

    aigc_rate: Optional[float] = None
    total_body_units: int = 0
    planned_modify: int = 0
    planned_rewrite: int = 0
    planned_rebuild: int = 0
    assigned_modify: int = 0
    assigned_rewrite: int = 0
    assigned_rebuild: int = 0
    assigned_freeze: int = 0
    frozen_protected: int = 0
    frozen_no_diagnosis: int = 0

    # Detailed tracking
    freeze_reasons: list[dict] = field(default_factory=list)
    action_samples: dict[str, list[dict]] = field(default_factory=dict)

    @property
    def total_assigned(self) -> int:
        return self.assigned_modify + self.assigned_rewrite + self.assigned_rebuild

    def to_dict(self) -> dict:
        return {
            "aigc_rate": self.aigc_rate,
            "total_body_units": self.total_body_units,
            "planned": {
                "modify": self.planned_modify,
                "rewrite": self.planned_rewrite,
                "rebuild": self.planned_rebuild,
            },
            "assigned": {
                "modify": self.assigned_modify,
                "rewrite": self.assigned_rewrite,
                "rebuild": self.assigned_rebuild,
                "freeze": self.assigned_freeze,
            },
            "frozen_breakdown": {
                "protected": self.frozen_protected,
                "no_diagnosis": self.frozen_no_diagnosis,
            },
        }


class RewriteRatioPlanner:
    """Plan the rewrite ratio based on AIGC risk level.

    Rules (from the specification):

    AIGC < 30%:
      - modify 80%, rewrite 20%, no rebuild

    30% <= AIGC < 50%:
      - modify 50%, rewrite 40%, rebuild 10%

    50% <= AIGC < 70%:
      - modify 25%, rewrite 55%, rebuild 20%

    AIGC >= 70%:
      - modify 10%, rewrite 50%, rebuild 40%

    CRITICAL: UNKNOWN risk paragraphs are NOT frozen.
    Only protected units (cover, declaration, TOC, references, formulas) are frozen.
    """

    RATIO_TABLE = {
        (0, 30):     (0.80, 0.20, 0.00),
        (30, 50):    (0.50, 0.40, 0.10),
        (50, 70):    (0.25, 0.55, 0.20),
        (70, 100):   (0.10, 0.50, 0.40),
    }

    def __init__(self):
        self.diagnoser = ParagraphDiagnoser()

    def plan(
        self,
        units: list[TextUnit],
        aigc_rate: Optional[float] = None,
        estimated_rate: Optional[float] = None,
    ) -> RatioPlan:
        """Plan rewrite ratios for body text units."""
        body_units = [u for u in units if u.is_body]
        total = len(body_units)

        if total == 0:
            return RatioPlan(total_body_units=0)

        effective_rate = aigc_rate or estimated_rate

        if effective_rate is not None:
            ratios = self._get_ratios(effective_rate)
        else:
            ratios = self._plan_from_risk_levels(body_units)

        return RatioPlan(
            aigc_rate=effective_rate,
            total_body_units=total,
            planned_modify=round(total * ratios[0]),
            planned_rewrite=round(total * ratios[1]),
            planned_rebuild=round(total * ratios[2]),
        )

    def apply_to_units(
        self, units: list[TextUnit], plan: RatioPlan
    ) -> list[TextUnit]:
        """Assign ActionType to units based on the ratio plan.

        CRITICAL FIX: UNKNOWN risk units are DIAGNOSED and SCORED,
        then sorted and allocated actions. Only truly protected units freeze.
        """
        # Separate protected and processable body units
        body_units = [u for u in units if u.is_body and not u.is_protected]
        protected_body = [u for u in units if u.is_body and u.is_protected]

        # Freeze protected units
        for u in protected_body:
            u.action = ActionType.FREEZE
            u.metadata["freeze_reason"] = f"受保护类型: {u.unit_type.value}"
        plan.frozen_protected = len(protected_body)

        # DIAGNOSE all body units — compute a numeric risk score (0-100)
        scored_units: list[tuple[TextUnit, float, ParagraphDiagnosis]] = []
        for unit in body_units:
            diagnosis = self.diagnoser.diagnose(unit)
            score = self._compute_risk_score(unit, diagnosis)
            unit.metadata["diagnostic_score"] = score
            unit.metadata["diagnosis_tags"] = [t.value for t in diagnosis.tags]
            unit.metadata["diagnosis_reasoning"] = diagnosis.reasoning
            scored_units.append((unit, score, diagnosis))

        # Sort by score descending (highest risk first)
        # Report-mapped (HIGH/MEDIUM risk) units get priority boost
        scored_units.sort(key=lambda x: (
            -(x[1] + (30 if x[0].risk_level == RiskLevel.HIGH else
                      20 if x[0].risk_level == RiskLevel.MEDIUM else
                      10 if x[0].risk_level == RiskLevel.LOW else 0)),
            -SECTION_PRIORITY.get(x[0].section, 0),
        ))

        # -- FORCE FILL quotas by score order (v1.2) --
        # When aigc_rate is provided, the RATIO PLAN IS MANDATORY.
        # desired_action is only a hint; quotas take absolute priority.
        rebuild_quota = plan.planned_rebuild
        rewrite_quota = plan.planned_rewrite
        modify_quota = plan.planned_modify

        # Pass 1: Fill rebuild quota with highest-scoring units
        for unit, score, diagnosis in scored_units:
            if rebuild_quota <= 0:
                break
            unit.action = ActionType.REBUILD
            unit.metadata["allocation"] = "quota:rebuild"
            rebuild_quota -= 1

        # Pass 2: Fill rewrite quota with next-highest (not yet assigned)
        for unit, score, diagnosis in scored_units:
            if rewrite_quota <= 0:
                break
            if unit.action != ActionType.FREEZE:
                continue  # already got rebuild
            unit.action = ActionType.REWRITE
            unit.metadata["allocation"] = "quota:rewrite"
            rewrite_quota -= 1

        # Pass 3: Fill modify quota
        for unit, score, diagnosis in scored_units:
            if modify_quota <= 0:
                break
            if unit.action != ActionType.FREEZE:
                continue
            unit.action = ActionType.MODIFY
            unit.metadata["allocation"] = "quota:modify"
            modify_quota -= 1

        # Remaining: freeze with reason
        for unit, score, diagnosis in scored_units:
            if unit.action != ActionType.FREEZE:
                continue
            unit.metadata["freeze_reason"] = (
                f"配额已用完 (score={score:.0f}), 风险分数相对较低"
            )

        # Track assigned counts and samples
        plan.assigned_modify = sum(1 for u in body_units if u.action == ActionType.MODIFY)
        plan.assigned_rewrite = sum(1 for u in body_units if u.action == ActionType.REWRITE)
        plan.assigned_rebuild = sum(1 for u in body_units if u.action == ActionType.REBUILD)
        plan.assigned_freeze = sum(1 for u in body_units if u.action == ActionType.FREEZE)
        plan.frozen_no_diagnosis = plan.assigned_freeze

        # Collect samples
        for action_name, action_type in [
            ("rebuild", ActionType.REBUILD),
            ("rewrite", ActionType.REWRITE),
            ("modify", ActionType.MODIFY),
            ("freeze", ActionType.FREEZE),
        ]:
            samples = []
            for u in body_units:
                if u.action == action_type:
                    samples.append({
                        "uid": u.uid,
                        "section": u.section,
                        "score": u.metadata.get("diagnostic_score", 0),
                        "tags": u.metadata.get("diagnosis_tags", []),
                        "reason": u.metadata.get("freeze_reason", u.metadata.get("diagnosis_reasoning", "")),
                        "preview": u.text[:80].replace("\n", " "),
                    })
                if len(samples) >= 5:
                    break
            plan.action_samples[action_name] = samples

        # Collect all freeze reasons
        for u in body_units:
            if u.action == ActionType.FREEZE:
                plan.freeze_reasons.append({
                    "uid": u.uid,
                    "section": u.section,
                    "score": u.metadata.get("diagnostic_score", 0),
                    "reason": u.metadata.get("freeze_reason", "未知"),
                })

        return units

    # -- Risk scoring ---------------------------------------------------------

    def _compute_risk_score(
        self, unit: TextUnit, diagnosis: ParagraphDiagnosis
    ) -> float:
        """Compute a numeric risk score (0-100) for the unit.

        Based on:
        - Diagnosis tags (template = +30, hollow = +25, etc.)
        - Section priority
        - Text length (very short = low risk to process)
        - Whether report assigned a risk_score
        """
        score = 0.0

        # Tag-based scoring
        tag_weights = {
            DiagnosisTag.TEMPLATE_SKELETON: 30,
            DiagnosisTag.HOLLOW_CONCLUSION: 25,
            DiagnosisTag.GRAND_NARRATIVE: 20,
            DiagnosisTag.PSEUDO_ANALYSIS: 18,
            DiagnosisTag.ENCYCLOPEDIA_STYLE: 15,
            DiagnosisTag.MISSING_DETAIL: 15,
            DiagnosisTag.FLOWCHART_PROSE: 12,
            DiagnosisTag.POLICY_SPEAK: 12,
            DiagnosisTag.ABSTRACT_ONLY: 12,
            DiagnosisTag.VAGUE_ACTION: 10,
            DiagnosisTag.UNIFORM_SENTENCE: 8,
            DiagnosisTag.OVERLY_SMOOTH: 8,
            DiagnosisTag.NO_LIMITATIONS: 5,
        }
        for tag in diagnosis.tags:
            score += tag_weights.get(tag, 5)

        # Section bonus: high-priority sections get a boost
        section_bonus = SECTION_PRIORITY.get(unit.section, 0) * 2
        score += section_bonus

        # If the unit already has a report-based risk_level, factor that in
        if unit.risk_level == RiskLevel.HIGH:
            score = max(score, 70)
        elif unit.risk_level == RiskLevel.MEDIUM:
            score = max(score, 50)
        elif unit.risk_level == RiskLevel.LOW:
            score = max(score, 30)

        # Very short text (< 20 chars) is hard to meaningfully rewrite
        if len(unit.text) < 20:
            score *= 0.5

        return min(100, max(0, score))

    def _desired_action(
        self, score: float, diagnosis: ParagraphDiagnosis
    ) -> ActionType:
        """Determine the desired action based on risk score."""
        if score >= 60:
            return ActionType.REBUILD
        elif score >= 40:
            return ActionType.REWRITE
        elif score >= 15:
            return ActionType.MODIFY
        else:
            return ActionType.FREEZE

    # -- Ratio helpers --------------------------------------------------------

    def _get_ratios(self, rate: float) -> tuple[float, float, float]:
        for (lo, hi), ratios in self.RATIO_TABLE.items():
            if lo <= rate < hi:
                return ratios
        return self.RATIO_TABLE[(70, 100)]

    def _plan_from_risk_levels(self, units: list[TextUnit]) -> tuple[float, float, float]:
        body_units = [u for u in units if u.is_body]
        total = len(body_units)
        if total == 0:
            return (0.8, 0.2, 0.0)

        high = sum(1 for u in body_units if u.risk_level == RiskLevel.HIGH)
        medium = sum(1 for u in body_units if u.risk_level == RiskLevel.MEDIUM)

        if high / total > 0.3:
            return (0.10, 0.50, 0.40)
        elif (high + medium) / total > 0.3:
            return (0.25, 0.55, 0.20)
        else:
            return (0.50, 0.40, 0.10)
