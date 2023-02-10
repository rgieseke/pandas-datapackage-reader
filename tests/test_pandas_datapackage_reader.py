import os
import pandas as pd
import numpy as np
import pytest
import requests
import sys

from datetime import datetime, date, time
from pandas_datapackage_reader import read_datapackage


path = os.path.dirname(__file__)


def test_local_package():
    dp = read_datapackage(os.path.join(path, "test-package"))
    assert isinstance(dp, dict)
    assert "moredata" in dp.keys()
    assert "data" in dp.keys()


def test_load_single_resource():
    df = pd.read_csv(os.path.join(path, "test-package/moredata.csv"))
    moredata = read_datapackage(os.path.join(path, "test-package"), "moredata")
    assert df.equals(moredata)


def test_load_multiple_resources():
    dp = read_datapackage(os.path.join(path, "test-package"), ["data", "moredata"])
    assert "data" in dp.keys()
    assert "moredata" in dp.keys()


@pytest.mark.slow
def test_remote_package():
    url = (
        "https://github.com/rgieseke/pandas-datapackage-reader/"
        "raw/main/tests/test-package/datapackage.json"
    )
    dp = read_datapackage(url)
    assert isinstance(dp, dict)
    assert "moredata" in dp.keys()
    assert isinstance(dp["moredata"], pd.DataFrame)
    assert "data" in dp.keys()


def test_not_existing_remote_package():
    with pytest.raises(requests.exceptions.HTTPError):
        dp = read_datapackage("http://www.example.com")


@pytest.mark.slow
def test_github_url():
    url = "https://github.com/datasets/country-codes"
    dp = read_datapackage(url)
    assert isinstance(dp, pd.DataFrame)


@pytest.mark.slow
def test_github_url_with_trailing_slash():
    url = "https://github.com/datasets/country-codes/"
    dp = read_datapackage(url)
    assert isinstance(dp, pd.DataFrame)


@pytest.mark.skipif(sys.version_info < (3, 4), reason="requires pathlib")
def test_pathlib_posixpath():
    from pathlib import Path

    path = Path(__file__).parents[0]
    dp = read_datapackage(path / "test-package")
    assert "data" in dp.keys()


def test_ignore_default_missing_values():
    df = read_datapackage(os.path.join(path, "test-package"), "datawithoutindex")
    assert pd.isna(df.iloc[1, 1])


def test_ignore_custom_missing_values():
    df = read_datapackage(os.path.join(path, "test-package"), "data")
    assert pd.isna(df.loc["c"].value)


def test_missing_integer_values():
    df_wo_index = read_datapackage(
        os.path.join(path, "test-package"), "datawithoutindex"
    )
    assert pd.isnull(df_wo_index.iloc[1].intvalue)
    assert df_wo_index["intvalue"].dtype == pd.Int64Dtype()


def test_missing_integer_values_with_index():
    df = read_datapackage(os.path.join(path, "test-package"), "datawithindex")
    assert pd.isnull(df.loc[2].intvalue)
    assert df["intvalue"].dtype == pd.Int64Dtype()


def test_datetimes():
    # Default test date/time '2017-01-01 01:23:45'
    df = read_datapackage(os.path.join(path, "test-package"), "datetimes")
    assert df["date"].iloc[0] == date(2017, 1, 1)
    assert df["datetime"].iloc[0] == datetime(2017, 1, 1, 1, 23, 45)
    assert df["time"].iloc[0] == time(1, 23, 45)
    assert df.reset_index()["year"].iloc[0] == 2017
    assert df["yearmonth"].iloc[0] == pd.Period("2017-01")
    assert df["yearmonth"].iloc[0] == pd.Period("2017-01")
    assert df["dayfirstdate"].iloc[0] == date(2017, 12, 13)

def test_strings():
    df = read_datapackage(os.path.join(path, "test-package"), "datawithmixedtypes")
    assert df["zipcode"].dtype == np.dtype(object)


def test_metadata():
    df = read_datapackage(os.path.join(path, "test-package"), "data")
    assert df._metadata["format"] == "csv"


def test_geojson():
    df = read_datapackage(os.path.join(path, "test-package"), "admin1-us")
    assert df._metadata["format"] == "geojson"
    assert "geometry" in df.columns


def test_unsupported_format():
    dp = read_datapackage(os.path.join(path, "test-package"))
    assert "json-only" not in dp.keys()


def test_decimal_char():
    df = read_datapackage(os.path.join(path, "test-package"), "europeandata")
    assert df['value'].dtype == float


def test_group_char():
    df = read_datapackage(os.path.join(path, "test-package"), "datawiththousands")
    assert df['value'].dtype == float


def test_encoding():
    df = read_datapackage(os.path.join(path, "test-package"), "data-8859-1")
    assert df['character'].iloc[0] == "à"

