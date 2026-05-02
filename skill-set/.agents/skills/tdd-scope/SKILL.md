---
name: tdd-scope
description: "Use when a bug fix, important logic change, API change, or reusable component should be driven by a focused failing test before implementation."
---


## Purpose

Use tests to define behavior before changing implementation when the behavior is important or regression-prone.

## Use when

- Fixing a bug with clear reproduction.
- Adding important domain logic.
- Changing API behavior.
- Adding reusable components or utilities.
- Preventing a regression from returning.

## Success conditions

- A focused failing test exists first when practical.
- The implementation is the smallest change that passes the test.
- Edge/error cases are covered when they define the behavior.
- Existing relevant tests still pass.

## Constraints

- Do not force TDD for trivial styling or mechanical renames.
- Do not add broad snapshot tests when behavior tests are better.
- Do not leave skipped, disabled, or brittle tests.
- Do not overfit tests to implementation details unless necessary.

## Output

- Behavior under test.
- Test added or updated.
- Verification result.
