[![PyPI](https://img.shields.io/pypi/v/pandas-datapackage-reader.svg)](https://pypi.python.org/pypi/pandas-datapackage-reader/)
[![Travis](https://img.shields.io/travis/rgieseke/pandas-datapackage-reader.svg)](https://travis-ci.org/rgieseke/pandas-datapackage-reader)

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

# Resource metadata is stored in a `metadata` attribute
print(country_codes.metadata)
```

## License

BSD-2-Clause, see [LICENSE](LICENSE)
