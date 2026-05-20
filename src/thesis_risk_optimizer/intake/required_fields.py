"""Required fields definition for IntakeGate.

Lists all fields that must be provided before optimization can begin,
along with explanations for materials and their purpose.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FieldDefinition:
    """Definition of a required intake field."""

    name: str
    label: str
    required: bool = True
    description: str = ""
    example: str = ""


# -- Required fields ----------------------------------------------------------

REQUIRED_FIELDS: list[FieldDefinition] = [
    FieldDefinition(
        name="major",
        label="论文专业",
        required=True,
        description="必须由用户声明，系统不会自动猜测。",
        example="人力资源管理",
    ),
    FieldDefinition(
        name="title",
        label="论文题目",
        required=True,
        description="论文的完整题目。",
        example="数智化时代A电商公司招聘管理优化研究",
    ),
    FieldDefinition(
        name="current_rate",
        label="当前 AIGC 疑似率",
        required=True,
        description="当前检测到的 AIGC 疑似率百分比。",
        example="76.67%",
    ),
    FieldDefinition(
        name="target_rate",
        label="目标 AIGC 疑似率",
        required=True,
        description="希望降到的 AIGC 疑似率百分比。",
        example="30%",
    ),
    FieldDefinition(
        name="has_report",
        label="是否有 AIGC 标红报告",
        required=True,
        description="是否有 AIGC 检测报告（标红/标色的 DOCX 报告）。",
        example="有",
    ),
    FieldDefinition(
        name="allow_rewrite",
        label="是否允许重写",
        required=True,
        description="是否允许系统对高风险段落进行局部或整段重写。",
        example="允许局部重写",
    ),
    FieldDefinition(
        name="allow_supplement",
        label="是否允许补充内容",
        required=True,
        description="是否允许在原文基础上补充内容以降低模板化。",
        example="允许，但必须基于我提供的材料",
    ),
    FieldDefinition(
        name="has_materials",
        label="是否有写论文时用到的材料",
        required=True,
        description="是否有参考文献、问卷数据、访谈记录、实验数据等真实材料。",
        example="有，包括参考文献、问卷数据、访谈提纲、老师批注",
    ),
]


# -- Material examples --------------------------------------------------------

MATERIAL_EXAMPLES: list[str] = [
    "参考文献",
    "真实问卷数据",
    "访谈记录",
    "实验数据",
    "调研数据",
    "企业资料",
    "案例材料",
    "项目源码",
    "系统截图",
    "测试报告",
    "开题报告",
    "任务书",
    "老师批注",
    "数据表",
    "课堂观察记录",
    "法条、案例、裁判文书",
    "护理记录、实验记录等",
]

# -- Material purpose ---------------------------------------------------------

MATERIAL_PURPOSE: list[str] = [
    "支撑重写内容",
    "防止模型编造细节",
    "提升论文真实感",
    "降低模板化表达",
    "避免无依据扩写导致 AIGC 疑似率反升",
]


def format_missing_fields_prompt(missing: list[str]) -> str:
    """Format a user-facing prompt listing missing fields.

    Args:
        missing: List of missing field names.

    Returns:
        Formatted string asking user to provide the missing fields.
    """
    field_map = {f.name: f for f in REQUIRED_FIELDS}

    lines = ["当前无法开始优化，请补充以下信息：", ""]
    for name in missing:
        f = field_map.get(name)
        if f:
            lines.append(f"- 缺失项：{f.label}")
        else:
            lines.append(f"- 缺失项：{name}")

    lines.append("")
    lines.append("请按以下格式补充：")
    lines.append("")
    for f in REQUIRED_FIELDS:
        lines.append(f"{f.label}：")

    lines.append("")
    lines.append('关于"写论文时用到的材料"，可以包括：')
    for m in MATERIAL_EXAMPLES:
        lines.append(f"  - {m}")
    lines.append("")
    lines.append("这些材料的作用：")
    for p in MATERIAL_PURPOSE:
        lines.append(f"  - {p}")

    return "\n".join(lines)
