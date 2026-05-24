"""Human resource management thesis strategy.

Handles: 人力资源管理, 员工招聘, 绩效考核, 薪酬激励, 员工培训,
职业发展, 离职率, 员工满意度, 组织文化, 岗位管理, 人岗匹配.

KEY DIFFERENCE from computer strategy: HR theses need enterprise scenarios,
management problems, survey processes, root cause analysis, and actionable
countermeasures — NOT function names, version numbers, or database schemas.

v14 FIX: Complete _section_guidance override, anti-template guard,
conservative mode, and HR-specific length controls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .base import BaseStrategy
from .contract import StrategyContract
from ..document_io.text_units import TextUnit, ActionType
from ..analysis.paragraph_diagnoser import DiagnosisTag, ParagraphDiagnosis


# -- HR anti-template guard ---------------------------------------------------

# Phrases that should NEVER appear in HR thesis rewrites.
# If any of these appear after rewriting, the rewrite is rejected.
HR_TEMPLATE_PHRASES: list[str] = [
    "随着经济社会的发展",
    "企业竞争日益激烈",
    "人力资源是企业最重要的资源",
    "具有重要意义",
    "提高员工积极性",
    "增强企业凝聚力",
    "完善绩效考核体系",
    "加强员工培训",
    "提高员工满意度",
    "促进企业可持续发展",
    "构建长效机制",
    "多措并举",
    "推动企业高质量发展",
    "从制度层面、管理层面、员工层面",
    "进一步完善相关机制",
    "构建体系",
    "提升效率",
    "优化流程",
    "强化能力",
    "丰富渠道",
    "数据驱动",
    "智能高效",
    "提供参考",
]

# Compiled patterns for partial matching (not just exact substring)
HR_TEMPLATE_PATTERNS: list[re.Pattern] = [
    re.compile(r"随着.{0,10}(?:经济|社会|时代).{0,10}(?:发展|进步|变化)"),
    re.compile(r"(?:企业|行业|市场).{0,6}竞争.{0,6}(?:激烈|加剧)"),
    re.compile(r"人力资源.{0,6}(?:最重要|核心|关键).{0,6}(?:资源|要素)"),
    re.compile(r"具有.{0,8}(?:重要|重大|深远).{0,6}(?:意义|价值|作用)"),
    re.compile(r"(?:进一步)?(?:完善|健全|优化).{0,6}(?:机制|体系|制度|体制)"),
    re.compile(r"(?:加强|强化|深化).{0,6}(?:培训|管理|建设|沟通)"),
    re.compile(r"(?:提高|提升|增强).{0,6}(?:满意度|积极性|凝聚力|归属感|竞争力)"),
    re.compile(r"(?:推动|促进|助力).{0,6}(?:高质量|可持续|健康).{0,4}发展"),
    re.compile(r"多措并举"),
    re.compile(r"构建长效.{0,4}机制"),
]

# Fabricated data patterns that HR rewrites must NOT introduce
HR_FABRICATION_PATTERNS: list[re.Pattern] = [
    re.compile(r"员工\s*\d+\s*(?:人|名|位)"),
    re.compile(r"(?:发放|回收|收回).{0,6}问卷\s*\d+\s*份"),
    re.compile(r"(?:离职率|流失率|满意度|有效率)\s*(?:为|达|约|：|:)\s*\d+\.?\d*\s*%"),
    re.compile(r"(?:年营业额|年产值|年收入)\s*(?:为|达|约|：|:)\s*\d+"),
    re.compile(r"(?:成立于|创立于)\s*\d{4}\s*年"),
]


@dataclass
class HRGuardResult:
    """Result of HR anti-template guard check."""
    passed: bool = True
    template_violations: list[str] = field(default_factory=list)
    fabrication_violations: list[str] = field(default_factory=list)
    failure_reason: str = ""


def check_hr_template(text: str, original_text: str = "") -> HRGuardResult:
    """Check if text contains HR template phrases that should be rejected.

    Args:
        text: The rewritten text to check.
        original_text: The original text (for fabrication comparison).

    Returns:
        HRGuardResult with pass/fail and details.
    """
    result = HRGuardResult()

    # 1. Check exact template phrases
    for phrase in HR_TEMPLATE_PHRASES:
        if phrase in text:
            result.template_violations.append(f"模板句: {phrase}")

    # 2. Check pattern-based templates
    for pattern in HR_TEMPLATE_PATTERNS:
        match = pattern.search(text)
        if match:
            result.template_violations.append(f"模板模式: {match.group()}")

    # 3. Check fabricated data (only if not in original)
    if original_text:
        for pattern in HR_FABRICATION_PATTERNS:
            new_matches = pattern.findall(text)
            orig_matches = pattern.findall(original_text)
            for m in new_matches:
                if m not in orig_matches:
                    result.fabrication_violations.append(f"疑似编造数据: {m}")

    if result.template_violations or result.fabrication_violations:
        result.passed = False
        all_violations = result.template_violations + result.fabrication_violations
        result.failure_reason = "; ".join(all_violations[:5])

    return result


# -- HR-specific paragraph length ranges --------------------------------------

# HR theses should NOT expand text — the problem is template padding, not missing detail
HR_REWRITE_LENGTH_RANGE = (0.80, 1.30)    # rewrite: 80%-130%
HR_REBUILD_LENGTH_RANGE = (0.90, 1.50)    # rebuild: 90%-150%
HR_CONSERVATIVE_LENGTH_RANGE = (0.90, 1.10)  # conservative: 90%-110% (near equal)


class HumanResourceStrategy(BaseStrategy):
    """Strategy for human resource management theses.

    MUST NOT inject computer-style details.
    MUST use enterprise scenarios, management problems, survey data, root cause analysis.

    v14 FIX: Complete section guidance override — no inheritance from base
    computer-style guidance.
    """

    name = "human_resource"
    label = "人力资源策略"

    # Whether to use conservative mode (set externally)
    conservative_mode: bool = False

    paragraph_transforms = (
        "【人力资源论文转换模板】\n"
        "删除或替换模板化表述（如'随着经济发展'、'具有重要意义'、'进一步完善'），改为平实的分析句式。\n"
        "降低'一是、二是、三是'这种呆板的枚举顺序，使用更自然的段落过渡。\n"
        "绝对不写函数名、版本号、数据库等计算机细节。\n"
        "不得编造企业人数、问卷数量、百分比、离职率、满意度等数据。\n"
        "没有企业/问卷/访谈材料时，只能基于原文已有信息保守重写，禁止新增以下实务术语：\n"
        "  - A公司具体数据、企业经营数据\n"
        "  - ROI、BEI、BES\n"
        "  - 胜任力词典、人才画像模型\n"
        "  - 招聘漏斗指标、offer接受率、招聘转化率、招聘周期\n"
        "  - 满意度百分比、离职率百分比\n"
        "不要把学生论文改成咨询报告，保留原有的学术分析视角。"
    )

    # -- Contract ---------------------------------------------------------------
    @property
    def contract(self) -> StrategyContract:
        return StrategyContract(
            discipline_name="human_resource",
            applicable_keywords=[
                "人力资源", "员工招聘", "绩效考核", "薪酬激励", "员工培训",
                "职业发展", "离职率", "员工满意度", "组织文化", "岗位管理",
                "人岗匹配", "人才", "用工", "考勤", "晋升",
            ],
            high_risk_patterns=[p for p in HR_TEMPLATE_PHRASES],
            evidence_schema={
                "企业基本情况": ["企业规模", "部门结构", "岗位类型", "员工层级", "用工特点"],
                "管理问题表现": ["绩效指标不清", "考核周期不合理", "培训内容与岗位脱节",
                         "薪酬激励单一", "晋升通道不清晰", "员工反馈渠道不足"],
                "调研过程": ["问卷维度", "访谈对象类型", "员工反馈主题", "数据统计口径",
                         "问题归纳过程"],
                "原因分析": ["制度设计原因", "执行过程原因", "沟通反馈原因", "岗位匹配原因",
                         "激励机制原因"],
                "对策落地": ["谁负责", "什么时候做", "怎么执行", "如何评价效果", "可能遇到什么阻力"],
            },
            rewrite_principles=[
                "多写企业场景和具体问题表现",
                "多写问卷维度、访谈对象、员工反馈",
                "对策要能落到企业操作层面（谁做、何时做、怎么做）",
                "问题和对策要一一对应",
                "把抽象管理建议改成具体操作方案",
                "不得编造企业数据（人数、百分比、离职率等）",
            ],
            forbidden_patterns=[
                "绝对不写函数名、代码目录、编程语言名称",
                "绝对不写版本号（包括 Python/Java/Django 等）",
                "绝对不写数据库表名、字段名、SQL 语句",
                "绝对不写 API 接口、HTTP 方法、请求响应格式",
                "绝对不写测试环境、命令行参数、Payload",
                "绝对不写软件开发、程序代码、技术架构等计算机术语堆砌",
                "不要写空泛意义（如'具有重要意义'、'提升竞争力'）",
                "不要用'加强、完善、提升、优化'空话堆叠",
                "不要只写'构建体系'、'提升效率'等抽象结论",
                "不得编造具体企业数据（人数、问卷数、离职率、满意度百分比）",
                "当没有用户补充材料时，禁止新增：A公司具体数据、ROI、BEI、BES、胜任力词典、人才画像、招聘漏斗、offer接受率等实务术语",
                "不要把学生论文改成咨询报告，不要让概念密度突然升高",
            ],
            paragraph_transforms=(
                "【人力资源论文转换模板】\n"
                "将空泛模板句删除，替换为平实的叙述。不要换成另一套高大上的模板句。\n"
                "核心任务是削减 AI 风格的过度连接词和排比，而不是注入大量不存在的专业术语。"
            ),
            validation_rules=[
                "改写后文本不得出现函数名、类名、编程语言名",
                "改写后文本不得出现版本号",
                "改写后文本不得出现数据库、API、URL 等技术架构细节",
                "改写后文本应包含具体企业部门、岗位或制度相关描述",
                "改写后文本应包含管理问题的具体表现或员工反馈",
                "改写后不得出现 HR_TEMPLATE_PHRASES 中的任何模板句",
                "改写后不得编造具体企业数据",
            ],
            fallback_behavior="conservative_rewrite",
        )

    # -- High-risk phrase patterns for ParagraphDiagnoser integration -------------
    @classmethod
    def hr_high_risk_phrases(cls) -> list[str]:
        return list(HR_TEMPLATE_PHRASES)

    # -- Section guidance: COMPLETE OVERRIDE (no computer terms) ------------------

    def _section_guidance(self, unit: TextUnit) -> str:
        """HR-specific section guidance.

        Completely overrides BaseStrategy._section_guidance.
        Contains NO computer terms (模块, 函数, 测试环境, 输入输出, 界面交互).
        """
        section = unit.section
        guidance = {
            "abstract": (
                "摘要: 研究对象 + 企业/行业背景 + 调研方式 + 发现问题 + 改进方向。"
                "禁止写'随着经济发展''具有重要意义'。"
                "不编造企业人数、问卷份数等数据。"
            ),
            "introduction": (
                "绪论: 企业用工背景 + 当前管理问题 + 选题原因。"
                "不写宏大背景（不写'随着经济社会的发展'）。"
                "写具体行业、企业面临的人力资源管理困境。"
            ),
            "literature_review": (
                "文献综述: 不要总结通用管理理论。"
                "改成'该理论在本企业/本行业的具体适用性 + 现有研究不足 + 本文切入点'。"
                "避免编造文献。"
            ),
            "requirements": (
                "现状分析: 企业规模、岗位结构、制度现状、员工反馈。"
                "不写泛泛理论。写具体管理问题表现。"
            ),
            "design": (
                "问题/原因分析: 绩效考核、薪酬激励、培训、招聘、离职率、满意度等具体问题。"
                "每个问题必须有表现和原因。"
                "原因分析: 制度设计、执行过程、沟通反馈、岗位匹配、激励机制。"
            ),
            "implementation": (
                "对策章节: 对策必须对应前文问题。"
                "写谁负责、怎么做、何时做、如何评价。"
                "禁止'加强、完善、提升、优化'空话。"
                "不写软件开发、程序实现等计算机内容。"
            ),
            "testing": (
                "效果评估: 写管理方案实施后的变化。"
                "员工满意度变化、离职率变化、绩效指标变化等。"
                "不编造具体数据。不写软件测试等计算机内容。"
            ),
            "conclusion": (
                "结论: 总结发现的问题和对策限制。"
                "写研究不足和后续改进方向。"
                "不写'推动企业高质量发展'式总结。"
                "不写空泛总结。每个结论点要有前文依据。"
            ),
        }
        return guidance.get(section, (
            "人力资源论文通用: 多写企业场景、具体问题表现、员工反馈、制度缺陷。"
            "不写函数名、版本号、数据库、API等计算机细节。"
            "不编造企业数据。"
        ))

    # -- Override base strategy methods -------------------------------------------

    FORBIDDEN_PATTERNS = [
        "不要写空泛意义(如'具有重要意义'、'提升竞争力')",
        "不要用'加强、完善、提升、优化'空话堆叠",
        "不要写没有企业场景的通用管理理论",
        "对策章节必须对应问题章节,不能凭空写对策",
        "绝对不写入函数名、代码目录、编程语言、技术架构",
        "绝对不写入版本号、数据库、API、命令行参数等计算机细节",
        "不得编造企业人数、问卷数量、百分比、离职率、满意度等具体数据",
        "禁止在无材料时新增 ROI、BEI、BES、胜任力词典、人才画像、招聘漏斗等具体术语",
        "禁止将学生论文改写为堆砌术语的咨询报告",
    ]

    PRIORITY_ELEMENTS = [
        "多写企业场景和具体问题表现",
        "多写问卷维度、访谈对象、员工反馈",
        "多写制度缺陷和管理问题根源",
        "对策要能落到企业操作层面",
        "问题和对策要一一对应",
        "没有材料时保守表达: '从论文已有描述看'、'现有材料主要反映出'",
    ]

    def _modify_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """HR-specific modification guidance."""
        if self.conservative_mode:
            return (
                "【保守修改模式】仅做等长重写。"
                "核心任务：删除模板句（如'随着经济发展'），降低 AI 句式和过度连接词。"
                "不扩写，不新增数据，不新增段落。"
                "禁止新增 ROI、BEI、人才画像等术语。保留原论文已有信息和事实。"
            )
        return (
            "【修改模式】调整句序、降低模板化、增加少量限定词,保持原意。"
            "不要同义替换。不要新增企业数据。"
        )

    def _rewrite_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """HR-specific rewrite guidance with length control."""
        if self.conservative_mode:
            return (
                "【保守重写模式】等长重写，字数控制在原文 90%-110%。"
                "只处理最高风险的模板表达，削减'具有重要意义'等空话。"
                "不新增数据。不新增 ROI、招聘转化率等无依据术语。"
                "不扩写。删除模板句后用原文信息填充，让语言更朴实。"
            )
        return (
            "【重写模式】保留主题,改变论证顺序。"
            "字数控制在原文 80%-130%，禁止空泛扩写。"
            "不是同义替换,而是重新组织内容。"
            "不得编造企业数据。"
            "没有材料时用保守表达: '从论文已有描述看'。"
        )

    def _rebuild_guidance(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        """HR-specific rebuild guidance with length control."""
        tags_str = ", ".join(t.value for t in diagnosis.tags) if diagnosis.tags else "高风险"
        if self.conservative_mode:
            return (
                f"【保守重构模式】原段落检测到: {tags_str}。"
                "等长重写，字数控制在原文 90%-110%。"
                "打破'一是、二是、三是'模板结构，改为自然过渡叙述。"
                "只删除模板句，保留原文事实。绝对不新增数据和生僻 HR 术语。"
            )
        return (
            f"【重构模式】原段落检测到: {tags_str}。"
            "按论文题目和章节功能重新生成内容。"
            "字数控制在原文 90%-150%，禁止空泛扩写。"
            "不得编造不存在的企业数据、问卷数据、访谈数据。"
            "没有企业/问卷/访谈材料时，只能保守表达。"
        )

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        section = unit.section
        rules = []

        if section in ("introduction", "abstract"):
            rules.append(
                "人力资源论文绪论/摘要: 减少宏大背景。"
                "改成'具体行业/企业面临的人力资源问题 + 为什么选这个题目 + 现有做法不足'。"
                "禁止'随着经济社会的发展'、'具有重要意义'。"
            )
        elif section == "literature_review":
            rules.append(
                "人力资源论文文献综述: 不要总结通用管理理论。"
                "改成'该理论在本企业/本行业的具体适用性 + 现有研究的不足 + 本文的研究切入点'。"
            )
        elif section in ("requirements", "design"):
            rules.append(
                "人力资源论文分析章节: 必须基于企业场景。"
                "写具体的管理问题表现（如绩效考核指标模糊、培训内容与岗位脱节）。"
                "写员工反馈和调研发现。不要只写通用管理概念。"
                "不编造企业人数、问卷份数、满意度百分比。"
            )
        elif section == "implementation":
            rules.append(
                "人力资源论文实施/对策章节: 写管理方案的落地过程。"
                "谁负责推进、什么时间节点、遇到什么阻力、如何调整。"
                "对策必须对应前文问题。禁止'加强管理、完善制度'式空话。"
                "不要写软件开发、程序实现等计算机内容。"
            )
        elif section == "testing":
            rules.append(
                "人力资源论文效果评估: 写管理方案实施后的变化。"
                "员工满意度变化、离职率变化、绩效指标变化等。"
                "不编造具体数据。不写软件测试、接口测试等计算机内容。"
            )
        elif section == "conclusion":
            rules.append(
                "人力资源论文结论: 对策必须对应前面分析的问题。"
                "每个对策要落到具体操作层面（谁做、怎么做、用什么指标衡量）。"
                "不要用'加强管理、完善制度、提升意识'式空话。"
                "指明局限和后续改进方向。"
                "不写'推动企业高质量发展'式总结。"
            )
        else:
            rules.append(
                "人力资源论文通用规则: "
                "多写企业场景、具体问题表现、员工反馈、制度缺陷、对策落地。"
                "绝对不写函数名、版本号、数据库、API等计算机细节。"
                "不编造企业数据。"
            )

        return " ".join(rules)

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        section = unit.section
        suggestions = {
            "introduction": "企业基本信息、所在行业、面临的具体人力资源管理问题",
            "literature_review": "相关理论在本行业的适用性说明",
            "requirements": "企业部门结构、岗位类型、员工层级、现有制度缺陷的具体表现",
            "design": "问卷维度、访谈对象、调研过程、问题归纳",
            "implementation": "制度设计方案、推进步骤、责任人、阻力与调整",
            "testing": "实施前后对比数据（员工满意度、离职率等）",
            "conclusion": "对策落地方式、衡量指标、后续改进计划",
        }
        return suggestions.get(section, "企业场景、员工反馈、管理制度、调研数据")

    def rebuild_section_structure(self, section: str) -> list[str]:
        """HR-specific rebuild structure with no computer defaults."""
        structures = {
            "abstract": ["案例企业/研究对象", "调研材料依据", "主要问题表现", "改进方向与限制"],
            "introduction": ["企业或行业用工背景", "具体人力资源问题", "选题来源", "研究范围与限制"],
            "literature_review": ["理论或研究对象差异", "对企业案例的适用性", "已有研究不足", "本文切入点"],
            "requirements": ["企业部门/岗位情况", "制度执行现状", "员工反馈或问卷维度", "问题边界"],
            "design": ["问题表现", "原因分析", "制度执行矛盾", "员工反馈对应关系"],
            "implementation": ["对策对应的问题", "负责部门或岗位", "执行步骤", "检查效果的方式"],
            "testing": ["评价对象", "员工反馈主题", "制度执行变化", "不能确认的限制"],
            "conclusion": ["已发现的问题", "对策落地范围", "研究限制", "后续需要补充的材料"],
        }
        return structures.get(section, ["案例企业/研究对象", "材料依据", "分析过程", "结论限制"])

    def rebuild_required_details(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> list[str]:
        """HR-specific details for rebuild planning."""
        details: list[str] = []
        section = unit.section

        if DiagnosisTag.MISSING_DETAIL in diagnosis.tags:
            if section == "implementation":
                details.extend(["企业/岗位对应问题", "制度执行步骤", "责任部门或岗位", "效果检查方式"])
            elif section in ("requirements", "design"):
                details.extend(["企业场景", "岗位或制度现状", "问卷维度/访谈对象类型", "员工反馈主题"])
            elif section == "testing":
                details.extend(["制度执行变化", "员工反馈主题", "无法确认的数据限制"])
            else:
                details.append("企业、岗位、制度、员工反馈或调研材料")

        if DiagnosisTag.ABSTRACT_ONLY in diagnosis.tags:
            details.append("抽象管理概念在案例企业中的具体表现")
        if DiagnosisTag.HOLLOW_CONCLUSION in diagnosis.tags:
            details.append("结论对应的企业材料、员工反馈和研究限制")

        if not details:
            details.append("企业实际情况、岗位制度或员工反馈中的具体材料")

        return details

    # -- HR-specific length limits ------------------------------------------------

    def get_paragraph_length_range(self, action: ActionType) -> tuple[float, float]:
        """Get HR-specific paragraph length range for the given action type.

        HR theses use tighter ranges than defaults to prevent empty expansion.
        """
        if self.conservative_mode:
            return HR_CONSERVATIVE_LENGTH_RANGE
        if action == ActionType.REWRITE:
            return HR_REWRITE_LENGTH_RANGE
        elif action == ActionType.REBUILD:
            return HR_REBUILD_LENGTH_RANGE
        return (0.90, 1.15)  # modify: tight

    # -- Conservative mode --------------------------------------------------------

    def enable_conservative_mode(self):
        """Enable conservative mode for HR strategy.

        Conservative mode:
        1. Only processes highest-risk (red) paragraphs
        2. No expansion
        3. No new data
        4. Equal-length rewrite only
        5. Delete template phrases
        6. Preserve original thesis information
        7. Focus on: abstract, introduction, problem analysis, countermeasure template expressions
        """
        self.conservative_mode = True

    def disable_conservative_mode(self):
        """Disable conservative mode."""
        self.conservative_mode = False
