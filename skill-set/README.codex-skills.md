# Minimal Codex App Skills

This bundle converts selected ECC-style best practices into Codex skills for app development.

Design principle:

- `AGENTS.md` stays small and durable.
- `.agents/skills/*/SKILL.md` is a discovery and execution boundary.
- Best practices are expressed as `success conditions` and `constraints` instead of long manuals.
- Security is intentionally thicker than the other skills.

Install by copying the contents of this ZIP into the repository root.

Expected structure after extraction:

```text
AGENTS.md
project_commands.yaml
.codex/config.toml
.agents/skills/*/SKILL.md
```

Notes:

- `.codex/config.toml` is project-local Codex configuration. It is intentionally comment-only until you decide model, sandbox, approval, and MCP policy.
- `.agents/skills` contains Codex skills.
- `.codex/agents` is not included by default. Add subagents only after the workflow proves a repeated need.
