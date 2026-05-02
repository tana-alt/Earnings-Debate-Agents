---
name: browser-qa
description: "Use for manual or scripted browser quality checks after frontend changes, preview deployments, responsive layout changes, console errors, or accessibility risks."
---


## Purpose

Catch visible browser regressions without turning every task into a full QA cycle.

## Use when

- A frontend PR needs a quick browser sanity check.
- A preview or local app is available.
- Responsive, accessibility, routing, or console behavior may be affected.
- Visual issues were reported by the user.

## Success conditions

- Critical page or flow loads.
- Console errors and network 4xx/5xx are checked where possible.
- Desktop and mobile layout are sampled when relevant.
- Keyboard or accessibility basics are checked for forms and controls.

## Constraints

- Do not inspect every page unless requested.
- Do not redesign the UI during QA.
- Do not treat cosmetic preferences as release blockers unless they break the stated goal.
- Do not use production accounts or destructive actions.

## Output

- Pass/fail/block.
- Pages or flows checked.
- Issues with file/route reference when possible.
