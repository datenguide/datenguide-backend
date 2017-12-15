"""
load data tables into pandas previously fetched from webservice
"""


import pandas as pd

import settings


def csv_to_pandas(definition):
    """
    load raw csv file into `pandas.DataFrame`

    Parameters
    ----------
    definition : dict
        Information for computing `pandas.read_csv` arguments.

        required:
            - fpath: Absolute path to csv file
        optional:
            - skip: value for skiprows
            - names: column names
            - index: column for use as `df.index`
            - subset: only include these columns in returned DataFrame
            - exclude: exclude these columns in returned DataFrame
        defaults if not present:
            - delimiter
            - encoding
            - na_values

    Returns
    -------
    df : `pandas.DataFrame`
    """

    df = pd.read_csv(
        definition['fpath'],
        skiprows=definition.get('skip'),
        names=definition.get('names'),
        delimiter=definition.get('delimiter', settings.DELIMITER),
        encoding=definition.get('encoding', settings.ENCODING),
        na_values=definition.get('na_values', settings.NA_VALUES)
    )

    if 'index' in definition:
        df.index = df[definition['index']]

    if 'subset' in definition:
        df = df[definition['subset']]

    if 'exclude' in definition:
        df = df[[c for c in df.columns if c not in definition['exclude']]]

    for col, dtype in df.dtypes.items():
        if dtype.name == 'object':
            df[col] = df[col].str.strip()

    return df
