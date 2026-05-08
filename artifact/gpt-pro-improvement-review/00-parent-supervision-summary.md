# Parent Supervision Summary

## Scope

User request: review and improve this repo as a robust general development
environment for financial algorithm work, using subagents, then place a compact
GPT Pro review packet in this folder. Specific financial knowledge is out of
scope; the target is foundation quality for durable algorithm development.

Allowed output target: `artifact/gpt-pro-improvement-review/`.

Denied context: archives, caches, `.venv`, `.serena`, broad logs, and unrelated
history. No secret or runtime state was copied into this packet.

## Subagent Assignment

- Subagent A: documentation and contract architecture.
- Subagent B: verification, CI, hooks, and development harness architecture.
- Subagent C: repo boundary, storage, skills/plugins, distribution hygiene, and
  future extension surfaces.

Each subagent reported exactly three trial steps and explained how its reasoning
changed.

## Parent Assessment

The repo is directionally sound. The best GPT Pro questions are not “should we
add a bigger runtime?” They are targeted consistency and enforcement questions
where compact docs can become ambiguous or where lightweight guardrails can
drift. For financial algorithm work, the highest-value foundation properties are
reproducibility, evidence quality, isolated agent writes, secret hygiene,
deterministic verification, and clear human gates.

The strongest cross-cutting themes are:

1. Reproducibility of tracked harness files.
   Several required hook/check files exist locally but are currently untracked.
   A clean checkout would fail if they are omitted from the final commit. This
   is primarily a packaging issue now, but GPT Pro should assess whether a
   tracked-file reproducibility test belongs in the repo.

2. Template wording versus boundary policy.
   `templates/project-storage-map.yaml` uses `projects/example_project`, while
   repo docs forbid introducing a default `projects/` root. GPT Pro should
   assess whether to rewrite that example as an external placeholder.

3. Canonical policy wording drift.
   Human gates and hook/worktree rules are repeated across active docs and
   references. GPT Pro should decide where duplication is useful and where it
   risks drift.

4. Extension surface maturity.
   `.agents/skills/` and `plugins/` are already significant surfaces. GPT Pro
   should determine whether minimal structure validation is enough or whether
   index/manifest/provenance checks are needed.

5. Guardrail scope.
   Secret scans target committable content. Hygiene checks target tracked root
   violations. GPT Pro should decide whether ignored/untracked local state
   needs opt-in scans, broader denylist checks, or no change.

## Recommended GPT Pro Prompt Order

Ask these first:

1. Should this repo add a test that asserts all required docs, hooks, scripts,
   templates, workflows, and dev defaults are tracked by `git ls-files`? The
   current tests check local file existence, but a clean checkout only sees
   tracked files.

2. Should `templates/project-storage-map.yaml` replace
   `projects/example_project` with `<external-project-root>` or another
   placeholder, given that this foundation repo forbids introducing a default
   `projects/` root?

3. Should human gate rules be canonical only in
   `docs/02-output-verification-contract.md`, with references linking back, or
   should the verification reference keep a restated list?

4. Should worktree hook language distinguish contract-level write prohibition
   from hook-level commit/push enforcement?

5. What minimal integrity checks should exist for `.agents/skills/` and
   `plugins/`? Consider `SKILL.md` front matter, `SKILL_INDEX.md` coverage,
   marketplace registry paths, plugin manifest consistency, MCP config shape,
   license/provenance, and smoke checks. Avoid a heavy package-manager design.

6. Should the required Gitleaks scan remain limited to tracked/current tree and
   Git history, with ignored/untracked local state out of scope, or should there
   be an opt-in deep local scan?

## Explicit Non-Goals

- Do not add a scheduler, queue, lock ledger, dashboard root, runtime plan
  store, or project-state database.
- Do not make this foundation repo a default storage root for other projects.
- Do not require routine agents to read every reference, every skill, plugin
  payloads, archives, or broad logs.
- Do not add deployment smoke tests while deployment remains
  `not_applicable`.
- Do not replace the Makefile with a heavier task runtime unless GPT Pro finds
  a concrete drift problem that simpler tests cannot solve.

## Verification Notes

This packet was generated from read-only subagent reports and parent
inspection. It is an advisory artifact, not a code implementation.

Recommended narrow verification after this file is written:

- `git diff --check`
- `make check-hygiene`
- `make check-secrets`
