"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""


import pandas as pd

import settings


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
        self.id = ':'.join(path)
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
        for k in self:
            child = self[k]
            yield {
                'id': child.id,
                'key': k,
                'value': _cast(child.leaf),
                'data': [] if child.leaf else '__follow__'
            }

    @property
    def datadict(self):
        return {d['key']: d['value'] for d in self.data}


DB = Database(pd.read_pickle(settings.DATABASE))
