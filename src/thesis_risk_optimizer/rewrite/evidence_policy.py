"""Evidence policy — defines what can and cannot be written into thesis text.

Three evidence classes:
A. verified_evidence — from original thesis, source code, screenshots, user uploads → can write
B. inferred_general_detail — conservative general statements from domain knowledge → can write
   but NO specific version numbers, function names, table names, parameter values, prices, quantities
C. missing_evidence — no source → cannot write into text, only into report suggestions
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class EvidenceClass(str, Enum):
    VERIFIED = "verified"
    INFERRED = "inferred"
    MISSING = "missing"


# -- Evidence contexts per discipline -----------------------------------------

@dataclass
class EvidenceContext:
    """What evidence types are accepted/forbidden for a specific discipline."""
    discipline: str
    accepted_evidence_types: list[str] = field(default_factory=list)
    forbidden_evidence_types: list[str] = field(default_factory=list)
    no_evidence_behavior: str = "conservative_rewrite"  # "conservative_rewrite" or "freeze"


EVIDENCE_CONTEXTS: dict[str, EvidenceContext] = {
    "computer": EvidenceContext(
        discipline="computer",
        accepted_evidence_types=[
            "源码", "系统截图", "测试报告", "数据库设计", "接口文档",
            "系统架构图", "模块设计文档",
        ],
        forbidden_evidence_types=[
            "编造的价格/成本数据", "编造的CVE编号", "编造的具体漏洞数量",
        ],
    ),
    "human_resource": EvidenceContext(
        discipline="human_resource",
        accepted_evidence_types=[
            "企业介绍", "问卷数据", "访谈记录", "岗位说明书",
            "绩效考核表", "薪酬制度", "培训记录", "员工满意度统计",
            "部门结构", "员工层级信息",
        ],
        forbidden_evidence_types=[
            "函数名", "代码目录", "版本号", "数据库表", "API",
            "测试环境", "命令行参数", "Payload",
            "软件模块输入输出", "程序代码",
        ],
    ),
    "management": EvidenceContext(
        discipline="management",
        accepted_evidence_types=[
            "企业介绍", "问卷数据", "访谈记录", "岗位说明书",
            "绩效考核表", "薪酬制度", "培训记录",
            "业务流程", "财务报表", "管理制度",
        ],
        forbidden_evidence_types=[
            "函数名", "代码目录", "版本号", "数据库表", "API",
        ],
    ),
    "education": EvidenceContext(
        discipline="education",
        accepted_evidence_types=[
            "课堂观察记录", "教案", "学生作业", "访谈", "问卷",
            "教学片段", "学生作品",
        ],
        forbidden_evidence_types=[
            "函数名", "代码目录", "版本号",
        ],
    ),
    "literature": EvidenceContext(
        discipline="literature",
        accepted_evidence_types=[
            "作品文本", "章节摘录", "人物关系", "叙事结构",
        ],
        forbidden_evidence_types=[
            "编造的文本引用", "AI生成的文本分析",
        ],
    ),
    "law": EvidenceContext(
        discipline="law",
        accepted_evidence_types=[
            "法条", "案例", "裁判文书", "政策文件",
        ],
        forbidden_evidence_types=[
            "编造的法条条号", "编造的案例事实",
        ],
    ),
    "medicine": EvidenceContext(
        discipline="medicine",
        accepted_evidence_types=[
            "护理记录", "操作规范", "指标数据", "观察表",
        ],
        forbidden_evidence_types=[
            "编造的临床数据", "编造的病例", "编造的实验组/对照组数据",
        ],
    ),
    "universal": EvidenceContext(
        discipline="universal",
        accepted_evidence_types=[
            "论文已有内容", "用户提供的材料",
        ],
        forbidden_evidence_types=[
            "编造的数据", "编造的文献", "编造的实验结果",
        ],
    ),
}


def get_evidence_context(discipline: str) -> EvidenceContext:
    """Get the evidence context for a discipline."""
    return EVIDENCE_CONTEXTS.get(discipline, EVIDENCE_CONTEXTS["universal"])


# -- Forbidden patterns when no verified evidence exists ----------------------
FORBIDDEN_WITHOUT_EVIDENCE = [
    # Version numbers
    re.compile(r"(?:Python|Java|Django|Flask|Spring|Vue|React|Node\.js|MySQL|PostgreSQL"
               r"|Redis|MongoDB|Docker|Linux|Ubuntu|CentOS|Nginx|Apache|Tomcat)\s*\d+\.\d+"),
    re.compile(r"(?:requests|BeautifulSoup|lxml|scrapy|selenium|pytest|unittest"
               r"|numpy|pandas|matplotlib|tensorflow|pytorch)\s*(?:==|version\s*)?\d+\.\d+"),
    # Specific function signatures
    re.compile(r"def\s+\w+\s*\([^)]*\)(?:\s*->\s*\w+)?"),
    # Database table/field details
    re.compile(r"(?:CREATE TABLE|ALTER TABLE|INSERT INTO|SELECT .+ FROM)\s+\w+"),
    # Command-line arguments
    re.compile(r"(?:python|java|npm|pip|docker|git)\s+\S+\s+(?:--?\w+|-\w)(?:\s+\S+)?"),
    # Specific prices / quantities
    re.compile(r"(?:价格|成本|费用|预算|花费|售价)\s*(?:为|约|：|:)\s*\d+"),
    re.compile(r"\d+\s*(?:元|万元|美元|欧元|日元)(?:/\s*(?:月|年|人|台|次))?"),
    # Specific experimental data
    re.compile(r"(?:准确率|召回率|F1|精确率|成功率|有效率|响应时间|延迟|吞吐量)\s*(?:为|达|约|：|:)\s*\d+\.?\d*\s*%"),
    re.compile(r"\d+\.?\d*\s*(?:ms|s|秒|毫秒|MB|GB|KB|Mbps|QPS|TPS|RPS)"),
    # Specific enterprise/school/system data
    re.compile(r"(?:员工\s*\d+\s*人|年营业额\s*\d+|市场占有率\s*\d+\.?\d*\s*%"
               r"|学生\s*\d+\s*人|班级\s*\d+\s*个)"),
]


@dataclass
class EvidenceCheckResult:
    """Result of checking a rewritten text for forbidden content."""
    passed: bool = True
    violations: list[str] = field(default_factory=list)
    risk_level: str = "low"  # low / medium / high


def check_evidence(text: str, has_source_code: bool = False,
                   has_test_report: bool = False,
                   has_user_materials: bool = False) -> EvidenceCheckResult:
    """Check if rewritten text contains content that requires evidence.

    If no evidence sources are available, any match against FORBIDDEN patterns
    is a violation. If some sources are available, violations are downgraded
    to warnings but still flagged.
    """
    result = EvidenceCheckResult()
    has_any_evidence = has_source_code or has_test_report or has_user_materials

    for pattern in FORBIDDEN_WITHOUT_EVIDENCE:
        matches = pattern.findall(text)
        for match in matches:
            match_str = str(match)[:80]
            if has_any_evidence:
                result.risk_level = "medium"
                result.violations.append(f"[WARNING] 需要确认来源: {match_str}")
            else:
                result.risk_level = "high"
                result.violations.append(f"[FORBIDDEN] 缺乏证据: {match_str}")
                result.passed = False

    return result


def check_no_fabrication(text: str, original_text: str) -> EvidenceCheckResult:
    """Check that rewritten text doesn't introduce fabricated claims.

    Compare against original — if original has no data/specifics,
    rewritten text should not invent them.
    """
    result = EvidenceCheckResult()

    # Count numeric values in original vs new
    orig_numbers = len(re.findall(r"\d+\.?\d*", original_text))
    new_numbers = len(re.findall(r"\d+\.?\d*", text))

    if orig_numbers < 3 and new_numbers >= 8:
        result.violations.append(
            f"新增大量数值(原文{orig_numbers}→新文{new_numbers})，可能编造数据"
        )
        result.passed = False
        result.risk_level = "high"

    return result


# -- Length policy (bidirectional) --------------------------------------------

@dataclass
class LengthRanges:
    """Configurable length ranges for total or paragraph-level checks."""
    ideal_low: float = 0.95
    ideal_high: float = 1.10
    acceptable_low: float = 0.90
    acceptable_high: float = 1.15
    hard_low: float = 0.85
    hard_high: float = 1.20

    def clamp_to_hard(self, min_length: int | None = None,
                      max_length: int | None = None,
                      target_range: tuple[float, float] | None = None) -> "LengthRanges":
        """Return a copy with user-specified overrides applied."""
        r = LengthRanges(
            ideal_low=self.ideal_low,
            ideal_high=self.ideal_high,
            acceptable_low=self.acceptable_low,
            acceptable_high=self.acceptable_high,
            hard_low=self.hard_low,
            hard_high=self.hard_high,
        )
        if target_range:
            r.ideal_low = target_range[0]
            r.ideal_high = target_range[1]
        return r


# Default ranges
TOTAL_RANGES = LengthRanges()
PARAGRAPH_RANGES = LengthRanges(
    ideal_low=0.80, ideal_high=1.40,
    acceptable_low=0.70, acceptable_high=1.60,
    hard_low=0.60, hard_high=1.80,
)

# Section-specific overrides: some sections tolerate more compression or expansion
SECTION_RANGE_OVERRIDES: dict[str, LengthRanges] = {
    "abstract": LengthRanges(
        ideal_low=0.90, ideal_high=1.10,
        acceptable_low=0.85, acceptable_high=1.15,
        hard_low=0.80, hard_high=1.20,
    ),
    "conclusion": LengthRanges(
        ideal_low=0.90, ideal_high=1.20,
        acceptable_low=0.85, acceptable_high=1.30,
        hard_low=0.80, hard_high=1.40,
    ),
}


def _classify_length(ratio: float, ranges: LengthRanges) -> str:
    """Classify a ratio into ideal / acceptable / hard / out_of_range."""
    if ranges.ideal_low <= ratio <= ranges.ideal_high:
        return "ideal"
    if ranges.acceptable_low <= ratio <= ranges.acceptable_high:
        return "acceptable"
    if ranges.hard_low <= ratio <= ranges.hard_high:
        return "hard"
    return "out_of_range"


def _detect_length_reasons(original_text: str, new_text: str) -> list[str]:
    """Heuristic analysis of why length changed."""
    reasons: list[str] = []
    delta = len(new_text) - len(original_text)
    if delta == 0:
        return reasons

    # Template / filler detection
    template_markers = ["随着", "具有十分重要的", "具有重要意义", "具有良好的",
                        "为相关领域提供了参考", "本文首先", "其次", "最后"]
    orig_templates = sum(1 for m in template_markers if m in original_text)
    new_templates = sum(1 for m in template_markers if m in new_text)
    if orig_templates > new_templates and delta < 0:
        reasons.append("压缩模板表达")

    # Repetition detection (simple: repeated sentences)
    import re
    orig_sents = set(re.findall(r"[^。！？]{4,}[。！？]", original_text))
    new_sents = set(re.findall(r"[^。！？]{4,}[。！？]", new_text))
    if len(orig_sents) > len(new_sents) + 1 and delta < 0:
        reasons.append("合并重复内容")

    # Expansion reasons
    if delta > 0:
        # Check if new text has more specific detail markers
        detail_markers = ["实现", "测试", "过程", "步骤", "方法", "结果"]
        orig_details = sum(1 for m in detail_markers if m in original_text)
        new_details = sum(1 for m in detail_markers if m in new_text)
        if new_details > orig_details:
            reasons.append("补充实现过程")
        else:
            reasons.append("扩写")

    if delta < 0 and not reasons:
        reasons.append("删除无效扩写")

    return reasons


class LengthPolicy:
    """Bidirectional length control policy.

    Rules:
    - ideal_range: 95%-110% of original (recommended)
    - acceptable_range: 90%-115% (acceptable with explanation)
    - hard_range: 85%-120% (boundary, needs human review)
    - Below 85% or above 120%: FAILURE
    - Per-paragraph: 80%-140% ideal, 70%-160% acceptable, 60%-180% hard
    """

    # Total document ranges
    TOTAL = TOTAL_RANGES
    # Single paragraph ranges
    PARAGRAPH = PARAGRAPH_RANGES

    @staticmethod
    def check_total(original_chars: int, new_chars: int,
                    ranges: LengthRanges | None = None,
                    min_length: int | None = None,
                    max_length: int | None = None) -> dict:
        """Check total document length against policy.

        Returns dict with keys: passed, level, ratio, band, message, reasons.
        """
        r = ranges or LengthPolicy.TOTAL
        ratio = new_chars / max(1, original_chars)
        band = _classify_length(ratio, r)

        # User-specified absolute bounds override ratio-based checks
        if min_length is not None and new_chars < min_length:
            return {
                "passed": False,
                "level": "FAILURE",
                "ratio": ratio,
                "band": band,
                "message": f"优化后字数 {new_chars} 低于用户指定最低字数 {min_length}。",
                "reasons": [],
            }
        if max_length is not None and new_chars > max_length:
            return {
                "passed": False,
                "level": "FAILURE",
                "ratio": ratio,
                "band": band,
                "message": f"优化后字数 {new_chars} 超过用户指定最高字数 {max_length}。",
                "reasons": [],
            }

        if band == "out_of_range":
            if ratio > r.hard_high:
                return {
                    "passed": False,
                    "level": "FAILURE",
                    "ratio": ratio,
                    "band": band,
                    "message": f"总字数增长 {ratio:.0%}，超过硬上限 {r.hard_high:.0%}，本轮优化失败。",
                    "reasons": [],
                }
            else:
                return {
                    "passed": False,
                    "level": "FAILURE",
                    "ratio": ratio,
                    "band": band,
                    "message": f"总字数压缩至 {ratio:.0%}，低于硬下限 {r.hard_low:.0%}，本轮优化失败。",
                    "reasons": [],
                }
        elif band == "hard":
            if ratio > r.acceptable_high:
                msg = f"总字数增长 {ratio:.0%}，处于硬上限区间 ({r.acceptable_high:.0%}-{r.hard_high:.0%})，建议人工复查。"
            else:
                msg = f"总字数压缩至 {ratio:.0%}，处于硬下限区间 ({r.hard_low:.0%}-{r.acceptable_low:.0%})，建议人工复查。"
            return {
                "passed": True,
                "level": "WARNING",
                "ratio": ratio,
                "band": band,
                "message": msg,
                "reasons": [],
            }
        elif band == "acceptable":
            return {
                "passed": True,
                "level": "OK",
                "ratio": ratio,
                "band": band,
                "message": "",
                "reasons": [],
            }
        else:  # ideal
            return {
                "passed": True,
                "level": "OK",
                "ratio": ratio,
                "band": band,
                "message": "",
                "reasons": [],
            }

    @staticmethod
    def check_paragraph(original_chars: int, new_chars: int,
                        section: str = "",
                        ranges: LengthRanges | None = None) -> dict:
        """Check single paragraph length against policy."""
        # Section-specific overrides
        r = ranges
        if r is None and section in SECTION_RANGE_OVERRIDES:
            r = SECTION_RANGE_OVERRIDES[section]
        if r is None:
            r = LengthPolicy.PARAGRAPH

        ratio = new_chars / max(1, original_chars)
        band = _classify_length(ratio, r)

        if band == "out_of_range":
            if ratio > r.hard_high:
                return {
                    "passed": False,
                    "ratio": ratio,
                    "band": band,
                    "message": f"单段字数增长 {ratio:.0%}，超过硬上限 {r.hard_high:.0%}。",
                }
            else:
                return {
                    "passed": False,
                    "ratio": ratio,
                    "band": band,
                    "message": f"单段字数压缩至 {ratio:.0%}，低于硬下限 {r.hard_low:.0%}。",
                }
        return {"passed": True, "ratio": ratio, "band": band, "message": ""}
