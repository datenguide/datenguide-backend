import pandas as pd

import settings


def get_metadata(raw_content):
    fields = [r.split(';')[0].strip() for r in raw_content.split('\n')[:6]]
    genesis_name, title, date, regional_depth, stat_source, year = fields
    return {
        'genesis_name': genesis_name,
        'title': title,
        'stat_source': stat_source,
        'regional_depth': regional_depth,
        'year': year,
        'date': date
    }


def get_annotations(raw_content):
    return raw_content.split('__________')[1].strip()
