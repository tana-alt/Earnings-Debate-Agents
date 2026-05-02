---
name: backend-implementation
description: "Use for backend services, repositories, jobs, database access, business logic, server validation, middleware, and integration changes."
---


## Purpose

Keep backend changes explicit, bounded, observable, and safe at trust boundaries.

## Use when

- Adding or changing service, repository, job, middleware, API handler, or database logic.
- Implementing business rules or server-side validation.
- Adding third-party integrations, webhooks, queues, or background jobs.

## Success conditions

- Business logic, data access, and transport concerns are separated according to repo pattern.
- Inputs are validated at server-side trust boundaries.
- Errors are handled with repo-standard categories and messages.
- Queries are bounded and avoid obvious N+1 behavior.
- Jobs and retries are idempotent where required.

## Constraints

- Do not use `select *` or unbounded queries unless the repo explicitly permits it.
- Do not log secrets, tokens, full request bodies, or sensitive user data.
- Do not return raw internal exceptions to users.
- Do not skip authorization because the caller is an internal API.
- Do not add new infrastructure if a local repo pattern already exists.

## Output

- Backend behavior changed.
- Data and trust boundaries touched.
- Verification run or blocked reason.
