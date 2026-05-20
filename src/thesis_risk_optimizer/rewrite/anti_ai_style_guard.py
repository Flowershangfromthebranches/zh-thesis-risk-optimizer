"""Anti-AI style guard: validate rewritten text does not introduce AI-like patterns.

This is the final quality gate for rewritten text. It checks that the output:
1. Does not contain forbidden template patterns
2. Is not overly abstract or smooth
3. Is not just a synonym-replaced version of the input
4. Has meaningful structural change (for rewrite/rebuild actions)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..document_io.text_units import ActionType


@dataclass
class GuardResult:
    """Result of an anti-AI style guard check."""

    passed: bool = True
    failure_reason: str = ""
    warnings: list[str] = field(default_factory=list)
    triggered_rules: list[str] = field(default_factory=list)


class AntiAIStyleGuard:
    """Validates that rewritten text avoids AI-like writing patterns.

    Checks for four categories of problems:
    1. Overly templated (随着...发展, 具有重要意义, etc.)
    2. Overly abstract (提升效率, 优化体验, etc.)
    3. Overly smooth (every sentence perfect, no variation)
    4. Overly formal (student thesis → policy report)
    5. Invalid rewrite (just synonym replacement, no new info)
    """

    # -- Category 1: Forbidden template patterns ------------------------------
    FORBIDDEN_TEMPLATES = [
        re.compile(r"随着.{1,20}(?:发展|进步|提高|深入|完善)"),
        re.compile(r"在(?:新|当前|信息|大数据|互联网|人工智能).{0,10}(?:时代|背景|环境)下"),
        re.compile(r"具有(?:(?:十分|非常|极其)?重要的)?(?:现实|理论|实践)?意义"),
        re.compile(r"本文首先.{1,30}其次.{1,30}最后"),
        re.compile(r"实验结果表明.{0,20}(?:具有|有着|表现).{0,10}(?:良好|优秀|较高)"),
        re.compile(r"为.{1,20}提供(?:了)?(?:参考|借鉴|依据)"),
        re.compile(r"具有(?:良好的|较高的)(?:可行性|实用性|稳定性|可靠性)"),
    ]

    # -- Category 2: Overly abstract patterns ---------------------------------
    ABSTRACT_PATTERNS = [
        re.compile(r"提升整体效率"),
        re.compile(r"优化用户体验"),
        re.compile(r"推动高质量发展"),
        re.compile(r"形成完整体系"),
        re.compile(r"构建长效机制"),
        re.compile(r"有效(?:提升|提高|增强|改善|促进)了"),
        re.compile(r"实现了.{0,10}(?:高效|智能|自动)化"),
    ]

    # -- Category 3: Overly smooth indicators ---------------------------------
    SMOOTH_INDICATORS = [
        # Every paragraph ends with a perfect summary sentence
        re.compile(r"^综上所述[,，]"),
        re.compile(r"^总而言之[,，]"),
    ]

    # -- Category 4: Over-formalization patterns ------------------------------
    OVER_FORMAL_PATTERNS = [
        re.compile(r"贯彻落实.{1,20}(?:方针|政策|精神|要求)"),
        re.compile(r"以.{1,20}为(?:指导|核心|导向|目标|抓手)"),
    ]

    def check(
        self,
        new_text: str,
        original_text: str,
        action: ActionType,
    ) -> GuardResult:
        """Check rewritten text for AI-like patterns.

        Args:
            new_text: The rewritten output.
            original_text: The original text before rewriting.
            action: The action type (modify/rewrite/rebuild).

        Returns:
            GuardResult with pass/fail and details.
        """
        result = GuardResult()

        # 1. Check forbidden templates
        self._check_templates(new_text, result)

        # 2. Check abstract patterns
        self._check_abstract(new_text, result)

        # 3. Check over-smoothness
        self._check_smooth(new_text, result)

        # 4. Check over-formalization
        self._check_over_formal(new_text, original_text, result)

        # 5. Check for ineffective rewrite (for rewrite/rebuild actions)
        if action in (ActionType.REWRITE, ActionType.REBUILD):
            self._check_effective_change(new_text, original_text, result)

        result.passed = len(result.triggered_rules) == 0
        if not result.passed:
            result.failure_reason = "; ".join(result.triggered_rules)

        return result

    def _check_templates(self, text: str, result: GuardResult) -> None:
        """Check for forbidden template patterns."""
        for i, pattern in enumerate(self.FORBIDDEN_TEMPLATES):
            if pattern.search(text):
                rule = f"模板句式#{i + 1}: {pattern.pattern[:40]}..."
                result.triggered_rules.append(rule)

    def _check_abstract(self, text: str, result: GuardResult) -> None:
        """Check for overly abstract phrases."""
        for i, pattern in enumerate(self.ABSTRACT_PATTERNS):
            if pattern.search(text):
                rule = f"过度抽象#{i + 1}: {pattern.pattern[:40]}..."
                result.triggered_rules.append(rule)

    def _check_smooth(self, text: str, result: GuardResult) -> None:
        """Check for overly smooth writing."""
        for pattern in self.SMOOTH_INDICATORS:
            if pattern.search(text):
                result.warnings.append("文本可能过于顺滑,建议增加转折和限制")
                # Warnings don't cause rejection, but are noted

    def _check_over_formal(
        self, new_text: str, original_text: str, result: GuardResult
    ) -> None:
        """Check if the text has been over-formalized compared to original."""
        for i, pattern in enumerate(self.OVER_FORMAL_PATTERNS):
            if pattern.search(new_text) and not pattern.search(original_text):
                rule = f"过度正式化#{i + 1}: 新增了政策套话式表达"
                result.triggered_rules.append(rule)

    def _check_effective_change(
        self, new_text: str, original_text: str, result: GuardResult
    ) -> None:
        """Check that the rewrite actually changed the content meaningfully.

        A rewrite that only does synonym replacement is not acceptable.
        """
        # 1. Check if texts are too similar (high overlap)
        similarity = self._text_similarity(new_text, original_text)
        if similarity > 0.85:
            result.triggered_rules.append(
                f"无效改写: 与原文字符相似度 {similarity:.0%}, 可能是同义替换"
            )
            return

        # 2. Check if new text is shorter (rewrite shouldn't compress)
        if len(new_text) < len(original_text) * 0.9:
            result.triggered_rules.append(
                f"字数压缩: 新文本({len(new_text)}字)比原文({len(original_text)}字)少"
            )
            return

        # 3. Check if sentence count is identical (suggests 1:1 replacement)
        orig_sentences = len(re.findall(r"[。！？]", original_text))
        new_sentences = len(re.findall(r"[。！？]", new_text))
        if orig_sentences == new_sentences and similarity > 0.7:
            result.warnings.append("句数相同且高度相似,可能未充分改写")

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        """Compute a simple character-level similarity ratio."""
        if not a or not b:
            return 0.0

        # Use set-based Jaccard similarity on character bigrams
        def bigrams(s):
            return {s[i:i+2] for i in range(len(s) - 1)}

        ba = bigrams(a)
        bb = bigrams(b)
        if not ba or not bb:
            return 0.0

        intersection = len(ba & bb)
        union = len(ba | bb)
        return intersection / union if union > 0 else 0.0
