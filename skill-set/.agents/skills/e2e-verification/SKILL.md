---
name: e2e-verification
description: "Use when a browser UI flow, release-critical journey, Playwright test, or reproduction steps must be verified end-to-end. Do not use for pure unit logic."
---


## Purpose

Verify a critical user journey in a real or scripted browser flow.

## Use when

- A UI flow must be verified before release.
- A bug report includes reproduction steps.
- The change touches routing, auth, forms, checkout, onboarding, or critical navigation.
- Existing unit tests cannot prove the user journey works.

## Success conditions

- Existing Playwright or e2e tests are preferred.
- If missing, add one minimal e2e test for the target flow only.
- Test result is reported as pass, fail, or blocked.
- Failure includes the failing step and the likely implementation area.

## Constraints

- Do not create a large e2e suite during a local task.
- Do not use arbitrary sleep; prefer deterministic waits and assertions.
- Do not run destructive production flows or real payment actions.
- Do not inspect unrelated pages or docs.
- Do not hide flakiness; report it as risk.

## Output

- Flow verified.
- Command run.
- Result.
- Artifacts or failure summary.
- Patch made, if any.
