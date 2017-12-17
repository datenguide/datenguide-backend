"""
create districts database
"""


import pandas as pd
import os
import yaml

import settings
from ..load import csv_to_pandas


def _add_fp(definition):
    table_id = definition['table']
    definition['fpath'] = os.path.join(settings.DISTRICTS_ROOT, 'raw', '%s.csv' % table_id)


def run():

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'meta.yml')) as f:
        INFO = yaml.load(f.read())

    sources = INFO['sources']
    for definition in sources.values():
        _add_fp(definition)

    df = csv_to_pandas(sources['base'])
    df = df.dropna(subset=('munis',))

    df['state__id'] = df['rs'].str[:2]
    df_states = df[df['rs'].map(len) == 2]
    df_states['state__name'] = df_states['name']
    df_states['state__id'] = df_states['rs']
    df = df.merge(df_states[['state__id', 'state__name']])

    df = df[df['rs'].map(len) == 5]

    df_area = csv_to_pandas(sources['area'])
    df_area['area'] = pd.to_numeric(df_area['area'].str.replace(',', '.'))

    df_pop = csv_to_pandas(sources['population'])

    df = df.merge(df_area)
    df = df.merge(df_pop)

    df.index = df['rs']

    df.to_pickle(settings.DISTRICTS_SOURCE)
