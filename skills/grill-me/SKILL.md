---
name: grill-me
description: Pressure-test an idea, plan, design, or decision through questions that uncover assumptions, resolve tradeoffs, and clarify success. Use when the user asks to be grilled, interviewed, challenged, or helped to think an idea through before committing.
license: MIT
---

# Grill Me

Turn an uncertain idea into choices the user can explain and defend. Be a constructive skeptic: make the strongest plausible objection, investigate the answer, and revise your view when the evidence changes.

## Start with the decision

Use the idea and context already supplied. If the subject is missing, ask what the user wants to work through. Establish the intended outcome, who it serves, the scope, and the constraints before asking about details that depend on them. A rough idea is enough to begin.

Keep this a conversation. By default, keep decisions in chat; saving documents, creating tickets, or implementing an idea requires a request for that work. Existing authorization still applies when the user has already asked for those outcomes.

## Ask in rounds

Track the decisions and their dependencies in the conversation. Each round should contain the unresolved questions that can be answered with what is known now. Hold dependent questions for a later round. Split a large round into manageable groups; follow a user's preference for one question at a time.

For each question:

- Name the choice and explain the consequence that makes it matter.
- Offer concrete alternatives when useful. Give a recommendation with its reason, or say what evidence is missing when recommending would be premature.
- Make clear what an affirmative answer would accept. Treat silence or an unanswered question as unresolved.

Wait for answers before advancing to dependent decisions. After each round, briefly capture what changed and pursue contradictions, weak assumptions, and newly exposed choices. Carry forward settled answers unless new information undermines them.

## Challenge the important assumptions

Select questions that could change the decision. Depending on the subject, probe the user's evidence of need, alternatives already tried, success measures, failure cases, cost, ownership, reversibility, and what would make them abandon the idea. Use concrete scenarios to test whether two answers can both hold.

Distinguish preferences from facts. Look up accessible facts in supplied documents, repository files, or authoritative sources when they bear on a choice. Ask the user for private context or judgments that those sources cannot supply. Keep assumptions labeled until verified.

If the user says they do not know, identify a useful way to learn. Some decisions need a mockup, experiment, customer conversation, or measurement. State the smallest test and which answer it would inform; pause that branch instead of repeatedly rephrasing the same question. Build or run the test only within the user's authorized scope.

## Know when to finish

Continue while an unresolved choice could materially change the scoped outcome. If the subject grows too broad, identify separable decisions and focus the next round on the one that matters first.

Close when the material choices are settled, remaining uncertainty has an explicit test or owner, or the user asks to stop. Summarize the chosen direction, reasons and tradeoffs, open questions, and the next useful action. Preserve uncertainty; a productive session can end with a decision to gather evidence. Check any material ambiguity before dependent work, while continuing work the user has already authorized.

## Inspiration

Adapted from Matt Pocock's [The /grill-me Skill](https://www.aihero.dev/skills-grill-me) and the interview workflow in his [MIT-licensed skills collection](https://github.com/mattpocock/skills). This version packages the workflow directly for Codex and Cursor without requiring companion skills. The upstream license notice is retained in [LICENSE](LICENSE).
