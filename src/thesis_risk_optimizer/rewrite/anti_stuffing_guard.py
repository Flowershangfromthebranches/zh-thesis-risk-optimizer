"""Anti-stuffing guard — prevents "technical detail stuffing" in rewritten text.

Detects when a rewrite just packs more technical terms into the paragraph
without actually improving the argument structure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class StuffingResult:
    """Result of anti-stuffing check."""
    passed: bool = True
    reasons: list[str] = field(default_factory=list)
    stuffing_score: int = 0  # 0-10, higher = more stuffed


TECH_TERMS = [
    "Python", "Java", "Spring", "Boot", "Vue", "React", "Django", "Flask",
    "MySQL", "PostgreSQL", "Redis", "MongoDB", "Docker", "Kubernetes",
    "Nginx", "Apache", "Tomcat", "Linux", "Ubuntu", "CentOS",
    "SQL", "XSS", "CSRF", "API", "HTTP", "HTTPS", "JSON", "XML", "HTML", "CSS",
    "REST", "RPC", "MVC", "ORM", "JWT", "OAuth", "SSL", "TLS",
    "requests", "BeautifulSoup", "lxml", "scrapy", "selenium",
    "numpy", "pandas", "matplotlib", "tensorflow", "pytorch",
    "ThreadPoolExecutor", "Session", "User-Agent", "Payload",
    "注入", "扫描", "爬虫", "检测", "模块", "引擎", "过滤器",
    "并发", "线程", "队列", "缓存", "代理",
]


def check_stuffing(new_text: str, original_text: str) -> StuffingResult:
    """Check if rewrite is just tech-term stuffing.

    Returns StuffingResult with score and reasons.
    """
    result = StuffingResult()

    # Count tech terms
    new_terms = sum(1 for t in TECH_TERMS if t in new_text)
    orig_terms = sum(1 for t in TECH_TERMS if t in original_text)
    term_growth = new_terms - orig_terms

    # Stuffing signals:
    signals = 0

    # 1. Dense consecutive tech terms (4+ in 100 chars)
    dense_count = 0
    for t in TECH_TERMS:
        dense_count += new_text.count(t)
    if len(new_text) > 0:
        density = dense_count / (len(new_text) / 100)  # terms per 100 chars
        if density > 4:
            result.reasons.append(f"技术术语密度过高 ({density:.1f}/100字)")
            signals += 3

    # 2. Many new tech terms added but argument unchanged
    if term_growth >= 5:
        result.reasons.append(f"新增 {term_growth} 个技术术语，但论证结构未改变")
        signals += 2

    # 3. Looks like a tech checklist (many 名词+名词 combinations)
    checklist_pattern = re.findall(r"\w{2,}(?:模块|引擎|器|层|池|队列|栈|表|库|系统|服务|接口)", new_text)
    if len(checklist_pattern) >= 5:
        result.reasons.append(f"检测到技术清单模式 ({len(checklist_pattern)} 个模块/组件名)")
        signals += 2

    # 4. Paragraph grew > 150% with mostly new tech terms
    orig_len = max(1, len(original_text))
    new_len = len(new_text)
    if new_len / orig_len > 1.5 and term_growth >= 4:
        result.reasons.append(f"字数增长 {new_len/orig_len:.0%} 且主要增加技术术语")
        signals += 2

    # 5. No improvement in sentence structure variation
    orig_sentences = len(re.findall(r"[。！？]", original_text))
    new_sentences = len(re.findall(r"[。！？]", new_text))
    if new_sentences <= orig_sentences + 1 and term_growth >= 3:
        result.reasons.append("技术术语增加但句数未显著变化（可能是堆砌而非重写）")
        signals += 1

    result.stuffing_score = min(10, signals)
    if signals >= 3:
        result.passed = False

    return result
