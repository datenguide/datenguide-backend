"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""


from collections import defaultdict
import pandas as pd

import settings


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


def _cast(value):
    if value:
        try:
            float(value)
            if float(value) == int(value):
                return int(value)
            return float(value)
        except ValueError:
            return value


class Database(object):

    def __init__(self, df, path=(), vertical=False):
        self.df = df
        self.path = path
        # self.vertical = vertical

    def __getitem__(self, attr):
        # i = 0
        # vertical = False
        # if len(attr) == 2:
        #     i, attr = attr
        #     vertical = True
        df = self.df[self.df['path'].map(_get_key) == attr].copy()
        # if not i:
        #     df['path'] = df['path'].map(lambda x: x[1:])
        df['path'] = df['path'].map(lambda x: x[1:])
        return self.__class__(df, self.path + (attr,))

    def __iter__(self):
        return (k for k in self.keys)

    @property
    def keys(self):
        return self.df['path'].map(_get_key).dropna().unique()

    @property
    def leaf(self):
        if self.df.shape[0] == 1:
            return self.df['value'][0]
        return None

    @property
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
        return self.keys


DB = Database(pd.read_pickle(settings.DATABASE))
