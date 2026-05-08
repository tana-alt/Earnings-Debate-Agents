# GPT Pro Improvement Review Packet

## Purpose

This folder is a handoff packet for asking GPT Pro whether this foundation repo
has remaining architecture or documentation improvements worth making for a
robust financial algorithm development environment.

The review target is development-environment quality, not financial domain
strategy. Exclude trading logic, market assumptions, portfolio construction, and
financial model recommendations. Focus on reproducibility, verification,
evidence, isolation, auditability, secrets hygiene, and agent/human handoff
quality.

The packet is intentionally compact. It does not include archives, caches,
runtime state, local secrets, or broad repo dumps.

## How To Read

1. Start with this `README.md`.
2. Read `06-final-subagent-supervision.md` for the implemented result and final
   no-must-fix supervision verdict.
3. Read `00-parent-supervision-summary.md` for the parent synthesis and
   prioritized prompts.
4. Read `04-repo-baseline-for-gpt-pro.md` for the current directory structure,
   principles, and test surface.
5. Read `05-robustness-review-report.md` for the robustness review result and
   follow-up prompts.
6. Read the three subagent reviews only as needed:
   - `01-doc-architecture.md`
   - `02-verification-harness.md`
   - `03-boundary-extension.md`

## Repo Snapshot

This repo is a compact development foundation. Active behavior is routed by
`AGENTS.md` and three short docs in `docs/`. Detailed material lives in
`docs/reference/`. Verification is Makefile-centered and backed by pytest,
Ruff, mypy, ShellCheck, Gitleaks, local Git hooks, and GitHub Actions.

Core principles:

- Keep active context small.
- Do not read the whole repo by default.
- Do not store runtime queues, lock ledgers, broad logs, local caches, browser
  sessions, or secrets in repo truth.
- Use one branch/worktree per parallel write agent.
- Treat skills/plugins as methods and extension payloads; they do not override
  active contracts.
- Keep algorithm-project artifacts outside repo truth unless a scoped contract
  explicitly makes a sanitized output part of the review surface.

## Current Known State

The worktree is still pre-initial-commit and contains many staged additions.
Final local verification passed after the implemented guardrail fixes. Direct
pushes to `main` or `master` and merge remain prohibited for agents; PR creation
from owned `agent/*` branches is allowed when scope, ownership, verification,
and evidence are clear.
