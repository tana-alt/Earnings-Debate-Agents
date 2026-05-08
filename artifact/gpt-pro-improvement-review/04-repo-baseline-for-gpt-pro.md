# Repo Baseline For GPT Pro

## Review Frame

Target environment: robust development foundation for financial algorithm work.
Domain-specific finance content is intentionally excluded. Review the
engineering substrate: reproducibility, verification, evidence records, boundary
control, local/CI parity, secret hygiene, and agent collaboration safety.

## Core Principles

- `AGENTS.md` is the compact entrypoint and routing map.
- Active behavior belongs in three short docs under `docs/`.
- Detailed operational material lives in `docs/reference/` and is opened by
  need, not by default.
- Work starts from explicit scope, source refs, allowed write targets, current
  file inspection, VCS status, and conflict awareness.
- Parallel write work requires one branch and one worktree per agent.
- Outputs must record source refs, changed paths or artifact refs, evidence,
  verification result, unverified surfaces, residual risk, and human gates.
- Repo truth excludes runtime queues, lock ledgers, broad logs, caches, browser
  sessions, secrets, and default external-project storage.
- Skills and plugins are methods and extension payloads; they do not override
  repo contracts, write boundaries, verification, or human gates.

## Directory Structure

- `AGENTS.md`: agent entrypoint and routing map.
- `README.md`: human overview, restore path, and verification summary.
- `docs/`: active operating, output/verification, and boundary contracts.
- `docs/reference/`: routed details for runtime scope, evidence, storage, CI,
  worktrees, migration, and acceptance.
- `templates/`: sanitized work, evidence, verification, rework, storage, Serena,
  and Codex configuration templates.
- `scripts/`: setup, environment inspection, hygiene, secret scan, ShellCheck,
  and worktree-policy helpers.
- `hooks/`: tracked `pre-commit` and `pre-push` guardrails installed through
  `core.hooksPath`.
- `tests/`: pytest checks for contracts, repo integrity, clean checkout
  reproducibility, and skill/plugin structure.
- `.github/workflows/ci.yml`: CI entrypoint for local parity checks and CD
  readiness guard.
- `.agents/skills/`: repo-local Codex skills.
- `.agents/plugins/marketplace.json`: local plugin registry.
- `plugins/`: plugin payloads, currently including `build-ios-apps`.
- `Plan/`: scoped planning notes, not runtime agent state.
- `app/` and `src/`: reserved future implementation surfaces.
- `artifact/`: compact review outputs and fixtures, not broad logs or secret
  material.

## Existing Test And Verification Surface

- `uv sync --frozen --group dev`: installs locked development dependencies.
- `make doctor`: read-only local environment inspection.
- `make lint`: Ruff lint check.
- `make typecheck`: strict mypy over tests.
- `make test`: full pytest suite.
- `make check-toolchain`: reports the local toolchain versions used by the
  foundation gate.
- `make check-contracts`: Pydantic template contract tests.
- `make check-doc-consistency`: doc and work contract consistency subset.
- `make check-hooks`: POSIX shell syntax checks for scripts and hooks.
- `make check-shell`: ShellCheck on tracked shell scripts/hooks.
- `make check-hygiene`: tracked ignored-file, forbidden-root, gitlink, and
  nested-git hygiene checks.
- `make check-secrets`: Gitleaks scan over committable content and Git history
  when history exists.
- `make check-cd`: guard that deployment remains `not_applicable` until a real
  deployment surface exists.
- `make check-required`: required local chain used by hooks and CI.
- `make check-foundation`: Foundation Robustness Gate combining
  `make check-toolchain`, `make check-required`, and `make check-cd`.

Test files:

- `tests/test_contract_models.py`: validates YAML contract/template schemas.
- `tests/test_foundation_integrity.py`: validates active docs, references,
  required files, dev defaults, hooks, worktree policy, hygiene, CD posture, and
  doc consistency.
- `tests/test_clean_checkout_reproducibility.py`: asserts required foundation
  files are tracked for clean-checkout reliability.
- `tests/test_extension_surface_integrity.py`: validates skill front matter,
  skill index coverage, plugin registry paths, plugin manifests, and MCP config
  shape without executing plugin code.

## GPT Pro Review Questions

1. Are the current contracts strong enough for high-consequence algorithm
   development without becoming a runtime state system?
2. Are verification records and evidence templates sufficient to audit changes
   across repeated experiments and agent handoffs?
3. Should the repo add stricter reproducibility checks for dependency, tool, and
   environment drift beyond the current `uv.lock`, `.python-version`, CI, and
   Makefile surface?
4. Are the secret and hygiene boundaries appropriate for algorithm work where
   credentials, datasets, and brokerage/API material may exist nearby but must
   not enter repo truth?
5. Is extension-surface validation for skills/plugins appropriately structural,
   or should provenance/licensing checks become required before wider reuse?
