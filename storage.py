import json
import requests

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A

import settings
from util import get_fields_from_info


NUTS_LEN = (None, 2, 3, 5, 8)  # FIXME

LOOKUPS = {
    'nuts': {
        'func': lambda id_, x: len(id_) == NUTS_LEN[x] if x < 5 and not id_ == 'DG' else False,
        'type': 'int',
        'description': """**Filter Regionen nach NUTS-Ebene.**\n\n*Optionen:*\n\n
1 – Bundesländer\n\n
2 – Regierungsbezirke / statistische Regionen\n\n
3 – Kreise / kreisfreie Städte\n\n
4 – Gemeinden (LAU 1 / LAU 2)"""
    },
    'parent': {
        'func': lambda id_, x: id_.startswith(x),
        'type': 'str',
        'description': 'Filter Regionen nach ID (Regionalschlüssel) der Elternregion'
    },
    # 'valid': {
    #     'func': lambda: True,
    #     'type': 'bool',
    #     'description': 'Filter for deprecated flag'
    # }
}


class ElasticStorage(object):
    def __init__(self):
        with open(settings.NAMES) as f:
            self.names = json.load(f)
        with open(settings.SCHEMA) as f:
            self.schema = json.load(f)
        self.data_roots = self.schema.keys()
        self.host = ':'.join((settings.ELASTIC['HOST'], settings.ELASTIC['PORT']))
        self.client = Elasticsearch(hosts=[self.host])
        self.index = settings.ELASTIC['INDEX']
        self.ids = self._get_ids()
        self.dtypes = self._get_dtypes()
        self.lookups = LOOKUPS

    def S(self):
        return Search(using=self.client, index=self.index)

    def _get_dtypes(self):
        res = requests.get('http://%s/%s/_mapping/' % (self.host, self.index))
        data = res.json()
        return {
            k: v.get('properties', {}).get('value', v)['type']
            for k, v in data[self.index]['mappings']['doc']['properties'].items()
            if k in self.schema.keys()
        }

    def _filter_regions(self, **filters):
        regions = self.ids
        for key, value in filters.items():
            regions = [r for r in regions if self.lookups[key]['func'](r, value)]
        return regions

    def _get_ids(self):
        s = self.S()
        s.aggs.bucket('ids', A('terms', field='id', size=20000))
        res = s.execute()
        return [i['key'] for i in res.aggregations.ids.buckets]

    def _get_id_part(self, ids):
        if len(ids) > 1:
            return {'terms': {'id': ids}}
        return {'term': {'id': ids[0]}}

    def _get_field_part(self, field, **filters):
        return [{'exists': {'field': field}}] + [{'term': {k: v}} for k, v in filters.items()]

    def _get_query(self, ids, fields):
        return {
            'query': {
                'constant_score': {
                    'filter': {
                        'bool': {
                            'must': self._get_id_part(ids),
                            'should': [{
                                'bool': {
                                    'must': self._get_field_part(field, **filters)
                                }
                            } for field, filters in fields.items() if field in self.schema.keys()]
                        }
                    }
                }
            }
        }

    def _get_base_value(self, id_, field):
        if field == 'id':
            return id_
        if field == 'name':
            return self.get_region_name(id_)
        if field in self.data_roots:
            return []
        return None

    def _compute_result(self, ids, fields, search):
        data_roots = self.data_roots
        result = {i: {f: self._get_base_value(i, f) for f in fields} for i in ids}
        for hit in search.scan():
            for field in fields:
                if field in hit:
                    if field in data_roots:
                        result[hit.id][field].append(self._get_fact(field, hit))
                    else:
                        result[hit.id][field] = hit[field]
        return sorted(result.values(), key=lambda x: x.get('id', 0))

    def _get_fact(self, key, hit):
        hit = hit.to_dict()
        fact = hit.pop(key)
        fact.update(hit)
        fact.update({
            'id': hit['fact_id'],
            'year': hit.get('year'),
            'date': hit.get('date'),
            'source': self.get_source(key)
        })
        return fact

    def region_resolver(self, root, info, **kwargs):
        id_ = kwargs.pop('id')
        if id_ in self.ids:
            fields = get_fields_from_info(info)
            s = self.S().update_from_dict(self._get_query([id_], fields))
            return list(self._compute_result([id_], fields.keys(), s))[0]  # FIXME

    def regions_resolver(self, root, info, **kwargs):
        ids = self._filter_regions(**kwargs)
        if ids:
            fields = get_fields_from_info(info)
            s = self.S().update_from_dict(self._get_query(ids, fields))
            return self._compute_result(ids, fields.keys(), s)

    def get_key(self, key):
        return self.schema.get(key, {'name': key})

    def get_key_name(self, key):
        return self.schema.get(key, {}).get('name', key)

    def get_region_name(self, id_):
        return self.names.get(id_, '(Region ohne Name)')

    def get_source(self, key):
        return self.schema.get(key, {}).get('source', {})


Storage = ElasticStorage()
