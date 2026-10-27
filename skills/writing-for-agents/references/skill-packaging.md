# Packaging an Agent Skill

Read this reference when the document being authored is an Agent Skill. Preserve the target repository's conventions and the user's requested agent support.

## Entry point and discovery

Use one directory per skill, named with lowercase letters, digits, and hyphens. Keep `SKILL.md` at its root, with YAML frontmatter containing a matching `name` and a description of the capability and the requests that should select it.

Keep discovery text concise and specific. Put procedures, detailed examples, and conditional instructions in the body or linked resources. Avoid attracting unrelated tasks with a list of loosely related keywords.

Keep normal automatic discovery unless the user requests explicit-only invocation. For Codex, that choice belongs in `agents/openai.yaml` as `policy.allow_implicit_invocation: false`. Consult the target agent's supported format before adding equivalent metadata elsewhere; agent-specific fields are not automatically portable.

## Resources and metadata

Keep shared task instructions in `SKILL.md` and Codex display metadata in `agents/openai.yaml`. A default prompt should name the skill as `$skill-name`. Preserve existing policy and dependency fields when updating display text.

Add scripts for repeated deterministic work, references for substantial conditional guidance, and assets for templates or output resources. Link each reference from the decision that needs it. Every package should work without an unrelated personal configuration or an unavailable companion skill.

Credit adapted work and preserve applicable license notices inside the package so they travel with an individual installation.

## Validation

Run the available skill validator after changes. Check that the folder and frontmatter names match, YAML parses, local links resolve, metadata matches the workflow, and scaffold instructions have been replaced.

Walk through a typical request and a nearby request that should not select the skill. Check conditional references and completion criteria. For executable helpers, verify meaningful observable behavior; for a documentation-only change, structural checks and a focused scenario review are usually sufficient. Report those checks accurately without presenting a walkthrough as an independent execution test.
