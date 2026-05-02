---
name: api-contract
description: "Use when creating or changing API endpoints, request/response schemas, status codes, pagination, auth, rate limits, webhooks, or error formats."
---


## Purpose

Make API changes explicit and stable before implementation is considered done.

## Use when

- Adding or changing an API route.
- Changing request or response shape.
- Adding pagination, filtering, sorting, rate limits, auth, or webhooks.
- Modifying error behavior or status codes.

## Success conditions

- Method, path, auth requirement, request schema, response schema, and error shape are clear.
- Status codes distinguish success, validation errors, auth failures, forbidden access, missing resources, conflicts, and server errors.
- API behavior matches existing repo conventions.
- Contract docs, types, or OpenAPI-like references are updated if the repo uses them.

## Constraints

- Do not use one generic `200` or `500` for all outcomes.
- Do not leak stack traces, internal IDs, secrets, or database details.
- Do not put verbs in REST resource paths unless the repo already uses that convention.
- Do not return unbounded lists.
- Do not trust client-side validation as the API contract.

## Output

- Contract summary.
- Files changed.
- Verification command or reason blocked.
