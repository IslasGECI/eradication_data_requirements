all: check coverage mutants

.PHONY: \
		all \
		check \
		clean \
		coverage \
		format \
		green \
		init \
		install \
		linter \
		mutants \
		red \
		refactor \
		setup \
		tests

module = eradication_data_requirements
codecov_token = a48e7aa8-fdb9-477c-9027-18ca3d4d16ff

define lint
	pylint \
        --disable=bad-continuation \
        --disable=missing-class-docstring \
        --disable=missing-function-docstring \
        --disable=missing-module-docstring \
        ${1}
endef

check:
	black --check --line-length 100 ${module}
	black --check --line-length 100 tests
	flake8 --max-line-length 100 ${module}
	flake8 --max-line-length 100 tests
	mypy ${module}
	mypy tests

clean:
	rm --force --recursive .*_cache
	rm --force --recursive ${module}.egg-info
	rm --force --recursive ${module}/__pycache__
	rm --force --recursive tests/__pycache__
	rm --force .mutmut-cache
	rm --force coverage.xml

coverage: setup
	pytest --cov=${module} --cov-report=xml --verbose && \
	coverage report --show-missing

format:
	black --line-length 100 ${module}
	black --line-length 100 tests

init: init_git setup tests

init_git:
	git config --global --add safe.directory /workdir
	git config --global user.name "Ciencia de Datos • GECI"
	git config --global user.email "ciencia.datos@islas.org.mx"

install:
	pip install --editable .

linter:
	$(call lint, ${module})
	$(call lint, tests)

mutants: setup
	mutmut run --paths-to-mutate ${module} || \
	mutmut html

setup: clean install

tests:
	pytest --verbose

red: format
	git restore $(module) \
	&& (pytest --verbose tests/*.py) \
	&& git restore tests/*.py \
	|| (git add tests/*.py && git commit -m "🛑🧪 Fail tests")
	chmod g+w -R .

green: format
	git restore tests/*.py \
	&& (pytest --verbose tests/*.py) \
	&& (git add $(module)/*.py && git commit -m "✅ Pass tests") \
	|| git restore $(module)/*.py
	chmod g+w -R .

refactor: format
	pytest --verbose tests/*.py \
	&& (git add $(module)/*.py tests/*.py && git commit -m "♻️  Refactor") \
	|| git restore $(module)/*.py tests/*.py
	chmod g+w -R .
