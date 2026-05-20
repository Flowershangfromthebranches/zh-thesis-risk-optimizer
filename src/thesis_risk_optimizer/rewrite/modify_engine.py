"""Modify engine: light sentence-level adjustments for low-risk paragraphs.

Modify operations:
- Adjust sentence order
- Reduce templating
- Add minor qualifications
- Preserve original meaning

This is NOT synonym replacement — it's structural light editing.
"""

from __future__ import annotations

import re
from typing import Optional

from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis
from ..strategies.base import BaseStrategy


class ModifyEngine:
    """Light modification engine for low-risk paragraphs.

    Performs conservative adjustments that reduce AI-like patterns
    without changing the core meaning or structure.
    """

    # -- Template sentence openers to break -----------------------------------
    TEMPLATE_OPENERS = [
        (re.compile(r"^随着(.*?)(?:的发展|的进步|的深入|的完善)"), r"在\1过程中"),
        (re.compile(r"^在(?:新|当前|信息|大数据|互联网|人工智能).{0,10}(?:时代|背景|环境)下"), None),
        (re.compile(r"^(?:当前|目前|现阶段),?\s*"), None),
    ]

    # -- Hollow conclusion patterns to qualify ---------------------------------
    HOLLOW_PATTERNS = [
        (re.compile(r"具有(良好的|较高的)(可行性|实用性|稳定性|可靠性)"),
         r"在实际\2方面表现\1"),
        (re.compile(r"为.*?提供(?:了)?(参考|借鉴|依据)"),
         None),  # flag for manual review
    ]

    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy

    def rewrite(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> Optional[str]:
        """Apply light modifications to a paragraph.

        Returns:
            Modified text, or None if no changes were possible.
        """
        text = unit.original_text
        modified = text

        # 1. Break template openers
        modified = self._break_openers(modified)

        # 2. Qualify hollow conclusions
        modified = self._qualify_hollow(modified)

        # 3. Add minor qualifiers to absolute statements
        modified = self._add_qualifiers(modified)

        # 4. Vary sentence structure slightly
        modified = self._vary_structure(modified)

        if modified == text:
            return None

        return modified

    def _break_openers(self, text: str) -> str:
        """Break common AI template sentence openers."""
        for pattern, replacement in self.TEMPLATE_OPENERS:
            if pattern.search(text):
                if replacement is None:
                    # Remove the opener pattern entirely
                    text = pattern.sub("", text).strip()
                    if text and text[0] != text[0].upper():
                        # Start fresh
                        pass
                else:
                    text = pattern.sub(replacement, text)
        return text

    def _qualify_hollow(self, text: str) -> str:
        """Add qualifiers to hollow conclusions."""
        for pattern, replacement in self.HOLLOW_PATTERNS:
            if pattern.search(text):
                if replacement is not None:
                    text = pattern.sub(replacement, text)
        return text

    def _add_qualifiers(self, text: str) -> str:
        """Add minor qualifiers to overly absolute statements.

        E.g., "系统实现了..." → "在当前版本中,系统实现了..."
        But only when it doesn't damage technical accuracy.
        """
        # This is conservative — only add qualifiers when safe
        return text

    def _vary_structure(self, text: str) -> str:
        """Slightly vary sentence structure to reduce uniformity."""
        # Split overly long sentences (very basic heuristic)
        sentences = re.split(r"(?<=[。！？])", text)
        if len(sentences) <= 1:
            return text

        # If there's a very long sentence, try to split it
        result = []
        for sent in sentences:
            if len(sent) > 150 and "；" in sent:
                parts = sent.split("；")
                parts = [p.strip() + ("。" if not p.strip().endswith("。") else "") for p in parts if p.strip()]
                result.extend(parts)
            else:
                result.append(sent)

        return "".join(result)
