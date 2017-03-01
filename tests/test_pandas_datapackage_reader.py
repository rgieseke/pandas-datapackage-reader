import os

import pandas as pd

from pandas_datapackage_reader import read_datapackage


path = os.path.dirname(__file__)


def test_local_package():
    df = pd.read_csv(os.path.join(path, "test-package/data.csv"))
    dp = read_datapackage(os.path.join(path, "test-package"))
    assert df.equals(dp["data"])
    assert isinstance(dp, dict)
    assert "moredata" in dp.keys()
    assert "data" in dp.keys()


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
