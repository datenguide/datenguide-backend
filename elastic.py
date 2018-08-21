from storage import Storage


def suggest(q):
    return {
        'suggestions': list(Storage.suggest(q))
    }


def search(q):
    if not q:
        return {
            'results': []
        }

    s = Storage.S().query('query_string',
                          fields=['id^2', 'fulltext'],
                          default_operator='AND',
                          query=q)
    return {
        'results': [{
            'region': {
                'id': hit.id,
                'name': Storage.get_region_name(hit.id)
            },
            'fact': Storage.get_verbose_fact(hit)
        } for hit in s]
    }


def get_fact(fact_id):
    return {
        'fact': Storage.get_fact(fact_id)
    }
