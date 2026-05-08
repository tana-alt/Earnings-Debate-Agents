# Final Subagent Supervision

## Result

Final read-only supervision found no remaining must-fix issues in the scoped
development-environment harness.

This report supersedes earlier advisory prompts in this packet where they have
already been implemented. Earlier files remain useful as reasoning history.

## Implemented After Review

- Made `docs/02-output-verification-contract.md` explicit that PR creation and
  updates are allowed for owned `agent/*` review branches when scope,
  ownership, verification, and evidence are clear.
- Made merge human-only. Scope cannot delegate merge authority.
- Kept direct pushes to `main` and `master` prohibited.
- Added `hooks/pre-push` destination-ref blocking so an agent branch cannot be
  pushed as `HEAD:main` or `HEAD:master`.
- Fixed the GitHub Actions Gitleaks bootstrap so checksum verification checks
  the archive filename that was actually downloaded.
- Changed `templates/project-storage-map.yaml` to use
  `<external-project-root>`, `<external-overlay-root>`, and `<project-id>`
  placeholders instead of repo-local project examples.
- Added clean-checkout reproducibility coverage for required tracked files and
  manifest-referenced plugin assets.
- Added structural extension checks for local skill front matter, skill-name
  uniqueness, skill-index coverage, plugin registry paths, manifests, MCP
  config shape, and plugin skill metadata.
- Renamed the imported Anthropic UI skill metadata name to
  `ui-anthropic-frontend-design` to avoid local skill-routing ambiguity.

## Subagent Closure

Final reviewer verdict:

- Must-fix findings: none.
- Optional improvements worth doing now under repo principles: none.
- Verification evidence is sufficient for this scope.

Rejected as overcomplex for now:

- Larger hook simulation harnesses beyond the protected destination-ref test.
- SLSA, cosign, or provenance verification for the Gitleaks CI bootstrap.
- Recursive interpretation of every plugin YAML asset reference.
- Broad skill-body or plugin-reference audits as required checks.

## Verification Evidence

Executed locally:

- `pytest -q tests/test_foundation_integrity.py tests/test_clean_checkout_reproducibility.py tests/test_extension_surface_integrity.py tests/test_contract_models.py`
  - Passed: 24 tests.
- `make check-hooks`
  - Passed.
- `make check-shell`
  - Passed.
- `git diff --check`
  - Passed.
- `make check-required`
  - Passed with Ruff, mypy, hook syntax checks, ShellCheck, repo hygiene,
    Gitleaks, and full pytest.
- `make check-cd`
  - Passed.

Sandbox note: `uv` commands needed escalated execution because the sandbox
could not read the user-level uv cache at `~/.cache/uv`.

## PR And Merge State

The repo currently has no local commits on `main`. I did not push to `main` and
did not merge anything.

The implemented policy now allows future agents to push owned `agent/*` review
branches and create or update PRs, while direct `main`/`master` pushes and merge
remain blocked or human-only.
