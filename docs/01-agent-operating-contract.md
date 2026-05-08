# Agent Operating Contract

## Purpose

This doc defines how workers act in this repo. It replaces broad role hierarchy
with small, bounded work contracts.

## Scope First

A worker starts from the user request, task packet, provided scope, and named
`source_refs`. Scope is not discovered by reading the whole repo.

Useful scope may include task intent, success criteria, source refs, optional
refs, expected outputs, allowed write targets, denied context, evidence
required, verification required, `git_scope` when writing in parallel,
blockers, open questions, and next action.

Do not invent missing facts, paths, requirements, state, roles, or ownership.

## Context Boundary

- Read named refs first.
- Inspect nearby files only when needed for a safe local change.
- Deny unrelated logs, broad history, archives, runtime state, secret material,
  and past-source material by default.
- If context expands, say why in the output.

## Write Preconditions

Before any local write, confirm:

- allowed write targets
- current contents of files to be edited
- canonical repo root and relevant VCS status
- conflict risk for the task scope

For parallel write work, also confirm a complete `git_scope`: `base_ref`,
`merge_target`, allowed write targets, conflict policy, and either explicit or
derivable branch and worktree targets. If the scope cannot provide or derive
these fields, return rework instead of inventing branch ownership.

Installed hooks block commits and pushes from the canonical root or
non-`agent/*` branches. They are guardrails, not full filesystem monitors. Do
not bypass hooks for agent work; return rework if the hook policy conflicts
with the task scope.

## Side Effects

Classify work before acting: read-only local, local write, external read,
external write, infra/deploy, secret-bearing, or irreversible/protected.

External writes, dependency changes, CI/CD changes, deployment, release, secret
handling, auth, billing, database migration, infrastructure, and
security-sensitive work require explicit approval or human gate.

When side effects occur, record the tool or command, target surface, permission
or gate status, input refs, output or artifact refs, and verification or
rollback note. The canonical human-gate list lives in
`docs/02-output-verification-contract.md`.

## Valid Output

A valid output follows `docs/02-output-verification-contract.md` and states
changed paths or artifact refs, evidence refs, verification result, unverified
surfaces, residual risk, and next action.

Return rework when scope, permission, evidence, output shape, or verification is
missing, unsafe, ambiguous, or in conflict with repo truth.
