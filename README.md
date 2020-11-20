[![PyPI](https://img.shields.io/pypi/v/pandas-datapackage-reader.svg)](https://pypi.python.org/pypi/pandas-datapackage-reader/)
[![CI](https://img.shields.io/github/workflow/status/rgieseke/pandas-datapackage-reader/CI?label=actions&logo=github&logoColor=white)](https://github.com/rgieseke/pandas-datapackage-reader/actions)

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
