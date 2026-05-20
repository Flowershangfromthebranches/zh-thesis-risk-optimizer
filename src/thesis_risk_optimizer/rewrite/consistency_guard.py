"""Consistency guard: prevent fabrication of inconsistent details.

Checks:
1. Python version consistency (no 3.9/3.10/3.11 mix without evidence)
2. Tool name consistency
3. Test environment/target names must have source
4. Prices, stats, CVE numbers without source → delete or conservative expression
5. No fabricated directory structure, class names, function names without source code
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ConsistencyResult:
    """Result of consistency check."""
    passed: bool = True
    violations: list[str] = field(default_factory=list)
    risk_level: str = "low"  # low / medium / high


# Patterns that indicate fabricated technical details
VERSION_PATTERNS = [
    # Python versions
    re.compile(r"Python\s+(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE),
    # Java versions
    re.compile(r"(?:Java|JDK|JRE)\s+(\d+(?:\.\d+)*(?:_\d+)?)", re.IGNORECASE),
    # MySQL versions
    re.compile(r"MySQL\s+(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE),
    # Node.js versions
    re.compile(r"Node\.?js\s+(?:v?)(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE),
    # Vue/React versions
    re.compile(r"(?:Vue|React|Angular)\s+(?:v?)(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE),
]

# Specific tool/project names that shouldn't appear without evidence
SPECIFIC_TOOLS = [
    "Nessus", "Acunetix", "OpenVAS", "Burp Suite", "OWASP ZAP",
    "DVWA", "SQLi-labs", "WebVulnScanner", "Pikachu", "Mutillidae",
    "WebGoat", "HackTheBox", "TryHackMe",
]

# Patterns for fabricated data
FABRICATED_DATA_PATTERNS = [
    # CVE numbers
    re.compile(r"CVE-\d{4}-\d{4,}", re.IGNORECASE),
    # Specific prices
    re.compile(r"(?:价格|费用|成本|售价)\s*(?:为|约|：|:)\s*\d+"),
    # Statistics without source
    re.compile(r"(?:据统计|根据调查|研究表明)\s*.{0,20}\d+%"),
    # IBM data breach cost
    re.compile(r"IBM.*?(?:数据泄露|安全事件).*?(?:成本|费用).*?\d+"),
]


class ConsistencyGuard:
    """Check for fabricated or inconsistent technical details."""

    def check(self, text: str, original_text: str = "",
              has_source_code: bool = False,
              has_test_report: bool = False,
              has_user_materials: bool = False) -> ConsistencyResult:
        """Check text for consistency violations.

        Args:
            text: Rewritten text to check
            original_text: Original text for comparison
            has_source_code: Whether user provided source code
            has_test_report: Whether user provided test report
            has_user_materials: Whether user provided other materials

        Returns:
            ConsistencyResult with violations
        """
        result = ConsistencyResult()
        has_any_evidence = has_source_code or has_test_report or has_user_materials

        # Check version consistency
        self._check_version_consistency(text, original_text, result, has_any_evidence)

        # Check specific tool names
        self._check_specific_tools(text, original_text, result, has_any_evidence)

        # Check fabricated data
        self._check_fabricated_data(text, original_text, result, has_any_evidence)

        # Check directory/class/function names
        self._check_code_artifacts(text, original_text, result, has_any_evidence)

        return result

    def _check_version_consistency(self, text: str, original_text: str,
                                    result: ConsistencyResult, has_evidence: bool):
        """Check for inconsistent version numbers."""
        # Find all versions in rewritten text
        versions = {}
        for pattern in VERSION_PATTERNS:
            for match in pattern.finditer(text):
                tech = match.group(0).split()[0]  # e.g., "Python"
                ver = match.group(1)
                if tech not in versions:
                    versions[tech] = set()
                versions[tech].add(ver)

        # Check for multiple versions of same technology
        for tech, vers in versions.items():
            if len(vers) > 1:
                if has_evidence:
                    result.risk_level = "medium"
                    result.violations.append(
                        f"[WARNING] {tech} 版本不一致: {', '.join(sorted(vers))}，请确认来源"
                    )
                else:
                    result.passed = False
                    result.risk_level = "high"
                    result.violations.append(
                        f"[FORBIDDEN] {tech} 版本不一致 ({', '.join(sorted(vers))})，"
                        "且无证据支持"
                    )

        # Check if versions appear in rewritten but not original
        for pattern in VERSION_PATTERNS:
            orig_matches = set(m.group(1) for m in pattern.finditer(original_text))
            new_matches = set(m.group(1) for m in pattern.finditer(text))
            new_only = new_matches - orig_matches
            if new_only and not has_evidence:
                tech = pattern.pattern.split("(")[0].strip("(?:")
                result.passed = False
                result.risk_level = "high"
                result.violations.append(
                    f"[FORBIDDEN] 新增版本号 {tech} {', '.join(new_only)}，无证据支持"
                )

    def _check_specific_tools(self, text: str, original_text: str,
                               result: ConsistencyResult, has_evidence: bool):
        """Check for specific tool names that shouldn't appear without evidence."""
        for tool in SPECIFIC_TOOLS:
            if tool.lower() in text.lower() and tool.lower() not in original_text.lower():
                if has_evidence:
                    result.risk_level = "medium"
                    result.violations.append(
                        f"[WARNING] 新增工具名称 '{tool}'，请确认来源"
                    )
                else:
                    result.passed = False
                    result.risk_level = "high"
                    result.violations.append(
                        f"[FORBIDDEN] 新增工具名称 '{tool}'，无证据支持"
                    )

    def _check_fabricated_data(self, text: str, original_text: str,
                                result: ConsistencyResult, has_evidence: bool):
        """Check for fabricated statistics, CVE numbers, prices."""
        for pattern in FABRICATED_DATA_PATTERNS:
            matches = pattern.findall(text)
            orig_matches = pattern.findall(original_text)

            # Only flag if new matches appear that weren't in original
            new_count = len(matches) - len(orig_matches)
            if new_count > 0:
                if has_evidence:
                    result.risk_level = "medium"
                    result.violations.append(
                        f"[WARNING] 新增 {new_count} 处统计数据/引用，请确认来源"
                    )
                else:
                    result.passed = False
                    result.risk_level = "high"
                    result.violations.append(
                        f"[FORBIDDEN] 新增 {new_count} 处统计数据/引用，无证据支持"
                    )

    def _check_code_artifacts(self, text: str, original_text: str,
                               result: ConsistencyResult, has_evidence: bool):
        """Check for fabricated code artifacts (directory, class, function names)."""
        # Directory structure patterns
        dir_pattern = re.compile(r"(?:src/|lib/|app/|test/|tests/|bin/|config/)\w+(?:/\w+)*")
        new_dirs = set(dir_pattern.findall(text)) - set(dir_pattern.findall(original_text))

        # Class name patterns (PascalCase)
        class_pattern = re.compile(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b")
        # Only flag if many new class-like names appear
        new_classes = set(class_pattern.findall(text)) - set(class_pattern.findall(original_text))

        # Function name patterns (camelCase or snake_case with parentheses)
        func_pattern = re.compile(r"\b[a-z][a-zA-Z0-9]*\s*\(|\b[a-z][a-z0-9_]+\s*\(")
        new_funcs = set(func_pattern.findall(text)) - set(func_pattern.findall(original_text))

        if (new_dirs or len(new_classes) > 3 or len(new_funcs) > 3) and not has_evidence:
            result.passed = False
            result.risk_level = "high"
            if new_dirs:
                result.violations.append(
                    f"[FORBIDDEN] 新增目录结构 {list(new_dirs)[:3]}，无源码证据"
                )
            if len(new_classes) > 3:
                result.violations.append(
                    f"[FORBIDDEN] 新增 {len(new_classes)} 个类名，无源码证据"
                )
            if len(new_funcs) > 3:
                result.violations.append(
                    f"[FORBIDDEN] 新增 {len(new_funcs)} 个函数名，无源码证据"
                )
