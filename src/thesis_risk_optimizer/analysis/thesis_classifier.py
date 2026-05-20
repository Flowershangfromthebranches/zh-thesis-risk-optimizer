"""Thesis classifier: determine the academic discipline from thesis metadata.

Uses title, abstract, keywords, and chapter headings to classify
the thesis into one of the supported discipline categories.

Outputs confidence score alongside the best discipline.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Optional


class Discipline(str, Enum):
    """Supported academic disciplines."""

    COMPUTER = "computer"
    MANAGEMENT = "management"
    HUMAN_RESOURCE = "human_resource"
    EDUCATION = "education"
    LITERATURE = "literature"
    LAW = "law"
    MEDICINE = "medicine"
    UNIVERSAL = "universal"  # fallback


# -- Keyword-based classification rules ---------------------------------------
# Each keyword list is discipline-specific.
# Generic words like "系统", "数据", "模型", "分析" are excluded to avoid
# false-positives for computer discipline.

# Words that should NOT trigger computer classification (too generic)
_GENERIC_WORDS = {"系统", "数据", "模型", "分析", "管理", "开发", "平台", "应用"}

COMPUTER_KEYWORDS = [
    # Strong signals: specific tech stacks
    "Python", "Java", "Spring Boot", "Vue", "Django", "Flask",
    "React", "Node.js", "MySQL", "Redis", "MongoDB", "Docker",
    "TensorFlow", "PyTorch", "Keras",
    # Strong signals: CS-specific domains
    "系统设计", "系统实现", "系统测试", "数据库", "数据库",
    "前端", "后端", "接口", "API", "服务器", "部署",
    "爬虫", "漏洞扫描", "神经网络", "深度学习", "机器学习",
    "人工智能", "算法", "数据结构", "软件开发", "Web",
    "APP", "小程序", "管理系统", "信息管理系统",
    "计算机", "软件工程", "网络",
    # Moderate signals (count separately with lower weight)
    "编程", "代码", "程序", "微服务", "容器化",
]

MANAGEMENT_KEYWORDS = [
    "企业管理", "财务管理", "市场营销",
    "工商管理", "电子商务", "物流管理", "会计",
    "战略", "竞争力", "品牌", "消费者", "客户",
    "供应链", "库存", "营销策略", "企业文化",
    "财务报表", "成本控制", "预算", "审计",
]

HUMAN_RESOURCE_KEYWORDS = [
    "人力资源管理", "人力资源", "员工招聘", "绩效考核", "薪酬激励",
    "员工培训", "职业发展", "离职率", "员工满意度",
    "组织文化", "岗位管理", "人岗匹配",
    "薪酬", "绩效", "员工", "招聘", "培训", "离职",
    "人才", "用工", "考勤", "晋升", "入职",
]

EDUCATION_KEYWORDS = [
    "教学", "教育", "课程", "课堂", "学生", "教师",
    "学前", "小学", "中学", "高校", "大学",
    "教学设计", "课程改革", "教学模式", "学习效果",
    "班级", "教材", "教案", "考试", "评价",
    "素养", "能力培养", "翻转课堂", "混合式教学",
    "教育学", "教育管理",
]

LITERATURE_KEYWORDS = [
    "文学", "小说", "诗歌", "散文", "戏剧",
    "人物形象", "叙事", "主题", "意象", "语言风格",
    "汉语言文学", "英语语言文学", "比较文学",
    "新闻传播", "传播学", "媒介", "舆论",
    "翻译", "修辞", "文本分析",
]

LAW_KEYWORDS = [
    "法律", "法规", "法条", "司法", "立法",
    "合同", "侵权", "刑事", "民事", "行政",
    "诉讼", "仲裁", "知识产权", "公司法",
    "宪法", "刑法", "民法典", "行政法",
    "法学", "法律事务", "案例",
]

MEDICINE_KEYWORDS = [
    "护理", "临床", "患者", "病例", "诊断",
    "治疗", "手术", "药物", "药学", "药理",
    "公共卫生", "预防", "流行病", "疫苗",
    "体检", "康复", "健康教育", "慢性病",
    "护理干预", "生活质量", "依从性",
    "医学", "医药", "护士",
]


class ThesisClassifier:
    """Classify a thesis into a discipline based on its content.

    Usage:
        classifier = ThesisClassifier()
        discipline, confidence, scores = classifier.classify(
            title, abstract, keywords, headings
        )
    """

    # Minimum confidence to pick a specific discipline
    MIN_CONFIDENCE = 0.65
    # Minimum score difference to pick non-universal (absolute)
    MIN_CONFIDENCE_DELTA = 2

    def classify(
        self,
        title: str = "",
        abstract: str = "",
        keywords: str = "",
        headings: list[str] = None,
    ) -> tuple[Discipline, float, dict[str, float]]:
        """Classify thesis discipline.

        Args:
            title: Thesis title
            abstract: Abstract text
            keywords: Keywords string
            headings: List of chapter/section headings

        Returns:
            Tuple of (best_discipline, confidence, score_breakdown).
        """
        combined = f"{title} {abstract} {keywords} {' '.join(headings or [])}"
        scores = self._score_all(combined)

        best = max(scores, key=scores.get)
        best_score = scores[best]
        total_score = sum(scores.values())
        confidence = best_score / max(1.0, total_score)

        # If no strong signal, fall back to universal
        if best_score < 3:
            return Discipline.UNIVERSAL, 0.0, scores

        # If confidence too low, use universal
        if confidence < self.MIN_CONFIDENCE and best != "universal":
            return Discipline.UNIVERSAL, confidence, scores

        # If best and second-best are close, use universal
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) >= 2 and (sorted_scores[0] - sorted_scores[1]) < self.MIN_CONFIDENCE_DELTA:
            return Discipline.UNIVERSAL, confidence, scores

        return Discipline(best), confidence, scores

    def _score_all(self, text: str) -> dict[str, float]:
        """Score text against all discipline keyword sets."""
        text_lower = text.lower()
        scores = {}

        for discipline, keywords in [
            ("computer", COMPUTER_KEYWORDS),
            ("human_resource", HUMAN_RESOURCE_KEYWORDS),
            ("management", MANAGEMENT_KEYWORDS),
            ("education", EDUCATION_KEYWORDS),
            ("literature", LITERATURE_KEYWORDS),
            ("law", LAW_KEYWORDS),
            ("medicine", MEDICINE_KEYWORDS),
        ]:
            score = 0.0
            for kw in keywords:
                if kw.lower() in text_lower:
                    score += max(1.0, len(kw) / 4)
            scores[discipline] = score

        # If management keywords hit but NOT human_resource keywords,
        # management gets both scores combined
        if scores.get("human_resource", 0) > 0 and scores.get("management", 0) > 0:
            # Human resource is a subset of management; keep both separate
            pass

        scores["universal"] = 1.0  # baseline
        return scores

    @staticmethod
    def from_user_input(major: str) -> Discipline:
        """Parse user-supplied major string into a Discipline."""
        mapping = {
            "computer": Discipline.COMPUTER,
            "management": Discipline.MANAGEMENT,
            "human_resource": Discipline.HUMAN_RESOURCE,
            "hr": Discipline.HUMAN_RESOURCE,
            "human": Discipline.HUMAN_RESOURCE,
            "education": Discipline.EDUCATION,
            "literature": Discipline.LITERATURE,
            "law": Discipline.LAW,
            "medicine": Discipline.MEDICINE,
            "universal": Discipline.UNIVERSAL,
        }
        major_lower = major.strip().lower()
        if major_lower in mapping:
            return mapping[major_lower]

        # Fuzzy match
        if any(kw in major_lower for kw in ["人力资源", "人力", "hr", "人事"]):
            return Discipline.HUMAN_RESOURCE
        if any(kw in major_lower for kw in ["计算机", "软件", "程序", "系统", "web", "python", "java"]):
            return Discipline.COMPUTER
        if any(kw in major_lower for kw in ["管理", "工商", "财务", "市场", "会计", "电商"]):
            return Discipline.MANAGEMENT
        if any(kw in major_lower for kw in ["教育", "教学", "课程", "学前"]):
            return Discipline.EDUCATION
        if any(kw in major_lower for kw in ["文学", "语言", "新闻", "传播", "翻译"]):
            return Discipline.LITERATURE
        if any(kw in major_lower for kw in ["法学", "法律", "法"]):
            return Discipline.LAW
        if any(kw in major_lower for kw in ["医学", "护理", "临床", "药学", "医"]):
            return Discipline.MEDICINE

        return Discipline.UNIVERSAL
