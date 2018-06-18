publish-on-pypi:
	@rm -rf build dist
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		./venv/bin/python setup.py bdist_wheel --universal; \
		./venv/bin/twine upload dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-pypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install pandas_datapackage_reader
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pandas_datapackage_reader as pdr; print(pdr.__version__)"

venv:
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install pytest pytest-cov
	./venv/bin/pip install twine wheel setuptools --upgrade
	./venv/bin/pip install -e .

.PHONY: publish-on-pypi test-pypi-install venv

