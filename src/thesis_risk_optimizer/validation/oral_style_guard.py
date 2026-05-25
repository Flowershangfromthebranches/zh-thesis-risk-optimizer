"""Oral-style guardrails for thesis output.

The project should not reduce AI-writing traces by making thesis text chatty.
This module is domain-neutral: it only checks whether oral expressions exceed
the shared thesis-style thresholds.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from ..strategies.domain_profiles import get_domain_profile


NATURAL_EXPRESSIONS: tuple[str, ...] = (
    "实际上", "具体来看", "从材料看", "从调研看", "对研究对象而言",
    "在实际过程中", "当前阶段", "后续", "这一问题", "相比之下",
)

MILD_ORAL_TERMS: tuple[str, ...] = (
    "比较明显", "不够及时", "跟不上", "来得慢", "看不清", "做得不够",
    "差距较大", "难以落地", "有一定影响", "受到限制", "过程没有被记录",
    "实际执行中容易出现问题",
)

STRONG_ORAL_REPLACEMENTS: dict[str, str] = {
    "说白了": "换言之",
    "说得直白点": "具体而言",
    "这两手": "这两类做法",
    "对不上": "难以匹配",
    "搞不清": "难以明确",
    "没人管": "缺少记录、反馈或管理",
    "不被当回事": "未得到充分重视",
    "看不见的活": "隐性工作",
    "上面说下面听": "单向指令式沟通",
    "没劲": "积极性下降",
    "杯水车薪": "难以产生充分作用",
    "心累": "容易产生倦怠感",
    "路子走窄了": "发展路径较为受限",
    "拿顶薪": "获得较高薪酬",
    "付出变现": "付出转化为实际回报",
    "基本生活兜住": "保障基本生活需要",
    "师父带徒弟那种": "传统师徒式带教",
    "全看有没有心": "主要取决于执行者投入程度",
    "这公司还行": "对该组织的评价相对正向",
    "不是不想干活": "并非排斥工作本身",
    "被打卡框死": "受到机械化考勤约束",
    "哪还有心情": "难以形成积极感受",
    "这帮人": "该群体",
    "走到头了": "即将结束",
    "跌跌撞撞": "经历并不总是一帆风顺",
    "撑不住": "面临较大压力",
    "靠一靠": "获得支持",
    "托起来": "给予支持和帮助",
    "太拉了": "表现不理想",
    "很离谱": "明显不合理",
    "特别扯": "缺乏合理性",
    "一堆问题": "存在多方面问题",
    "乱七八糟": "秩序较为混乱",
    "硬凑": "缺少充分依据",
    "糊弄": "处理较为敷衍",
    "说不过去": "缺乏充分合理性",
}

STRONG_ORAL_TERMS: tuple[str, ...] = tuple(STRONG_ORAL_REPLACEMENTS)

FORMAL_SECTIONS: set[str] = {
    "abstract", "theory", "theoretical_basis", "methodology", "method",
    "research_method", "data_analysis", "analysis", "conclusion",
}

ACKNOWLEDGEMENT_SECTIONS: set[str] = {"acknowledgement", "thanks", "致谢"}


@dataclass(frozen=True)
class OralStyleResult:
    total_sentences: int
    natural_expression_count: int
    mild_oral_count: int
    strong_oral_count: int
    oral_density: float
    strong_oral_terms: list[str] = field(default_factory=list)
    status: str = "pass"
    suggested_replacements: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status != "fail"


class OralStyleGuard:
    """Detect and limit oral expressions in thesis text."""

    def check(self, text: str, section: str = "body", domain: str | None = None) -> OralStyleResult:
        section_key = self._section_key(section)
        domain_key = get_domain_profile(domain).name if domain else ""
        sentences = self.split_sentences(text)
        total = max(1, len(sentences))

        natural_count = self._count_terms(text, NATURAL_EXPRESSIONS)
        mild_count = self._count_terms(text, MILD_ORAL_TERMS)
        strong_terms = self._strong_terms(text)
        strong_count = len(strong_terms)
        density = mild_count / total

        warnings: list[str] = []
        status = "pass"
        max_mild = self._max_mild_count(total, section_key, domain_key)

        if strong_count > 0:
            status = "fail"
            warnings.append("正文或正式章节中存在过度口语化表达")

        if mild_count > max_mild:
            if section_key in FORMAL_SECTIONS:
                warnings.append("正式章节轻微口语化表达超过阈值")
                status = "warning" if status != "fail" else status
            elif density > 0.15:
                warnings.append("正文轻微口语化密度超过 15%")
                status = "fail"
            else:
                warnings.append("正文轻微口语化密度超过 10%")
                status = "warning" if status != "fail" else status

        if section_key in FORMAL_SECTIONS and density > 0.05 and status != "fail":
            status = "warning"
            warnings.append("正式章节轻微口语化密度超过 5%")

        return OralStyleResult(
            total_sentences=total,
            natural_expression_count=natural_count,
            mild_oral_count=mild_count,
            strong_oral_count=strong_count,
            oral_density=density,
            strong_oral_terms=strong_terms,
            status=status,
            suggested_replacements={
                term: STRONG_ORAL_REPLACEMENTS[term]
                for term in strong_terms
                if term in STRONG_ORAL_REPLACEMENTS
            },
            warnings=warnings,
        )

    @staticmethod
    def split_sentences(text: str) -> list[str]:
        parts = re.split(r"(?<=[。！？!?；;])", text)
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _count_terms(text: str, terms: tuple[str, ...]) -> int:
        return sum(text.count(term) for term in terms)

    def _strong_terms(self, text: str) -> list[str]:
        unquoted = self._strip_quoted_text(text)
        return [term for term in STRONG_ORAL_TERMS if term in unquoted]

    @staticmethod
    def _strip_quoted_text(text: str) -> str:
        text = re.sub(r"“[^”]*”", "", text)
        text = re.sub(r"\"[^\"]*\"", "", text)
        text = re.sub(r"'[^']*'", "", text)
        return text

    @staticmethod
    def _section_key(section: str | None) -> str:
        return (section or "body").strip().lower()

    @staticmethod
    def _max_mild_count(total_sentences: int, section_key: str, domain_key: str = "") -> int:
        if domain_key in {"law", "medicine"}:
            return 0
        if section_key in FORMAL_SECTIONS:
            return 0
        per_10 = 2 if section_key in ACKNOWLEDGEMENT_SECTIONS else 1
        return math.floor(total_sentences * per_10 / 10)
