# Template Residue Detector Cases

## Case 1: Real Failure Residue In Abstract

Patched text still contains:

```text
随着大数据、人工智能等数字技术的深度发展
研究发现，A 电商公司在数智化招聘方面存在四个核心问题
针对上述问题，本研究基于……提出系统性的优化对策
```

Expected:

- `residue_detected = true`
- `template_residue_detector_result = failed`
- `final_delivery_status = TEMPLATE_RESIDUE_FAILURE`
- Must not output `COMPLETED`.
- Must re-enter `CONTROLLED_HUMANIZATION_ENGINE`.

## Case 2: Theory Definition Residue

Patched text still contains:

```text
招聘是组织为获取合格人才而进行的一系列系统性活动
其本质是……
具有重要意义
```

Expected:

- `template_residue_detector_result = failed`
- Section is high-priority because it is theoretical basis.
- Required action: convert definition to "how this thesis uses the concept".

## Case 3: Management Jargon Residue

Patched text still contains:

```text
构建……体系
赋能……
闭环优化机制
成为支撑组织战略的引擎
```

Expected:

- `residue_detected = true`
- `template_residue_sections` includes the paragraph section.
- Must request concrete evidence if rewrite requires company/process/indicator details.
