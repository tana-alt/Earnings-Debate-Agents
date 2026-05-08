# GPT Pro improvement review

## 1. Prioritized recommendation table

| Priority | Topic                                                                | Decision                                            | Recommendation                                                                                                                                                                                          |
| -------: | -------------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|       P0 | Required files tracked by `git ls-files`                             | **Implement now**                                   | Add a focused pytest that asserts required docs, hooks, scripts, templates, workflows, and dev defaults are tracked. This directly addresses clean-checkout reproducibility before initial commit.      |
|       P0 | `templates/project-storage-map.yaml` uses `projects/example_project` | **Implement now**                                   | Replace it with an explicit external placeholder such as `"<external-project-root>"` or `"/abs/path/to/external-project-root"`. The current example conflicts with the no-default-`projects/` boundary. |
|       P0 | Worktree hook language                                               | **Implement now**                                   | Clarify that repo policy forbids certain writes, while hooks only enforce commit/push boundaries. Hooks are not runtime monitors.                                                                       |
|       P1 | Human gate rule duplication                                          | **Implement now**                                   | Make `docs/02-output-verification-contract.md` canonical. References may summarize or give examples, but should not maintain an independent normative list.                                             |
|       P1 | Minimal `.agents/skills/` and `plugins/` integrity checks            | **Implement now, narrowly**                         | Add structural validation only: required files exist, metadata parses, indexes cover local entries, manifest paths are relative and resolve inside allowed roots. No install/load/runtime execution.    |
|       P1 | Required Gitleaks scope                                              | **Implement now as wording / config clarification** | Required scans should remain limited to committable content and Git history. Ignored/untracked local state should remain out of required CI/hook scope.                                                 |
|       P2 | Optional deep local secret scan                                      | **Ask GPT Pro follow-up or defer**                  | Acceptable only as opt-in developer hygiene, with explicit exclusions. Do not make it required.                                                                                                         |
|       P2 | License/provenance enforcement for skills/plugins                    | **Defer**                                           | Add only if external/vendored payloads or marketplace distribution are real. Otherwise it becomes premature package-governance work.                                                                    |
|       P2 | MCP/plugin smoke execution                                           | **Defer**                                           | Parse config and validate paths now; do not execute servers, install packages, or run integration smoke tests yet.                                                                                      |
|       P3 | Runtime queue, lock ledger, dashboard root, project-state DB         | **Reject**                                          | Explicitly outside foundation scope and inconsistent with the compact-agent premise.                                                                                                                    |
|       P3 | Default repo `projects/` root                                        | **Reject**                                          | This would turn the foundation into a storage root, which the repo policy already forbids.                                                                                                              |
|       P3 | Heavy package-manager model for skills/plugins                       | **Reject for now**                                  | Manifest registries, provenance graphs, dependency resolution, and marketplace semantics are overbuilt unless distribution becomes a concrete goal.                                                     |

---

## 2. Implement-now: exact minimal file-level changes

### A. Clean-checkout reproducibility test

Add one pytest file:

```text
tests/test_clean_checkout_reproducibility.py
```

Purpose:

* Assert each required harness/doc/config file is present in `git ls-files`.
* Do **not** require `git status` to be clean.
* Do **not** scan or require ignored/untracked runtime state.
* Keep the list finite and contractual, not "everything in the repo."

The required path list should include, at minimum:

```text
Makefile
pyproject.toml
.pre-commit-config.yaml            # if present / required
.gitleaks.toml                     # if present / required
.github/workflows/...              # all required CI workflows
scripts/...                        # required check scripts
.githooks/... or hooks/...          # required local hook entrypoints
templates/project-storage-map.yaml
docs/02-output-verification-contract.md
docs/reference/...                 # only reference docs that active docs route to as required
.agents/skills/SKILL_INDEX.md      # if this index is a required surface
.agents/skills/*/SKILL.md          # required skill definitions
plugins/*/manifest.* or plugin.*   # required plugin manifests, using the repo's actual convention
```

Optional but still small:

* For hook/shell entrypoints, assert executable bit only where execution depends on it.
* Do not add a separate manifest file unless the inline pytest list becomes hard to maintain.

---

### B. External project placeholder

Edit:

```text
templates/project-storage-map.yaml
```

Change any value like:

```text
projects/example_project
```

to a clearly external placeholder, for example:

```text
"<external-project-root>"
```

or:

```text
"/abs/path/to/external-project-root"
```

Also add a short comment in the template:

```text
# This is external to the foundation repo.
# Do not create a default projects/ root inside this repository.
```

Add or extend one existing boundary/template test:

```text
tests/test_repo_boundary.py
```

or equivalent existing hygiene test.

Minimal assertion:

* `templates/project-storage-map.yaml` must not contain `projects/example_project`.
* It should not imply a default top-level `projects/` root inside the foundation repo.

---

### C. Human gate canonicalization

Edit:

```text
docs/02-output-verification-contract.md
```

Make this the only canonical location for human gate rules.

Then edit the existing verification reference, for example:

```text
docs/reference/output-verification.md
```

or the repo's equivalent file.

Change any duplicated normative gate list into:

```text
Canonical human gate rules are defined in docs/02-output-verification-contract.md.
This reference may provide examples and operational notes only.
```

Keep examples if useful, but label them as examples, not policy.

---

### D. Worktree hook scope clarification

Edit the existing hook/worktree reference, for example:

```text
docs/reference/worktree-hooks.md
```

or the repo's equivalent file.

Add a distinction like this:

```text
Contract-level prohibition:
Agents must not write prohibited runtime, cache, secret, log, or external project state into repo truth.

Hook-level enforcement:
Hooks only block commits or pushes that would introduce tracked policy violations. They do not monitor every filesystem write and do not make ignored/untracked local state part of repo truth.
```

If the active verification doc mentions hooks, add one sentence there pointing to the reference and preserving this distinction.

No hook implementation change is required unless current hooks claim broader enforcement than they actually provide.

---

### E. Minimal extension-surface validation

Add one pytest file:

```text
tests/test_extension_surface_integrity.py
```

Scope should stay structural.

For `.agents/skills/`:

* Every skill directory has a `SKILL.md`.
* `SKILL.md` metadata/front matter parses, if front matter is the repo convention.
* Required metadata should be minimal: `name` and `description` are enough.
* If `.agents/skills/SKILL_INDEX.md` exists, it should cover every local skill directory exactly once.
* Do not require routine agents to read every skill.

For `plugins/`:

* Every plugin directory has the repo's chosen manifest file.
* Use one manifest convention if possible; avoid supporting many equivalent names.
* Required fields should be minimal: `id`, `name`, `description`, and declared local path/entrypoint if applicable.
* Referenced paths must be relative.
* Referenced paths must resolve inside the plugin directory or allowed plugin surface.
* No absolute paths.
* No `..` path escapes.
* Marketplace or registry entries, if present, must point to existing relative paths under `plugins/`.

For MCP config samples:

* Parse JSON/YAML only.
* Validate top-level shape and required keys.
* Validate referenced paths.
* Do not launch servers.
* Do not install dependencies.
* Do not perform network calls.

Do **not** add:

* Package installation tests.
* Plugin runtime smoke tests.
* Marketplace dependency resolution.
* Provenance graphs.
* Checksum registries.

If no concise contract exists, add or update:

```text
docs/reference/extension-surface-contract.md
```

Keep it to one page-equivalent: required files, required metadata fields, path rules, and non-goals.

---

### F. Gitleaks scope wording

Edit the existing security/hygiene reference, for example:

```text
docs/reference/security-hygiene.md
```

or equivalent.

Clarify:

```text
Required secret scanning covers committable content and Git history.
Ignored and untracked local state is outside required CI/hook scope.
Optional local deep scans may be run manually, but they are not repo truth and are not required for CI.
```

If the Makefile currently scans ignored/untracked state by default, change the default target to match the required scope. Otherwise no Makefile change is needed.

---

## 3. Direct answers to the six questions

### 1. Should the repo add a `git ls-files` tracked-file reproducibility test?

**Yes. Implement now.**

This is the strongest improvement in the packet. Current local existence checks can pass even when required files are untracked. A clean checkout only sees tracked files, so initial commit reproducibility depends on this.

The test should be narrow:

* assert required paths are tracked;
* avoid asserting a clean working tree;
* avoid scanning ignored runtime/local state;
* avoid trying to infer every possible important file dynamically.

The goal is not "no untracked files." The goal is "all required foundation files are committed."

---

### 2. Should `templates/project-storage-map.yaml` replace `projects/example_project`?

**Yes. Implement now.**

`projects/example_project` is a misleading example because the repo explicitly forbids becoming a default storage root for projects. Use an external placeholder.

Best replacement:

```text
"<external-project-root>"
```

or:

```text
"/abs/path/to/external-project-root"
```

Add a comment that the path is outside the foundation repo.

---

### 3. Should human gate rules be canonical only in `docs/02-output-verification-contract.md`?

**Yes.**

`docs/02-output-verification-contract.md` should be canonical. The reference doc may contain examples, explanations, and implementation notes, but it should not maintain a second normative list.

Reason: human gates are policy, and duplicated policy text is likely to drift. Compact active docs work only if the canonical source is obvious.

Recommended pattern:

```text
Canonical rule: active doc.
Reference doc: examples and operational notes.
```

---

### 4. Should worktree hook language distinguish contract-level prohibition from hook-level enforcement?

**Yes. Implement now.**

This distinction prevents overclaiming.

Correct model:

| Layer            | Meaning                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------------- |
| Contract         | Agents must not write prohibited runtime/cache/log/secret/project state into repo truth. |
| Hooks            | Hooks block commits or pushes that introduce tracked violations.                         |
| Local filesystem | Ignored/untracked state is not fully policed by default hooks and is not repo truth.     |

Hooks are guardrails, not a runtime monitor.

---

### 5. What minimal integrity checks should exist for `.agents/skills/` and `plugins/`?

**Implement structural integrity checks only.**

Minimum acceptable checks:

| Surface                           | Minimal check                                                             |
| --------------------------------- | ------------------------------------------------------------------------- |
| `.agents/skills/<skill>/SKILL.md` | Required file exists.                                                     |
| Skill front matter                | Parseable if used; require only `name` and `description`.                 |
| `SKILL_INDEX.md`                  | Covers each local skill directory exactly once, if the index exists.      |
| Plugin manifests                  | Required manifest exists and parses.                                      |
| Plugin IDs/names                  | Non-empty and locally unique.                                             |
| Plugin paths                      | Relative, no `..`, no absolute paths, resolve inside allowed plugin root. |
| Marketplace/registry paths        | Relative paths under `plugins/`, target exists.                           |
| MCP config samples                | Parse shape only; validate referenced paths; no execution.                |

Do not add runtime loading, package installation, dependency resolution, network tests, or marketplace governance.

License/provenance checks should be deferred unless the repo actually vendors external payloads or distributes plugins as independent artifacts.

---

### 6. Should required Gitleaks remain limited to tracked/current tree and Git history?

**Yes.**

Required scans should target committable content and Git history. That is what CI and repo truth can consistently enforce.

Ignored/untracked local state should remain out of required scope because:

* CI cannot reliably see it;
* ignored state may include `.venv`, caches, logs, archives, and local scratch;
* broad scans create false positives and slow checks;
* the repo explicitly says local runtime state is not repo truth.

An opt-in deep local scan is acceptable only as a manual developer target, not as a required hook or CI gate.

---

## 4. Likely overfitting / overengineering in the packet

The following ideas should be constrained or rejected:

1. **Tracked-file reproducibility test that enumerates too much**

   Good:

   ```text
   required harness files must be tracked
   ```

   Overfit:

   ```text
   every doc, every reference, every local helper, every generated artifact must be tracked
   ```

2. **Independent duplicate human-gate lists**

   A restated reference list feels helpful, but it creates policy drift. Keep one canonical list.

3. **Treating hooks as full write-prevention**

   Hooks can block commits and pushes. They cannot guarantee agents never write temporary files locally.

4. **Skill/plugin package-manager design**

   Front matter, index coverage, manifest parsing, and path checks are enough now. Dependency graphs, provenance registries, checksums, marketplace semantics, and package resolution are premature.

5. **Default deep scans of ignored/untracked local state**

   This conflicts with the repo boundary model. Optional local scans are fine; required broad scans are not.

6. **License/provenance automation before distribution**

   If plugins/skills are local foundation examples, top-level repo licensing is enough. Per-plugin provenance should wait until external vendoring or marketplace distribution exists.

7. **Deployment smoke tests while deployment is `not_applicable`**

   Do not add deployment verification until deployment becomes a real surface.

8. **Runtime state infrastructure**

   Scheduler, queue, lock ledger, dashboard root, runtime plan store, and project-state DB should remain rejected. They contradict the compact foundation premise.

---

## Bottom line

Implement now:

```text
1. git ls-files clean-checkout reproducibility test
2. external project placeholder in templates/project-storage-map.yaml
3. canonical human gate source in docs/02-output-verification-contract.md
4. explicit contract-vs-hook enforcement wording
5. minimal structural checks for skills/plugins
6. clarified required Gitleaks scope
```

Defer or reject anything that turns the repo into:

```text
a runtime system,
a project storage root,
a package manager,
a marketplace registry,
or a broad local-state scanner.
```
