publish-on-pypi:
	python setup.py register -r https://pypi.python.org/pypi
	python setup.py sdist upload -r https://pypi.python.org/pypi

test-pypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install pandas_datapackage_reader
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pandas_datapackage_reader as pdr; print(pdr.__version__)"

.PHONY: publish-on-pypi test-pypi-install publish-on-testpypi test-testpypi-install

