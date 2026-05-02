---
name: release-check
description: "Use before merge, release, handoff, or after a large change to run the narrowest useful build, lint, typecheck, test, security, and e2e verification."
---


## Purpose

Confirm that a change is shippable or clearly report why it is not.

## Use when

- Before PR handoff or release.
- After a broad refactor.
- After touching build, dependency, auth, data, or release-critical flow.
- When the user asks whether the change is done.

## Success conditions

- Relevant commands are selected from `project_commands.yaml` or existing package scripts.
- Typecheck, lint, unit tests, build, security audit, and e2e are run only when relevant and available.
- Results are summarized as `pass`, `rework`, or `blocked`.
- Failures include the minimal next fix, not a broad diagnosis essay.

## Constraints

- Do not invent commands when repo scripts exist.
- Do not run destructive commands.
- Do not claim pass if verification was not run.
- Do not chase unrelated failures unless they block the task.
- Do not expand into full QA when a narrow verification is enough.

## Output

- Verdict.
- Commands run.
- Relevant output summary.
- Remaining risk or blocked reason.
