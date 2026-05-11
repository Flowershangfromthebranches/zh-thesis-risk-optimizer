# AI Writing Pattern Library

This library helps diagnose AIGC-style risk in Chinese academic writing. It is a diagnostic aid, not a promise about any external detector.

## Pattern 1: Theory-First Opening

Risk signal: a paragraph starts from a broad theory, concept, or policy phrase before connecting to the actual research object.

Repair:

- Move the thesis object or problem to the front.
- Keep the theory only where it explains a concrete analytical choice.
- Replace abstract claims with paper-specific scope.

## Pattern 2: Mechanical Three-Part Structure

Risk signal: paragraph order repeatedly follows "background -> method -> significance" or "problem -> solution -> value".

Repair:

- Start from data, contradiction, observation, or boundary condition.
- Merge short template sections if they repeat the same function.
- Use varied paragraph lengths.

## Pattern 3: Passive Analysis Formula

Risk signal: frequent empty analysis verbs such as "体现", "表明", "说明", "反映", without explaining mechanism.

Repair:

- State the mechanism directly.
- Add evidence, condition, or exception if already present in the source material.
- Delete the analysis sentence if it only repeats the previous sentence.

## Pattern 4: Template Problem Statement

Risk signal: the paragraph says the problem is "complex", "important", or "urgent" but does not name the thesis-specific object, constraint, data, or scenario.

Repair:

- Add the specific object under study.
- Connect the problem to a method, dataset, system module, or research question.
- Avoid adding unsupported facts.

## Pattern 5: Highly Symmetric Sentences

Risk signal: several clauses have the same length, grammar, and connector pattern.

Repair:

- Collapse repeated clauses.
- Change one clause into a condition, example, limitation, or consequence.
- Keep at most two similar parallel units before changing structure.

## Pattern 6: Vague Attribution

Risk signal: "有研究认为", "专家指出", "学界普遍认为" appears without source boundaries.

Repair:

- Preserve or request a citation.
- If no citation is provided, mark "建议补充来源".
- Do not turn the claim into the author's own conclusion.

## Pattern 7: Generalized Ending

Risk signal: a paragraph ends with broad value claims that could fit many papers.

Repair:

- Replace with a concrete implication for this paper.
- End with limitation, next analytical step, or evidence-based result.
- Delete the ending if it adds no new information.

## Pattern 8: High-Frequency AI-Like Expressions

Risk signal: high density of abstract evaluation and universal transitions.

Common categories:

- Empty emphasis: "需要指出的是", "值得注意的是".
- Broad value: "具有重要意义", "提供有力支撑".
- Generic connection: "由此可见", "综上".
- Universal mechanism: "共同作用", "形成体系".

Repair:

- Delete empty prompts.
- Replace broad value with evidence.
- Use local transitions based on the paragraph's real logic.

## Pattern 9: Over-Clean Prose

Risk signal: all sentences are similarly polished, similarly long, and similarly balanced.

Repair:

- Let some sentences be shorter.
- Keep discipline-appropriate variation.
- Avoid inserting deliberate errors or nonstandard symbols.

## Pattern 10: Report-Like Uniformity

Risk signal: every paragraph has the same layout: definition, expansion, summary.

Repair:

- Match paragraph structure to chapter function.
- Use observation-first structure for experiments.
- Use constraint-first structure for system design.
- Use source-comparison structure for literature review.
