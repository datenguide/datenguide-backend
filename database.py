"""
build a tree-like database interface out of a
single master path->value `pd.DataFrame`
"""

import json

import settings


with open(settings.KEYS_TREE) as f:
    DB_KEYS = json.load(f)

with open(settings.KEYS_DTYPES) as f:
    DTYPES = json.load(f)
