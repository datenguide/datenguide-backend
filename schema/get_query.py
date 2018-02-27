import json

from schema.get_schema import KEYS, slugify


def dictify(tree):
    return {slugify(k): dictify(tree[k]) for k in tree if ':' not in k}


query = """{
  regions %s
}""" % json.dumps(dictify(KEYS), indent=2)\
    .replace(':', '').replace('{}', '')\
    .replace('"', '').replace(',', '')
