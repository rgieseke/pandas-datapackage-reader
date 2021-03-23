# encoding: UTF-8

"""
pandas-datapackage-reader
-------------------------

Easy loading of tabular data from Data Packages into Pandas DataFrames.

See README.md and repository for details:
  https://github.com/rgieseke/pandas-datapackage-reader
"""

import json
import os

import requests
import pandas as pd

import logging

try:
    import frictionless
except ImportError:
    logging.warning("Frictionless-py package missing: cannot import from datapackage object.")

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


def read_datapackage(dp, resource_name=None):
    """
    Read tabular CSV files from Data Packages into DataFrames.

    Parameters:
    -----------
    dp: string, PathLike or DataPackage object
        Local path or URL of a Data Package. For GitHub URLs the repository can
        be used. You can also use a frictionless.package.Package object.
    resource_name: string or list of strings
        Name or names of resources to read. Lists of strings are used to
        request multiple resources.

    Returns
    -------
    data_frames : DataFrame or Dict of DataFrames
        DataFrame(s) of the passed in Data Package. See notes in resource_name
        argument for more information on when a Dict of DataFrames is returned.

    """
    if isinstance(dp, (str, os.PathLike)):
        url_or_path = str(dp)  # Allows using PosixPath
        if url_or_path.startswith("https://github.com/") and not url_or_path.endswith(
            "/datapackage.json"
        ):
            username_project = url_or_path.split("https://github.com/")[1]
            if username_project.endswith("/"):
                username_project = username_project[:-1]
            url_or_path = (
                "https://raw.githubusercontent.com/"
                + username_project
                + "/master/datapackage.json"
            )
        elif not url_or_path.endswith("datapackage.json"):
            url_or_path = os.path.join(url_or_path, "datapackage.json")

        if url_or_path.startswith("http"):
            r = requests.get(url_or_path)
            if r.status_code == 200:
                metadata = json.loads(r.text)
            else:
                r.raise_for_status()
        else:
            with open(url_or_path, "r") as f:
                metadata = json.load(f)
    elif isinstance(dp, frictionless.package.Package):
        url_or_path = "datapackage.json"
        metadata = dp.to_dict()
    else:
        logging.error("Format not recognized. Parameter dp accepts string, PathLike or DataPackage object.")

    if type(resource_name) is str:
        resource_name = [resource_name]

    resources = [resource for resource in metadata["resources"]]
    if resource_name is not None:
        resources = [
            resource for resource in resources if resource["name"] in resource_name
        ]

    data_frames = {}

    for idx, resource in enumerate(resources):
        if "name" in resource.keys():
            name = resource["name"]
        else:
            name = str(idx)

        index_col = None

        resource_path = url_or_path.replace("datapackage.json", resource["path"])

        if "format" in resource.keys():
            format = resource["format"]
        else:
            format = resource_path.rsplit(".", 1)[-1]

        dtypes = {}
        if "schema" in resource:
            # Get missing values representations if defined
            missing_values = resource["schema"].get("missingValues", [''])

            # Get decimal character if they are defined
            decimal_char = resource["schema"].get("decimalChar", '.')

            # Get encoding
            encoding = resource.get("encoding", "utf-8")

            if "fields" in resource["schema"]:
                for column in resource["schema"]["fields"]:
                    col_type = column.get("type", None)
                    # Get thousands separator from field level, if defined.
                    # Note that this will be applied to all fields.
                    thousands_sep = column.get("groupChar", None)
                    if col_type == "number":
                        dtypes[column["name"]] = "float64"
                    elif col_type == "integer":
                        dtypes[column["name"]] = "Int64"
                    elif col_type == "string":
                        dtypes[column["name"]] = "object"

        if format == "csv":
            df = pd.read_csv(
                resource_path,
                na_filter=True,
                na_values=missing_values,
                keep_default_na=False,
                dtype=dtypes,
                thousands=thousands_sep,
                decimal=decimal_char,
                encoding=encoding,
            )
        elif format == "geojson":
            import geopandas

            df = geopandas.read_file(resource_path)
        else:
            continue

        if "primaryKey" in resource["schema"]:
            index_col = resource["schema"]["primaryKey"]

        # Process dates.
        for column in resource["schema"]["fields"]:
            format = column.get("format", None)
            if column["type"] == "date":
                df[column["name"]] = pd.to_datetime(
                    df[column["name"]], format=format
                ).dt.date
            elif column["type"] == "datetime":
                df[column["name"]] = pd.to_datetime(df[column["name"]], format=format)
            elif column["type"] == "time":
                df[column["name"]] = pd.to_datetime(
                    df[column["name"]], format=format
                ).dt.time
            elif column["type"] == "year":
                df[column["name"]] = df[column["name"]].astype(int)
            elif column["type"] == "yearmonth":
                df[column["name"]] = pd.to_datetime(
                    df[column["name"]], format="%Y-%m"
                ).dt.to_period("M")

        # Set index column
        if index_col:
            try:
                df = df.set_index(index_col)
            except KeyError:
                raise KeyError("Error dealing with {}".format(name))

        # Add resource description as a `_metadata` attribute. This won't
        # survive methods returning new DataFrames but can be useful.
        df._metadata = resource

        data_frames[name] = df

    if len(list(data_frames.values())) == 1:
        return list(data_frames.values())[0]
    else:
        return data_frames
