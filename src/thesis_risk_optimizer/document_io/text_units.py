"""Text unit model — the fundamental data type for all processing.

Every piece of the thesis is represented as a TextUnit with a type,
so that different unit types can be handled differently during rewrite.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TextUnitType(str, Enum):
    """Types of text units in a thesis document."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    TABLE_CELL = "table_cell"
    CAPTION = "caption"          # figure/table captions
    ABSTRACT = "abstract"
    CONCLUSION = "conclusion"
    REFERENCE = "reference"      # bibliography entries
    APPENDIX = "appendix"
    HEADER = "header"            # page header
    FOOTER = "footer"            # page footer
    FOOTNOTE = "footnote"
    ENDNOTE = "endnote"
    COVER = "cover"              # cover page text
    DECLARATION = "declaration"  # 原创性声明
    TOC = "toc"                  # table of contents
    FORMULA = "formula"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Risk level for a text unit."""

    HIGH = "high"        # >= 70% AIGC
    MEDIUM = "medium"    # 50-70%
    LOW = "low"          # 30-50%
    MINIMAL = "minimal"  # < 30%
    UNKNOWN = "unknown"


class ActionType(str, Enum):
    """What to do with a text unit."""

    MODIFY = "modify"      # light sentence-level adjustments
    REWRITE = "rewrite"    # keep topic, change argument structure
    REBUILD = "rebuild"    # full reconstruction from topic
    FREEZE = "freeze"      # do not modify
    SKIP = "skip"          # skip entirely


@dataclass
class TextUnit:
    """A single text unit in the thesis.

    Attributes:
        uid: Unique identifier within the document.
        unit_type: Type of text unit.
        text: The actual text content.
        section: Which section/chapter this belongs to.
        risk_level: Assessed AIGC risk level.
        risk_score: Numeric risk score (0-100), if available from report.
        action: Planned action for this unit.
        original_text: Original text before modification (for diff).
        metadata: Arbitrary extra data (style info, formatting, etc.).
    """

    uid: str
    unit_type: TextUnitType
    text: str
    section: str = ""
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    risk_score: Optional[float] = None
    action: ActionType = ActionType.FREEZE
    original_text: str = ""
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.original_text:
            self.original_text = self.text

    @property
    def char_count(self) -> int:
        """Chinese character count (approximate)."""
        return len(self.text)

    @property
    def is_protected(self) -> bool:
        """Whether this unit is protected from modification."""
        return self.unit_type in {
            TextUnitType.COVER,
            TextUnitType.DECLARATION,
            TextUnitType.TOC,
            TextUnitType.REFERENCE,
            TextUnitType.FORMULA,
        }

    @property
    def is_body(self) -> bool:
        """Whether this is body text that can be processed."""
        return self.unit_type in {
            TextUnitType.PARAGRAPH,
            TextUnitType.HEADING,
            TextUnitType.ABSTRACT,
            TextUnitType.CONCLUSION,
        }

    def mark_modified(self, new_text: str):
        """Record a modification to this unit."""
        self.text = new_text

    def diff_summary(self) -> str:
        """Return a summary of changes made."""
        if self.text == self.original_text:
            return f"[{self.uid}] unchanged"
        added = len(self.text) - len(self.original_text)
        delta = f"+{added}" if added >= 0 else str(added)
        return f"[{self.uid}] {self.action.value}: {delta} chars"

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "unit_type": self.unit_type.value,
            "section": self.section,
            "risk_level": self.risk_level.value,
            "risk_score": self.risk_score,
            "action": self.action.value,
            "char_count": self.char_count,
            "text_preview": self.text[:120] + "..." if len(self.text) > 120 else self.text,
        }
