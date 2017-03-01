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
```

## License

BSD-2-Clause, see [LICENSE](LICENSE)
