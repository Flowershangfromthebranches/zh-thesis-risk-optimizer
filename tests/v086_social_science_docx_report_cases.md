# v0.8.6 Social-Science DOCX Report Cases

Use this checklist for HR, management, education, business, and other social-science theses with Word color-marked AIGC reports.

## Case 1: Color-Marked DOCX Report

Input:

```text
这是原文 DOCX 和原版 AIGC 报告 DOCX，报告用红色、橙色、紫色、黑色标记疑似度。
```

Expected:

- Load `DOCX_COLOR_REPORT_EXTRACTION` before plain-text extraction.
- Extract DOCX color metadata from font color, highlight, or shading.
- Build red/orange task table from colored runs.
- Do not treat the report as a plain duplicate of the thesis.

## Case 2: HR Thesis With Broad Red/Orange Coverage

Input:

```text
人力资源管理论文，报告中摘要、绪论、理论、现状、问题和对策大面积红橙。
```

Expected:

- Route to `SOCIAL_SCIENCE_TEMPLATE_BOTTLENECK`.
- Treat the issue as document-level template skeleton risk, not isolated sentence wording.
- Repair section skeletons and evidence placement before polishing.

## Case 3: Rhythm Already Varied But Still Red/Orange

Input:

```text
段落句长已经有变化，但报告仍然标红。
```

Expected:

- Do not keep adding short sentences.
- Switch to template-skeleton repair, abstract-noun reduction, evidence-first reconstruction, or citation-boundary handling.

## Case 4: Upstream Scan-Only Workflow Fails

Input:

```text
使用扫描诊断类 Skill 后 AIGC 反而上升。
```

Expected:

- Diagnose likely causes: color metadata not parsed, academic polish regression, template skeleton retained, evidence underused.
- Do not blame a specific upstream project.
- Recommend report-color extraction and social-science template repair.

## Case 5: Slogan-Like Burstiness

Input:

```text
改写稿把管理论文改成很多短句，例如“渠道太单一。问题很明显。”
```

Expected:

- Mark as unsuitable burstiness for formal thesis style.
- Replace with formal but less template-like expressions.
- Preserve data, citations, and academic register.
