"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""

import json
import pandas as pd
import sys

from collections import defaultdict

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
    for data in df[['path', 'value', 'date']].T.to_dict().values():
        _add_path(t, data['path'], data['value'])
    return t


def get_key_tree(df):
    t = _tree()
    for path in df['path'].map(lambda x: x[1:]).unique():
        _add_path(t, path)
    return t


def run():
    sys.stdout.write('Building trees ...\n')

    df = pd.read_pickle(settings.DATABASE)
    data_tree = get_data_tree(df)
    keys_tree = get_key_tree(df)

    with open(settings.DATA_TREE, 'w') as f:
        json.dump(data_tree, f)
    sys.stdout.write('Saved data tree to "%s" .\n' % settings.DATA_TREE)

    with open(settings.KEYS_TREE, 'w') as f:
        json.dump(keys_tree, f)
    sys.stdout.write('Saved key tree to "%s" .\n' % settings.KEYS_TREE)
