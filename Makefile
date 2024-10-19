OK_COLOR := $(shell tput -Txterm setaf 2)
NO_COLOR := $(shell tput -Txterm sgr0)

name='yaspin'

# Use $$ if running awk inside make
# https://lists.freebsd.org/pipermail/freebsd-questions/2012-September/244810.html
version := $(shell poetry version | awk '{ print $$2 }')
pypi_usr := $(shell grep username ~/.pypirc | awk -F"= " '{ print $$2 }')
pypi_pwd := $(shell grep password ~/.pypirc | awk -F"= " '{ print $$2 }')

.PHONY: lint
lint:
	@poetry run ruff check --fix ./$(name) ./tests ./examples

.PHONY: check-lint
check-lint:
	@poetry run ruff check --diff ./$(name) ./tests ./examples

.PHONY: fmt
fmt:
	@poetry run ruff format ./$(name) ./tests ./examples

.PHONY: check-fmt
check-fmt:
	@poetry run ruff format --check ./$(name) ./tests ./examples

.PHONY: spellcheck
spellcheck:
	@cspell -c .cspell.json $(name)/*.py tests/*.py examples/*.py README.md HISTORY.rst pyproject.toml Makefile

.PHONY: clean
clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done

.PHONY: clean-pyc
clean-pyc:
	@echo "$(OK_COLOR)==> Cleaning bytecode ...$(NO_COLOR)"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: test
test: clean-pyc
	@echo "$(OK_COLOR)==> Runnings tests ...$(NO_COLOR)"
	@poetry run py.test -n auto -v

.PHONY: coverage
coverage: clean-pyc
	@echo "$(OK_COLOR)==> Calculating coverage...$(NO_COLOR)"
	@poetry run py.test --cov-report=term --cov-report=html --cov-report=xml --cov $(name) tests/
	@echo "open file://`pwd`/htmlcov/index.html"

.PHONY: rm-build
rm-build:
	@rm -rf build dist .egg $(name).egg-info

.PHONY: build
build: rm-build
	@echo "$(OK_COLOR)==> Building...$(NO_COLOR)"
	@poetry build

.PHONY: publish
publish: build
	@echo "$(OK_COLOR)==> Publishing...$(NO_COLOR)"
	@poetry publish -u $(pypi_usr) -p $(pypi_pwd)

.PHONY: tag
tag:
	@echo "$(OK_COLOR)==> Creating tag $(version) ...$(NO_COLOR)"
	@git tag -a "v$(version)" -m "Version $(version)"
	@echo "$(OK_COLOR)==> Pushing tag $(version) to origin ...$(NO_COLOR)"
	@git push origin "v$(version)"

.PHONY: bump
bump:
	@poetry version patch

.PHONY: bump-minor
bump-minor:
	@poetry version minor

.PHONY: export-requirements
export-requirements:
	@poetry export -f requirements.txt --with dev > requirements.txt

.PHONY: semgrep
semgrep:
	poetry run semgrep --error --config "p/secrets" --config "p/bandit" --config "p/secrets" .

.PHONY: mypy
mypy:
	@poetry run mypy $(name)/
