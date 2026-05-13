# Web Scanner Targeted Multipass Case

## Case

《基于 Python 的 Web 漏洞扫描工具设计》

## Metrics

- Original: AIGC 59.83%, Similarity 19%.
- v0.5: AIGC 68.3%, Similarity 11%.
- v0.4 best: AIGC 43.62%.
- User target: Similarity <10%, AIGC <20%.

The target is a user optimization goal, not a guaranteed detection result.

## Diagnosis

- v0.5 similarity improved but AIGC regressed.
- v0.4 is only a partial historical reference, not a success standard.
- Main issue: template structure, formalization regression, and insufficient evidence density.

## Available Evidence

- Crawler.
- Detector.
- Reporter.
- Helpers.
- `requests.Session`.
- `BeautifulSoup`.
- `ThreadPoolExecutor`.
- Payload.
- SQL injection.
- Reflected XSS.
- HTML report.
- Local test environment: `http://127.0.0.1:5001`.
- `max_depth = 2`.
- `max_pages = 30`.
- 15 crawled pages.
- 1 SQL injection vulnerability.
- 5 XSS vulnerabilities.
- 10/10 successful tests for crawler, SQL injection, XSS, and report generation.

## Recommended Treatment

- Abstract: reconstruct with system evidence.
- Introduction: cut macro background and link quickly to this tool.
- Technology overview: remove encyclopedia definitions.
- Feasibility: convert generic feasibility into dependency, environment, and parameter-based feasibility.
- Implementation: preserve concrete objects.
- Testing: use test data as core evidence.
- Conclusion: include limitations and next work.

## Example Next Task

| section | paragraph_id | failure_reason | rewrite_mode | required_evidence | next_action |
|---|---|---|---|---|---|
| Abstract | A-01 | formalization regression | AIGC_REGRESSION_GUARD | module names, test results | rebuild with object-flow-result-scope |
| Testing | T-03 | evidence dilution | CONTENT_SUBSTANCE_INJECTION | target URL, counts, result values | keep exact data and explain limits |
