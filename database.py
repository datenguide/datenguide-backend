"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""


from collections import defaultdict
import pandas as pd

import settings


def _tree():
    return defaultdict(_tree)


def _add_path(t, path, value=None):
    for i, p in enumerate(path):
        if value and i+1 == len(path):
            t[p] = value
        else:
            t = t[p]


def get_data_tree(df):
    t = _tree()
    for data in df[['path', 'value']].T.to_dict().values():
        _add_path(t, data['path'], data['value'])
    return t


def get_key_tree(df):
    t = _tree()
    for path in df['path'].map(lambda x: x[1:]).unique():
        _add_path(t, path)
    return t


df = pd.read_pickle(settings.DATABASE)
DB = get_data_tree(df)
Districts = [DB[k] for k in DB.keys()]
KEYS = get_key_tree(df)
