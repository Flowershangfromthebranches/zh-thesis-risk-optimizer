"""Generic template-risk detector for Chinese thesis paragraphs."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from .material_anchor_detector import MaterialAnchorDetector


@dataclass
class TemplateRiskResult:
    paragraph_id: str
    template_risk_score: float = 0.0
    matched_patterns: list[str] = field(default_factory=list)
    abstract_density: float = 0.0
    material_anchor_score: float = 0.0
    suggested_action: str = "keep"
    reason: str = ""


class TemplateRiskDetector:
    """Detect professional-neutral template and abstraction risk."""

    TEMPLATE_PATTERNS: tuple[tuple[str, re.Pattern], ...] = (
        ("主要用于", re.compile(r"主要用于")),
        ("主要包括", re.compile(r"主要包括")),
        ("围绕.*展开", re.compile(r"围绕.{0,40}展开")),
        ("从.*角度看", re.compile(r"从.{0,20}角度看")),
        ("从.*方面", re.compile(r"从.{0,20}方面")),
        ("通过.*实现", re.compile(r"通过.{0,40}实现")),
        ("能够.*", re.compile(r"能够.{0,30}")),
        ("用于.*", re.compile(r"用于.{0,30}")),
        ("便于.*", re.compile(r"便于.{0,30}")),
        ("有助于.*", re.compile(r"有助于.{0,30}")),
        ("由此可见", re.compile(r"由此可见")),
        ("综上所述", re.compile(r"综上所述")),
        ("本文主要完成", re.compile(r"本文主要完成")),
        ("本文从.*展开", re.compile(r"本文从.{0,40}展开")),
        ("第一.*第二.*第三", re.compile(r"第一.{0,80}第二.{0,80}第三")),
        ("既.*又", re.compile(r"既.{0,30}又")),
        ("不仅.*而且", re.compile(r"不仅.{0,40}而且")),
        ("不只是.*而是", re.compile(r"不只是.{0,40}而是")),
        ("承担.*任务", re.compile(r"承担.{0,30}任务")),
        ("提供.*支撑", re.compile(r"提供.{0,30}支撑")),
        ("形成.*闭环", re.compile(r"形成.{0,30}闭环")),
        ("具有.*意义", re.compile(r"具有.{0,20}意义")),
        ("具有重要意义", re.compile(r"具有重要意义")),
        ("提升.*效率", re.compile(r"提升.{0,20}效率")),
        ("降低.*成本", re.compile(r"降低.{0,20}成本")),
        ("满足.*需求", re.compile(r"满足.{0,20}需求")),
        ("为.*提供参考", re.compile(r"为.{0,30}提供参考")),
        ("为.*奠定基础", re.compile(r"为.{0,30}奠定基础")),
        ("具有一定的理论意义和实践意义", re.compile(r"具有一定的理论意义和实践意义")),
        ("相关研究表明", re.compile(r"相关研究表明")),
        ("随着.*发展", re.compile(r"随着.{0,30}发展")),
        ("在.*背景下", re.compile(r"在.{0,30}背景下")),
    )

    ABSTRACT_WORDS = (
        "系统", "功能", "模块", "流程", "数据", "管理", "实现", "优化",
        "提升", "支撑", "机制", "平台", "体系", "路径", "策略", "价值",
        "意义", "问题", "措施", "水平", "能力", "质量", "效率", "发展",
        "建设", "完善", "推进",
    )

    def __init__(self):
        self.anchor_detector = MaterialAnchorDetector()

    def detect_paragraph(
        self,
        text: str,
        paragraph_id: str = "",
        domain: str | None = None,
    ) -> TemplateRiskResult:
        matched = [label for label, pattern in self.TEMPLATE_PATTERNS if pattern.search(text)]
        abstract_hits = sum(text.count(word) for word in self.ABSTRACT_WORDS)
        abstract_density = abstract_hits / max(1.0, len(text) / 10.0)
        anchor = self.anchor_detector.detect(text, domain)

        score = min(100.0, len(matched) * 15.0)
        if abstract_density > 0.12:
            score += min(25.0, abstract_density * 12.0)
        if anchor.anchor_score == 0 and len(text.strip()) >= 25:
            score += 20.0
        score = min(100.0, score)

        action = self._suggest_action(score, anchor.anchor_score)
        reasons: list[str] = []
        if matched:
            reasons.append("命中模板句式: " + "、".join(matched[:6]))
        if abstract_density > 0.12:
            reasons.append("抽象词密度偏高")
        if anchor.missing_anchor_warning:
            reasons.append(anchor.missing_anchor_warning)

        return TemplateRiskResult(
            paragraph_id=paragraph_id,
            template_risk_score=score,
            matched_patterns=matched,
            abstract_density=abstract_density,
            material_anchor_score=anchor.anchor_score,
            suggested_action=action,
            reason="；".join(reasons) if reasons else "未发现明显模板化风险",
        )

    def detect_section(self, paragraphs: list[str], domain: str | None = None) -> list[TemplateRiskResult]:
        results = [
            self.detect_paragraph(text, paragraph_id=f"p{i + 1}", domain=domain)
            for i, text in enumerate(paragraphs)
        ]
        skeletons = [self._paragraph_skeleton(text) for text in paragraphs]
        counts = Counter(s for s in skeletons if s)
        repeated = {s for s, count in counts.items() if count >= 2}

        for result, skeleton in zip(results, skeletons):
            if skeleton in repeated:
                result.template_risk_score = min(100.0, result.template_risk_score + 15.0)
                result.suggested_action = self._suggest_action(result.template_risk_score, result.material_anchor_score)
                suffix = "连续段落段首结构重复"
                result.reason = f"{result.reason}；{suffix}" if result.reason else suffix

        if self._has_even_enumeration("".join(paragraphs)):
            for result in results:
                result.template_risk_score = min(100.0, result.template_risk_score + 8.0)
                result.reason = f"{result.reason}；枚举结构过于整齐"

        return results

    @staticmethod
    def _suggest_action(score: float, anchor_score: float) -> str:
        if score >= 85 and anchor_score == 0:
            return "rebuild"
        if score >= 55:
            return "rewrite"
        if score >= 25:
            return "light_edit"
        return "keep"

    @staticmethod
    def _paragraph_skeleton(text: str) -> str:
        head = text.strip()[:28]
        if re.search(r"主要用于", head):
            return "主要用于"
        if re.search(r"(?:功能|模块)", head):
            return "功能模块开头"
        if re.search(r"^从.{0,10}(?:角度|方面)", head):
            return "从...角度"
        if head.startswith("本文"):
            return "本文开头"
        return ""

    @staticmethod
    def _has_even_enumeration(text: str) -> bool:
        return bool(re.search(r"第一.{5,80}第二.{5,80}第三.{5,80}第四", text))
