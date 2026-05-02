---
name: deploy-readiness
description: "Use when changing deployment, Docker, CI/CD, environment variables, build output, runtime config, health checks, or release process."
---


## Purpose

Prevent deployment regressions caused by configuration, packaging, runtime, or release-process changes.

## Use when

- Dockerfile, CI/CD, deployment scripts, env vars, or runtime config change.
- A build or production startup behavior changes.
- Health checks, rollback, monitoring, or release commands are touched.

## Success conditions

- Build and startup path are clear.
- Required env vars are documented without secret values.
- Health check or smoke test exists when repo pattern supports it.
- Rollback or mitigation path is clear for risky changes.
- Runtime image and permissions follow repo security expectations.

## Constraints

- Do not bake secrets into images, scripts, logs, or config.
- Do not use floating `latest` tags unless repo policy allows it.
- Do not run as root in containers unless justified.
- Do not include dev dependencies in production artifacts unless necessary.
- Do not change deployment policy during unrelated feature work.

## Output

- Deploy risk summary.
- Commands checked.
- Env/config changes.
- Blockers.
