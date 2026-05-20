"""Management / business thesis strategy."""

from .base import BaseStrategy
from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis


class ManagementStrategy(BaseStrategy):
    """Strategy for management, business, and related fields.

    Applicable to: 工商管理, 财务管理, 市场营销, 人力资源,
    电子商务, 物流管理, 会计.
    """

    name = "management"
    label = "管理/商科策略"

    paragraph_transforms = (
        "【管理论文转换模板】\n"
        "企业场景 + 问题表现 + 数据流程 + 制度分析 + 操作方案。\n"
        "不写空泛建议，对策要落到具体部门和执行步骤。"
    )

    FORBIDDEN_PATTERNS = [
        "不要写空泛意义(如'具有重要意义'、'提升竞争力')",
        "不要用'加强、完善、提升、优化'空话堆叠",
        "不要写没有企业场景的通用管理理论",
        "不要只写'构建体系'、'提升效率'等抽象结论",
        "对策章节必须对应问题章节,不能凭空写对策",
    ]

    PRIORITY_ELEMENTS = [
        "多写企业场景和具体问题表现",
        "多写数据、流程、岗位、制度、案例",
        "对策要能落到企业操作层面",
        "问题和对策要一一对应",
        "把抽象管理建议改成具体操作方案",
    ]

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        section = unit.section

        rules = []

        if section == "introduction":
            rules.append(
                "管理论文绪论: 减少宏大背景。"
                "改成'具体行业/企业面临的问题 + 为什么选这个题目 + 现有做法不足'。"
            )
        elif section in ("requirements", "design"):
            rules.append(
                "管理论文分析章节: 必须基于企业场景。"
                "多写具体业务流程、岗位职责、现有问题表现、数据支撑。"
                "不要只写通用管理概念。"
            )
        elif section == "conclusion":
            rules.append(
                "管理论文结论: 对策必须对应前面分析的问题。"
                "每个对策要能落到具体操作层面(谁做、怎么做、用什么指标衡量)。"
                "不要用'加强管理、完善制度、提升意识'式空话。"
            )
        else:
            rules.append(
                "管理论文通用规则: "
                "多写企业场景、具体问题表现、数据、流程、岗位、制度、案例。"
                "对策要能落地,不要写抽象管理建议。"
            )

        return " ".join(rules)

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return "企业背景、业务流程、岗位职责、问卷数据、访谈对象类型、具体问题表现、对策落地方式"
