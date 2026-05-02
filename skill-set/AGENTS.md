# Codex Project Guidance

## Operating principle

Keep durable guidance small. Codex should read the current task, the closest relevant `AGENTS.md`, changed files, and only the selected skill instructions.

## Skill routing

Repo-scoped skills live in `.agents/skills/*/SKILL.md`.

Do not pre-read every skill. Treat each skill's `name` and `description` front matter as the discovery layer. Read the full `SKILL.md` only when the task matches the description or the user explicitly invokes that skill.

## Read order

1. Current task or packet.
2. Closest `AGENTS.md` guidance.
3. Relevant project state, changed files, or local command registry.
4. One selected skill, if needed.
5. Additional docs only when the selected skill explicitly requires them.

## Default constraints

- Prefer small diffs.
- Prefer existing commands, tests, and repo patterns.
- Do not add dependencies unless necessary.
- Do not inspect unrelated project logs or old artifacts unless referenced.
- Do not put secrets in prompts, logs, packets, tests, or committed files.
- Report `pass`, `rework`, or `blocked` with the narrowest useful evidence.

## Done means

A change is done only when the narrowest relevant verification has run, or the reason it cannot run is clearly reported.
