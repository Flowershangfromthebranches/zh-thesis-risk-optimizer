"""Strategy contract: defines the protocol that every discipline strategy must fulfill.

Each StrategyContract ensures:
- Discipline isolation: strategies do not share rewrite templates
- Evidence isolation: each discipline has its own evidence schema
- Validation: each discipline has its own risk patterns and rules
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StrategyContract:
    """Contract defining a discipline-specific rewrite strategy.

    Every BaseStrategy subclass must expose a contract property that returns
    an instance of this dataclass.
    """

    # -- Identity ---------------------------------------------------------------
    discipline_name: str
    applicable_keywords: list[str] = field(default_factory=list)

    # -- Risk patterns ----------------------------------------------------------
    high_risk_patterns: list[str] = field(default_factory=list)
    """Discipline-specific high-risk phrases that must be rewritten."""

    # -- Evidence ---------------------------------------------------------------
    evidence_schema: dict[str, list[str]] = field(default_factory=dict)
    """Mapping: evidence_category -> list of accepted evidence types."""

    # -- Rewrite behavior -------------------------------------------------------
    rewrite_principles: list[str] = field(default_factory=list)
    """Core principles guiding how text should be rewritten for this discipline."""

    forbidden_patterns: list[str] = field(default_factory=list)
    """Patterns / content that must NEVER appear in rewritten text."""

    paragraph_transforms: str = ""
    """Sentence-level transform template applied to high-risk paragraphs."""

    # -- Validation -------------------------------------------------------------
    validation_rules: list[str] = field(default_factory=list)
    """Rules for validating that rewritten text is discipline-appropriate."""

    # -- Fallback ---------------------------------------------------------------
    fallback_behavior: str = ""
    """Behavior when no evidence is available: 'conservative_rewrite' or 'freeze'."""
