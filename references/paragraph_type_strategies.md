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

## Relation To SKILL.md

Use this file when assigning chapter and paragraph tasks in target-driven multi-pass work.
