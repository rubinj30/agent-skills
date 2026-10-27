# Agent Skills

A personal collection of reusable Agent Skills for Codex, with the same `SKILL.md` packages usable in Cursor and other compatible coding agents.

## Skills

### [Create Audio Podcast](skills/create-audio-podcast/SKILL.md)

- Turn documents, webpages, research, or code changes into a podcast for listening on the go.
- Write a conversation between a female and male co-host who share the lead, ask follow-ups, and explore examples and tradeoffs.
- Guide natural phrasing, varied turn lengths, and voice delivery; audition a short pilot when changing voices or delivery.
- Generate distinct OpenAI voices, a transcript, and an iPhone-friendly M4A recording and player.
- Keep claims grounded in the source and check the audio bundle before delivery.
- Use with: `$create-audio-podcast Turn this report into a podcast I can listen to on my iPhone.`

### [Improve Codebase Architecture](skills/improve-codebase-architecture/SKILL.md)

- Review code, tests, and commit history to find recurring architectural friction.
- Identify scattered logic, complicated interfaces, tangled dependencies, and weak test coverage.
- Rank a small set of refactoring opportunities with evidence, tradeoffs, and a top recommendation.
- Help design and implement a selected change when requested, using reversible steps and behavior checks.
- Use with: `$improve-codebase-architecture Find the most valuable architecture improvement in this repository.`

### [Create Explainer](skills/create-explainer/SKILL.md)

- Make complex topics, systems, research, or AI outputs easier to understand.
- Choose clear writing, diagrams, interactive HTML, or narrated video according to the learning task and available tools.
- Use simplified technical language, concrete examples, and visuals that show how the mechanism works.
- Check factual accuracy and verify interactive controls or generated media before delivery.
- Use with: `$create-explainer Explain this system with an interactive visual that lets me explore how it works.`

### [Grill Me](skills/grill-me/SKILL.md)

- Pressure-test an idea, plan, design, or decision before committing.
- Ask questions in rounds that build on settled answers, with alternatives and reasoned recommendations.
- Identify assumptions that need evidence, experiments, or prototypes; finish with decisions and open questions in chat.
- Inspired by Matt Pocock's [The /grill-me Skill](https://www.aihero.dev/skills-grill-me).
- Use with: `$grill-me Help me pressure-test this product idea before I build it.`

### [Writing for Agents](skills/writing-for-agents/SKILL.md)

- Write or improve skills, repository guidance, specifications, handoffs, and prompts that agents read.
- Make discovery conditions and completion criteria explicit, organize conditional references, and remove repetition while preserving requirements.
- Includes focused packaging guidance for portable Agent Skills and Codex metadata.
- Adapted from Matt Pocock's [The /writing-for-agents Skill](https://www.aihero.dev/skills-writing-for-agents).
- Use with: `$writing-for-agents Review this AGENTS.md and make its instructions more precise without losing requirements.`

The podcast skill is for an audio conversation; the explainer skill helps choose a format and can use the podcast skill when audio is the best fit.

## Install

Install globally for use across local Codex and Cursor projects:

```bash
npx skills@latest add rubinj30/agent-skills --global --agent codex cursor
```

Or install into one project and choose the target agent when prompted:

```bash
npx skills@latest add rubinj30/agent-skills
```

Because this repository is private, authenticate GitHub on the machine before installing.

Then invoke a skill explicitly—for example:

```text
$create-audio-podcast Turn this report into a podcast I can play on my iPhone.
$improve-codebase-architecture Find the highest-leverage architecture improvement in this repository.
$create-explainer Explain this system with an interactive visual that lets me explore how it works.
$grill-me Help me pressure-test this product idea before I build it.
$writing-for-agents Improve this AGENTS.md while preserving its required behavior.
```

Cursor may display installed skills as slash commands, such as `/create-audio-podcast`, `/grill-me`, and `/writing-for-agents`.

Each folder under `skills/` is self-contained. `SKILL.md` is the cross-agent source of truth; `agents/openai.yaml` adds Codex-facing metadata.

## Acknowledgment

`improve-codebase-architecture` is an original adaptation inspired by the deep-module and hotspot-first workflow in [Matt Pocock's MIT-licensed skills collection](https://github.com/mattpocock/skills).

`grill-me` and `writing-for-agents` are self-contained adaptations of Matt Pocock's workflows, described in [The /grill-me Skill](https://www.aihero.dev/skills-grill-me) and [The /writing-for-agents Skill](https://www.aihero.dev/skills-writing-for-agents). Each package retains his MIT license notice.

`create-explainer` draws on [Andrej Karpathy's original post about clearer explanations and custom learning artifacts](https://x.com/karpathy/status/2105819303471976479).

