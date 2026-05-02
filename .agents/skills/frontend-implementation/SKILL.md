---
name: frontend-implementation
description: "Use for React, Next.js, UI component, form, routing, client state, accessibility, loading, error, and responsive behavior changes."
---


## Purpose

Keep frontend changes small, testable, accessible, and consistent with the existing UI architecture.

## Use when

- Adding or changing UI components.
- Implementing forms, navigation, client state, data fetching, or error/loading states.
- Touching responsive layout or accessibility behavior.

## Success conditions

- The component has clear responsibility boundaries.
- Loading, empty, error, and success states are handled when applicable.
- Basic keyboard and screen-reader accessibility are preserved.
- Form validation occurs at the appropriate client/server boundaries.
- Styling follows existing tokens, components, and layout conventions.

## Constraints

- Do not expose secrets, tokens, raw errors, or private data to the client.
- Do not add a new state library or UI library unless necessary.
- Do not perform broad redesign while implementing a local change.
- Do not hide server authorization requirements behind UI-only checks.
- Do not add arbitrary animations or decorative complexity without task need.

## Output

- UI behavior changed.
- States covered.
- Verification run or blocked reason.
