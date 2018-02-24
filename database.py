"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""

import json

import pandas as pd

import settings


df = pd.read_pickle(settings.DATABASE)

with open(settings.DATA_TREE) as f:
    DB = json.load(f)

with open(settings.KEYS_TREE) as f:
    KEYS = json.load(f)

Districts = [DB[k] for k in sorted(DB.keys())]

keys_db = pd.read_pickle(settings.KEYS_DB)


def get_key_info(key):
    try:
        return keys_db.loc[key].to_dict()
    except KeyError:
        d = {c: '' for c in keys_db.columns}
        d['name'] = key.title()
        d['code'] = key
        return d
