"""PermissionGate: checks user permissions and generates confirmation prompts.

Step 4 of the 7-step workflow.
Before execution, must verify that the user's permissions match the plan's needs.
If there's a mismatch, returns a confirmation prompt and halts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PermissionResult:
    """Result of permission checks."""

    can_proceed: bool = True
    needs_confirmation: bool = False
    confirmation_prompts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class PermissionGate:
    """Checks permission conditions and generates confirmation prompts.

    Scenarios:
    A. User disallows rewrite but system needs rewrite/rebuild.
    B. User disallows supplement but content is hollow.
    C. No AIGC report available.
    D. User allows supplement but has no materials.
    E. User allows web search.
    """

    def check(
        self,
        current_rate: float,
        target_rate: float,
        allow_rewrite: bool,
        allow_supplement: bool,
        has_report: bool,
        has_materials: bool,
        needs_rewrite: bool = False,
        needs_rebuild: bool = False,
        allow_web_search: bool = False,
        has_web_access: bool = False,
    ) -> PermissionResult:
        """Check all permission conditions.

        Args:
            current_rate: Current AIGC suspicion rate.
            target_rate: Target AIGC suspicion rate.
            allow_rewrite: Whether user allows rewriting.
            allow_supplement: Whether user allows content supplementation.
            has_report: Whether AIGC color report is available.
            has_materials: Whether thesis materials are available.
            needs_rewrite: Whether the plan requires rewrite actions.
            needs_rebuild: Whether the plan requires rebuild actions.
            allow_web_search: Whether user allows web search for materials.
            has_web_access: Whether the system has web access capability.

        Returns:
            PermissionResult with prompts that need user confirmation.
        """
        result = PermissionResult()
        gap = current_rate - target_rate

        # Situation A: User disallows rewrite but system needs it
        if not allow_rewrite and (needs_rewrite or needs_rebuild or current_rate >= 50):
            result.needs_confirmation = True
            result.confirmation_prompts.append(
                "当前 AIGC 疑似率较高，若不允许重写，只做轻度修改可能难以达到目标。"
                "是否改为允许局部重写？如果继续禁止重写，系统将只做保守修改，效果可能有限。"
            )

        # Situation B: User disallows supplement but content likely hollow
        if not allow_supplement and current_rate >= 50:
            result.needs_confirmation = True
            result.confirmation_prompts.append(
                "当前论文可能存在内容空泛、模板化表达较多的问题。"
                "如果不允许补充内容，系统只能在原文范围内调整表达，"
                "可能难以显著降低 AIGC 疑似率。是否允许基于你提供的材料进行适度补充？"
            )

        # Situation C: No AIGC report
        if not has_report:
            result.needs_confirmation = True
            result.confirmation_prompts.append(
                "未提供 AIGC 标红报告，系统无法准确定位红色/橙色高风险段落，"
                "只能根据文本特征估计风险区域，优化效果可能不稳定。是否继续？"
            )

        # Situation D: Allows supplement but no materials
        if allow_supplement and not has_materials:
            result.needs_confirmation = True
            result.confirmation_prompts.append(
                "你允许补充内容，但未提供参考文献、问卷数据、访谈记录、实验数据、"
                "项目源码、系统截图等真实材料。系统可以基于论文已有内容和模型常识进行保守补充；"
                "如允许联网，也可搜索公开资料辅助改写。"
                "但这可能带来准确性和来源风险。是否同意继续？"
            )

        # Situation E: User allows web search
        if allow_web_search:
            if has_web_access:
                result.warnings.append(
                    "已启用联网搜索辅助。搜索到的公开资料将记录来源，"
                    "不会伪造引用，不会将无来源数据写成确定事实。"
                )
            else:
                result.needs_confirmation = True
                result.confirmation_prompts.append(
                    "当前环境不支持联网搜索。只能使用用户材料和模型常识进行保守改写。"
                )

        # Large gap warning
        if gap > 30:
            result.warnings.append(
                f"目标降幅较大（{gap:.1f} 个百分点），可能需要较高比例重写和内容重构。"
                "如果不允许重写或不允许补充材料，实际效果可能无法达到目标。"
            )

        # Determine if we can proceed without confirmation
        if result.needs_confirmation:
            result.can_proceed = False

        return result
