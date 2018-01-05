"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""


from collections import defaultdict
import pandas as pd

import settings
from util import cached_property


def _tree():
    return defaultdict(_tree)


def _add_path(t, path):
    for p in path:
        t = t[p]


def _get_key(path, i=0):
    try:
        return path[i]
    except IndexError:
        return None


class Database(object):

    def __init__(self, df):
        self.df = df

    def __getitem__(self, attr):
        df = self.df[self.df['path'].map(_get_key) == attr].copy()
        df['path'] = df['path'].map(lambda x: x[1:])
        return self.__class__(df)

    def __iter__(self):
        return (k for k in self.keys)

    @cached_property
    def keys(self):
        return self.df['path'].map(_get_key).dropna().unique()

    @cached_property
    def leaf(self):
        if self.df.shape[0] == 1:
            return self.df['value'][0]
        return None

    @cached_property
    def data(self):
        return {
            k: self[k].leaf if self[k].leaf else self[k].data
            for k in self
        }

    def get_key_tree(self):
        t = _tree()
        for path in self.df['path'].map(lambda x: x[1:]).unique():
            _add_path(t, path)
        return t

    def all(self):
        return [self[k].data for k in self]


DB = Database(pd.read_pickle(settings.DATABASE))
