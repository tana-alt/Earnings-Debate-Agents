# GPT Pro Improvement Review: Boundary And Extension

## Review Bounds

Subagent C performed a read-only review. No files were edited during the
subagent pass.

Scope: repo boundary, skills/plugins, storage, distribution hygiene, and future
extension surfaces.

## Verdict

There are improvement questions worth sending to GPT Pro. The boundary model is
sound: compact active docs, routed references, project-local truth, and no
runtime-state storage. The gaps are mostly about extension architecture becoming
enforceable as skills/plugins grow.

## Repo Context For GPT Pro

Active repo truth is explicitly bounded to `AGENTS.md`, `docs/`,
`docs/reference/`, `README.md`, `templates/`, `scripts/`, `tests`, tooling
files, `.agents/skills/`, `.agents/plugins/marketplace.json`, `plugins/`,
`hooks/`, `Plan/`, `app/`, `src/`, and `artifact/`.

Non-truth surfaces include `.serena/`, `archive/`, auth files, tokens, cookies,
API keys, logs, caches, browser sessions, downloaded runtime payloads, and
local runtime state. `Plan/` is scoped human planning only, not a queue or lock
ledger.

Skills/plugins are extension surfaces, not policy overrides.
`.agents/skills/SKILL_INDEX.md` is human-facing; Codex discovers skills from
`SKILL.md` front matter. The index lists core/conditional skills, but the tree
currently contains more skill roots than the index enumerates.

Plugin distribution is local: `.agents/plugins/marketplace.json` registers one
local plugin, `build-ios-apps`, pointing at `./plugins/build-ios-apps`. That
plugin has a manifest, local MCP config, assets, agent metadata, and bundled
skills.

Current hygiene checks enforce top-level tracked roots, forbidden tracked roots,
tracked ignored files, nested Git dirs, secrets via Gitleaks, and basic
skill-root presence. They do not currently validate skill front matter,
skill-index coverage, plugin registry/manifest consistency, plugin MCP shape,
or a clear distinction between canonical plugin payloads and downloaded runtime
payloads.

## Trial 1

Initial reasoning: the boundary docs looked strong enough that likely
improvements seemed limited to wording. The contract already says not to store
runtime state, broad logs, secrets, queues, lock indexes, or browser sessions.

What changed: after checking the reference, the model is more than wording:
future durable storage requires ownership, retention, verification, and cleanup
rules. That is good architecture, but it needs sharper extension tests once
`plugins/`, `app/`, `src/`, and `artifact/` become active.

Trial 1 candidate: ask GPT Pro whether the storage contract needs an activation
checklist for reserved surfaces such as `app/`, `src/`, `artifact/`, and new
plugin roots.

## Trial 2

Reasoning changed because the extension payload is already large.
`.agents/skills/` contains more roots than the human index enumerates, and
`plugins/build-ios-apps` contains bundled plugin skills and assets.
`pyproject.toml` excludes `.agents/skills` and `plugins` from Ruff, so these
surfaces rely mostly on structure and secret checks.

Trial 2 candidate: ask GPT Pro whether the repo should treat skill/plugin
payloads as canonical source, vendored distribution payloads, or restoreable
external artifacts. The answer affects whether the repo needs generated
indexes, manifest schema tests, license/provenance checks, or stronger ignore
rules.

Rejected complexity: do not introduce a full plugin package manager, submodules,
or broad lint/typecheck across all skill/plugin payloads unless GPT Pro
identifies a concrete failure mode. A small manifest/structure validator is
likely enough.

## Trial 3

Reasoning changed again after checking hygiene. `.gitignore` ignores common
Python caches, `.serena/`, `archive/`, and legacy roots, but not common
secret/runtime names such as `.env`, logs, cookies, auth files, browser
profiles, or MCP/download output directories. Gitleaks scans tracked
content/history, while repo hygiene focuses on tracked root violations. That
may be intentional, but it leaves the docs stronger than the automated
guardrails.

A second tension appeared in `templates/project-storage-map.yaml`: it uses
`projects/example_project`, while the boundary reference says not to introduce
a default `projects/` root in this foundation repo. This may be only an
illustrative external path, but future agents could misread it.

Trial 3 candidate: ask GPT Pro for the smallest distribution-hygiene guardrail
set that catches accidental runtime/secret storage without making `.gitignore`
so broad that important untracked mistakes disappear.

## Candidate Improvements

1. Add a minimal skill/plugin integrity check:
   validate each `.agents/skills/*/SKILL.md`, decide whether
   `SKILL_INDEX.md` must enumerate all roots or only curated routing skills,
   validate marketplace plugin paths, plugin manifest presence, skills
   directory presence, MCP config presence, and registry/manifest name
   consistency.

2. Clarify plugin payload ownership:
   distinguish “local plugin bundles tracked as repo truth” from “downloaded
   runtime payloads not repo truth.”

3. Add a reserved-surface activation rule:
   for `app/`, `src/`, `artifact/`, and new plugin roots, require ownership,
   retention, verification, cleanup, and allowed generated-output rules before
   adding durable content.

4. Tighten storage/distribution hygiene:
   decide whether to expand `.gitignore`, add tracked-file denylist checks for
   names like `.env`, `auth.json`, cookies, and logs, or keep the current
   docs-plus-Gitleaks posture.

5. Fix or clarify the project storage map template:
   make clear that `projects/example_project` is an external placeholder, not a
   new root to create inside this foundation repo.

## Exact GPT Pro Prompts

1. Given this foundation repo boundary model, should `.agents/skills/` and
   `plugins/` be treated as canonical source payloads, vendored distribution
   payloads, or restoreable external artifacts? Recommend the smallest contract
   and test changes to make that unambiguous.

2. What minimal integrity checks should exist for skill/plugin extension
   surfaces? Consider `SKILL_INDEX.md` coverage, `SKILL.md` front matter,
   marketplace registry paths, plugin manifest consistency, plugin MCP config
   shape, license/provenance, and smoke checks. Avoid a heavy package-manager
   design.

3. The docs forbid secrets, logs, browser sessions, runtime state, and
   downloaded runtime payloads, but `.gitignore` and hygiene checks only cover a
   smaller subset. Should the repo add broader ignore patterns, tracked-file
   denylist checks, or both? Propose a minimal guardrail set that avoids hiding
   important untracked mistakes.

4. The storage-map template uses `projects/example_project`, while the repo
   boundary says not to introduce a default `projects/` root. Should this
   template be rewritten to use `<project_root>` or explicitly mark the path as
   outside the foundation repo?

5. For reserved future surfaces `app/`, `src/`, `artifact/`, and future
   plugins, what activation checklist should be required before durable content
   is added: owner, retention, cleanup, verification, generated-output policy,
   and distribution policy?
