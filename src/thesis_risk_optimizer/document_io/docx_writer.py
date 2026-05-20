"""DOCX writer: write modified text back to a .docx file.

Uses OOXML-level patching via lxml to modify only w:t text nodes
in word/document.xml, preserving styles, numbering, headers, footers,
images, and all other document structure.

KEY FIX v1.1:
- Uses body_element_index + paragraph_index for re-location, NOT
  reader's p_element objects (which belong to a different XML tree).
- Uses qn("w:t") instead of NS["w:t"] (which was a KeyError).
- Skips protected paragraphs (cover, declaration, TOC, references, formulas).
"""

from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path
from typing import Optional

from docx.oxml.ns import qn
from lxml import etree

from .text_units import TextUnit, TextUnitType
from .format_preserver import FROZEN_UNIT_TYPES

WML_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


class DocxWriter:
    """Write modified text units back to a DOCX file.

    Works by:
    1. Loading the original DOCX (zip)
    2. Parsing word/document.xml into an lxml tree
    3. Re-locating paragraphs by body_element_index
    4. Patching w:t text nodes with modified text
    5. Writing the new DOCX

    NEVER modifies the original file.
    """

    PROTECTED_TYPES = FROZEN_UNIT_TYPES | {
        TextUnitType.FOOTNOTE,
        TextUnitType.ENDNOTE,
    }

    def __init__(self, original_path: str | Path):
        self.original_path = Path(original_path)
        if not self.original_path.exists():
            raise FileNotFoundError(f"File not found: {self.original_path}")
        self._doc_xml: Optional[etree._Element] = None
        self._body_elements: list = []
        self._mod_count = 0
        self._error_count = 0
        self._skip_count = 0

    # -- Public API -----------------------------------------------------------

    def apply_modifications(self, units: list[TextUnit]) -> dict:
        """Apply text modifications from units back to the document XML.

        Returns dict with counts: modified, skipped, errors.
        """
        self._load_document_xml()
        self._mod_count = 0
        self._error_count = 0
        self._skip_count = 0

        # Index body elements
        body = self._doc_xml.find(f"{{{WML_NS}}}body")
        if body is None:
            return {"modified": 0, "skipped": 0, "errors": 1, "msg": "no body found"}
        self._body_elements = list(body)

        for unit in units:
            # Skip unchanged
            if unit.text == unit.original_text:
                self._skip_count += 1
                continue
            # Skip protected types
            if unit.unit_type in self.PROTECTED_TYPES:
                self._skip_count += 1
                continue
            # Skip freeze/skip actions
            if unit.action.value in ("freeze", "skip"):
                self._skip_count += 1
                continue

            # Re-locate and patch
            success = self._patch_unit(unit)
            if not success:
                self._error_count += 1

        return {
            "modified": self._mod_count,
            "skipped": self._skip_count,
            "errors": self._error_count,
        }

    def save(self, output_path: str | Path) -> Path:
        """Save the modified document to a new file."""
        output_path = Path(output_path)

        if self._doc_xml is None:
            shutil.copy2(self.original_path, output_path)
            return output_path

        with zipfile.ZipFile(self.original_path, "r") as zin:
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename == "word/document.xml":
                        xml_bytes = etree.tostring(
                            self._doc_xml,
                            xml_declaration=True,
                            encoding="UTF-8",
                            standalone=True,
                        )
                        zout.writestr(item, xml_bytes)
                    else:
                        zout.writestr(item, zin.read(item.filename))

        return output_path

    # -- Internal -------------------------------------------------------------

    def _load_document_xml(self) -> None:
        """Load word/document.xml from the DOCX zip for patching."""
        with zipfile.ZipFile(self.original_path, "r") as zf:
            doc_xml_bytes = zf.read("word/document.xml")
        self._doc_xml = etree.fromstring(doc_xml_bytes)

    def _patch_unit(self, unit: TextUnit) -> bool:
        """Re-locate the paragraph in the writer's XML tree and patch its text.

        Uses body_element_index from the reader's metadata to find the
        correct paragraph in the freshly-loaded document.xml.
        """
        body_idx = unit.metadata.get("body_element_index")
        if body_idx is None or body_idx >= len(self._body_elements):
            return False

        p_element = self._body_elements[body_idx]

        # Verify it's the right paragraph by checking text hash
        # (skip verification for table cells since text is concatenated)
        if unit.unit_type != TextUnitType.TABLE_CELL:
            current_text = self._extract_text_from_element(p_element)
            expected_hash = unit.metadata.get("original_text_hash", "")
            current_hash = hashlib.sha256(current_text.encode()).hexdigest()[:16]
            if expected_hash and current_hash != expected_hash:
                # Hash mismatch — try adjacent elements (off-by-one tolerance)
                found = False
                for offset in [-1, 1, -2, 2]:
                    adj_idx = body_idx + offset
                    if 0 <= adj_idx < len(self._body_elements):
                        adj_text = self._extract_text_from_element(self._body_elements[adj_idx])
                        adj_hash = hashlib.sha256(adj_text.encode()).hexdigest()[:16]
                        if adj_hash == expected_hash:
                            p_element = self._body_elements[adj_idx]
                            found = True
                            break
                if not found:
                    return False

        # For table cells, locate within the table
        if unit.unit_type == TextUnitType.TABLE_CELL:
            row = unit.metadata.get("table_row")
            col = unit.metadata.get("table_col")
            if row is not None and col is not None:
                p_element = self._find_table_cell(p_element, row, col)
                if p_element is None:
                    return False

        # Patch the text
        self._patch_paragraph_text(p_element, unit)
        return True

    def _extract_text_from_element(self, element) -> str:
        """Extract plain text from a w:p or w:tc element."""
        texts = []
        for t in element.iter(qn("w:t")):
            if t.text:
                texts.append(t.text)
        return "".join(texts)

    def _find_table_cell(self, tbl_element, row: int, col: int):
        """Find a specific table cell within a w:tbl element."""
        rows = list(tbl_element.iter(qn("w:tr")))
        if row >= len(rows):
            return None
        cells = list(rows[row].iter(qn("w:tc")))
        if col >= len(cells):
            return None
        # Return the first paragraph in the cell
        for p in cells[col].iter(qn("w:p")):
            return p
        return None

    def _patch_paragraph_text(self, p_element, unit: TextUnit) -> None:
        """Replace text in a w:p element's w:t nodes with modified text.

        Uses qn("w:t") for namespace-safe lookup.
        """
        t_nodes = list(p_element.iter(qn("w:t")))
        if not t_nodes:
            return

        new_text = unit.text
        if not new_text:
            return

        # Put all new text in the first w:t, clear the rest
        t_nodes[0].text = new_text
        for tn in t_nodes[1:]:
            tn.text = ""

        self._mod_count += 1

    # -- Validation -----------------------------------------------------------

    def validate_output(self, path: str | Path) -> bool:
        """Check that a saved DOCX is a valid zip with required parts."""
        try:
            with zipfile.ZipFile(path, "r") as zf:
                required = {"word/document.xml", "[Content_Types].xml"}
                present = set(zf.namelist())
                if required - present:
                    return False
                zf.read("word/document.xml")
            return True
        except Exception:
            return False
