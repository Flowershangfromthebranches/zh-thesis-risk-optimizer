# Prompt: SECOND_PASS_REWRITE_REQUIREMENT

## Purpose

Run this mode when post-rewrite AIGC self-audit still finds 3 or more AI-like risks.

## Requirements

1. Do not polish the first rewrite's surface wording.
2. Return to the original facts.
3. Rebuild paragraph structure.
4. Delete new boilerplate created in the first pass.
5. Add concrete objects already present in the source.
6. Change sentence relationships.
7. Output final version.
8. Output self-audit result.

## Output

- Why second pass was required.
- Preserved facts.
- Final rewrite.
- Final self-audit.

## Safety

No new facts, data, modules, interfaces, limitations, or references unless the user provided them.
