# Agent Skills

A personal collection of reusable Agent Skills for Codex, with the same `SKILL.md` packages usable in Cursor and other compatible coding agents.

## Skills

- **`create-audio-podcast`** — turn source material into a grounded two-host podcast, natural AI narration, transcript, and iPhone-friendly player.
- **`improve-codebase-architecture`** — inspect a repository, find evidence-backed architectural friction, and rank high-leverage refactoring opportunities.

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
```

Cursor may display installed skills as slash commands, such as `/create-audio-podcast`.

Each folder under `skills/` is self-contained. `SKILL.md` is the cross-agent source of truth; `agents/openai.yaml` adds Codex-facing metadata.

## Acknowledgment

`improve-codebase-architecture` is an original adaptation inspired by the deep-module and hotspot-first workflow in [Matt Pocock's MIT-licensed skills collection](https://github.com/mattpocock/skills).
