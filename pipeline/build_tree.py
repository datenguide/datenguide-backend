"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""

import json
import pandas as pd
import sys

from collections import defaultdict
from multiprocessing import Pool, cpu_count

import settings


CPUS = cpu_count()


def _tree():
    return defaultdict(_tree)


def _add_path(t, path, value=None):
    for i, p in enumerate(path):
        if value and i+1 == len(path):
            t[p] = value
        else:
            t = t[p]


def _add_to_tree(t, path, value=None):
    # FIXME reorganise code
    _add_path(t, path, value)
    if ':' in path[-1]:
        leaf = path[-2]
        field, query = path[-1].split(':')
        query_path = path[:-2] + ('%s__%ss' % (leaf, field), '_' + query)
        _add_path(t, query_path, value)


def get_data_tree(chunk):
    id_, df = chunk
    t = _tree()
    for _, data in df.iterrows():
        _add_to_tree(t, data['path'], data['value'])
    return id_, t


def get_key_tree(df):
    t = _tree()
    for path in df['path'].map(lambda x: x[1:]).unique():
        _add_to_tree(t, path)
    return t


def run():
    sys.stdout.write('Building trees ...\n')

    df = pd.read_pickle(settings.DATABASE)

    chunks = [(id_, df[df['id'] == id_]) for id_ in df['id'].unique()]

    with Pool(processes=CPUS) as P:
        trees = P.map(get_data_tree, chunks)

    data_tree = {id_: t[id_] for id_, t in trees}
    keys_tree = get_key_tree(df)

    with open(settings.DATA_TREE, 'w') as f:
        json.dump(data_tree, f)
    sys.stdout.write('Saved data tree to "%s" .\n' % settings.DATA_TREE)

    with open(settings.KEYS_TREE, 'w') as f:
        json.dump(keys_tree, f)
    sys.stdout.write('Saved key tree to "%s" .\n' % settings.KEYS_TREE)
