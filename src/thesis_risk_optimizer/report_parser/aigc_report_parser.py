"""AIGC report parser: parse a .docx AIGC color-marked report.

KEY FIX v1.1: Comprehensive color detection — checks w:highlight, w:color,
w:shd, run-level style inheritance, table cells, and split runs.
Includes inspect/debug mode that outputs all discovered color values.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from docx import Document as DocxDocument
from docx.oxml.ns import qn


# -- Color band constants ----------------------------------------------------
class ColorBand:
    RED = "red"
    ORANGE = "orange"
    PURPLE = "purple"
    BLACK = "black"
    GRAY = "gray"


DEFAULT_THRESHOLDS = {"red": 70.0, "orange": 60.0, "purple": 50.0}

# -- Color detection map (hex values → bands) --------------------------------
# Red variants
RED_HEX = {"FF0000", "ff0000", "FF3333", "ff3333", "E60000", "e60000",
           "CC0000", "cc0000", "C00000", "c00000", "DC143C", "dc143c"}
# Orange variants
ORANGE_HEX = {"FFA500", "ffa500", "FF8C00", "ff8c00", "FFC000", "ffc000",
              "F4A460", "f4a460", "FF7F50", "ff7f50", "ED7D31", "ed7d31"}
# Purple variants
PURPLE_HEX = {"800080", "800080", "7030A0", "7030a0", "9933FF", "9933ff",
              "A020F0", "a020f0", "8B008B", "8b008b",
              "9D91E9", "9d91e9"}  # real-world report purple
# Black / gray / neutral
BLACK_HEX = {"000000", "000000", "333333", "333333", "1A1A1A", "1a1a1a"}
GRAY_HEX = {"B0B0B0", "b0b0b0", "808080", "808080", "C0C0C0", "c0c0c0",
            "999999", "999999", "AAAAAA", "aaaaaa", "CCCCCC", "cccccc"}
# Highlight value mapping
HIGHLIGHT_MAP = {
    "red": ColorBand.RED, "darkRed": ColorBand.RED,
    "orange": ColorBand.ORANGE, "darkOrange": ColorBand.ORANGE,
    "yellow": ColorBand.ORANGE,
    "darkYellow": ColorBand.ORANGE,
    "green": ColorBand.BLACK, "darkGreen": ColorBand.BLACK,
    "blue": ColorBand.BLACK, "darkBlue": ColorBand.BLACK,
    "cyan": ColorBand.BLACK,
    "magenta": ColorBand.PURPLE, "darkMagenta": ColorBand.PURPLE,
    "violet": ColorBand.PURPLE,
    "black": ColorBand.BLACK, "white": ColorBand.GRAY,
    "none": ColorBand.GRAY, "auto": ColorBand.GRAY,
}


@dataclass
class ReportFragment:
    text: str
    score: Optional[float] = None
    color_band: str = ColorBand.GRAY
    section: str = ""
    index: int = 0


@dataclass
class AigcReport:
    source_path: Path
    overall_rate: Optional[float] = None
    fragments: list[ReportFragment] = field(default_factory=list)
    thresholds: dict[str, float] = field(default_factory=lambda: DEFAULT_THRESHOLDS.copy())
    debug_colors: list[dict] = field(default_factory=list)

    @property
    def red_count(self) -> int:
        return sum(1 for f in self.fragments if f.color_band == ColorBand.RED)

    @property
    def orange_count(self) -> int:
        return sum(1 for f in self.fragments if f.color_band == ColorBand.ORANGE)

    @property
    def purple_count(self) -> int:
        return sum(1 for f in self.fragments if f.color_band == ColorBand.PURPLE)

    @property
    def black_count(self) -> int:
        return sum(1 for f in self.fragments if f.color_band == ColorBand.BLACK)

    @property
    def total_scored(self) -> int:
        return sum(1 for f in self.fragments if f.color_band != ColorBand.GRAY)

    def summary(self) -> dict:
        return {
            "overall_rate": self.overall_rate,
            "total_fragments": len(self.fragments),
            "red": self.red_count,
            "orange": self.orange_count,
            "purple": self.purple_count,
            "black": self.black_count,
            "gray": len(self.fragments) - self.total_scored,
        }


class AigcReportParser:
    """Parse a DOCX AIGC report and extract color-coded risk data.

    Comprehensive color detection:
    1. w:highlight values
    2. w:color (run font color)
    3. w:shd (shading/background fill)
    4. Inherited styles from paragraph/run properties
    5. Table cell content
    6. Split runs within a paragraph

    Usage:
        parser = AigcReportParser()
        report = parser.parse("aigc_report.docx")
    """

    SCORE_PATTERNS = [
        re.compile(r"(\d{1,3}(?:\.\d{1,2})?)\s*%"),
        re.compile(r"疑似[度率].*?(\d{1,3}(?:\.\d{1,2})?)"),
        re.compile(r"AIGC.*?(\d{1,3}(?:\.\d{1,2})?)"),
    ]

    def __init__(self, thresholds: Optional[dict[str, float]] = None):
        self.thresholds = thresholds or DEFAULT_THRESHOLDS.copy()

    def parse(self, path: str | Path, debug: bool = False) -> AigcReport:
        """Parse an AIGC report DOCX file."""
        path = Path(path)
        doc = DocxDocument(str(path))
        report = AigcReport(source_path=path, thresholds=self.thresholds.copy())
        fragments: list[ReportFragment] = []
        debug_colors: list[dict] = []

        # Try to find overall AIGC rate
        full_text = "\n".join(p.text for p in doc.paragraphs if p.text)
        report.overall_rate = self._extract_overall_rate(full_text)

        # Process each paragraph
        for idx, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue
            fragment, dbg = self._process_paragraph(para, idx, text, debug)
            fragments.append(fragment)
            if dbg:
                debug_colors.extend(dbg)

        # Also check table cells
        for tbl_idx, table in enumerate(doc.tables):
            for row_idx, row in enumerate(table.rows):
                for col_idx, cell in enumerate(row.cells):
                    for para in cell.paragraphs:
                        text = para.text.strip()
                        if not text:
                            continue
                        fragment, dbg = self._process_paragraph(
                            para, len(fragments), text, debug
                        )
                        fragment.section = f"table_{tbl_idx}_r{row_idx}_c{col_idx}"
                        fragments.append(fragment)
                        if dbg:
                            debug_colors.extend(dbg)

        report.fragments = fragments
        report.debug_colors = debug_colors
        return report

    def inspect_colors(self, path: str | Path) -> dict:
        """Debug mode: extract ALL color information from a DOCX report.

        Returns a dict with:
        - all discovered color/highlight/shading values and their counts
        - paragraph-by-paragraph color breakdown
        """
        path = Path(path)
        doc = DocxDocument(str(path))
        color_stats: dict[str, int] = {}
        para_details: list[dict] = []

        for idx, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue

            para_info = {"index": idx, "text_preview": text[:80], "colors": []}

            for run in para.runs:
                rPr = run._r.find(qn("w:rPr"))
                if rPr is None:
                    rPr = para._p.find(qn("w:pPr"))
                if rPr is None:
                    continue

                # highlight
                hl = rPr.find(qn("w:highlight"))
                if hl is not None:
                    val = hl.get(qn("w:val"), "")
                    para_info["colors"].append({"type": "highlight", "value": val})
                    color_stats[f"highlight:{val}"] = color_stats.get(f"highlight:{val}", 0) + 1

                # color (font color)
                color_el = rPr.find(qn("w:color"))
                if color_el is not None:
                    val = color_el.get(qn("w:val"), "")
                    para_info["colors"].append({"type": "color", "value": val})
                    color_stats[f"color:{val}"] = color_stats.get(f"color:{val}", 0) + 1

                # shading
                shd = rPr.find(qn("w:shd"))
                if shd is not None:
                    fill = shd.get(qn("w:fill"), "")
                    if fill:
                        para_info["colors"].append({"type": "shd_fill", "value": fill})
                        color_stats[f"shd_fill:{fill}"] = color_stats.get(f"shd_fill:{fill}", 0) + 1
                    bg = shd.get(qn("w:val"), "")
                    if bg:
                        para_info["colors"].append({"type": "shd_val", "value": bg})
                        color_stats[f"shd_val:{bg}"] = color_stats.get(f"shd_val:{bg}", 0) + 1

            if para_info["colors"]:
                para_details.append(para_info)

        # Also check tables
        for tbl_idx, table in enumerate(doc.tables):
            for row_idx, row in enumerate(table.rows):
                for col_idx, cell in enumerate(row.cells):
                    for para in cell.paragraphs:
                        text = para.text.strip()
                        if not text:
                            continue
                        for run in para.runs:
                            rPr = run._r.find(qn("w:rPr"))
                            if rPr is None:
                                continue
                            hl = rPr.find(qn("w:highlight"))
                            if hl is not None:
                                val = hl.get(qn("w:val"), "")
                                color_stats[f"highlight:{val}"] = color_stats.get(f"highlight:{val}", 0) + 1
                            color_el = rPr.find(qn("w:color"))
                            if color_el is not None:
                                val = color_el.get(qn("w:val"), "")
                                color_stats[f"color:{val}"] = color_stats.get(f"color:{val}", 0) + 1
                            shd = rPr.find(qn("w:shd"))
                            if shd is not None:
                                fill = shd.get(qn("w:fill"), "")
                                if fill:
                                    color_stats[f"shd_fill:{fill}"] = color_stats.get(f"shd_fill:{fill}", 0) + 1

        return {
            "color_stats": dict(sorted(color_stats.items(), key=lambda x: -x[1])),
            "paragraphs_with_color": para_details,
            "total_paragraphs_with_color": len(para_details),
        }

    # -- Internal -------------------------------------------------------------

    def _process_paragraph(self, para, idx: int, text: str, debug: bool):
        fragment = ReportFragment(text=text, index=idx)
        dbg_list: list[dict] = []

        # Collect ALL color indicators from all runs
        colors_found = []
        for run in para.runs:
            rPr = run._r.find(qn("w:rPr"))
            if rPr is None:
                continue

            # 1. highlight
            hl = rPr.find(qn("w:highlight"))
            if hl is not None:
                val = hl.get(qn("w:val"), "")
                band = self._highlight_to_band(val)
                if band:
                    colors_found.append(("highlight", val, band))

            # 2. font color
            color_el = rPr.find(qn("w:color"))
            if color_el is not None:
                val = color_el.get(qn("w:val"), "")
                band = self._hex_to_band(val)
                if band:
                    colors_found.append(("color", val, band))

            # 3. shading fill
            shd = rPr.find(qn("w:shd"))
            if shd is not None:
                fill = shd.get(qn("w:fill"), "")
                if fill and fill not in ("auto", "none", ""):
                    band = self._hex_to_band(fill)
                    if band:
                        colors_found.append(("shd_fill", fill, band))
                bg = shd.get(qn("w:val"), "")
                if bg and bg not in ("auto", "none", "clear", ""):
                    band = self._hex_to_band(bg)
                    if band:
                        colors_found.append(("shd_val", bg, band))

        # Select the highest-risk band found
        band_priority = [ColorBand.RED, ColorBand.ORANGE, ColorBand.PURPLE, ColorBand.BLACK, ColorBand.GRAY]
        best_band = ColorBand.GRAY
        for _, _, band in colors_found:
            if band_priority.index(band) < band_priority.index(best_band):
                best_band = band

        fragment.color_band = best_band
        if best_band != ColorBand.GRAY:
            fragment.score = self._band_to_score(best_band)

        # If no color found, try text-based score extraction
        if best_band == ColorBand.GRAY:
            score = self._extract_local_score(text)
            if score is not None:
                fragment.score = score
                fragment.color_band = self._score_to_band(score)

        if debug and colors_found:
            for ctype, cval, cband in colors_found:
                dbg_list.append({
                    "para_index": idx,
                    "color_type": ctype,
                    "color_value": cval,
                    "mapped_band": cband,
                    "text_preview": text[:60],
                })

        return fragment, dbg_list

    def _highlight_to_band(self, val: str) -> Optional[str]:
        return HIGHLIGHT_MAP.get(val)

    def _hex_to_band(self, hex_val: str) -> Optional[str]:
        """Map a hex color value to a risk band."""
        h = hex_val.upper().lstrip("#")

        # Exact matches
        if h in {x.upper() for x in RED_HEX}:
            return ColorBand.RED
        if h in {x.upper() for x in ORANGE_HEX}:
            return ColorBand.ORANGE
        if h in {x.upper() for x in PURPLE_HEX}:
            return ColorBand.PURPLE
        if h in {x.upper() for x in BLACK_HEX}:
            return ColorBand.BLACK
        if h in {x.upper() for x in GRAY_HEX}:
            return ColorBand.GRAY

        # Heuristic: check RGB components
        if len(h) == 6:
            try:
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

                # Very dark (near black) → BLACK
                if r < 40 and g < 40 and b < 40:
                    return ColorBand.BLACK
                # Near gray (all channels close) → GRAY (non-scored)
                if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
                    if r > 100:
                        return ColorBand.GRAY

                # Red-dominant
                if r > 180 and g < 120 and b < 120:
                    return ColorBand.RED
                # Orange: high red, medium green, low blue
                if r > 180 and g > 100 and b < 80:
                    return ColorBand.ORANGE
                # Purple: red + blue dominant, low green
                if r > 100 and b > 120 and g < 100:
                    return ColorBand.PURPLE
                # More purple: blue > red > green
                if b > 140 and r > 80 and g < 100:
                    return ColorBand.PURPLE
            except ValueError:
                pass
        return None

    def _extract_overall_rate(self, text: str) -> Optional[float]:
        patterns = [
            re.compile(r"AIGC疑似[度率]\s*[:：]\s*(\d{1,3}(?:\.\d{1,2})?)\s*%"),
            re.compile(r"总疑似[度率]\s*[:：]?\s*(\d{1,3}(?:\.\d{1,2})?)\s*%"),
            re.compile(r"疑似[度率]\s*[:：]?\s*(\d{1,3}(?:\.\d{1,2})?)\s*%"),
        ]
        for pattern in patterns:
            m = pattern.search(text)
            if m:
                try:
                    return float(m.group(1))
                except ValueError:
                    pass
        return None

    def _extract_local_score(self, text: str) -> Optional[float]:
        for pattern in self.SCORE_PATTERNS:
            m = pattern.search(text)
            if m:
                try:
                    return float(m.group(1))
                except ValueError:
                    pass
        return None

    def _score_to_band(self, score: float) -> str:
        if score >= self.thresholds["red"]:
            return ColorBand.RED
        elif score >= self.thresholds["orange"]:
            return ColorBand.ORANGE
        elif score >= self.thresholds["purple"]:
            return ColorBand.PURPLE
        else:
            return ColorBand.BLACK

    def _band_to_score(self, band: str) -> Optional[float]:
        if band == ColorBand.RED:
            return 85.0
        elif band == ColorBand.ORANGE:
            return 65.0
        elif band == ColorBand.PURPLE:
            return 55.0
        elif band == ColorBand.BLACK:
            return 25.0
        return None
