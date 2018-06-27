import json
import requests

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A  # , Q

import settings
from util import get_fields_from_info


NUTS_LEN = (None, 2, 3, 5, 8)  # FIXME

LOOKUPS = {
    'nuts': {
        'func': lambda id_, x: len(id_) == NUTS_LEN[x] if x < 5 else False,
        'type': 'int',
        'description': 'NUTS level to filter Regions for'
    },
    'parent': {
        'func': lambda id_, x: id_.startswith(x),
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
    }
}


class ElasticStorage(object):
    def __init__(self):
        with open(settings.SCHEMA) as f:
            self.schema = json.load(f)
        self.host = ':'.join((settings.ELASTIC['HOST'], settings.ELASTIC['PORT']))
        self.client = Elasticsearch(hosts=[self.host])
        self.index = settings.ELASTIC['INDEX']
        self.ids = self._get_ids()
        self.dtypes = self._get_dtypes()
        self.lookups = LOOKUPS

    def S(self):
        return Search(using=self.client, index=self.index, doc_type='fact')

    def _get_dtypes(self):
        res = requests.get('http://%s/%s/_mapping/fact/' % (self.host, self.index))
        data = res.json()
        return {
            k: v['properties']['value']['type']
            for k, v in data[self.index]['mappings']['fact']['properties'].items()
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
        return sorted([i['key'] for i in res.aggregations.ids.buckets])

    # def _get_field_query(self, field, **filters):
    #     return Q('bool', must=[Q('exists', **{'field': field})] +
    #              [Q('term', **{k: v}) for k, v in filters.items()])

    # def _get_ids_query(self, ids):
    #     return Q('bool', should=[Q('term', **{'id': id_}) for id_ in ids])
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
    # def _get_regions_query(self, ids, **fields):
    #     return Q('bool', filter=self._get_ids_query(ids),
    #              should=[self._get_field_query(field, **filters)
    #                      for field, filters in fields.items()])

    # def _get_region_query(self, id_, **fields):
    #     return Q('bool', filter=Q('term', **{'id': id_}),
    #              should=[self._get_field_query(field, **filters)
    #                      for field, filters in fields.items()])

    def _compute_result(self, ids, fields, search):
        roots = self.schema.keys()
        result = {i: {f: i if f == 'id' else [] for f in fields} for i in ids}  # FIXME
        for hit in search.scan():
            for field in fields:
                if field in hit:
                    if field in roots:
                        result[hit.id][field].append(self._get_fact(field, hit))
                    else:
                        result[hit.id][field] = hit[field]
        return result.values()

    def _get_fact(self, key, hit):
        hit = hit.to_dict()
        fact = hit.pop(key)
        fact.update(hit)
        fact.update({
            'id': hit['fact_id'],
            'year': hit.get('year'),
            'source': self.schema.get(key, {}).get('source', {})
        })
        return fact

    def region_resolver(self, root, info, **kwargs):
        id_ = kwargs.pop('id')
        if id_ in self.ids:
            fields = get_fields_from_info(info)
            # q = self._get_region_query(id_, **fields)
            s = self.S().update_from_dict(self._get_query([id_], fields))
            # print(json.dumps(s.to_dict(), indent=2))
            return list(self._compute_result([id_], fields.keys(), s))[0]  # FIXME

    def regions_resolver(self, root, info, **kwargs):
        ids = self._filter_regions(**kwargs)
        if ids:
            fields = get_fields_from_info(info)
            # q = self._get_regions_query(ids, **fields)
            # s = self.S().query(q)
            s = self.S().update_from_dict(self._get_query(ids, fields))
            # print(json.dumps(s.to_dict(), indent=2))
            return self._compute_result(ids, fields.keys(), s)

    # def get_key(self, id_):
    #     return self.keys.get(id_, {
    #         'id': id_,
    #         'name': id_.title(),
    #         'description': ''
    #     })

    # def get_keys(self):
    #     return sorted(self.keys.values(), key=lambda x: x.get('id'))
