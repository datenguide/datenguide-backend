"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""

import json

import settings


with open(settings.DATA_TREE) as f:
    DB = json.load(f)

with open(settings.KEYS_TREE) as f:
    DB_KEYS = json.load(f)

with open(settings.KEYS_INFO) as f:
    KEYS = json.load(f)
