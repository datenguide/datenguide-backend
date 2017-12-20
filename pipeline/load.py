"""
load data tables into pandas previously fetched from webservice
"""


import pandas as pd

import settings


def pivot(df, colname):
    """
    pivot given `df` by `colname`, prepend values from `c`
    """
    dfs = []
    for col in df.columns:
        if col not in ('id', colname):
            _df = df.pivot('id', colname, col)
            _df = _df.rename(columns={c: '%s__%s' % (c, col) for c in _df.columns})
            dfs.append(_df)
    return pd.concat(dfs, axis=1)


def csv_to_pandas(fp, definition={}):
    """
    load raw csv file into `pandas.DataFrame`

    Parameters
    ----------
    fp : str, required: Absolute or relative path to csv file

    definition : dict, optional
        Information for computing `pandas.read_csv` arguments.

        keys:
            - skip: value for skiprows
            - skipfooter: value for skipfooter
            - names: column names
            - prefix: prefix to add to each column name
            - index: column for use as `df.index`
            - subset: only include these columns in returned DataFrame
            - exclude: exclude these columns in returned DataFrame
            - pivot: column to pivot by (see `pivot` above)
        defaults if not present:
            - delimiter
            - encoding
            - na_values

    Returns
    -------
    df : `pandas.DataFrame`
    """

    df = pd.read_csv(
        fp,
        skiprows=definition.get('skip'),
        skipfooter=definition.get('skipfooter'),
        names=definition.get('names'),
        delimiter=definition.get('delimiter', settings.DELIMITER),
        encoding=definition.get('encoding', settings.ENCODING),
        na_values=definition.get('na_values', settings.NA_VALUES),
        engine='python'
    )

    if 'index' in definition:
        df.index = df[definition['index']]
    elif 'id' in df.columns:
        df.index = df['id']

    if 'subset' in definition:
        df = df[definition['subset']]

    if 'exclude' in definition:
        df = df[[c for c in df.columns if c not in definition['exclude']]]

    for col, dtype in df.dtypes.items():
        if dtype.name == 'object':
            df[col] = df[col].str.strip()

    df = df.dropna(how='all')

    if 'pivot' in definition:
        df = pivot(df, definition['pivot'])

    if 'prefix' in definition:
        df = df.rename(columns={c: '%s__%s' % (definition['prefix'], c)
                                for c in df.columns})

    return df
