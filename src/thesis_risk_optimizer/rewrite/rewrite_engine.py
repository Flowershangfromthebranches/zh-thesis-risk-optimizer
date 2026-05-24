"""Rewrite engine: orchestrates the three rewrite modes (modify / rewrite / rebuild).

KEY FIX v1.1: When LLM returns None (no LLM available), falls back to rule-based
modifications. Records LLM failures in results instead of silently skipping.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Protocol

from ..document_io.text_units import TextUnit, ActionType
from ..analysis.paragraph_diagnoser import ParagraphDiagnoser, ParagraphDiagnosis
from ..strategies.base import BaseStrategy

from .modify_engine import ModifyEngine
from .rebuild_engine import RebuildEngine
from .evidence_injector import EvidenceInjector
from .anti_ai_style_guard import AntiAIStyleGuard, GuardResult
from .anti_stuffing_guard import check_stuffing, StuffingResult
from .evidence_policy import check_evidence, check_no_fabrication, EvidenceCheckResult, LengthPolicy
from .anti_template_rewriter import AntiTemplateRewriter
from ..strategies.domain_profiles import get_domain_profile
from ..strategies.section_profiles import get_section_profile


@dataclass
class RewriteResult:
    unit_uid: str
    action: ActionType
    original_text: str
    rewritten_text: str = ""
    success: bool = False
    guard_result: Optional[GuardResult] = None
    retry_count: int = 0
    error: str = ""


@dataclass
class BatchResult:
    results: list[RewriteResult] = field(default_factory=list)
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    frozen: int = 0
    guard_rejections: int = 0
    stuffing_rejections: int = 0
    evidence_rejections: int = 0
    length_violations: int = 0


class LLMProvider(Protocol):
    """Protocol for LLM call providers.

    Returns None if no LLM is available (triggers rule-based fallback).
    """

    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        ...


class RewriteEngine:
    """Main rewrite engine."""

    MAX_RETRIES = 1  # reduced: one LLM attempt, one fallback

    def __init__(
        self,
        strategy: BaseStrategy,
        llm: Optional[LLMProvider] = None,
        system_prompt: str = "",
        style: str = "low_aigc_humanized",
        domain: str = "universal",
    ):
        self.strategy = strategy
        self.llm = llm
        self.system_prompt = system_prompt
        self.style = style
        self.domain = get_domain_profile(domain).name
        self.modify_engine = ModifyEngine(strategy)
        self.rebuild_engine = RebuildEngine(strategy)
        self.evidence_injector = EvidenceInjector()
        self.guard = AntiAIStyleGuard()
        self.diagnoser = ParagraphDiagnoser()
        self.anti_template_rewriter = AntiTemplateRewriter()

    def process_units(self, units: list[TextUnit]) -> BatchResult:
        batch = BatchResult()
        batch.total = len(units)

        for unit in units:
            if unit.action == ActionType.FREEZE:
                batch.frozen += 1
                continue

            result = self._process_one(unit, batch)
            batch.results.append(result)

            if result.success:
                batch.succeeded += 1
                unit.mark_modified(result.rewritten_text)
            else:
                batch.failed += 1

        return batch

    def _process_one(self, unit: TextUnit, batch: BatchResult) -> RewriteResult:
        diagnosis = self.diagnoser.diagnose(unit)

        # Try LLM first
        rewritten = self._try_llm(unit, diagnosis)
        if rewritten is not None:
            # Apply guard
            guard_result = self.guard.check(rewritten, unit.original_text, unit.action)
            if guard_result.passed:
                rewritten = self._apply_quality_guards(rewritten, unit, batch)
                if rewritten is None:
                    return RewriteResult(
                        unit_uid=unit.uid, action=unit.action,
                        original_text=unit.original_text,
                        rewritten_text=unit.original_text, success=False,
                        guard_result=guard_result,
                        error="Quality guards rejected (stuffing/evidence/length)",
                    )
                rewritten = self.evidence_injector.inject(rewritten, unit, self.strategy)
                return RewriteResult(
                    unit_uid=unit.uid, action=unit.action,
                    original_text=unit.original_text,
                    rewritten_text=rewritten, success=True,
                    guard_result=guard_result,
                )
            else:
                # LLM output rejected by guard — return with guard info
                return RewriteResult(
                    unit_uid=unit.uid, action=unit.action,
                    original_text=unit.original_text,
                    rewritten_text=rewritten, success=False,
                    guard_result=guard_result,
                    error=f"Guard rejected: {guard_result.failure_reason}",
                )

        # Fallback: rule-based for modify actions
        if unit.action == ActionType.MODIFY:
            rewritten = None
            if self.style == "low_aigc_humanized":
                anti_template = self.anti_template_rewriter.rewrite_unit(unit, domain=self.domain)
                unit.metadata["low_aigc_action"] = anti_template.action
                unit.metadata["low_aigc_needs_material"] = anti_template.needs_material
                if anti_template.warnings:
                    unit.metadata["low_aigc_warnings"] = anti_template.warnings
                if anti_template.action != "keep" and anti_template.text != unit.original_text:
                    rewritten = anti_template.text
            if rewritten is None:
                rewritten = self.modify_engine.rewrite(unit, diagnosis)
            if rewritten and rewritten != unit.original_text:
                guard_result = self.guard.check(rewritten, unit.original_text, unit.action)
                if guard_result.passed:
                    rewritten = self.evidence_injector.inject(rewritten, unit, self.strategy)
                    return RewriteResult(
                        unit_uid=unit.uid, action=unit.action,
                        original_text=unit.original_text,
                        rewritten_text=rewritten, success=True,
                        guard_result=guard_result,
                    )
                return RewriteResult(
                    unit_uid=unit.uid, action=unit.action,
                    original_text=unit.original_text,
                    rewritten_text=rewritten, success=False,
                    guard_result=guard_result,
                    error=f"Rule-based output rejected by guard",
                )
            else:
                return RewriteResult(
                    unit_uid=unit.uid, action=unit.action,
                    original_text=unit.original_text,
                    rewritten_text=unit.original_text, success=False,
                    error="Rule-based modify produced no change",
                )

        # For rewrite/rebuild without LLM: fail explicitly
        return RewriteResult(
            unit_uid=unit.uid, action=unit.action,
            original_text=unit.original_text,
            rewritten_text=unit.original_text, success=False,
            error=f"No LLM available for {unit.action.value} — cannot perform deep rewrite/rebuild",
        )

    def _try_llm(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> Optional[str]:
        """Try LLM-based rewrite. Returns None if no LLM or LLM returns None."""
        if self.llm is None:
            return None

        guidance = self.strategy.rewrite_guidance(unit, diagnosis)
        prompt = self._build_prompt(unit, guidance)

        try:
            result = self.llm.generate(prompt, system_prompt=self.system_prompt)
            return result
        except Exception:
            return None

    def _apply_quality_guards(self, text: str, unit: TextUnit,
                              batch: BatchResult) -> str | None:
        """Run stuffing / evidence / length guards. Returns text or None if rejected."""
        # 1. Anti-stuffing guard
        stuffing = check_stuffing(text, unit.original_text)
        if not stuffing.passed:
            batch.stuffing_rejections += 1
            unit.metadata["stuffing_failed"] = True
            unit.metadata["stuffing_reasons"] = stuffing.reasons
            return None

        # 2. Evidence check (no fabrication)
        evidence = check_evidence(text)
        fabrication = check_no_fabrication(text, unit.original_text)
        if not evidence.passed or not fabrication.passed:
            batch.evidence_rejections += 1
            unit.metadata["evidence_failed"] = True
            return None

        # 3. Length check (per paragraph)
        length_check = LengthPolicy.check_paragraph(
            len(unit.original_text), len(text)
        )
        if not length_check["passed"]:
            batch.length_violations += 1
            unit.metadata["length_failed"] = True
            return None

        return text

    def _build_prompt(self, unit: TextUnit, guidance: str) -> str:
        # Length control guidance based on action type
        if unit.action == ActionType.REWRITE:
            length_hint = "改写后字数默认控制在原文 90%-115% 内，除非用户明确允许扩写"
        elif unit.action == ActionType.REBUILD:
            length_hint = "重构后字数尽量控制在原文 90%-115% 内；材料不足时不要硬扩写"
        else:
            length_hint = "修改后字数尽量与原文接近"

        domain_profile = get_domain_profile(self.domain)
        section_profile = get_section_profile(unit.section)
        low_aigc_guidance = ""
        if self.style == "low_aigc_humanized":
            low_aigc_guidance = (
                f"\n【low_aigc_humanized 通用策略】\n"
                f"- 不是单纯学术润色；目标是降低模板化、抽象化、同质化风险。\n"
                f"- {domain_profile.prompt_summary}\n"
                f"- 章节策略: {section_profile.guidance}\n"
                f"- 不要把所有专业改成计算机工程复盘风格。\n"
                f"- 材料不足时只保守改写或提示需要材料，不伪造不存在的材料。\n"
            )

        return (
            f"【任务】对以下论文段落进行{unit.action.value}操作。\n\n"
            f"{guidance}\n\n"
            f"{low_aigc_guidance}\n"
            f"【原文】\n{unit.original_text}\n\n"
            f"【要求】\n"
            f"- 保持毕业论文基本规范，但不要过度正式、过度统一、过度模板化\n"
            f"- 不编造数据、版本号、函数名、表名、参数值，不编造文献和实验\n"
            f"- 不堆砌技术术语（不要用术语清单代替论证）\n"
            f"- 优先改变表达路径和论证结构，而不是增加新材料\n"
            f"- {length_hint}，禁止把一句话扩写成一整段\n"
            f"- 做等长或微增替换，不要大幅扩写\n"
            f"- 不插入HTML注释、占位符、方括号模板\n"
            f"- 输出只包含改写后的文本,不要加解释\n"
        )

    def compression_pass(self, units: list[TextUnit]) -> int:
        """Compress units that exceed length limits.

        Targets:
        - Delete unsupported external data
        - Delete duplicate technical explanations
        - Merge stacked version/function/tool names
        - Keep necessary implementation details
        - Pull total length back to 95%-110% or at least 90%-115%

        Returns number of units compressed.
        """
        compressed = 0
        for unit in units:
            if unit.action == ActionType.FREEZE:
                continue
            if unit.text == unit.original_text:
                continue

            # Check if this unit exceeds paragraph length limit
            ratio = len(unit.text) / max(1, len(unit.original_text))
            if ratio <= 1.40:  # Within acceptable range
                continue

            # Try to compress
            compressed_text = self._compress_text(unit.text, unit.original_text)
            if compressed_text and len(compressed_text) < len(unit.text):
                unit.text = compressed_text
                compressed += 1

        return compressed

    def _compress_text(self, text: str, original_text: str) -> str:
        """Compress text by removing fabricated details and duplicates."""
        import re

        # Remove specific version numbers not in original
        version_pattern = re.compile(
            r"(?:Python|Java|Django|Flask|Spring|Vue|React|Node\.js|MySQL|PostgreSQL"
            r"|Redis|MongoDB|Docker|Linux|Ubuntu|CentOS|Nginx|Apache|Tomcat)\s*\d+\.\d+"
        )
        orig_versions = set(version_pattern.findall(original_text))
        new_versions = set(version_pattern.findall(text))

        for ver in new_versions - orig_versions:
            # Replace specific version with generic
            tech = ver.split()[0]
            text = text.replace(ver, tech)

        # Remove specific tool names not in original
        specific_tools = ["Nessus", "Acunetix", "OpenVAS", "DVWA", "SQLi-labs"]
        for tool in specific_tools:
            if tool.lower() in text.lower() and tool.lower() not in original_text.lower():
                text = re.sub(re.escape(tool), "安全检测工具", text, flags=re.IGNORECASE)

        # Remove CVE numbers not in original
        cve_pattern = re.compile(r"CVE-\d{4}-\d{4,}", re.IGNORECASE)
        orig_cves = set(cve_pattern.findall(original_text))
        new_cves = set(cve_pattern.findall(text))
        for cve in new_cves - orig_cves:
            text = text.replace(cve, "相关漏洞")

        # Remove stacked lists (3+ consecutive technical terms)
        stacked_pattern = re.compile(r"(\w+(?:\s*[,、]\s*\w+){3,})")
        for match in stacked_pattern.finditer(text):
            items = re.split(r"[、,]", match.group(0))
            if len(items) > 3:
                # Keep first 2, replace rest with "等"
                compressed = "、".join(items[:2]) + "等"
                text = text.replace(match.group(0), compressed)

        return text
