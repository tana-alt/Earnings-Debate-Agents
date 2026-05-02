---
name: db-migration
description: "Use when changing database schema, indexes, constraints, migrations, seed data, backfills, or data migration strategy."
---


## Purpose

Make database changes deployable and reversible enough for the repo's release model.

## Use when

- Adding, changing, or removing columns, tables, indexes, constraints, or enums.
- Writing migrations, seed changes, backfills, or data cleanup scripts.
- Changing data access assumptions that depend on schema.

## Success conditions

- Migration is forward-safe for existing data.
- Rollback or mitigation is considered according to repo policy.
- Large-table locking and long-running operations are considered.
- App code and migration order are compatible.
- Indexes match new query patterns where relevant.

## Constraints

- Do not edit already-applied migrations unless the repo policy allows it.
- Do not combine risky schema and data migration without reason.
- Do not drop data before consumers are migrated.
- Do not assume nullable/non-nullable changes are safe without checking existing data.
- Do not run destructive migrations without explicit approval.

## Output

- Migration plan.
- Compatibility risk.
- Verification command or blocked reason.
