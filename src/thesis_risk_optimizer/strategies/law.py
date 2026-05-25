"""Law thesis strategy."""

from .base import BaseStrategy
from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis


class LawStrategy(BaseStrategy):
    """Strategy for law and legal studies theses.

    Applicable to: 法学, 法律事务, 社会治理, 行政管理中的法规问题.
    """

    name = "law"
    label = "法学策略"
    domain_name = "law"
    preferred_anchors = ["法条", "案例事实", "争议焦点", "裁判逻辑", "权利义务关系", "法律适用条件", "责任承担"]
    allowed_natural_expressions = ["在该案中", "争议集中在", "从规范适用看"]
    banned_strong_oral = ["说白了", "对不上", "搞不清", "没人管", "很离谱", "说不过去"]
    template_phrases_to_avoid = ["具有重要法治价值", "法治意义重大", "具有重要意义", "促进法治建设"]
    oral_threshold_profile = "law"

    paragraph_transforms = (
        "【法学论文转换模板】\n"
        "法律关系 + 争议焦点 + 规范依据 + 适用边界 + 风险提示。\n"
        "不伪造法条和案例。"
    )

    FORBIDDEN_PATTERNS = [
        "不要伪造法条(条号、款号、内容)",
        "不要编造案例事实",
        "不要做没有依据的价值判断",
        "不要用'显然'、'毫无疑问'代替论证",
    ]

    PRIORITY_ELEMENTS = [
        "多写法律条文的具体适用",
        "多写案例情境和争议焦点",
        "多写适用条件和限制",
        "写出推理逻辑链",
    ]

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return (
            "法学论文规则: "
            "多写法律条文、案例情境、争议焦点、适用条件和限制。"
            "写出完整的法律推理链条,避免没有依据的价值判断。"
            "不得伪造法条条号和内容,不得编造案例事实。"
            "如果有不确定的法条或案例,应标注需要用户提供资料。"
        )

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return "法律条文原文、案例事实、争议焦点、裁判逻辑、适用边界"
