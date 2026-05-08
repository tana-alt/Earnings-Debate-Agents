---
status: reference
owner: foundation
source_of_truth_level: reference
created_at: 2026-05-06
---

# Packet, Evidence, And Rework Reference

Use this reference when creating or reviewing work contracts, packets, evidence
records, verification records, and rework records. Keep records small and use
refs instead of raw bodies or logs.

## Work Contract Fields

A work contract defines one bounded unit of work for a human, LLM session,
script, automation, review lane, or release lane.

Core fields:

- `task_intent`
- `success_criteria`
- `source_refs`
- `optional_refs`
- `expected_outputs`
- `allowed_write_targets`
- `denied_context`
- `evidence_required`
- `verification_required`
- `git_scope`
- `artifact_refs`
- `changed_paths`
- `decision_refs`
- `verification_results`
- `residual_risk`
- `blockers`
- `open_questions`
- `next_action`

Identity fields such as `work_id`, `run_id`, `project_id`, `correlation_id`,
and `idempotency_key` are required when concurrency, retry safety, handoff, or
stored records need them. Templates may show placeholders; delete or leave empty
identity fields that were not supplied by scope.

Use `git_scope` in work contract boundaries when branch or worktree isolation
matters:

```yaml
git_scope:
  mode: single | parallel
  base_ref: origin/main
  merge_target: origin/main
  branch_target: agent/<work_id>/<lane>/<slug>
  worktree_target: ../worktrees/<repo>/<work_id>-<lane>
  sibling_branch_refs: []
  conflict_policy: no_overlap
```

## Ref Fields

Prefer refs over embedded bodies:

- `source_refs`
- `artifact_refs`
- `evidence_refs`
- `verification_refs`
- `decision_refs`
- `content_ref`
- `body_ref`
- `rework_refs`

Do not embed raw bodies, credentials, tokens, cookies, browser sessions, local
logs, secret-bearing metadata, or unrelated context in docs, packets, records,
prompts, or artifacts.

## Evidence Rules

Evidence should separate observed facts from inference.

- Cite concrete source refs.
- Put observations under `facts`.
- Put conclusions under `inferences` and label them as inference.
- Record decisions separately from facts and inferences.
- State missing evidence, stale refs, confidence, residual risk, and next action.
- Preserve enough detail for another worker to reproduce the check.

## Verification Records

Each verification record should include check name, method or command, result
state, evidence ref, unverified surfaces, residual risk, and next action.

Result states:

- `passed`: check ran and passed.
- `failed`: check ran and failed.
- `blocked`: check could not run because of a blocker.
- `skipped`: check was intentionally not run.
- `not_applicable`: check does not apply to this work unit.

## Rework

Return rework when work is incomplete, unsafe, unverifiable, ambiguous, missing
required context, missing permission, missing evidence, mismatched to contract,
or conflicting with repo truth.

A useful rework record includes type, blocker summary, failed or missing
requirement, evidence refs, requested repair, and suggested next action. Use
`work_id` or `project_id` only when the scope already provides them or handoff
safety requires them.

Common types: `missing_context`, `ambiguous_instruction`, `contract_mismatch`,
`verification_failed`, `evidence_gap`, `unsafe_assumption`,
`blocked_dependency`, and `scope_conflict`.

## Template Locations

Use `templates/work-contract.yaml`, `templates/evidence-record.yaml`,
`templates/verification-record.yaml`, and `templates/rework-record.yaml` when the
task asks for structured records.
