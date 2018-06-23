import json

from elasticsearch import Elasticsearch, NotFoundError

import settings


class BaseStorage(object):
    def __init__(self):
        self.lookups = {
            'nuts': {
                'func': lambda r, x: r.get('nuts', {}).get('level', None) == x,
                'type': 'int',
                'description': 'NUTS level to filter Regions for'
            },
            'parent': {
                'func': lambda r, x: r['id'].startswith(x),
                'type': 'str',
                'description': 'Parent region by ID'
            },
            'deprecated': {
                'func': lambda r, x: r.get('deprecated') if x else not bool(r.get('deprecated')),
                'type': 'bool',
                'description': 'Filter for valid regions'
            },
            'valid': {
                'func': lambda r, x: r.get('valid') if x else not bool(r.get('valid')),
                'type': 'bool',
                'description': 'Filter for deprecated flag'
            },
        }
        with open(settings.KEYS_INFO) as f:
            self.keys = json.load(f)
        with open(settings.DTYPES) as f:
            self.dtypes = json.load(f)
        with open(settings.KEYS_TREE) as f:
            self.keys_tree = json.load(f)

    def get_region(self, id_):
        raise NotImplemented

    def get_regions(self, **filters):
        raise NotImplemented

    def get_key(self, id_):
        return self.keys.get(id_, {
            'id': id_,
            'name': id_.title(),
            'description': ''
        })

    def get_keys(self):
        return sorted(self.keys.values(), key=lambda x: x.get('id'))

    def _filter_region_list(self, regions, **filters):
        for key, value in filters.items():
            regions = [r for r in regions if self.lookups[key]['func'](r, value)]
        return regions


class JSONFileStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        with open(settings.DATA_TREE) as f:
            self.db = json.load(f)

    def get_region(self, id_):
        return self.db[id_]

    def get_regions(self, info, **filters):
        return self._filter_region_list(self.db.values(), **filters)


class ElasticStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.client = Elasticsearch(hosts=[':'.join((settings.ELASTIC['HOST'], settings.ELASTIC['PORT']))])
        self.index = settings.ELASTIC['INDEX']
        with open(settings.IDS_FILE) as f:
            self.ids = sorted([i.strip() for i in f.readlines()])

    def get_region(self, id_):
        try:
            res = self.client.get(index=self.index, doc_type='region', id=id_)
            return res['_source']
        except NotFoundError:
            return {}

    def get_regions(self, info, **filters):
        fields = [f.name.value for f in info.field_asts[0].selection_set.selections]
        res = self.client.mget({'ids': self.ids}, index=self.index, doc_type='region', _source=fields)
        regions = [doc['_source'] for doc in res['docs'] if doc['found']]
        return self._filter_region_list(regions, **filters)


Storage = locals()[settings.STORAGE]()
