---
name: writing-for-agents
description: Write or revise instructions consumed by AI agents, including skills, AGENTS.md, CLAUDE.md, task specifications, handoffs, and runtime prompts. Use to make agent-facing documents precise, discoverable, and concise while preserving their required behavior.
license: MIT
---

# Writing For Agents

Make the intended behavior easy to discover, execute, and verify. Improve reliability before optimizing length.

## Establish the contract

Read the target document, its callers or entry points, and applicable repository guidance. Identify the intended reader, when the document enters context, the work it authorizes, and what successful execution produces. For a review request, return findings and suggested changes; for an editing request, edit the requested document and preserve unrelated work.

Before rewriting, identify requirements that must survive: required outputs, constraints, exceptions, decision ownership, and verification. Resolve contradictions from the available source of truth; ask about consequential ambiguity rather than silently changing policy.

When creating or changing an Agent Skill, read [references/skill-packaging.md](references/skill-packaging.md) for packaging and discovery guidance.

## Give instructions a clear shape

Separate actions from facts consulted while doing them. Put a rule beside the decision it governs. Order dependent actions and give consequential steps an observable completion condition: which files, cases, evidence, or outputs must be accounted for before proceeding.

Use stable terms for recurring concepts. Prefer familiar concepts that compress a real instruction, such as a reversible migration or a failing regression test. Define project-specific terms once. Broad adjectives such as “robust” need a concrete criterion when different interpretations would change the result.

State the desired action directly. Keep prohibitions where they enforce a real boundary, and pair them with the permitted path. Match detail to risk: exact steps help fragile operations; decision criteria leave room for judgment in open-ended work.

## Put detail where it is needed

Always-loaded instructions consume attention even on tasks they do not govern. Keep those entry points focused on rules that commonly apply and pointers to conditional material.

A useful pointer identifies both the material and the condition for reading it. For example: “Before changing a database schema, read `docs/migrations.md`.” Verify the path and check that a reader following the trigger can reach the required instructions.

Keep guidance used on every path in the main document. Move substantial guidance used only on a particular path into a linked reference. Split only when the new boundary makes the active task easier to follow; a small document rarely needs a routing layer.

## Prune without losing behavior

For each passage, ask what the agent would do differently if it disappeared. Remove repetition, stale advice, and explanation that has no effect on the task. Keep non-obvious constraints and lessons supported by actual failures.

Choose one authoritative location per rule. Prefer reading current configuration to maintaining a second copy of commands or settings in prose, unless the explanation supplies a convention or reason the configuration cannot express. Generalize examples so they teach the task class without baking in one machine, repository, or past run.

## Verify the revision

Compare the result with the original behavior requirements. Follow every changed local reference, check that triggers select the intended guidance, and walk a representative request through the instructions. Include an exception or boundary case when the edit changes a decision rule.

Run applicable structural validators and operational checks when executable behavior changed. Distinguish a successful format check from evidence that an agent follows the workflow well. Report what changed, the behavior preserved, and any verification limit. Keep review notes and temporary test artifacts outside the target repository unless requested.

## Inspiration

Adapted from Matt Pocock's [The /writing-for-agents Skill](https://www.aihero.dev/skills-writing-for-agents) and his [MIT-licensed skills collection](https://github.com/mattpocock/skills), particularly its guidance on discovery, conditional references, completion criteria, and pruning. The upstream license notice is retained in [LICENSE](LICENSE).
