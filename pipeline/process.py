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
import pandas as pd
from multiprocessing import Pool, cpu_count

import settings
from .load import csv_to_pandas


CPUS = cpu_count()


def _fp(*args):
    return os.path.join(settings.DATA_ROOT, *args)


def _get_chunks(rows, n=CPUS):
    total = len(rows)
    chunk_size = int(total / n)
    chunks = []
    for i in range(n):
        if not i-1 == n:
            chunks.append(rows[i*chunk_size:(i+1)*chunk_size])
        else:
            chunks.append(rows[i*chunk_size:])
    return chunks


def _process_rows(rows, source):
    db = pd.DataFrame(columns=('_id', 'source', 'date', 'path', 'value'))
    for id, data in rows:
        date = data.get('date')
        for key, value in data.items():
            if not key == 'date':
                path = tuple([id] + key.split('__'))
                db.loc['__'.join(path)] = [id, source, date, path, value]
    return db


def run():
    print('detected %s cores ...' % CPUS)
    print('Collecting tables from %s ...' % settings.DATA_ROOT)

    dbs = []
    for fname in os.listdir(_fp('src')):

        if os.path.isfile(_fp('src', fname)) and '.' in fname:
            name, ext = fname.split('.')

            if ext == 'yaml':
                print('Loading table %s.csv ...' % name)
                with open(_fp('src', fname)) as f:
                    meta = yaml.load(f.read().strip())
                df = csv_to_pandas(_fp('src', '%s.csv' % name), meta)

                with Pool(processes=CPUS) as P:
                    _dbs = P.starmap(
                        _process_rows,
                        zip(_get_chunks(list(df.iterrows())), [name]*CPUS)
                    )

                dbs += _dbs

    print('Write DB to %s ...' % settings.DATABASE)

    DB = pd.concat(dbs)
    DB = DB.sort_values('path')
    DB = DB.drop_duplicates(subset=('date', 'path'))
    DB.to_pickle(settings.DATABASE)

    print('Done.')
