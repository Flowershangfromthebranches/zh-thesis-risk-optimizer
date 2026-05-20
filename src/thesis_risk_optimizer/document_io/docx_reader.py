"""DOCX reader: extract text units from a .docx thesis file.

Uses python-docx for high-level access and lxml for OOXML-level detail.
Each TextUnit stores stable location info (body_element_index, paragraph_index)
so the writer can re-locate it in a freshly-loaded document.xml.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from docx import Document as DocxDocument
from docx.oxml.ns import qn
from lxml import etree

from .text_units import TextUnit, TextUnitType

# -- OOXML namespaces --------------------------------------------------------
WML_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


@dataclass
class FormatInfo:
    """Paragraph/run formatting metadata for preservation."""

    style_name: str = ""
    bold: bool = False
    italic: bool = False
    font_name: str = ""
    font_size: Optional[float] = None  # in pt
    alignment: str = ""  # left, center, right, justify
    outline_level: Optional[int] = None  # heading level
    first_line_indent: Optional[float] = None


class DocxReader:
    """Read a .docx thesis and extract structured text units.

    Each unit stores stable location info for write-back:
    - body_element_index: index of the w:p or w:tbl in document body
    - paragraph_index: sequential index of all parsed paragraphs
    - original_text_hash: SHA256 of original text for verification
    """

    # -- Section markers for auto-classification -----------------------------
    SECTION_PATTERNS = [
        (re.compile(r"^(摘要|Abstract|摘要|ABSTRACT)\s*$"), "abstract"),
        (re.compile(r"^(绪论|绪言|引言|前言|第一章|第1章|研究背景)"), "introduction"),
        (re.compile(r"^(国内外)?研究现状|文献综述|相关工作"), "literature_review"),
        (re.compile(r"^(相关技术|关键技术|技术背景)"), "tech_background"),
        (re.compile(r"^(需求分析|可行性分析|系统分析)"), "requirements"),
        (re.compile(r"^(系统设计|总体设计|概要设计|详细设计|架构设计)"), "design"),
        (re.compile(r"^(系统实现|实现|开发|编码)"), "implementation"),
        (re.compile(r"^(系统测试|测试|实验)"), "testing"),
        (re.compile(r"^(结论|总结|展望|结束语)"), "conclusion"),
        (re.compile(r"^(致谢|Acknowledgement)"), "acknowledgement"),
        (re.compile(r"^(参考文献|References|Bibliography)"), "references"),
        (re.compile(r"^(附录|Appendix)"), "appendix"),
    ]

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        self._doc: Optional[DocxDocument] = None
        self._unit_counter = 0
        self._paragraph_index = 0
        self._current_section = ""
        self._units: list[TextUnit] = []

    # -- Public API -----------------------------------------------------------

    def read(self) -> list[TextUnit]:
        """Read the entire document and return all text units."""
        self._doc = DocxDocument(str(self.path))
        self._units = []
        self._unit_counter = 0
        self._paragraph_index = 0
        self._current_section = ""

        # Process body elements in order with stable indexing
        body = self._doc.element.body
        body_elements = list(body)
        for body_idx, element in enumerate(body_elements):
            tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag
            if tag == "p":
                self._process_paragraph_element(element, body_idx)
            elif tag == "tbl":
                self._process_table_element(element, body_idx)
            elif tag == "sdt":
                for p in element.iter(qn("w:p")):
                    self._process_paragraph_element(p, body_idx)

        return self._units

    # -- Paragraph processing -------------------------------------------------

    def _process_paragraph_element(self, p_element, body_idx: int) -> None:
        """Process a w:p element into a TextUnit."""
        text = self._extract_paragraph_text(p_element)
        if not text.strip():
            return

        fmt = self._extract_format(p_element)
        unit_type = self._classify_paragraph(p_element, text, fmt)
        section = self._update_section(text, unit_type)

        uid = self._next_uid()
        para_idx = self._paragraph_index
        self._paragraph_index += 1

        unit = TextUnit(
            uid=uid,
            unit_type=unit_type,
            text=text,
            section=section,
            metadata={
                "format": fmt,
                "body_element_index": body_idx,
                "paragraph_index": para_idx,
                "original_text_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            },
        )
        self._units.append(unit)

    def _extract_paragraph_text(self, p_element) -> str:
        """Extract plain text from a w:p element."""
        texts = []
        for t in p_element.iter(qn("w:t")):
            if t.text:
                texts.append(t.text)
        return "".join(texts)

    def _extract_format(self, p_element) -> FormatInfo:
        """Extract formatting info from a paragraph element."""
        fmt = FormatInfo()

        pPr = p_element.find(qn("w:pPr"))
        if pPr is not None:
            pStyle = pPr.find(qn("w:pStyle"))
            if pStyle is not None:
                fmt.style_name = pStyle.get(qn("w:val"), "")

            jc = pPr.find(qn("w:jc"))
            if jc is not None:
                fmt.alignment = jc.get(qn("w:val"), "")

            outline_lvl = pPr.find(qn("w:outlineLvl"))
            if outline_lvl is not None:
                try:
                    fmt.outline_level = int(outline_lvl.get(qn("w:val"), "0"))
                except ValueError:
                    pass

            ind = pPr.find(qn("w:ind"))
            if ind is not None:
                first_line = ind.get(qn("w:firstLine"))
                if first_line:
                    try:
                        fmt.first_line_indent = int(first_line) / 20
                    except ValueError:
                        pass

        for r in p_element.iter(qn("w:r")):
            rPr = r.find(qn("w:rPr"))
            if rPr is not None:
                b = rPr.find(qn("w:b"))
                if b is not None:
                    fmt.bold = True
                i = rPr.find(qn("w:i"))
                if i is not None:
                    fmt.italic = True
                rFonts = rPr.find(qn("w:rFonts"))
                if rFonts is not None:
                    fmt.font_name = rFonts.get(qn("w:ascii"), rFonts.get(qn("w:eastAsia"), ""))
                sz = rPr.find(qn("w:sz"))
                if sz is not None:
                    try:
                        fmt.font_size = int(sz.get(qn("w:val"), "0")) / 2
                    except ValueError:
                        pass
            break

        return fmt

    def _classify_paragraph(self, p_element, text: str, fmt: FormatInfo) -> TextUnitType:
        """Determine the TextUnitType of a paragraph.

        Returns COVER/TOC for protected content, HEADING for section titles,
        REFERENCE for bibliography, PARAGRAPH for body text.
        """
        clean = text.strip()
        style_lower = fmt.style_name.lower()

        if fmt.outline_level is not None or any(
            h in style_lower for h in ["heading", "标题"]
        ):
            return TextUnitType.HEADING

        if re.match(r"^\[\d+\]", clean):
            return TextUnitType.REFERENCE

        # Identity / cover patterns → COVER
        cover_patterns = [
            r"^(学号|学号|姓名|指导教师|导师|学院|专业方向|专业|班级|年级)",
            r"^(编号|题目|Title|学生姓名|Student|作者|Author)",
            r"^(本科生毕业设计|毕业设计|毕业论文|硕士学位论文)",
            r"^(原创性声明|学位论文原创性|版权使用|学位论文版权|独创性声明)",
            r"^(作者签名|导师签名|指导老师签名)",
            r"^\d{4}\s*年\s*\d{1,2}\s*月",
            r"^关键词\s*[：:]", r"^Keywords\s*[：:]",
            r"^目\s*录", r"^第[一二三四五六七八九十\d]+章\s",
            r"^[1-9]\d*(?:\.[1-9]\d*)*\s+\S",
            r"^绪\s*论\s*$", r"^结\s*论\s*$",
            r"^(致\s*谢|Acknowledgement)\s*$",
            r"^(参考文献|References|Bibliography)\s*$",
            r"^(附录|Appendix)\s",
            r"^(图|表|Figure|Table)\s*\d+",
        ]
        for pat in cover_patterns:
            if re.match(pat, clean):
                return TextUnitType.COVER

        # TOC lines (dots + page numbers)
        dots = clean.count(".") + clean.count("·") + clean.count("…")
        if dots >= 3 and re.search(r"\d{1,3}\s*$", clean):
            return TextUnitType.TOC

        # Diagram/entity/module text via ProtectionDetector
        from .protection_detector import classify_protection
        result = classify_protection(clean)
        if result.protected:
            return TextUnitType.COVER

        # Section markers → HEADING
        for pattern, _ in self.SECTION_PATTERNS:
            if pattern.search(clean):
                if "参考文献" in clean or "References" in clean:
                    return TextUnitType.REFERENCE
                return TextUnitType.HEADING

        return TextUnitType.PARAGRAPH

    def _update_section(self, text: str, unit_type: TextUnitType) -> str:
        """Update current section tracking. COVER/HEADING titles both update context."""
        if unit_type in (TextUnitType.HEADING, TextUnitType.COVER):
            clean = text.strip()
            # Explicit section markers for frozen titles
            if re.match(r"^(摘\s*要|ABSTRACT)\s*$", clean):
                self._current_section = "abstract"
                return "abstract"
            if re.match(r"^(绪\s*论|绪言|引言|前言)", clean):
                self._current_section = "introduction"
                return "introduction"
            if re.match(r"^(结\s*论|总结|展望)", clean):
                self._current_section = "conclusion"
                return "conclusion"
            for pattern, section_name in self.SECTION_PATTERNS:
                if pattern.search(clean):
                    self._current_section = section_name
                    return section_name
        return self._current_section

    # -- Table processing -----------------------------------------------------

    def _process_table_element(self, tbl_element, body_idx: int) -> None:
        """Process a w:tbl element — extract text from each cell."""
        for row_idx, tr in enumerate(tbl_element.iter(qn("w:tr"))):
            for col_idx, tc in enumerate(tr.iter(qn("w:tc"))):
                texts = []
                for p in tc.iter(qn("w:p")):
                    t = self._extract_paragraph_text(p)
                    if t.strip():
                        texts.append(t.strip())
                if texts:
                    uid = self._next_uid()
                    para_idx = self._paragraph_index
                    self._paragraph_index += 1
                    cell_text = " ".join(texts)
                    unit = TextUnit(
                        uid=uid,
                        unit_type=TextUnitType.TABLE_CELL,
                        text=cell_text,
                        section=self._current_section,
                        metadata={
                            "row": row_idx,
                            "col": col_idx,
                            "body_element_index": body_idx,
                            "paragraph_index": para_idx,
                            "original_text_hash": hashlib.sha256(cell_text.encode()).hexdigest()[:16],
                            "table_row": row_idx,
                            "table_col": col_idx,
                        },
                    )
                    self._units.append(unit)

    # -- Utility --------------------------------------------------------------

    def _next_uid(self) -> str:
        self._unit_counter += 1
        return f"u{self._unit_counter:04d}"

    @classmethod
    def detect_sections(cls, units: list[TextUnit]) -> dict[str, list[TextUnit]]:
        """Group units by their detected section."""
        sections: dict[str, list[TextUnit]] = {}
        for unit in units:
            sec = unit.section or "unknown"
            sections.setdefault(sec, []).append(unit)
        return sections
