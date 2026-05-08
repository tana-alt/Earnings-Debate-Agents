# GPT Pro Improvement Review: Verification Harness

## Review Bounds

Subagent B performed a read-only review. No files were edited during the
subagent pass.

Source refs used: `Makefile`, `.github/workflows/ci.yml`, `hooks/`,
`scripts/check-*.sh`, `scripts/setup-agent-environment.sh`,
`tests/test_foundation_integrity.py`, `tests/test_contract_models.py`,
`pyproject.toml`, `docs/reference/verification-ci-and-pr-reference.md`, and
`docs/02-output-verification-contract.md`.

## Current Command Map

- `make sync`: `uv sync --frozen --group dev`
- `make doctor`: local tool/config inspection
- `make lint`: `ruff check .`
- `make format`: `ruff format .`
- `make typecheck`: `mypy`
- `make test`: `pytest`
- `make check-contracts`: contract model tests only
- `make check-doc-consistency`: targeted doc/worktree consistency tests
- `make check-hooks`: `sh -n` syntax checks for shell hooks/scripts
- `make check-shell`: ShellCheck
- `make check-hygiene`: tracked ignored files, forbidden roots, gitlinks, and
  nested `.git`
- `make check-secrets`: Gitleaks over tracked/current tree plus history when
  commits exist
- `make check-cd`: pytest guard proving deployment remains `not_applicable`
- `make check-required`: lint, typecheck, hook syntax, ShellCheck, hygiene,
  secrets, tests

## Trial 1

Initial reasoning: the harness is intentionally small and Makefile-centered.

What changed in reasoning: at first, the command surface looked appropriately
boring. The main improvement area did not look like “add more tools”; it looked
like “make sure this small map cannot drift.”

## Trial 2

Second pass focused on hook policy, CI, and whether files referenced by the
harness are packageable.

Hook policy:

- `hooks/pre-commit` runs `scripts/check-agent-worktree-policy.sh`.
- `hooks/pre-push` runs worktree policy, `make check-required`, and
  `make check-cd`.
- Worktree policy blocks detached HEAD, direct `main`/`master`, malformed
  branches, non-`agent/*` branches, the canonical root, and worktrees nested
  under the canonical root.
- `scripts/setup-agent-environment.sh` installs `core.hooksPath=hooks` and
  `foundation.canonicalRoot`.

CI posture:

- GitHub Actions runs on all pushes and PRs.
- Permissions are read-only.
- Timeout is 10 minutes.
- Python comes from `.python-version`.
- `uv` is pinned to `0.11.4`.
- Gitleaks is pinned to `8.30.1`; ShellCheck comes from apt.
- CI runs `make check-required`, then `make check-cd`.

What changed in reasoning: comparing the harness to Git tracking exposed a
concrete reproducibility gap. In the current worktree, hooks and
`scripts/check-*.sh` exist locally but several are untracked. The tests assert
files exist on disk, but do not assert required harness files are tracked.

## Trial 3

Third pass ran read-only checks:

- `make check-hooks`: passed.
- `sh scripts/check-dev-environment.sh`: passed.
- `sh scripts/check-repo-hygiene.sh`: passed.
- `sh scripts/check-shell-static-analysis.sh`: passed.
- `sh scripts/check-secrets.sh`: passed, but history scan was skipped because
  this repo currently has no commits.
- `sh scripts/check-agent-worktree-policy.sh`: failed as expected in canonical
  `main`.

What changed in reasoning: syntax/tool installation is not the weak point. The
remaining questions are design questions: tracked-file guarantees,
bootstrap/maintainer flow for strict worktree policy, secret scan scope, and CD
keyword guard brittleness.

## Test Coverage Summary

Current tests cover active doc size/routing, reference set consistency,
required files existing, forbidden roots, setup wiring, dev defaults, hook
wiring/executable bits, worktree policy behavior, repo hygiene behavior,
Makefile/CI wiring for shell/hygiene/secrets, skill root shape, CD readiness,
result-state spelling, work contract `git_scope`, and Pydantic validation of
YAML templates.

Main gap: required harness files are not asserted to be tracked by Git.

## Candidate Improvements

1. Add a tracked-file reproducibility test.
   Assert every required contract file, hook, script, workflow, template, and
   dev default appears in `git ls-files`.

2. Add a single harness inventory or drift test.
   The same shell files are listed in Makefile,
   `check-shell-static-analysis.sh`, tests, and docs. Either centralize this
   list or add a test proving the lists stay aligned.

3. Clarify bootstrap and human-maintainer behavior.
   Current hooks block commits from canonical `main`. That matches agent
   policy, but makes first commit or maintainer hotfix flow depend on
   `FOUNDATION_ALLOW_AGENT_POLICY_BYPASS=1`.

4. Decide secret scan scope.
   Current Gitleaks scan is appropriate for tracked/committable content, but
   does not scan ignored/untracked local files. That may be correct; document
   the boundary or add a separate opt-in local deep scan.

5. Revisit CD readiness guard brittleness.
   The guard blocks deployment configs/workflows and workflow lines containing
   deployment keywords. This is conservative but may false-positive on future
   harmless workflow text.

6. Consider CI determinism only if needed.
   `ubuntu-latest` and apt ShellCheck are acceptable for a small harness, but
   `ubuntu-24.04` and pinned ShellCheck would improve reproducibility.

## Rejected Complexity

- Do not add Nox/Tox or a custom Python task runner yet; Makefile is enough.
- Do not add deployment smoke tests while deployment is explicitly absent.
- Do not add broad e2e/browser checks for a docs/harness repo.
- Do not scan all ignored caches or local homes for secrets by default.
- Do not generate docs from command metadata unless drift becomes frequent.

## Exact GPT Pro Prompts

1. Given this Makefile/CI/hook architecture, should we add a test that asserts
   all required harness files are tracked by `git ls-files`? Current issue:
   hooks and `scripts/check-*.sh` exist and are executable locally but are
   untracked, while tests only assert filesystem existence.

2. Should the hook worktree policy block all commits from canonical `main`, or
   should it distinguish agent write work from human/bootstrap maintainer work?
   Is the `FOUNDATION_ALLOW_AGENT_POLICY_BYPASS=1` escape hatch sufficient?

3. Is the current Gitleaks strategy correct for this repo: scan tracked/current
   tree and history, but not untracked/ignored files? Should we add an opt-in
   deep local scan or keep required checks limited to committable surfaces?

4. Should the CD readiness guard stay as a conservative keyword/config absence
   check, or should it use an explicit denylist/allowlist of deployment actions
   to reduce false positives?

5. Is it worth centralizing the hook/script inventory shared by Makefile,
   ShellCheck script, docs, and tests, or is a simple drift test better than a
   manifest?

6. For CI reproducibility, should this repo pin `runs-on: ubuntu-24.04` and
   install a pinned ShellCheck binary, or is `ubuntu-latest` plus apt acceptable
   for this foundation harness?
