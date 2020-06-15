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

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


def read_datapackage(url_or_path, resource_name=None):
    """
    Read tabular CSV files from Data Packages into DataFrames.

    Parameters:
    -----------
    path_or_url: string
        Local path or URL of a Data Package. For GitHub URLs the repository can
        be used.
    resource_name: string or list of strings
        Name or names of resources to read. Lists of strings are used to
        request multiple resources.

    Returns
    -------
    data_frames : DataFrame or Dict of DataFrames
        DataFrame(s) of the passed in Data Package. See notes in resource_name
        argument for more information on when a Dict of DataFrames is returned.

    """
    url_or_path = str(url_or_path)  # Allows using PosixPath
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
        if ("schema" in resource) and ("fields" in resource["schema"]):
            for column in resource["schema"]["fields"]:
                col_type = column.get("type", None)
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
                na_values="",
                keep_default_na=False,
                dtype=dtypes,
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
