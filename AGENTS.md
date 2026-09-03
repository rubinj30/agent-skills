# Repository guidance

- Treat each directory under `skills/` as one portable Agent Skill.
- Keep `SKILL.md` compatible with Codex and Cursor; place Codex UI metadata in `agents/openai.yaml`.
- Use the skill-creator workflow for new skills and validate every changed skill before committing.
- Keep secrets, generated media, reports, and test outputs out of this repository.
- Prefer one cross-agent source of truth over duplicated editor-specific copies.
