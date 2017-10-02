src_dir := iptun

python ?= python3.6
virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/pip
linter := $(virtualenv_dir)/bin/python -m flake8
py_requirements ?= requirements/prod.txt requirements/dev.txt
pytest := $(virtualenv_dir)/bin/py.test


.PHONY: test
test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):. $(pytest) --cov=$(src_dir) tests -s

.PHONY: lint
lint: $(virtualenv_dir)
	$(linter) $(src_dir)

$(virtualenv_dir): $(py_requirements)
	$(python) -m venv $@
	for r in $^ ; do \
		$(pip) install -r $$r ; \
	done
