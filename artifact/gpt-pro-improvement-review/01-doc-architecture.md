# GPT Pro Improvement Review: Doc Architecture

## Review Bounds

Subagent A performed a read-only review. No files were edited during the
subagent pass.

Source refs inspected: `AGENTS.md`, `README.md`,
`docs/01-agent-operating-contract.md`,
`docs/02-output-verification-contract.md`,
`docs/03-repo-boundary-and-storage-contract.md`, `docs/reference/*.md`, and
`templates/*.yaml`.

Verification: manual inspection plus targeted consistency checks. Runtime tests
were not applicable because this was documentation review only.

## Repo Context For GPT Pro

- `AGENTS.md`: compact agent entrypoint and routing map.
- `docs/01-agent-operating-contract.md`: scope, context boundary, write
  preconditions, side effects, and rework.
- `docs/02-output-verification-contract.md`: output shape, verification order,
  PR/handoff evidence, and human gates.
- `docs/03-repo-boundary-and-storage-contract.md`: repo truth, storage
  boundaries, secrets, skills, and plugins.
- `docs/reference/`: detailed routed references for runtime/scope, packets and
  evidence, repo storage, verification/CI/PR, git worktrees, and migration.
- `templates/*.yaml`: reusable work contract, evidence, verification, rework,
  and project storage map templates.
- `README.md`: human overview, restore instructions, and main folder map.

The foundation principle is compact active context: routine agents should read
`AGENTS.md`, the user request, named refs, and only the reference needed for the
current scope. Detailed examples stay in routed references, not active docs.

## Trial 1

Initial reasoning: the architecture is broadly coherent. `AGENTS.md` stays
compact, active docs are short, and references hold operational detail.

What changed: the review moved from “is the architecture sound?” to “where
could compactness become ambiguity?”

Why: the core routing pattern is already supported by `AGENTS.md`, `README.md`,
and the three active contracts.

## Trial 2

Second reasoning: the best GPT Pro questions are consistency questions, not new
system questions.

Evidence-backed tensions:

- Docs list `optional_refs`, while `templates/work-contract.yaml` uses
  `required_context` and `optional_context`.
- `docs/reference/repo-boundary-and-storage-reference.md` says not to introduce
  default roots such as `projects/`, but `templates/project-storage-map.yaml`
  uses `projects/example_project`.
- `docs/01-agent-operating-contract.md` says hooks block agent writes on the
  canonical root, while the verification reference describes hooks mainly as
  commit/push guardrails.
- Human gate lists appear in both the active output contract and the
  verification reference.
- The git reference both requires `base_ref` for parallel work and gives
  fallback behavior when `base_ref` is not supplied.

What changed: candidate improvements narrowed to places where a future agent
may follow the wrong template or over-read the wrong reference.

## Trial 3

Final reasoning: ask GPT Pro only for minimal clarifications that preserve
compact context.

What changed: broad additions such as scheduler state, repo-level project
storage, runtime ledgers, or moving examples into active docs were rejected.

Why: those changes conflict with the strongest current principles: compact
active docs, routed references, no broad runtime state, no secret/local state,
and no default project storage root.

## Candidate Improvements

1. Align work contract field names.
   Ask whether `templates/work-contract.yaml` should use documented names like
   `optional_refs`, or whether docs should explicitly define
   `required_context` and `optional_context`.

2. Clarify project storage template paths.
   Ask whether `templates/project-storage-map.yaml` should replace
   `projects/example_project` with a neutral placeholder such as
   `<project-root>/...`.

3. De-duplicate human gate wording.
   Ask whether `docs/02-output-verification-contract.md` should remain the
   canonical human-gate list, with references linking back instead of
   restating near-duplicate lists.

4. Clarify hook enforcement language.
   Ask whether active docs should distinguish contract-level write prohibition
   from hook-level commit/push enforcement.

5. Resolve `base_ref` derivation rules.
   Ask whether missing `base_ref` is always rework for parallel work, or
   whether deriving it from `origin/HEAD` is allowed under a specific
   single-lane/local-write condition.

6. Add a tiny read-only output rule.
   Ask whether read-only advisory reviews may mark changed paths and runtime
   verification as `not_applicable`, while still citing source refs and
   residual risk.

## Rejected Improvements

- Do not add a scheduler, queue, lock ledger, dashboard root, or runtime plan
  store.
- Do not make this foundation repo a generic project storage root.
- Do not require routine agents to read all references, skills, plugin
  payloads, logs, or archives.
- Do not move detailed examples from `docs/reference/` into active docs.
- Do not broaden verification so every read-only review must run the full
  required check chain.

## Exact GPT Pro Prompts

1. Review this documentation architecture for a compact agent foundation repo.
   Active docs are intentionally short; detailed procedures live in
   `docs/reference/`. Should the work contract template field names be aligned
   with the documented scope fields? In particular, docs mention
   `optional_refs`, while `templates/work-contract.yaml` uses
   `required_context` and `optional_context`. Recommend the smallest wording or
   template change, or explain why no change is needed.

2. The repo forbids introducing default roots such as `projects/`, but
   `templates/project-storage-map.yaml` uses `projects/example_project` as its
   example canonical root. Should this be changed to a neutral placeholder like
   `<project-root>/...` to avoid teaching the wrong storage pattern?

3. Human gate rules are stated in the active output contract and restated in
   the verification reference. Should the active contract be the sole canonical
   list with references linking back, or is the duplication useful enough to
   keep?

4. The active operating contract says installed hooks block agent writes on the
   canonical root or non-`agent/*` branches, while the verification reference
   describes hooks as pre-commit/pre-push guardrails. Should the wording
   distinguish contract-level write prohibition from hook-level commit/push
   enforcement?

5. The git worktree reference requires `base_ref` for parallel work but also
   describes inspecting `origin/HEAD` when `base_ref` is not supplied. Should
   derivation of `base_ref` be allowed, and if so under what exact scope?

6. The output contract says every meaningful output must state changed
   paths/artifact refs, evidence, verification, unverified surfaces, and
   residual risk. Should there be a one-sentence rule for read-only advisory
   reviews where changed paths and runtime checks are `not_applicable`, while
   source refs and residual risk remain required?
