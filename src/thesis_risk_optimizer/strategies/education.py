"""Education thesis strategy."""

from .base import BaseStrategy
from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis


class EducationStrategy(BaseStrategy):
    """Strategy for education, pedagogy, and teaching-related theses.

    Applicable to: 教育学, 学前教育, 小学教育, 教学设计, 课程改革.
    """

    name = "education"
    label = "教育学策略"

    paragraph_transforms = (
        "【教育论文转换模板】\n"
        "课堂场景 + 学生表现 + 教师行为 + 教学反馈 + 改进活动。\n"
        "多写具体教学片段，不写政策套话。"
    )

    FORBIDDEN_PATTERNS = [
        "不要写政策套话",
        "不要用'培养全面发展的人才'式空泛表述",
        "不要只在理论层面讨论,不联系课堂实际",
        "不要把教学描述写成课程标准原文",
    ]

    PRIORITY_ELEMENTS = [
        "多写课堂观察记录",
        "多写学生具体表现和反馈",
        "多写教师行为和教学决策",
        "多写访谈、问卷、教学片段",
        "对策要能落到课堂操作层面",
    ]

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        section = unit.section

        rules = []

        if section in ("introduction", "literature_review"):
            rules.append(
                "教育论文绪论/文献综述: 减少政策文件堆砌。"
                "多写'实际教学中观察到的具体问题'。"
            )
        elif section in ("design", "implementation"):
            rules.append(
                "教育论文教学设计/实施: "
                "多写课堂观察、学生表现、教师行为、教学片段。"
                "描述具体教学活动、师生互动、评价方式。"
            )
        elif section == "testing":
            rules.append(
                "教育论文效果分析: "
                "多写学生前后变化的具体表现、访谈反馈、问卷数据。"
                "增加对照组或前后对比的具体描述。"
            )
        else:
            rules.append(
                "教育论文通用规则: "
                "多写课堂场景、学生反馈、教师行为、教学片段、评价方式。"
                "减少政策套话,对策要能落到课堂操作。"
            )

        return " ".join(rules)

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        return "课堂观察记录、学生反馈、教师访谈、问卷数据、教学片段、学生作品"
