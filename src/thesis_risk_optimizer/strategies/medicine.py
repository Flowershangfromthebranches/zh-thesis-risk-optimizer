"""Medicine / nursing thesis strategy."""

from .base import BaseStrategy
from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis


class MedicineStrategy(BaseStrategy):
    """Strategy for medicine, nursing, pharmacy, and public health theses.

    Applicable to: 护理, 临床, 药学, 公共卫生.
    """

    name = "medicine"
    label = "医学/护理策略"

    paragraph_transforms = (
        "【医学/护理论文转换模板】\n"
        "操作流程 + 观察指标 + 护理风险 + 干预方式 + 注意事项。\n"
        "绝对不伪造临床数据和病例。"
    )

    FORBIDDEN_PATTERNS = [
        "绝对不要伪造临床数据",
        "绝对不要编造病例",
        "不要编造实验组/对照组数据",
        "不要写没有依据的疗效结论",
    ]

    PRIORITY_ELEMENTS = [
        "多写护理流程、观察指标、操作规范",
        "多写风险控制和注意事项",
        "基于论文已有数据进行分析和讨论",
        "无依据内容应标注需要用户提供资料",
    ]

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return (
            "医学/护理论文规则(极高安全要求): "
            "绝对不伪造临床数据和病例。"
            "多写护理流程、观察指标变化、操作规范和注意事项。"
            "对实验或数据描述必须谨慎,只基于论文已有数据讨论。"
            "如果需要补充数据才能改写某段,应明确标注'需要用户提供资料',不要编造。"
        )

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return "护理操作流程、观察指标、患者数据(脱敏)、风险控制措施、注意事项"
