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
__version__ = get_versions()['version']
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

    Notes:
    ------
    Columns of type "integer" with missing values are converted to "object" as
    integer columns in Pandas do not support missing values.

    Returns
    -------
    data_frames : DataFrame or Dict of DataFrames
        DataFrame(s) of the passed in Data Package. See notes in resource_name
        argument for more information on when a Dict of Dataframes is returned.

    """
    url_or_path = str(url_or_path)  # Allows using PosixPath
    if url_or_path.startswith("https://github.com/"):
        username_project = url_or_path.split("https://github.com/")[1]
        if username_project.endswith("/"):
            username_project = username_project[:-1]
        url_or_path = "https://raw.githubusercontent.com/" + \
                      username_project + \
                      "/master/datapackage.json"
    elif not url_or_path.endswith("datapackage.json"):
        url_or_path = os.path.join(url_or_path, "datapackage.json")

    if url_or_path.startswith("http"):
        r = requests.get(url_or_path)
        if r.status_code == 200:
            metadata = json.loads(r.text)
    else:
        metadata = json.load(open(url_or_path, "r"))

    if type(resource_name) is str:
        resource_name = [resource_name]

    resources = [resource for resource in metadata["resources"]]
    if resource_name is not None:
        resources = [resource for resource in resources
                     if resource["name"] in resource_name]

    data_frames = {}

    for idx, resource in enumerate(resources):
        if "name" in resource.keys():
            name = resource["name"]
        else:
            name = str(idx)

        index_col = None
        parse_dates = []

        int_columns = []

        csv_path = url_or_path.replace("datapackage.json", resource["path"])
        if not csv_path.endswith(".csv"):
            continue

        if "primaryKey" in resource["schema"]:
            index_col = resource["schema"]["primaryKey"]

        for column in resource["schema"]["fields"]:
            if column["type"] == "integer" and (index_col and column["name"]
                                                not in index_col):
                int_columns.append(column["name"])
            elif column["type"] == "date":
                parse_dates.append(column["name"])

        if len(parse_dates) == 0:
            parse_dates = None

        df = pd.read_csv(
            csv_path,
            index_col=index_col,
            parse_dates=parse_dates
        )

        # Add resource description as a new attribute. This won't survive
        # methods returning new DataFrames  but can be useful nonetheless.
        df.metadata = resource

        # Convert integer columns with missing values to type 'object'
        for int_col in int_columns:
            if df[int_col].isnull().sum() > 0:
                df[int_col] = df[int_col].astype(object)

        data_frames[name] = df

    if len(list(data_frames.values())) == 1:
        return list(data_frames.values())[0]
    else:
        return data_frames
