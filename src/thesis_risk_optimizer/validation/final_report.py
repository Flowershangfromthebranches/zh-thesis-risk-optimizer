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
from ..analysis.template_risk_detector import TemplateRiskDetector
from ..analysis.material_anchor_detector import MaterialAnchorDetector
from ..rewrite.anchor_first_policy import AnchorFirstPolicy
from ..validation.oral_style_guard import OralStyleGuard


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
    domain_profile_name: str = ""
    domain_profile_evidence: list[str] = field(default_factory=list)
    domain_user_specified: bool = False


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
    domain_profile_name: str = ""
    domain_profile_evidence: list[str] = field(default_factory=list)
    domain_user_specified: bool = False
    template_phrase_counts: dict[str, int] = field(default_factory=dict)
    template_high_risk_count: int = 0
    template_action_counts: dict[str, int] = field(default_factory=dict)
    material_anchors_by_section: dict[str, list[str]] = field(default_factory=dict)
    abstract_material_shortages: list[str] = field(default_factory=list)
    over_polish_warnings: list[str] = field(default_factory=list)
    oral_style_summary: dict[str, object] = field(default_factory=dict)
    oral_rewrite_log: list[dict[str, str]] = field(default_factory=list)
    anchor_first_summary: dict[str, object] = field(default_factory=dict)
    domain_integrity_check: dict[str, object] = field(default_factory=dict)

    @staticmethod
    def _format_counts(counts: dict[str, int]) -> str:
        if not counts:
            return "无"
        return "、".join(f"{key}({value})" for key, value in list(counts.items())[:12])

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

        # 6. Domain profile
        lines.append("## 6. domain profile 判断结果")
        lines.append(f"- 使用的专业画像: {self.domain_profile_name or self.detected_discipline or 'universal'}")
        lines.append(f"- 判断方式: {'用户指定 --domain' if self.domain_user_specified else 'auto / 专业路由辅助判断'}")
        if self.domain_profile_evidence:
            lines.append(f"- 识别依据: {', '.join(self.domain_profile_evidence[:12])}")
        else:
            lines.append("- 识别依据: 未获得明显专业锚点，按通用规则保守处理")
        lines.append("")

        # 7. Template risk
        lines.append("## 7. 模板化风险报告")
        lines.append(f"- 高频模板短语: {self._format_counts(self.template_phrase_counts)}")
        lines.append(f"- 高风险段落数量: {self.template_high_risk_count}")
        lines.append(f"- 处理方式统计: {self._format_counts(self.template_action_counts)}")
        lines.append("")

        # 8. Material anchors
        lines.append("## 8. 材料锚点报告")
        if self.material_anchors_by_section:
            for section, anchors in self.material_anchors_by_section.items():
                lines.append(f"- {section or '未分节'}: {', '.join(anchors)}")
        else:
            lines.append("- 暂未识别到稳定的专业材料锚点")
        if self.abstract_material_shortages:
            lines.append(f"- 过于抽象或材料不足段落: {len(self.abstract_material_shortages)}")
            for item in self.abstract_material_shortages[:8]:
                lines.append(f"  - {item}")
            lines.append("- 存在材料不足时，无法安全补充不存在的数据、访谈、案例、实验或源码功能")
        else:
            lines.append("- 未发现必须提示的材料不足段落")
        lines.append("")

        # 9. Oral style guard
        lines.append("## 9. oral_style_summary")
        if self.oral_style_summary:
            lines.append(f"- 总句数: {self.oral_style_summary.get('total_sentences', 0)}")
            lines.append(f"- mild_oral 数量: {self.oral_style_summary.get('mild_oral_count', 0)}")
            lines.append(f"- strong_oral 数量: {self.oral_style_summary.get('strong_oral_count', 0)}")
            lines.append(f"- 每 10 句口语化密度: {self.oral_style_summary.get('mild_per_10', 0)}")
            lines.append(f"- 是否通过阈值: {self.oral_style_summary.get('status', 'unknown')}")
        else:
            lines.append("- 暂无口语化统计")
        lines.append("")

        lines.append("## 10. oral_rewrite_log")
        if self.oral_rewrite_log:
            for item in self.oral_rewrite_log[:20]:
                lines.append(
                    f"- {item.get('section', '未分节')}: "
                    f"{item.get('original', '')} -> {item.get('replacement', '')} "
                    f"({item.get('reason', '')})"
                )
        else:
            lines.append("- 未触发过度口语表达回收")
        lines.append("")

        lines.append("## 11. anchor_first_summary")
        if self.anchor_first_summary:
            anchors = self.anchor_first_summary.get("used_anchors", [])
            missing = self.anchor_first_summary.get("missing_anchor_sections", [])
            lines.append(f"- 使用了哪些专业锚点: {', '.join(anchors) if anchors else '无'}")
            lines.append(f"- 哪些章节缺少锚点: {', '.join(missing) if missing else '无'}")
            lines.append(
                f"- 是否存在用口语化替代材料的风险: "
                f"{'是' if self.anchor_first_summary.get('oralization_without_anchor_risk') else '否'}"
            )
        else:
            lines.append("- 暂无 anchor-first 统计")
        lines.append("")

        lines.append("## 12. domain_integrity_check")
        if self.domain_integrity_check:
            pollution = self.domain_integrity_check.get("cross_domain_pollution", [])
            lines.append(f"- 是否出现跨专业污染: {'是' if pollution else '否'}")
            if pollution:
                lines.append(f"- 不属于本专业的锚点: {', '.join(pollution)}")
            lines.append(
                f"- 是否保留了本专业核心材料: "
                f"{'是' if self.domain_integrity_check.get('kept_domain_anchors') else '否'}"
            )
        else:
            lines.append("- 暂无专业完整性检查结果")
        lines.append("")

        # 13. Over-polish warning
        lines.append("## 13. 过度润色警告")
        if self.over_polish_warnings:
            for warning in self.over_polish_warnings:
                lines.append(f"- {warning}")
        else:
            lines.append("- 未发现提供支撑、具有重要意义、提升效率、形成闭环、主要用于、便于等表达的明显堆积")
        lines.append("")

        # 14. Uncertainty
        lines.append("## 14. 不确定性说明")
        lines.append("- 不承诺任何检测器一定降低。")
        lines.append("- 本次主要处理模板化、抽象化、同质化风险，并保留毕业论文基本规范。")
        lines.append("- 材料不足时只提示需要补充，不伪造数据、文献、访谈、问卷、实验、案例或功能。")
        lines.append("")

        # 15. 字数变化
        lines.append("## 15. 字数变化")
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
        report.domain_profile_name = ctx.domain_profile_name or discipline or "universal"
        report.domain_profile_evidence = list(ctx.domain_profile_evidence or [])
        report.domain_user_specified = ctx.domain_user_specified
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

        self._populate_humanized_risk_report(report, units, report.domain_profile_name)
        self._populate_oral_anchor_report(report, units, report.domain_profile_name)

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

    def _populate_humanized_risk_report(self, report: FinalReport, units: list[TextUnit], domain: str) -> None:
        detector = TemplateRiskDetector()
        anchor_detector = MaterialAnchorDetector()
        body_units = [u for u in units if u.is_body]

        phrase_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        high_count = 0
        shortages: list[str] = []
        anchors_by_section: dict[str, set[str]] = {}
        over_polish_terms = ["提供支撑", "具有重要意义", "提升效率", "形成闭环", "主要用于", "便于"]
        over_polish_counts = {term: 0 for term in over_polish_terms}

        for unit in body_units:
            risk = detector.detect_paragraph(unit.text, paragraph_id=unit.uid, domain=domain)
            if risk.template_risk_score >= 55:
                high_count += 1
            action_counts[risk.suggested_action] = action_counts.get(risk.suggested_action, 0) + 1
            for pattern in risk.matched_patterns:
                phrase_counts[pattern] = phrase_counts.get(pattern, 0) + 1

            anchor = anchor_detector.detect(unit.text, domain)
            if anchor.anchor_terms:
                section = unit.section or "未分节"
                anchors_by_section.setdefault(section, set()).update(anchor.anchor_terms)
            if anchor.missing_anchor_warning and risk.template_risk_score >= 45:
                shortages.append(f"{unit.uid} / {unit.section or '未分节'}: {anchor.missing_anchor_warning}")

            for term in over_polish_terms:
                over_polish_counts[term] += unit.text.count(term)

        report.template_phrase_counts = dict(sorted(phrase_counts.items(), key=lambda item: item[1], reverse=True))
        report.template_action_counts = dict(sorted(action_counts.items(), key=lambda item: item[0]))
        report.template_high_risk_count = high_count
        report.material_anchors_by_section = {
            section: sorted(anchors)
            for section, anchors in sorted(anchors_by_section.items())
        }
        report.abstract_material_shortages = shortages
        report.over_polish_warnings = [
            f"{term} 出现 {count} 次，建议人工复查是否过度规范化"
            for term, count in over_polish_counts.items()
            if count >= 2
        ]

    def _populate_oral_anchor_report(self, report: FinalReport, units: list[TextUnit], domain: str) -> None:
        guard = OralStyleGuard()
        policy = AnchorFirstPolicy()
        body_units = [u for u in units if u.is_body]
        body_text = "".join(u.text for u in body_units)
        oral = guard.check(body_text, section="body", domain=domain)

        report.oral_style_summary = {
            "total_sentences": oral.total_sentences,
            "mild_oral_count": oral.mild_oral_count,
            "strong_oral_count": oral.strong_oral_count,
            "mild_per_10": round((oral.mild_oral_count / max(1, oral.total_sentences)) * 10, 2),
            "status": oral.status,
        }

        rewrite_log: list[dict[str, str]] = []
        used_anchors: set[str] = set()
        missing_sections: set[str] = set()
        oralization_without_anchor_risk = False

        for unit in body_units:
            for item in unit.metadata.get("oral_rewrite_log", []):
                rewrite_log.append({
                    "original": str(item.get("original", "")),
                    "replacement": str(item.get("replacement", "")),
                    "section": str(item.get("section", unit.section or "未分节")),
                    "reason": str(item.get("reason", "过度口语化表达回收")),
                })

            anchor_result = policy.evaluate(unit.text, domain, section=unit.section)
            used_anchors.update(anchor_result.anchor_terms)
            if anchor_result.missing_anchor_warning:
                missing_sections.add(unit.section or "未分节")
                unit_oral = guard.check(unit.text, section=unit.section, domain=domain)
                if unit_oral.mild_oral_count or unit_oral.strong_oral_count:
                    oralization_without_anchor_risk = True

        report.oral_rewrite_log = rewrite_log
        report.anchor_first_summary = {
            "used_anchors": sorted(used_anchors),
            "missing_anchor_sections": sorted(missing_sections),
            "oralization_without_anchor_risk": oralization_without_anchor_risk,
        }

        computer_terms = ["源码", "接口", "字段", "数据库", "数据表", "版本号", "API"]
        original_text = "".join(u.original_text for u in body_units)
        cross_pollution: list[str] = []
        if domain not in {"computer_engineering", "engineering_general"}:
            cross_pollution = [
                term for term in computer_terms
                if term in body_text and term not in original_text
            ]

        report.domain_integrity_check = {
            "cross_domain_pollution": cross_pollution,
            "kept_domain_anchors": bool(used_anchors),
            "domain": domain,
        }

        if oral.status == "fail":
            report.honest_warnings.append(
                "口语化限流检查未通过，输出中仍有过度口语化或轻微口语密度超阈值。"
            )
        if oralization_without_anchor_risk:
            report.honest_warnings.append(
                "部分缺少材料锚点的段落存在口语化替代材料的风险，建议补充真实材料。"
            )
