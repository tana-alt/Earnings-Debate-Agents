UV ?= uv

.PHONY: help sync doctor lint format typecheck test check-toolchain check-contracts check-doc-consistency check-hooks check-shell check-hygiene check-secrets check-cd check-required check-foundation

help:
	@printf '%s\n' \
		'Targets:' \
		'  make sync                  Install locked dev dependencies' \
		'  make doctor                Inspect local dev environment without changing it' \
		'  make lint                  Run ruff' \
		'  make format                Format supported files with ruff' \
		'  make typecheck             Run mypy' \
		'  make test                  Run pytest' \
		'  make check-toolchain       Report local toolchain versions' \
		'  make check-contracts       Run contract model tests' \
		'  make check-doc-consistency Run doc consistency tests' \
		'  make check-hooks           Run shell syntax checks on hooks/scripts' \
		'  make check-shell           Run ShellCheck on tracked shell hooks/scripts' \
		'  make check-hygiene         Run repo hygiene guardrails' \
		'  make check-secrets         Run Gitleaks with redacted output' \
		'  make check-required        Run required local checks' \
		'  make check-cd              Run deployment-readiness guard' \
		'  make check-foundation      Run the Foundation Robustness Gate'

sync:
	$(UV) sync --frozen --group dev

doctor:
	sh scripts/check-dev-environment.sh

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run mypy

test:
	$(UV) run pytest

check-toolchain:
	@git --version | sed 's/^/ok: /'
	@$(UV) --version | sed 's/^/ok: /'
	@python3 --version | sed 's/^/ok: /'
	@shellcheck --version | sed -n 's/^version: /ok: shellcheck /p' | head -n 1
	@gitleaks version | sed 's/^/ok: gitleaks /'

check-contracts:
	$(UV) run pytest tests/test_contract_models.py

check-doc-consistency:
	$(UV) run pytest tests/test_foundation_integrity.py -k "doc_consistency or work_contract_git_scope"

check-hooks:
	sh -n scripts/setup-agent-environment.sh
	sh -n scripts/check-agent-worktree-policy.sh
	sh -n scripts/check-dev-environment.sh
	sh -n scripts/check-repo-hygiene.sh
	sh -n scripts/check-secrets.sh
	sh -n scripts/check-shell-static-analysis.sh
	sh -n hooks/pre-commit
	sh -n hooks/pre-push

check-shell:
	sh scripts/check-shell-static-analysis.sh

check-hygiene:
	sh scripts/check-repo-hygiene.sh

check-secrets:
	sh scripts/check-secrets.sh

check-cd:
	$(UV) run pytest tests/test_foundation_integrity.py -k cd_readiness

check-required: lint typecheck check-hooks check-shell check-hygiene check-secrets test

check-foundation: check-toolchain check-required check-cd
