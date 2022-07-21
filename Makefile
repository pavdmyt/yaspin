OK_COLOR := $(shell tput -Txterm setaf 2)
NO_COLOR := $(shell tput -Txterm sgr0)

.PHONY: build

name='yaspin'

# Use $$ if running awk inside make
# https://lists.freebsd.org/pipermail/freebsd-questions/2012-September/244810.html
version := $(shell poetry version | awk '{ print $$2 }')
pypi_usr := $(shell grep username ~/.pypirc | awk -F"= " '{ print $$2 }')
pypi_pwd := $(shell grep password ~/.pypirc | awk -F"= " '{ print $$2 }')

flake:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@poetry run flake8 --ignore=F821,E501,W503 .

lint:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@poetry run pylint $(name)/ ./tests -rn -f colorized

isort:
	@poetry run isort --atomic --verbose --only-modified --line-length=88 $(name)/ tests/ examples/

fmt: isort
	@poetry run black ./$(name) ./tests ./examples

check-fmt:
	@poetry run isort --check --line-length=88 $(name)/ tests/ examples/
	@poetry run black --check ./$(name) ./tests ./examples

spellcheck:
	@cspell -c .cspell.json $(name)/*.py tests/*.py examples/*.py README.rst HISTORY.rst pyproject.toml Makefile

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done

clean-pyc:
	@echo "$(OK_COLOR)==> Cleaning bytecode ...$(NO_COLOR)"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

test: clean-pyc flake
	@echo "$(OK_COLOR)==> Runnings tests ...$(NO_COLOR)"
	@poetry run py.test -n auto -v

coverage: clean-pyc
	@echo "$(OK_COLOR)==> Calculating coverage...$(NO_COLOR)"
	@poetry run py.test --cov-report=term --cov-report=html --cov-report=xml --cov $(name) tests/
	@echo "open file://`pwd`/htmlcov/index.html"

rm-build:
	@rm -rf build dist .egg $(name).egg-info

check-rst:
	@echo "$(OK_COLOR)==> Checking RST will render...$(NO_COLOR)"
	@twine check dist/*

build: rm-build
	@echo "$(OK_COLOR)==> Building...$(NO_COLOR)"
	@poetry build

publish: flake build check-rst
	@echo "$(OK_COLOR)==> Publishing...$(NO_COLOR)"
	@poetry publish -u $(pypi_usr) -p $(pypi_pwd)

tag:
	@echo "$(OK_COLOR)==> Creating tag $(version) ...$(NO_COLOR)"
	@git tag -a "v$(version)" -m "Version $(version)"
	@echo "$(OK_COLOR)==> Pushing tag $(version) to origin ...$(NO_COLOR)"
	@git push origin "v$(version)"

bump:
	@poetry version patch

bump-minor:
	@poetry version minor

export-requirements:
	@poetry export -f requirements.txt --dev > requirements.txt
