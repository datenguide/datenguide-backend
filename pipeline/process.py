"""
process data pipeline:

build 1 single key->value database out of many tables
key is a tuple of path items

how to store source datasets:
for each csv-file, put it into 'src'-subfolder of
`settings.DATA_ROOT`

each csv-file needs a metadata file with the same name
(but .yaml-extension instead of .csv) where the info
for `pipeline.load.csv_to_pandas` goes in (see docstring in `pipeline.load`)

as a convention, filenames should map to the table id from Genesis.
"""


import os
import yaml
import uuid
import pandas as pd

import settings
from .load import csv_to_pandas


def _fp(*args):
    return os.path.join(settings.DATA_ROOT, *args)

def run():
    print('Collecting tables from %s ...' % settings.DATA_ROOT)

    DB = pd.DataFrame(columns=('id', 'source', 'date', 'path', 'value'))

    for fname in os.listdir(_fp('src')):
        if os.path.isfile(_fp('src', fname)) and '.' in fname:
            name, ext = fname.split('.')
            if ext == 'yaml':
                print('Loading table %s.csv ...' % name)
                with open(_fp('src', fname)) as f:
                    meta = yaml.load(f.read().strip())
                df = csv_to_pandas(_fp('src', '%s.csv' % name), meta)
                for id, data in df.iterrows():
                    date = data.get('date')
                    for key, value in data.items():
                        if key not in ('date', 'id'):
                            DB.loc[uuid.uuid4()] = [id, name, date, tuple([id] + key.split('__')), value]

    print('Write DB to %s ...' % settings.DATABASE)
    DB = DB.drop_duplicates(subset=('date', 'path'))
    DB.to_pickle(settings.DATABASE)
    print('Done.')
