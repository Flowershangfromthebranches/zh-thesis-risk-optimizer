"""Format preserver: rules for what to protect and how to preserve DOCX formatting.

This module defines the protection rules and formatting preservation policies,
not the mechanics (which are in docx_reader.py and docx_writer.py).
"""

from __future__ import annotations

from .text_units import TextUnit, TextUnitType


# -- Unit types that are NEVER modified ---------------------------------------
FROZEN_UNIT_TYPES: set[TextUnitType] = {
    TextUnitType.COVER,
    TextUnitType.DECLARATION,
    TextUnitType.TOC,
    TextUnitType.REFERENCE,
    TextUnitType.FORMULA,
}

# -- Unit types that are protected by default but may be modified -------------
#    if user explicitly allows it.
PROTECTED_BY_DEFAULT: set[TextUnitType] = {
    TextUnitType.APPENDIX,
    TextUnitType.FOOTNOTE,
    TextUnitType.ENDNOTE,
    TextUnitType.HEADER,
    TextUnitType.FOOTER,
}

# -- Formatting attributes to preserve ----------------------------------------
PRESERVED_FORMAT_ATTRS = [
    "bold",
    "italic",
    "font_name",
    "font_size",
    "alignment",
    "outline_level",
    "first_line_indent",
    "style_name",
]


def should_freeze(unit: TextUnit) -> bool:
    """Check if a text unit should be frozen (never modified).

    Frozen units include: cover, declaration, TOC, references, formulas.
    Also freezes section-marker headings (abstract, declaration, etc.).
    English abstract body is NOT frozen (can be rewritten).
    """
    if unit.unit_type in FROZEN_UNIT_TYPES:
        return True
    # Freeze section-marker headings that should not be modified
    if unit.unit_type == TextUnitType.HEADING:
        if unit.section in ("abstract", "declaration", "acknowledgement"):
            return True
    # Freeze English keywords (Keywords: ... at end of abstract)
    if unit.section == "abstract" and unit.text.strip().startswith("Keywords"):
        return True
    # English abstract body is NOT frozen - it can be rewritten
    return False


def should_protect(unit: TextUnit) -> bool:
    """Check if a text unit should be protected by default."""
    return unit.unit_type in FROZEN_UNIT_TYPES or unit.unit_type in PROTECTED_BY_DEFAULT


def classify_no_edit_zones(units: list[TextUnit]) -> dict[str, list[str]]:
    """Classify all units into editable and non-editable zones.

    Returns:
        Dict with 'frozen', 'protected', 'editable' keys listing unit UIDs.
    """
    result = {"frozen": [], "protected": [], "editable": []}
    for unit in units:
        if unit.unit_type in FROZEN_UNIT_TYPES:
            result["frozen"].append(unit.uid)
        elif unit.unit_type in PROTECTED_BY_DEFAULT:
            result["protected"].append(unit.uid)
        else:
            result["editable"].append(unit.uid)
    return result


# -- Identity info patterns to skip -------------------------------------------
IDENTITY_PATTERNS = [
    "学号", "学号", "姓名", "导师", "学院", "专业", "班级",
    "Student ID", "Name", "Supervisor", "School", "Major",
]
