---
name: doc-lookup
description: "Use when current framework, library, API, CLI, or platform documentation is needed to avoid stale or guessed implementation. Do not use for stable repo-local behavior."
---


## Purpose

Confirm current external behavior before implementing code that depends on it.

## Use when

- A library, SDK, CLI, or platform may have changed.
- Version-specific behavior matters.
- The implementation depends on auth, billing, webhooks, deployment, routing, caching, or browser behavior.
- The agent is not confident about the API surface.

## Success conditions

- Prefer official documentation or primary source material.
- Capture only the 1-3 constraints that affect implementation.
- Note the relevant version or date when available.
- Apply the constraint directly to the implementation plan.

## Constraints

- Do not use memory alone for change-prone external APIs.
- Do not paste long documentation into the task context.
- Do not continue searching after the implementation constraint is clear.
- Do not treat third-party blog posts as authoritative when official docs exist.

## Output

- Source checked.
- Constraint summary.
- Implementation implication.
