"""Final report generator: produce the optimization report after processing.

KEY FIX v1.1: Honest reporting — never outputs "success" when:
- processed_count == 0
- AIGC report parse failed
- No LLM was used for rewrite/rebuild

KEY FIX v2.0: Risk delta evaluation — never outputs "success" when:
- risk_chars increased
- red_chars increased
- purple_chars increased
- length exceeds hard_range
- drop mainly from denominator expansion
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ..document_io.text_units import TextUnit, ActionType, RiskLevel
from ..analysis.rewrite_ratio_planner import RatioPlan
from ..rewrite.rewrite_engine import BatchResult
from ..rewrite.anti_ai_style_guard import GuardResult
from ..rewrite.evidence_injector import get_evidence_report_items
from ..validation.structure_validator import StructureReport
from ..validation.length_validator import LengthReport
from ..document_io.format_preserver import FROZEN_UNIT_TYPES
from ..validation.risk_delta_evaluator import RiskDeltaResult
from ..rewrite.denominator_dilution_guard import DilutionResult


@dataclass
class ReportContext:
    """Additional context for honest reporting."""
    no_llm: bool = False
    report_parse_failed: bool = False
    processed_zero: bool = False
    aigc_rate: Optional[float] = None
    post_aigc_rate: Optional[float] = None
    has_report: bool = False
    classification_confidence: Optional[float] = None
    strategy_misuse_risk: bool = False
    rollback_recommended: bool = False
    # v14: Strategy selection tracking
    detected_discipline: str = ""
    selected_strategy: str = ""
    user_forced_major: bool = False


@dataclass
class FinalReport:
    input_file: str = ""
    output_file: str = ""
    has_aigc_report: bool = False
    aigc_rate: Optional[float] = None
    detected_discipline: str = ""
    classification_confidence: float = 0.0
    strategy_misuse_risk: bool = False
    recommend_user_specify: bool = False
    strategy_mode: str = ""
    selected_strategy: str = ""
    user_forced_major: bool = False
    ratio_plan: Optional[RatioPlan] = None
    total_units: int = 0
    body_units: int = 0
    high_risk_count: int = 0
    processed_count: int = 0
    frozen_count: int = 0
    focused_sections: list[str] = field(default_factory=list)
    guard_triggered: bool = False
    guard_details: list[str] = field(default_factory=list)
    original_chars: int = 0
    modified_chars: int = 0
    length_compressed: bool = False
    length_delta_pct: float = 0.0
    length_band: str = ""
    length_in_ideal: bool = False
    length_in_acceptable: bool = False
    length_triggered_hard: bool = False
    length_change_reasons: list[str] = field(default_factory=list)
    structure_passed: bool = True
    format_passed: bool = True
    frozen_items: list[str] = field(default_factory=list)
    remaining_high_risk: list[str] = field(default_factory=list)
    remaining_risk_reasons: list[str] = field(default_factory=list)
    suggested_materials: list[str] = field(default_factory=list)

    # Honest reporting flags
    honest_warnings: list[str] = field(default_factory=list)

    # Risk delta evaluation (v2.0)
    risk_delta_result: Optional[RiskDeltaResult] = None
    dilution_result: Optional[DilutionResult] = None

    def to_markdown(self) -> str:
        lines = []
        lines.append("# 论文优化处理报告")
        lines.append(f"\n生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Derive boolean flags based on honest_warnings or risk_delta_result
        is_failed = False
        is_rollback = False
        for w in self.honest_warnings:
            if "本轮优化失败" in w or "反升" in w or "效果未验证" in w:
                is_failed = True
            if "建议回滚" in w:
                is_rollback = True

        if self.risk_delta_result and self.risk_delta_result.verdict == "failed":
            is_failed = True
            is_rollback = True

        # 1. 是否达到目标
        lines.append("## 1. 是否达到目标")
        if not self.has_aigc_report:
            lines.append("- 未知 (无 AIGC 报告，无法判断是否达到降重目标)")
        elif is_failed:
            lines.append("- 否 ❌")
        else:
            lines.append("- 是 ✅ (或有部分改善)")
        lines.append("")

        # 2. 是否反升
        lines.append("## 2. 是否反升")
        if self.risk_delta_result:
            increased = any("上升至" in w for w in self.honest_warnings)
            if increased:
                lines.append(f"- 是 ❌ (AIGC 疑似率反升)")
            else:
                lines.append(f"- 否 ✅")
        elif any("上升至" in w for w in self.honest_warnings):
            lines.append("- 是 ❌ (AIGC 疑似率反升)")
        elif not self.has_aigc_report:
            lines.append("- 未知 (尚未验证检测结果)")
        else:
            lines.append("- 未知")
        lines.append("")

        # 3. 是否建议使用
        lines.append("## 3. 是否建议使用")
        if is_rollback or is_failed:
            lines.append("- 不建议 ❌ (效果不佳或反升)")
        else:
            if not self.has_aigc_report:
                lines.append("- 未知 (已生成候选版本，请自行判断)")
            else:
                lines.append("- 建议使用 ✅")
        lines.append("")

        # 4. 是否建议回滚
        lines.append("## 4. 是否建议回滚")
        if is_rollback or is_failed:
            lines.append("- 强烈建议回滚 ⚠️ (请恢复至优化前的原文)")
        else:
            lines.append("- 暂无需回滚")
        lines.append("")

        # 5. 本轮处理了什么
        lines.append("## 5. 本轮处理了什么")
        lines.append(f"- 输入文件: {self.input_file}")
        lines.append(f"- 输出文件: {self.output_file}")
        lines.append(f"- 专业路线: {self.detected_discipline}")
        lines.append(f"- 置信度 classification_confidence: {self.classification_confidence:.2f}")
        lines.append(f"- 策略误用风险: {'是' if self.strategy_misuse_risk else '否'}")
        lines.append(f"- 处理策略: {self.strategy_mode}")
        lines.append(f"- 处理总段落数: {self.processed_count}")
        if self.ratio_plan:
            d = self.ratio_plan.to_dict()["assigned"]
            lines.append(f"- 具体动作: 修改({d['modify']}) / 重写({d['rewrite']}) / 重构({d['rebuild']}) / 冻结({d['freeze']})")
        if self.focused_sections:
            lines.append(f"- 重点章节: {', '.join(self.focused_sections)}")
        lines.append("")

        # 6. 字数变化
        lines.append("## 6. 字数变化")
        lines.append(f"- 原文字数: {self.original_chars}")
        lines.append(f"- 优化后字数: {self.modified_chars}")
        lines.append(f"- 变化比例: {self.length_delta_pct:.1%}")
        lines.append(f"- ideal_range: 95%-110%")
        lines.append(f"- acceptable_range: 90%-115%")
        lines.append(f"- hard_range: 85%-120%")
        if self.length_band:
            lines.append(f"- 当前区间: {self.length_band}")
        if self.length_change_reasons:
            lines.append(f"- 字数变化原因: {'; '.join(self.length_change_reasons)}")
        elif self.modified_chars != self.original_chars:
            direction = "字数增长" if self.modified_chars > self.original_chars else "字数压缩"
            lines.append(f"- 字数变化原因: {direction}，需结合段落处理记录人工复核")
        else:
            lines.append("- 字数变化原因: 字数基本不变")
        lines.append("")

        # 7. 诚实告警
        if self.honest_warnings or self.remaining_risk_reasons:
            lines.append("## 7. 诚实告警")
            for warning in self.honest_warnings:
                lines.append(f"- {warning}")
            for reason in self.remaining_risk_reasons:
                lines.append(f"- 剩余风险: {reason}")
            lines.append("")

        if self.suggested_materials:
            lines.append("## 8. 建议补充材料")
            for item in self.suggested_materials:
                lines.append(f"- {item}")
            lines.append("")


        lines.append("---")
        lines.append("*zh-thesis-risk-optimizer v2.0 — 不承诺检测结果,不伪造数据*")
        return "\n".join(lines)


class FinalReportGenerator:
    def generate(
        self,
        input_path, output_path, units, discipline, strategy_label,
        ratio_plan, batch_result, aigc_rate, has_report,
        structure_report=None, length_report=None, guard_results=None,
        context: Optional[ReportContext] = None,
        risk_delta_result: Optional[RiskDeltaResult] = None,
        dilution_result: Optional[DilutionResult] = None,
    ) -> FinalReport:
        report = FinalReport()
        report.input_file = str(Path(input_path).name)
        report.output_file = str(Path(output_path).name)
        report.has_aigc_report = has_report
        report.aigc_rate = aigc_rate
        report.detected_discipline = discipline
        report.strategy_mode = strategy_label
        report.ratio_plan = ratio_plan

        # Populate discipline context from ReportContext if available
        ctx = context or ReportContext()
        report.classification_confidence = ctx.classification_confidence or 0.0
        report.strategy_misuse_risk = ctx.strategy_misuse_risk
        report.selected_strategy = ctx.selected_strategy
        report.user_forced_major = ctx.user_forced_major
        report.recommend_user_specify = (
            ctx.classification_confidence is not None and ctx.classification_confidence < 0.65
        )

        body_units = [u for u in units if u.is_body]
        report.total_units = len(units)
        report.body_units = len(body_units)
        report.high_risk_count = sum(1 for u in units if u.risk_level == RiskLevel.HIGH)

        processed = [r for r in batch_result.results if r.success]
        report.processed_count = len(processed)
        report.frozen_count = batch_result.frozen

        focused = {u.section for u in units if u.action != ActionType.FREEZE and u.section}
        report.focused_sections = sorted(focused)

        report.original_chars = sum(len(u.original_text) for u in units)
        report.modified_chars = sum(len(u.text) for u in units)
        report.length_compressed = report.modified_chars < report.original_chars

        # Populate length analysis from LengthReport if available
        if length_report:
            report.length_delta_pct = length_report.delta_pct
            report.length_band = length_report.band
            report.length_in_ideal = length_report.in_ideal_range
            report.length_in_acceptable = length_report.in_acceptable_range
            report.length_triggered_hard = length_report.triggered_hard_range
            report.length_change_reasons = length_report.reasons
        elif report.original_chars > 0:
            report.length_delta_pct = (report.modified_chars - report.original_chars) / report.original_chars

        if guard_results:
            failures = [g for g in guard_results if not g.passed]
            report.guard_triggered = len(failures) > 0
            for g in failures:
                report.guard_details.append(g.failure_reason)

        if structure_report:
            report.structure_passed = structure_report.passed

        report.frozen_items = [t.value for t in FROZEN_UNIT_TYPES]

        remaining = [u for u in units if u.risk_level == RiskLevel.HIGH and u.action == ActionType.FREEZE]
        if remaining:
            report.remaining_risk_reasons.append(
                f"{len(remaining)} 个高风险段落因受保护或证据不足未处理"
            )

        # Evidence needs
        evidence_items = get_evidence_report_items(units)
        if evidence_items:
            report.suggested_materials = evidence_items

        # Risk delta evaluation (v2.0)
        report.risk_delta_result = risk_delta_result
        report.dilution_result = dilution_result

        # Add risk delta warnings to honest_warnings if failed
        if risk_delta_result and risk_delta_result.verdict == "failed":
            report.honest_warnings.append(
                "本轮优化失败 — 风险字符未减少或字数失控。"
            )
            for reason in risk_delta_result.failure_reasons:
                report.honest_warnings.append(f"  - {reason}")

        if dilution_result and dilution_result.triggered:
            report.honest_warnings.append(dilution_result.warning_message)

        # ⚠️ HONEST WARNINGS
        # ctx already initialized above

        # Track assigned vs processed
        assigned_total = 0
        if ratio_plan:
            assigned_total = ratio_plan.total_assigned

        processed_ratio = report.processed_count / max(1, assigned_total)
        failed_count = batch_result.failed if batch_result else 0

        if ctx.no_llm and assigned_total > 0:
            report.honest_warnings.append(
                "未接入 LLM — rewrite/rebuild 任务未能完成，"
                "当前结果不能视为有效降 AIGC 版本。"
                "请使用 --llm-provider openai --model gpt-4o 等参数接入 LLM。"
            )

        if ctx.processed_zero:
            report.honest_warnings.append(
                "未实际处理正文 — 输出不可视为优化结果。"
                "请接入 LLM 或检查 AIGC 报告是否正确。"
            )

        if assigned_total > 0 and processed_ratio < 0.5:
            report.honest_warnings.append(
                f"实际处理比例不足 ({report.processed_count}/{assigned_total} = {processed_ratio:.0%})，"
                "仍存在较高 AIGC 风险。"
            )

        if failed_count > 0:
            report.honest_warnings.append(
                f"{failed_count} 个段落处理失败 (rewrite/rebuild 无 LLM 时全部失败是预期行为)。"
            )

        if ctx.report_parse_failed:
            report.honest_warnings.append(
                "AIGC 标红报告未成功映射到正文段落。请运行 "
                "'thesis-optimize inspect-report --input <报告.docx>' 检查颜色统计。"
            )

        # -- Failure diagnosis (v2.0 — bidirectional) --
        length_ratio = report.modified_chars / max(1, report.original_chars)
        if length_ratio > 1.20:
            report.honest_warnings.append(
                f"本轮优化存在过度扩写风险 (字数增长 {length_ratio:.0%})，"
                "可能引入新的 AIGC 高风险内容。"
            )
        elif length_ratio > 1.15:
            report.honest_warnings.append(
                f"字数增长 {length_ratio:.0%}，超过推荐上限 15%。"
            )
        elif length_ratio < 0.85:
            report.honest_warnings.append(
                f"总字数压缩至 {length_ratio:.0%}，低于硬下限 85%，本轮优化失败。"
            )
        elif length_ratio < 0.90:
            report.honest_warnings.append(
                f"总字数压缩至 {length_ratio:.0%}，处于硬下限区间 (85%-90%)，建议人工复查。"
            )

        # Stuffing / evidence violations
        if batch_result:
            if getattr(batch_result, 'stuffing_rejections', 0) > 0:
                report.honest_warnings.append(
                    f"{batch_result.stuffing_rejections} 段因技术术语堆砌被拒绝，"
                    "存在改写质量不足的风险。"
                )
            if getattr(batch_result, 'evidence_rejections', 0) > 0:
                report.honest_warnings.append(
                    f"{batch_result.evidence_rejections} 段因缺乏证据被拒绝，"
                    "以下内容需要用户确认或提供材料，否则不建议保留。"
                )
            if getattr(batch_result, 'length_violations', 0) > 0:
                report.honest_warnings.append(
                    f"{batch_result.length_violations} 段因字数增长超标被拒绝。"
                )

        # AIGC drop diagnosis
        if ctx.aigc_rate is not None and ctx.post_aigc_rate is not None:
            drop = ctx.aigc_rate - ctx.post_aigc_rate
            if drop < 10:
                report.honest_warnings.append(
                    f"本轮优化未达到预期 (AIGC 下降仅 {drop:.1f} 个百分点)，"
                    "不建议作为最终版本。"
                )

        # Only mark risk as "low" if ALL conditions are met:
        all_ok = (
            processed_ratio >= 0.8
            and not ctx.no_llm
            and failed_count == 0
            and not ctx.report_parse_failed
            and 0.85 <= length_ratio <= 1.20
            and getattr(batch_result, 'stuffing_rejections', 0) == 0
            and getattr(batch_result, 'evidence_rejections', 0) == 0
        )
        if not all_ok and not report.remaining_risk_reasons:
            report.remaining_risk_reasons.append(
                "由于以上警告，当前版本仍存在较高 AIGC 风险，不应视为最终优化结果。"
            )

        return report

    def save(self, report: FinalReport, path) -> Path:
        path = Path(path)
        path.write_text(report.to_markdown(), encoding="utf-8")
        return path
