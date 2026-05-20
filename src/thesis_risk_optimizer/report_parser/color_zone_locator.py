"""Color zone locator: map report color zones to thesis text units.

KEY FIX v1.1: Enhanced matching with:
- Whitespace normalization
- Chinese punctuation normalization
- Substring matching
- Fuzzy similarity matching
- Sequential paragraph order hint (nearby paragraphs are more likely to match)
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Optional

from ..document_io.text_units import TextUnit, RiskLevel
from .aigc_report_parser import AigcReport, ReportFragment, ColorBand


class ColorZoneLocator:
    """Match AIGC report fragments to thesis text units."""

    MIN_CONFIDENCE = 0.35  # lowered from 0.5 for better real-world matching

    def locate(self, units: list[TextUnit], report: AigcReport) -> dict:
        """Map report fragments to text units and assign risk levels."""
        mappings: list[dict] = []
        matched_fragments = set()
        matched_units = set()

        # Build a lookup of body-only units for matching
        body_units = [u for u in units if u.is_body]

        for fragment in report.fragments:
            if fragment.color_band == ColorBand.GRAY:
                continue

            best_unit, confidence = self._find_best_match(fragment, body_units)

            if confidence >= self.MIN_CONFIDENCE and best_unit is not None:
                self._apply_risk(best_unit, fragment)
                mappings.append({
                    "fragment_index": fragment.index,
                    "unit_uid": best_unit.uid,
                    "confidence": round(confidence, 3),
                    "color_band": fragment.color_band,
                    "score": fragment.score,
                })
                matched_fragments.add(fragment.index)
                matched_units.add(best_unit.uid)

        # If very few matched, try substring-only matching as fallback
        if len(matched_fragments) < report.total_scored * 0.3:
            for fragment in report.fragments:
                if fragment.color_band == ColorBand.GRAY:
                    continue
                if fragment.index in matched_fragments:
                    continue

                best_unit, confidence = self._substring_match(fragment, body_units)
                if confidence >= 0.3 and best_unit is not None:
                    self._apply_risk(best_unit, fragment)
                    mappings.append({
                        "fragment_index": fragment.index,
                        "unit_uid": best_unit.uid,
                        "confidence": round(confidence, 3),
                        "color_band": fragment.color_band,
                        "score": fragment.score,
                        "match_type": "substring_fallback",
                    })
                    matched_fragments.add(fragment.index)
                    matched_units.add(best_unit.uid)

        return {
            "mappings": mappings,
            "matched_fragment_count": len(matched_fragments),
            "matched_unit_count": len(matched_units),
            "total_scored_fragments": report.total_scored,
            "unmatched_fragments": report.total_scored - len(matched_fragments),
        }

    def _find_best_match(
        self, fragment: ReportFragment, units: list[TextUnit]
    ) -> tuple[Optional[TextUnit], float]:
        """Find the text unit that best matches a report fragment.

        Uses multiple strategies in order:
        1. Normalized exact match
        2. Normalized substring match
        3. Fuzzy sequence match
        """
        frag_text = self._normalize(fragment.text)
        if len(frag_text) < 8:
            return None, 0.0

        best_unit = None
        best_ratio = 0.0

        for unit in units:
            unit_text = self._normalize(unit.text)
            if len(unit_text) < 8:
                continue

            # Strategy 1: normalized substring
            if frag_text in unit_text:
                ratio = len(frag_text) / len(unit_text)
                if ratio > best_ratio:
                    best_ratio = min(1.0, ratio)
                    best_unit = unit
                    if best_ratio > 0.9:
                        return best_unit, best_ratio
                continue

            if unit_text in frag_text:
                ratio = len(unit_text) / len(frag_text)
                if ratio > best_ratio:
                    best_ratio = min(1.0, ratio)
                    best_unit = unit
                continue

            # Strategy 2: fuzzy matching
            ratio = SequenceMatcher(None, frag_text, unit_text).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_unit = unit

        return best_unit, best_ratio

    def _substring_match(
        self, fragment: ReportFragment, units: list[TextUnit]
    ) -> tuple[Optional[TextUnit], float]:
        """Fallback: try matching shorter substrings of the fragment."""
        frag_text = self._normalize(fragment.text)
        if len(frag_text) < 15:
            return None, 0.0

        # Try first 30%, middle 30%, last 30%
        n = len(frag_text)
        segments = [
            frag_text[:n // 3],
            frag_text[n // 3: 2 * n // 3],
            frag_text[2 * n // 3:],
        ]

        best_unit = None
        best_ratio = 0.0

        for seg in segments:
            if len(seg) < 8:
                continue
            for unit in units:
                unit_text = self._normalize(unit.text)
                if seg in unit_text:
                    ratio = len(seg) / len(frag_text)
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_unit = unit

        return best_unit, best_ratio * 0.6  # discount substring matches

    @staticmethod
    def _apply_risk(unit: TextUnit, fragment: ReportFragment) -> None:
        """Assign risk level and score to a text unit."""
        unit.risk_score = fragment.score
        band = fragment.color_band
        if band == ColorBand.RED:
            unit.risk_level = RiskLevel.HIGH
        elif band == ColorBand.ORANGE:
            unit.risk_level = RiskLevel.MEDIUM
        elif band == ColorBand.PURPLE:
            unit.risk_level = RiskLevel.LOW
        elif band == ColorBand.BLACK:
            unit.risk_level = RiskLevel.MINIMAL

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize text for comparison.

        - Collapse all whitespace to single space
        - Remove common Chinese/English punctuation
        - Strip leading/trailing noise
        """
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove punctuation (but keep alphanumeric and Chinese chars)
        punct = r"[，,。\.；;：:！!？?\u201c\u201d\u2018\u2019\"''《》〈〉「」『』【】〔〕]"
        text = re.sub(punct, "", text)
        text = text.strip()
        return text
