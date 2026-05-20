"""Unified protection detector — single source of truth for all protection rules.

Used by DocxReader, TextUnit.is_protected, RewriteRatioPlanner, and dry-run stats.
Ensures consistent freeze decisions across all modules.

Key principle: REAL technical text has sentence-ending punctuation (。！？).
Diagram/entity/module text does NOT. Punctuation is the primary differentiator.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class FreezeReason(str, Enum):
    """Why a text unit was frozen."""

    DIAGRAM_TEXT = "diagram_text"
    ER_ENTITY_TEXT = "er_entity_text"
    DENSE_FIELD_BLOCK = "dense_field_block"
    MODULE_DIAGRAM = "module_diagram"
    FLOWCHART_TEXT = "flowchart_text"
    NORMAL = "normal"


@dataclass
class ProtectionResult:
    protected: bool
    reason: FreezeReason = FreezeReason.NORMAL
    details: str = ""


def _has_sentence_structure(text: str) -> bool:
    """Check if text has normal sentence-ending punctuation + commas.

    Real Chinese technical writing has periods (。) and commas (，).
    Diagram/entity text lacks these.
    """
    periods = text.count("。") + text.count("！") + text.count("？")
    commas = text.count("，") + text.count("；") + text.count("：")
    if periods >= 2:
        return True
    if periods >= 1 and commas >= 1:
        return True
    en_periods = text.count(".") + text.count("!") + text.count("?")
    en_commas = text.count(",") + text.count(";") + text.count(":")
    if en_periods >= 2:
        return True
    if en_periods >= 1 and en_commas >= 1:
        return True
    return False


def _is_module_diagram(text: str) -> bool:
    """Detect module/architecture diagram text."""
    if _has_sentence_structure(text):
        return False
    module_keywords = [
        "模块", "引擎", "处理器", "过滤器", "解析器", "检测器",
        "爬虫", "扫描", "提取", "解析", "请求", "响应",
        "报告", "存储", "格式化", "规范化", "过滤", "汇总",
        "并发", "线程", "队列", "缓存", "日志",
    ]
    kw_count = sum(1 for kw in module_keywords if kw in text)
    if len(text) > 60:
        head = text[:min(40, len(text)//4)]
        if text.count(head) >= 2 and kw_count >= 6:
            return True
    if kw_count >= 8:
        return True
    return False


def _is_flowchart_text(text: str) -> bool:
    """Detect flow-chart node text."""
    if _has_sentence_structure(text):
        return False
    flow_keywords = ["开始", "结束", "是否", "是", "否", "请求", "返回",
                    "解析", "判断", "输入", "输出", "初始化", "队列",
                    "链接", "提取", "页面", "URL", "域名", "达到",
                    "限制", "扫描", "爬虫", "发送", "接收"]
    kw_count = sum(1 for kw in flow_keywords if kw in text)
    if kw_count >= 4:
        return True
    return False


def _is_er_entity_text(text: str) -> bool:
    """Detect ER-diagram / entity attribute blocks."""
    if _has_sentence_structure(text):
        return False

    id_fields = len(re.findall(r"\w+_id", text))
    field_keywords = [
        "漏洞_id", "任务_id", "报告_id", "记录_id", "用户_id",
        "url地址", "漏洞url", "漏洞类型", "漏洞证据", "漏洞记录",
        "Payload", "发现时间", "严重程度", "参数名", "状态码",
        "响应大小", "爬取深度", "文件名", "文件路径", "生成时间",
        "扫描报告", "爬取记录", "扫描任务",
    ]
    field_kw_count = sum(1 for kw in field_keywords if kw in text)
    chinese_fields = len(re.findall(
        r"(?:地址|大小|深度|状态码|路径|时间|名称|编号|类型|描述|日期|数量"
        r"|漏洞|参数|证据|Payload|扫描|爬取|记录|报告)", text
    ))
    has_entity_marker = any(m in text for m in [
        "实体属性图", "实体属性", "ER图", "E-R图", "关系图",
    ])
    has_figure_caption = bool(re.search(r"图\s*\d+\.?\d*", text))
    dup_score = 0
    if len(text) > 30:
        head = text[:min(30, len(text)//3)]
        if head and text.count(head) >= 2:
            dup_score = 3

    score = 0
    if id_fields >= 2:
        score += 4
    if field_kw_count >= 3:
        score += 4
    if chinese_fields >= 6:
        score += 3
    if has_entity_marker:
        score += 4
    if has_figure_caption and field_kw_count >= 2:
        score += 2
    if dup_score:
        score += dup_score

    comma_count = len(re.findall(r"[，,;；]", text))
    if score >= 3:
        return True
    if len(text) > 80 and comma_count <= 1 and not re.search(r"[。！？!\?]", text):
        if field_kw_count >= 1 or id_fields >= 1 or chinese_fields >= 4:
            return True
    return False


def classify_protection(text: str) -> ProtectionResult:
    """Classify whether a text should be protected (frozen)."""
    if len(text) < 8:
        return ProtectionResult(protected=False)

    if _is_module_diagram(text):
        return ProtectionResult(protected=True, reason=FreezeReason.MODULE_DIAGRAM,
                               details="module names repeated without sentence structure")
    if _is_er_entity_text(text):
        return ProtectionResult(protected=True, reason=FreezeReason.ER_ENTITY_TEXT,
                               details="database fields repeated without sentence structure")
    if _is_flowchart_text(text):
        return ProtectionResult(protected=True, reason=FreezeReason.FLOWCHART_TEXT,
                               details="flow-chart keywords without sentence structure")

    return ProtectionResult(protected=False)
