publish-on-pypi:
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		python setup.py bdist_wheel --universal; \
		twine upload dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-pypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install pandas_datapackage_reader
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pandas_datapackage_reader as pdr; print(pdr.__version__)"

.PHONY: publish-on-pypi test-pypi-install

