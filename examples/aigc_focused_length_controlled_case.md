# AIGC-Focused Length-Controlled Case

> ARCHIVED_COMPATIBILITY_ONLY / internal branch, not an entry mode: legacy mode names in this file are historical compatibility labels or internal task-type references. Route through `SKILL.md` Minimal Mode Router.

## Case

《基于 Python 的 Web 漏洞扫描工具设计》

## Situation

- Original thesis: about 17000 Chinese characters.
- Latest revised version: about 24000 Chinese characters.
- Similarity reduction is strong and basically meets user expectations.
- AIGC reduction remains limited.
- User wants further AIGC reduction while controlling growth to 0-2000 Chinese characters.

## Correct Strategy

- Do not continue aggressive similarity rewrite.
- Enter AIGC-focused mode.
- Use sentence-level localization.
- Replace high-risk template sentences.
- Compress repeated AI expressions.
- Use existing evidence from the thesis:
  - Crawler.
  - Detector.
  - Reporter.
  - Helpers.
  - `requests.Session`.
  - `BeautifulSoup`.
  - `ThreadPoolExecutor`.
  - Payload.
  - Local test environment.
  - `max_depth`.
  - `max_pages`.
  - 15 crawled pages.
  - 1 SQL injection vulnerability.
  - 5 XSS vulnerabilities.
- Do not expand every section.
- Use length budget controller.

## Wrong Strategy

- Add background explanation to every paragraph.
- Add generic significance statements.
- Expand all chapters evenly.
- Use expressions such as "持续演进", "深度嵌入", "支撑", "赋能", "机制", "体系", and "价值".
- Preserve the original template sentence and append a more specific sentence after it.

## Mode Decision Example

| signal | decision |
|---|---|
| similarity is already acceptable | downgrade similarity to stability check |
| current draft grew from 17000 to 24000 | enter LENGTH_COMPRESSION_PASS |
| AIGC remains high | enter AIGC_FOCUSED_LENGTH_CONTROLLED |
| missing implementation reason | output HUMAN_EVIDENCE_REQUEST |
