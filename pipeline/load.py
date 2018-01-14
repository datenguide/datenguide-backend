"""
load data tables into pandas previously fetched from webservice
"""


import pandas as pd

from util import slugify


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
            - prefix: prefix to add to each column name
            - index: column for use as `df.index`
            - subset: only include these columns in returned DataFrame
            - exclude: exclude these columns in returned DataFrame
            - pivot: column to pivot by (see `pivot` above)
            - slugify: column that should be used to build an extra `slug`-column
            - filter: dict for columns that should be filtered by a given lambda function
        options from `pandas.read_csv`
            - skip: skiprows shortcut
            - skipfooter
            - names
            - delimiter
            - encoding
            - na_values
            - dtype

    Returns
    -------
    df : `pandas.DataFrame`
    """

    df = pd.read_csv(
        fp,
        skiprows=definition.get('skip'),
        skipfooter=definition.get('skipfooter'),
        names=definition.get('names'),
        delimiter=definition.get('delimiter'),
        encoding=definition.get('encoding'),
        na_values=definition.get('na_values'),
        dtype=definition.get('dtype'),
        engine='python'
    )

    if 'index' in definition:
        df.index = df[definition['index']]
    elif 'id' in df.columns:
        df.index = df['id']

    if 'filter' in definition:
        for col, func in definition['filter'].items():
            df = df[df[col].map(eval(func))]

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

    if 'slugify' in definition:
        df['slug'] = df[definition['slugify']].map(slugify)

    return df
