OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

.PHONY: build

flake:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@flake8 .

lint:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@pylint setup.py yaspin/ -rn -f colorized

isort-all:
	isort -rc --atomic --verbose setup.py yaspin/

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done

clean-pyc:
	@echo "$(OK_COLOR)==> Cleaning bytecode ...$(NO_COLOR)"
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

test: clean-pyc flake
	@echo "$(OK_COLOR)==> Runnings tests ...$(NO_COLOR)"
	@py.test -v

coverage: clean-pyc
	@echo "$(OK_COLOR)==> Calculating coverage...$(NO_COLOR)"
	@py.test --cov-report term --cov-report html --cov yaspin tests/
	@echo "open file://`pwd`/htmlcov/index.html"

rm-build:
	@rm -rf build dist .egg yaspin.egg-info

# requires docutils and pygments to be installed
# -s stands for strict (raises errors instead of warnings)
check-rst:
	@python setup.py check --restructuredtext -s

build: rm-build
	@echo "$(OK_COLOR)==> Building...$(NO_COLOR)"
	@python setup.py sdist
	@python setup.py bdist_wheel --universal

publish: check-rst rm-build
	@echo "$(OK_COLOR)==> Publishing...$(NO_COLOR)"
	@python setup.py sdist upload -r pypi
	@python setup.py bdist_wheel --universal upload -r pypi
