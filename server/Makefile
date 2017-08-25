src_dir := pyvpnd

python ?= python3.6
virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/python -m pip
pytest := $(virtualenv_dir)/bin/py.test
linter := $(virtualenv_dir)/bin/python -m flake8
py_requirements ?= requirements/prod.txt requirements/dev.txt
mypy := $(virtualenv_dir)/bin/python -m mypy


.PHONY: test
test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):. $(pytest) --cov=$(src_dir) tests

.PHONY: lint
lint: $(virtualenv_dir)
	$(linter) $(src_dir)

.PHONY: check-types
check-types: $(virtualenv_dir)
	$(mypy) --ignore-missing-imports $(src_addr)

$(virtualenv_dir): $(py_requirements)
	$(python) -m venv $@
	for r in $^ ; do \
		$(pip) install -r $$r ; \
	done
