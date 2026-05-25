"""Computer science / software engineering thesis strategy.

KEY CHANGE v1.7: No more tech-detail stuffing.
Focus on design rationale, process flow, and limitations — not version numbers,
function names, or database schema unless verified from source materials.
"""

from .base import BaseStrategy
from ..document_io.text_units import TextUnit
from ..analysis.paragraph_diagnoser import ParagraphDiagnosis, DiagnosisTag


class ComputerStrategy(BaseStrategy):
    """Strategy for computer science and software engineering theses.

    DO NOT:
    - Stuff version numbers, function names, table names without evidence
    - Turn abstract templates into longer abstract templates
    - Write encyclopedia-style technology introductions

    DO:
    - Explain WHY this module/technology is needed in THIS system
    - Describe design tradeoffs + processing flow + known limitations
    - Write test process + observations + conservative conclusions
    - Describe applicable scenarios + shortcomings + future improvements
    """

    name = "computer"
    label = "计算机/软件工程策略"
    domain_name = "computer_engineering"
    preferred_anchors = ["源码", "页面", "字段", "接口", "数据库表", "测试用例", "输入输出"]
    allowed_natural_expressions = ["源码中", "实际测试时", "当前版本", "这里"]
    banned_strong_oral = ["说白了", "搞不清", "糊弄", "太拉了", "很离谱"]
    template_phrases_to_avoid = ["具有重要意义", "提供支撑", "形成闭环", "赋能", "助力"]
    oral_threshold_profile = "computer_engineering"

    paragraph_transforms = (
        "【计算机论文转换模板】\n"
        "模块职责 + 输入输出 + 处理流程 + 异常情况。\n"
        "不写未经证实的函数名、版本号、数据库表名。"
    )

    FORBIDDEN_PATTERNS = [
        "不要做百科式技术介绍",
        "不要批量插入版本号、函数名、数据库表和命令行参数（除非材料中明确存在）",
        "不要把抽象模板改成更长的抽象模板",
        "不要把背景宏大叙事 + 技术名词 = 更长背景宏大叙事",
    ]

    PRIORITY_ELEMENTS = [
        "背景段落：改成「具体问题场景 + 本文处理范围 + 为什么只做这一范围」",
        "技术介绍：改成「该技术在本文中承担的作用 + 使用边界 + 局限」",
        "系统实现：改成「模块职责 + 输入输出 + 处理流程 + 异常情况」（不写未经证实的函数名）",
        "系统测试：改成「测试对象 + 操作过程 + 观察结果 + 未覆盖部分」",
        "结论：改成「完成了什么 + 哪些方面还不足 + 后续如何改」",
    ]

    def _section_guidance(self, unit: TextUnit) -> str:
        """Computer-science-specific section guidance.

        Contains terms like 模块关系, 数据流, 输入输出, 函数, 异常处理,
        界面交互, 测试环境, 测试用例 — which are ONLY appropriate for CS theses.
        """
        section = unit.section
        guidance = {
            "abstract": "摘要应加入具体研究对象、核心功能、测试方式、实际结论,不要只写背景+方法+结果模板",
            "introduction": "绪论应减少宏大背景,改成'具体问题+本文为什么做+当前方案不足'",
            "literature_review": "不要用'国外起步较早,国内也取得进展'模板句;调整综述逻辑,避免编造文献",
            "tech_background": "不要百科式介绍;必须写'本文中该技术具体用于哪里'",
            "requirements": "避免空话;改成具体功能、用户、场景、约束;可行性不要只写'技术成熟、成本低、操作简单'",
            "design": "重点写模块关系、数据流、输入输出;增加设计取舍",
            "implementation": "增加函数、流程、异常处理、界面交互;避免只写'实现了某模块'",
            "testing": "增加测试环境、测试步骤、测试用例、预期结果、实际结果;增加不足和人工复核",
            "conclusion": "不要只夸系统;必须写局限和后续改进;结论要和全文实际工作对应",
        }
        return guidance.get(section, "")

    def _discipline_rules(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        section = unit.section
        rules = []

        if section == "tech_background":
            rules.append(
                "不要写百科式介绍。改为：该技术在本文系统中的具体角色、为什么选它（不是因为它流行）、"
                "使用的边界和限制条件。不写具体版本号，除非论文原文已有。"
            )
        elif section == "design":
            rules.append(
                "重点写设计取舍：为什么这样划分模块、数据如何流动、有哪些替代方案被放弃及原因。"
                "不写具体数据库表名和字段名，除非原文已有。"
            )
        elif section == "implementation":
            rules.append(
                "写模块职责和输入输出，描述处理流程和异常情况处理方式。"
                "不写未经证实的函数名和类名。不写具体命令行参数。"
            )
        elif section == "testing":
            rules.append(
                "写测试对象和操作过程，报告观察到的结果。"
                "写测试的局限性——哪些场景没覆盖、为什么没覆盖。"
                "不编造测试数据（准确率、响应时间等），除非原文已有。"
            )
        elif section == "conclusion":
            rules.append(
                "总结已完成的工作，客观说明不足和后续改进方向。"
                "不要只夸系统，不要写「具有良好的实用性和稳定性」。"
            )
        else:
            rules.append(
                "通用规则：优先改变写作路径，不是单纯补技术细节。"
                "原背景套话 → 改成具体问题场景。原技术百科 → 改成技术作用和局限。"
                "不堆版本号、函数名、表名、参数值。"
            )

        return " ".join(rules)

    def evidence_suggestion(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> str:
        section = unit.section
        suggestions = {
            "implementation": "系统设计文档、核心模块的输入输出描述（不需要具体代码）",
            "testing": "测试场景列表、观察到的实际效果（不需要具体数值）",
            "design": "模块划分理由、数据流说明",
        }
        return suggestions.get(section, "论文已有内容、系统架构说明、设计理由")

    def rebuild_section_structure(self, section: str) -> list[str]:
        """Computer-specific rebuild structure."""
        structures = {
            "abstract": ["研究对象/系统", "核心功能/方法", "关键发现/测试结果", "实际结论(含局限)"],
            "introduction": ["具体问题描述", "现有方案不足", "本文解决思路", "本文范围与限制"],
            "tech_background": ["技术名称与版本", "在本系统中的角色", "为什么选它(对比替代方案)", "使用方式和配置"],
            "design": ["模块功能", "模块间关系", "数据流/输入输出", "设计取舍理由"],
            "implementation": ["开发环境与依赖", "核心实现逻辑", "关键代码/流程", "遇到的异常与处理"],
            "testing": ["测试环境", "测试步骤", "测试用例与参数", "预期vs实际结果", "不足与改进"],
            "conclusion": ["已完成工作总结", "实际效果/发现", "局限与不足", "后续改进方向"],
        }
        return structures.get(section, ["模块职责", "材料依据", "处理流程", "结论限制"])

    def rebuild_required_details(self, unit: TextUnit, diagnosis: ParagraphDiagnosis) -> list[str]:
        """Computer-specific details for rebuild planning."""
        details: list[str] = []
        section = unit.section

        if DiagnosisTag.MISSING_DETAIL in diagnosis.tags:
            if section == "implementation":
                details.extend(["开发环境版本号", "核心函数输入输出", "异常处理方式"])
            elif section == "testing":
                details.extend(["测试用例", "测试参数", "实际运行结果"])
            elif section == "design":
                details.extend(["模块接口定义", "数据流方向", "设计取舍理由"])
            else:
                details.append("具体数据/过程/案例")

        if DiagnosisTag.ABSTRACT_ONLY in diagnosis.tags:
            details.append("该概念/技术在本文系统中的具体应用方式")

        if not details:
            details.append("更具体的研究过程或实现细节")

        return details
