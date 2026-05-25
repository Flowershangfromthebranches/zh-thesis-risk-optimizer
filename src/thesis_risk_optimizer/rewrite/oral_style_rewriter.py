"""Recover over-oral expressions into thesis-appropriate wording."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..validation.oral_style_guard import (
    STRONG_ORAL_REPLACEMENTS,
    OralStyleGuard,
    OralStyleResult,
)


TEMPLATE_REGRESSION_PHRASES: tuple[str, ...] = (
    "具有重要意义", "提供支撑", "提供有力支撑", "完善机制", "优化路径",
    "提升水平", "促进发展", "形成闭环", "赋能", "助力", "不断推进",
    "进一步加强",
)


@dataclass(frozen=True)
class OralRewriteItem:
    original: str
    replacement: str
    section: str
    reason: str = "过度口语化表达回收"


@dataclass(frozen=True)
class OralRewriteResult:
    text: str
    replacements: list[OralRewriteItem] = field(default_factory=list)
    guard_result: OralStyleResult | None = None


class OralStyleRewriter:
    """Replace strong oral expressions without converting them into templates."""

    def __init__(self):
        self.guard = OralStyleGuard()

    def rewrite(self, text: str, section: str = "body", domain: str | None = None) -> OralRewriteResult:
        result = self.guard.check(text, section=section, domain=domain)
        rewritten = text
        replacements: list[OralRewriteItem] = []

        for term, replacement in result.suggested_replacements.items():
            if term not in rewritten:
                continue
            safe_replacement = self._avoid_template_regression(replacement)
            rewritten = rewritten.replace(term, safe_replacement)
            replacements.append(
                OralRewriteItem(
                    original=term,
                    replacement=safe_replacement,
                    section=section or "body",
                )
            )

        rewritten = self._tidy(rewritten)
        return OralRewriteResult(
            text=rewritten,
            replacements=replacements,
            guard_result=self.guard.check(rewritten, section=section, domain=domain),
        )

    @staticmethod
    def _avoid_template_regression(replacement: str) -> str:
        for phrase in TEMPLATE_REGRESSION_PHRASES:
            replacement = replacement.replace(phrase, "结合具体材料说明")
        return replacement

    @staticmethod
    def _tidy(text: str) -> str:
        return (
            text.replace("，，", "，")
            .replace("，。", "。")
            .replace("。。", "。")
            .strip()
        )
