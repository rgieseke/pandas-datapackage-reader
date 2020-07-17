"""
pandas-datapackage-reader
-------------------------

Easy loading of tabular data from Data Packages into Pandas DataFrames.

Install using ::

    pip install pandas-datapackage-reader

See README.md and repository for details: <https://github.com/rgieseke/pandas-datapackage-reader>
"""

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import versioneer


path = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.exit(pytest.main(self.test_args))


with open(os.path.join(path, "README.md"), "r") as f:
    readme = f.read()


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": PyTest})

REQUIREMENTS = ["pandas>=0.24.0", "requests"]
REQUIREMENTS_EXTRAS = {"tests": ["pytest>=4.1", "geopandas"]}

setup(
    name="pandas-datapackage-reader",
    version=versioneer.get_version(),
    description="Pandas Data Package Reader",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rgieseke/pandas-datapackage-reader",
    author="Robert Gieseke",
    author_email="robert.gieseke@pik-potsdam.de",
    license="BSD",
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["data-package"],
    cmdclass=cmdclass,
    packages=["pandas_datapackage_reader"],
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRAS,
)
