import os
import pandas as pd

from pandas_datapackage_reader import read_datapackage
from pathlib import Path


path = os.path.dirname(__file__)


def test_local_package():
    df = pd.read_csv(os.path.join(path, "test-package/data.csv"))
    dp = read_datapackage(os.path.join(path, "test-package"))
    assert df.equals(dp["data"])
    assert isinstance(dp, dict)
    assert "moredata" in dp.keys()
    assert "data" in dp.keys()


def test_load_single_resource():
    df = pd.read_csv(os.path.join(path, "test-package/moredata.csv"))
    moredata = read_datapackage(os.path.join(path, "test-package"), "moredata")
    assert df.equals(moredata)


def test_load_multiple_resources():
    dp = read_datapackage(os.path.join(path, "test-package"),
                          ["data", "moredata"])
    assert "data" in dp.keys()
    assert "moredata" in dp.keys()


def test_remote_package():
    url = ("https://raw.githubusercontent.com/datasets/"
           "country-codes/master/datapackage.json")
    dp = read_datapackage(url)
    print(dp)
    assert isinstance(dp, pd.DataFrame)


def test_github_url():
    url = "https://github.com/datasets/country-codes"
    dp = read_datapackage(url)
    print(dp)
    assert isinstance(dp, pd.DataFrame)


def test_github_url_with_trailing_slash():
    url = "https://github.com/datasets/country-codes/"
    dp = read_datapackage(url)
    print(dp)
    assert isinstance(dp, pd.DataFrame)

def test_pathlib_posixpath():
    path = Path(__file__).parents[0]
    dp = read_datapackage(path / "test-package")
    assert "data" in dp.keys()
