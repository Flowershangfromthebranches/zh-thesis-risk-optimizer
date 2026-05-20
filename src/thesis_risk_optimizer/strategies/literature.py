"""Literature / humanities thesis strategy."""

from .base import BaseStrategy
from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis


class LiteratureStrategy(BaseStrategy):
    """Strategy for literature, language, and journalism theses.

    Applicable to: 汉语言文学, 英语, 新闻传播, 文学作品分析.
    """

    name = "literature"
    label = "文学/人文策略"

    paragraph_transforms = (
        "【文学/人文论文转换模板】\n"
        "文本细节 + 人物行为 + 叙事方式 + 语言特征 + 个人分析。\n"
        "不写空泛主题拔高和AI式总结。"
    )

    FORBIDDEN_PATTERNS = [
        "不要做AI式总结(如'综上所述,该作品深刻反映了...')",
        "不要写空泛主题拔高(如'具有深刻的社会意义')",
        "不要只写他人观点,缺少自己的分析",
        "不要编造文本引用",
    ]

    PRIORITY_ELEMENTS = [
        "多写文本细读和具体分析",
        "多写具体章节、人物、叙事手法",
        "保留个人判断和分析路径",
        "用原文片段支撑论点",
    ]

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return (
            "文学/人文论文规则: "
            "多写文本细读、具体章节分析、人物行为、叙事视角、意象、语言风格。"
            "避免空泛主题拔高和AI式总结。"
            "保留个人判断,写出分析路径(从文本细节到结论的推理过程)。"
            "不编造文本引用,所有引用必须来自原文。"
        )

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return "原作文本片段、人物行为举例、章节结构分析、语言风格观察"
