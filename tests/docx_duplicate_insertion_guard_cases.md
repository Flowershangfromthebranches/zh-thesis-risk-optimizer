# DOCX Duplicate Insertion Guard Test Cases

## Case 1: Real Failure — Section 5.2 Repeated Insertion

**Background:** In older version bff6860, the paragraph "工具优化的目标是让系统从记录工具变成决策辅助……" in Section 5.2 was inserted into multiple locations, causing the document to grow from ~30 pages to ~45+ pages.

**Input:**
- Original paragraph matches 3 locations in document.xml.
- Revised text is ready for writeback.

**Expected:**
- DUPLICATE_MATCH_WARNING = true (3 candidate_locations found).
- Writeback stops immediately.
- DUPLICATE_INSERTION_RISK = true (if any writeback was attempted before detection).
- final_delivery_status = FORMAT_FAILURE.

## Case 2: Single Match — Safe Writeback

**Input:**
- Original paragraph matches exactly 1 location in document.xml.
- Confidence = HIGH.

**Expected:**
- Writeback proceeds.
- Post-writeback n-gram check: no 100+ char segment repeats more than twice.
- DUPLICATE_INSERTION_RISK = NONE.
- final_delivery_status = not affected by this guard.

## Case 3: Page Count Explosion

**Input:**
- Original DOCX: 30 pages.
- After patching: 42 pages (+40%).

**Expected:**
- FORMAT_REGRESSION_RISK = DETECTED.
- final_delivery_status = FORMAT_FAILURE.
- File not delivered as completed.

## Case 4: Page Count Normal

**Input:**
- Original DOCX: 30 pages.
- After patching: 31 pages (+3.3%).

**Expected:**
- FORMAT_REGRESSION_RISK = NONE.
- Page count change within acceptable range.

## Case 5: N-Gram Repeat Detection

**Input:**
- After patching, paragraph at index 87 contains "工具优化的目标是让系统从记录工具变成决策辅助，通过数据整合和智能分析为管理层提供决策依据。"
- The same 100+ character text also appears at paragraph indices 142, 203, and 267.

**Expected:**
- N-gram check detects 4 occurrences of the same 100+ char segment.
- DUPLICATE_INSERTION_RISK = DETECTED.
- final_delivery_status = FORMAT_FAILURE.

## Case 6: Multiple Replacement IDs — Each Unique Location

**Input:**
- replacement_id 1 targets paragraph 42 → writeback OK.
- replacement_id 2 targets paragraph 87 → writeback OK.
- replacement_id 3 targets paragraph 103 → writeback OK.

**Expected:**
- All three writebacks succeed.
- No duplicate detection triggered.
- Each replacement_id has exactly one confirmed target location.
