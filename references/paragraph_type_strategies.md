# Paragraph Type Strategies

## Purpose

Route paragraphs by thesis section type so risk treatment matches the role of the paragraph.

## 1. Abstract

Problem: most likely to become formulaic.

Strategy:

- Do not use "随着...发展", "本文设计并实现...", or "实验结果表明..." as the main structure.
- Rebuild with: research object -> system structure -> detection flow -> test result -> scope.
- Introduce at least two concrete objects or results.

## 2. Introduction / Background

Problem: broad background padding and source similarity.

Strategy:

- Compress industry-wide background.
- Move toward why this tool needs to be lightweight, command-line-oriented, or modular.
- Avoid broad "important significance" endings.

## 3. Literature Review

Problem: stacked papers and repeated sentence patterns.

Strategy:

- Group studies by research direction.
- Explain how each group relates to the current tool.
- Preserve citation boundaries.

## 4. Technology Overview

Problem: definitions resemble textbooks.

Strategy:

- Do not write encyclopedic definitions.
- Keep only the part used by this thesis.
- Explain what the technology does in this system.

## 5. Feasibility / Requirement Analysis

Problem: often empty and generic.

Strategy:

- Technical feasibility should name libraries and modules.
- Economic feasibility should mention dependency, deployment, and runtime environment.
- Operational feasibility should mention command-line parameters and report-viewing flow.
- Functional requirements should describe input, output, and boundaries.

## 6. System Design / Implementation

Problem: usually lower AIGC risk, but can be over-abstracted by rewriting.

Strategy:

- Preserve class names, function names, parameters, and flows.
- Do not turn concrete steps into abstract capabilities.
- Use this section as a core evidence source.

## 7. Testing

Problem: real data exists, but expression can be formulaic.

Strategy:

- Preserve environment, target address, parameters, counts, and results.
- Rebuild as: test purpose -> operation -> observation point -> result explanation.
- Do not stop at "function works normally".

## 8. Conclusion

Problem: often lists generic achievements.

Strategy:

- Rewrite as: completed work -> test support -> limitation -> next step.
- Include real boundary and limitation.
- Avoid generalized value endings.

## 9. Social-Science / Management Countermeasure Paragraph

Problem: countermeasure paragraphs often sound like standard answers:

```text
完善机制 -> 优化流程 -> 加强培训 -> 健全保障 -> 提升效果
```

Strategy:

- Do not keep every measure as "第一、第二、第三".
- Start from the organization's real process node, survey result, interview feedback,制度,岗位, or indicator.
- Explain which concrete link is being adjusted.
- Delete broad value claims unless they are supported by evidence.
- If evidence is missing, request author input instead of adding theory.

## 10. Social-Science / Management Status And Problem Paragraph

Problem: status/problem paragraphs repeat "现状 -> 问题 -> 影响" without enough local evidence.

Strategy:

- Put survey or case evidence before general evaluation.
- Name the affected department, group, channel, process, or service object when provided.
- Preserve data and citation boundaries.
- Avoid abstract nouns as the main load-bearing content.

## Relation To SKILL.md

Use this file when assigning chapter and paragraph tasks in target-driven multi-pass work.
