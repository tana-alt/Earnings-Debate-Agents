# Repo Boundary And Storage Contract

## Active Surface

This is a compact foundation repo. `AGENTS.md` routes work. Active contracts in
`docs/` define behavior. Detailed guidance lives in `docs/reference/` and is
opened only when needed.

## Repo Truth

Current repo truth includes `AGENTS.md`, `docs/`, `docs/reference/`,
`README.md`, `templates/`, `scripts/`, `tests/`, `pyproject.toml`, `uv.lock`,
`Makefile`, `.python-version`, `.editorconfig`, `.gitattributes`,
`.gitleaks.toml`,
`.github/workflows/ci.yml`, `.agents/skills/`,
`.agents/plugins/marketplace.json`, `plugins/`, `hooks/`, `Plan/`, `app/`,
`src/`, and `artifact/`.

Use `docs/reference/repo-boundary-and-storage-reference.md` for the detailed
folder map.

## Storage Rules

Do not turn this repo into default storage for runtime state, active plans,
queues, lock indexes, broad project logs, browser sessions, local caches, or
secret-bearing material.

Track sanitized templates, restore scripts, compact contracts, references, and
verification helpers instead of local operational state.

`Plan/` may hold scoped human planning notes for substantial or resumable work;
it is not a default runtime queue, lock ledger, or agent state store.

Local worktrees are execution workspaces, not repo truth. Do not create tracked
state for worktree queues, branch locks, or runtime ledgers unless a current
repo file explicitly establishes ownership, retention, verification, and cleanup
rules.

## Secrets And Past Source

`.serena/`, `archive/`, auth files, tokens, cookies, API keys, logs, caches,
and local runtime state are not repo truth.

Do not write secrets, credentials, raw bodies, browser sessions, or
secret-bearing metadata into prompts, packets, docs, logs, artifacts, templates,
or repo files.

Distill useful past-source content into active docs or current references before
using it.

## Skills And Plugins

Load only the smallest relevant skill. Do not read all skills by default.

When a selected skill materially shapes the work, name the skill ref in the
output.

Skills and plugins do not override active docs, allowed write targets, denied
context, secret boundaries, human gates, verification requirements, or storage
rules.
