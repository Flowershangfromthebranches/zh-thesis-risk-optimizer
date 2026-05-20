"""MajorRouter: routes user-declared major to the correct strategy.

Step 2 of the 7-step workflow.
User declaration has HIGHEST priority. Auto-classification is only a fallback
and MUST NOT override user declaration.

Supported routes:
1. computer_engineering — CS, SE, AI, Web, Apps
2. human_resource — HR management, recruitment, performance, compensation
3. business_management — business admin, marketing, finance, logistics
4. education — pedagogy, teaching design, curriculum
5. literature_language — Chinese/English literature, journalism
6. law_governance — law, legal affairs, social governance
7. medical_nursing — nursing, clinical, pharmacy, public health
8. universal_light — only when user explicitly selects; not for high-AIGC rewrite
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class RouteResult:
    """Result of routing a user-declared major."""

    strategy_name: str
    route_name: str
    user_declared: bool = True
    warning: str = ""


# -- Route definitions --------------------------------------------------------

MAJOR_ROUTES: dict[str, dict] = {
    "computer_engineering": {
        "strategy": "computer",
        "aliases": [
            "计算机科学与技术", "软件工程", "网络工程", "网络安全",
            "人工智能", "数据科学", "信息管理系统", "信息管理",
            "Web", "小程序", "APP", "计算机", "软件",
            "Python", "Java", "Spring Boot", "Vue", "Django", "Flask",
            "computer", "cs", "se", "ai",
        ],
    },
    "human_resource": {
        "strategy": "human_resource",
        "aliases": [
            "人力资源管理", "人力资源", "招聘管理", "绩效考核",
            "薪酬管理", "员工培训", "员工满意度", "离职率",
            "人岗匹配", "胜任力素质模型", "人事管理",
            "hr", "human_resource",
        ],
    },
    "business_management": {
        "strategy": "management",
        "aliases": [
            "工商管理", "企业管理", "市场营销", "财务管理",
            "物流管理", "电子商务", "会计", "行政管理",
            "管理学", "商科",
            "management", "business",
        ],
    },
    "education": {
        "strategy": "education",
        "aliases": [
            "教育学", "学前教育", "小学教育", "教学设计",
            "课程教学", "班级管理", "教育管理", "教育",
            "education",
        ],
    },
    "literature_language": {
        "strategy": "literature",
        "aliases": [
            "汉语言文学", "英语", "新闻传播", "文学",
            "语言学", "翻译", "传播学",
            "literature", "language",
        ],
    },
    "law_governance": {
        "strategy": "law",
        "aliases": [
            "法学", "法律事务", "社会治理", "行政法",
            "法律", "司法",
            "law",
        ],
    },
    "medical_nursing": {
        "strategy": "medicine",
        "aliases": [
            "护理", "临床", "药学", "公共卫生",
            "医学", "护理学", "医药",
            "medicine", "nursing",
        ],
    },
    "universal_light": {
        "strategy": "universal",
        "aliases": [
            "通用", "其他", "universal", "universal_light",
        ],
    },
}


class MajorRouter:
    """Routes user-declared major to the appropriate strategy.

    Rules:
    1. User declaration has highest priority.
    2. Auto-classification MUST NOT override user declaration.
    3. If user does not provide major, return missing-field error.
    4. universal_light is only available when explicitly selected.
    """

    def route(self, user_major: str) -> RouteResult:
        """Route a user-declared major to a strategy.

        Args:
            user_major: The user's declared thesis major/discipline.

        Returns:
            RouteResult with strategy name and any warnings.
        """
        if not user_major or not user_major.strip():
            return RouteResult(
                strategy_name="",
                route_name="",
                user_declared=False,
                warning='未提供论文专业，无法执行优化。请补充"论文专业"。',
            )

        major_lower = user_major.strip().lower()

        # Exact match on route names first
        if major_lower in MAJOR_ROUTES:
            route = MAJOR_ROUTES[major_lower]
            return RouteResult(
                strategy_name=route["strategy"],
                route_name=major_lower,
                user_declared=True,
            )

        # Match against aliases
        for route_name, route_def in MAJOR_ROUTES.items():
            for alias in route_def["aliases"]:
                if alias.lower() == major_lower or alias.lower() in major_lower:
                    # Check universal_light restriction
                    if route_name == "universal_light":
                        return RouteResult(
                            strategy_name=route_def["strategy"],
                            route_name=route_name,
                            user_declared=True,
                            warning="通用模式不适用于高 AIGC 论文的大规模 rewrite/rebuild。",
                        )
                    return RouteResult(
                        strategy_name=route_def["strategy"],
                        route_name=route_name,
                        user_declared=True,
                    )

        # No match found — try fuzzy keywords
        strategy = self._fuzzy_match(major_lower)
        if strategy:
            return RouteResult(
                strategy_name=strategy[0],
                route_name=strategy[1],
                user_declared=True,
            )

        # Final fallback: use universal but warn
        return RouteResult(
            strategy_name="universal",
            route_name="universal_light",
            user_declared=True,
            warning=f'未找到专业"{user_major}"对应的策略路线，已使用通用模式。'
                    '通用模式不适用于高 AIGC 论文的大规模 rewrite/rebuild。',
        )

    def _fuzzy_match(self, major_lower: str) -> Optional[tuple[str, str]]:
        """Fuzzy match against keywords."""
        keyword_map = [
            (["人力", "人事", "hr", "绩效", "薪酬", "招聘", "培训"], "human_resource", "human_resource"),
            (["计算机", "软件", "程序", "web", "python", "java", "vue", "django"], "computer", "computer_engineering"),
            (["管理", "工商", "财务", "市场", "会计", "电商", "物流", "行政"], "management", "business_management"),
            (["教育", "教学", "课程", "学前", "小学", "班级"], "education", "education"),
            (["文学", "语言", "新闻", "传播", "翻译", "英语", "汉语"], "literature", "literature_language"),
            (["法学", "法律", "法", "司法", "诉讼"], "law", "law_governance"),
            (["医学", "护理", "临床", "药学", "医", "健康"], "medicine", "medical_nursing"),
        ]
        for keywords, strategy, route in keyword_map:
            if any(kw in major_lower for kw in keywords):
                return (strategy, route)
        return None
