"""Format validator: verify DOCX formatting is preserved.

Checks:
- Document can be opened as valid DOCX
- Required OOXML parts are present
- No corrupt XML
"""

from __future__ import annotations

import zipfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FormatReport:
    """Report on format integrity."""

    passed: bool = True
    is_valid_zip: bool = True
    has_document_xml: bool = True
    has_content_types: bool = True
    issues: list[str] = field(default_factory=list)


class FormatValidator:
    """Validate that DOCX format is intact after write-back."""

    REQUIRED_PARTS = [
        "word/document.xml",
        "[Content_Types].xml",
        "_rels/.rels",
        "word/_rels/document.xml.rels",
    ]

    def validate(self, path: str | Path) -> FormatReport:
        """Check format integrity of a DOCX file."""
        report = FormatReport()
        path = Path(path)

        if not path.exists():
            report.passed = False
            report.issues.append(f"文件不存在: {path}")
            return report

        try:
            with zipfile.ZipFile(path, "r") as zf:
                # Check for errors
                bad = zf.testzip()
                if bad:
                    report.passed = False
                    report.issues.append(f"ZIP 损坏: {bad}")

                names = set(zf.namelist())

                # Check required parts
                for part in self.REQUIRED_PARTS:
                    if part not in names:
                        report.passed = False
                        report.issues.append(f"缺少必需部件: {part}")
                        if part == "word/document.xml":
                            report.has_document_xml = False
                        elif part == "[Content_Types].xml":
                            report.has_content_types = False

                # Verify document.xml is valid XML
                if "word/document.xml" in names:
                    try:
                        from lxml import etree
                        etree.fromstring(zf.read("word/document.xml"))
                    except Exception as e:
                        report.passed = False
                        report.issues.append(f"document.xml 解析失败: {e}")

        except zipfile.BadZipFile:
            report.passed = False
            report.is_valid_zip = False
            report.issues.append("不是有效的 ZIP 文件")
        except Exception as e:
            report.passed = False
            report.issues.append(f"验证异常: {e}")

        return report
