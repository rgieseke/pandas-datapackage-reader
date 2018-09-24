[![PyPI](https://img.shields.io/pypi/v/pandas-datapackage-reader.svg)](https://pypi.python.org/pypi/pandas-datapackage-reader/)
[![Travis](https://img.shields.io/travis/rgieseke/pandas-datapackage-reader.svg)](https://travis-ci.org/rgieseke/pandas-datapackage-reader)
[![Codecov](https://img.shields.io/codecov/c/github/rgieseke/pandas-datapackage-reader.svg)](https://codecov.io/gh/rgieseke/pandas-datapackage-reader)

# pandas-datapackage-reader

Easy loading of tabular data from [Data Packages](http://frictionlessdata.io/data-packages/) into Pandas DataFrames.

## Installation

    pip install pandas-datapackage-reader

## Usage

```python
from pandas_datapackage_reader import read_datapackage

# From GitHub repository
country_codes = read_datapackage("https://github.com/datasets/country-codes")

# From local directory
country_codes = read_datapackage("country-codes")

# Data Package with GeoJSON
geo_countries = read_datapackage("https://github.com/datasets/geo-countries")
```

Resource metadata from the Data Package is returned as a dictionary in the
`_metadata` attribute.

```python
country_codes._metadata
```

contains

```
{'format': 'csv',
  'name': 'country-codes',
  'path': 'data/country-codes.csv',
  'schema': {'fields': [{'description': 'Country or Area official Arabic short name from UN Statistics Divsion',
        'name': 'official_name_ar',
        'title': 'official name Arabic',
        'type': 'string'},
      {'description': 'Country or Area official Chinese short name from UN Statistics Divsion',
        'name': 'official_name_cn',
        'title': 'official name Chinese',
        'type': 'string'},
# ...
```

## License

BSD-2-Clause, see [LICENSE](LICENSE)
