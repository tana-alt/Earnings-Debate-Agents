---
name: research-before-build
description: "Use before building when the change may already have a repo pattern, external API constraint, dependency/version issue, or known implementation approach. Do not use for obvious local refactors."
---


## Purpose

Prevent unnecessary custom work by checking existing repo patterns and external constraints before implementation.

## Use when

- Adding a new feature or integration.
- Touching an external API, SDK, framework, or dependency behavior.
- Unsure whether the repo already has a pattern for the task.
- The task has multiple plausible implementation paths.

## Success conditions

- Existing repo patterns are checked first.
- External constraints are checked only when relevant.
- The chosen path is stated as `reuse`, `extend`, `replace`, or `build new`.
- The implementation scope is narrowed before coding.

## Constraints

- Do not browse or research broadly when local code is sufficient.
- Do not add a dependency unless it clearly reduces complexity or risk.
- Do not copy external patterns blindly; adapt to the repo's conventions.
- Keep the research note to the minimum needed decision.

## Output

- Decision.
- Files or docs checked.
- Implementation constraint.
- Remaining uncertainty, if any.
