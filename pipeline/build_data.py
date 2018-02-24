"""
process data pipeline:

build 1 single key->value database out of many tables
key is a tuple of path items

how to store source datasets:
for each csv-file, put it into `settings.DATA_SRC`

each csv-file needs a metadata file with the same name
(but .yaml-extension instead of .csv) where the info
for `pipeline.load.csv_to_pandas` goes in (see docstring in `pipeline.load`)

as a convention, filenames should map to the table id from Genesis.
"""


import pandas as pd
import os
import yaml

from multiprocessing import Pool, cpu_count

import settings
from .load import csv_to_pandas


CPUS = cpu_count()


def _fp(*args):
    return os.path.join(settings.DATA_ROOT, *args)


def _fpsrc(*args):
    return os.path.join(settings.DATA_SRC, *args)


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
    res = []
    for id, data in rows:
        date = data.get('date')
        for key, value in data.items():
            if not key == 'date':
                path = tuple([id] + key.split('__'))
                res.append((id, source, date, path, value))
    return res


def run():
    print('detected %s cores ...' % CPUS)
    print('Collecting tables from %s ...' % settings.DATA_ROOT)

    chunks = []
    for fname in os.listdir(_fpsrc()):
        if os.path.isfile(_fpsrc(fname)) and '.' in fname:
            name_parts = fname.split('.')
            name, ext = name_parts[0::len(name_parts)-1]

            if ext == 'yaml':
                print('Loading table %s.csv ...' % name)
                with open(_fp('defaults.yaml')) as f:
                    defaults = yaml.load(f.read().strip())
                with open(_fpsrc(fname)) as f:
                    definition = yaml.load(f.read().strip())
                defaults.update(definition)
                df = csv_to_pandas(_fpsrc('%s.csv' % name), defaults)

                with Pool(processes=CPUS) as P:
                    chunks += P.starmap(
                        _process_rows,
                        zip(_get_chunks(list(df.iterrows())), [name]*CPUS)
                    )

    DB = pd.DataFrame(
        [row for chunk in chunks for row in chunk],
        columns=('id', 'source', 'date', 'path', 'value')
    )
    DB = DB.sort_values(['path', 'date'])
    DB = DB.drop_duplicates(subset=('date', 'path'))

    print('Write DB to %s ...' % settings.DATABASE)
    DB.to_pickle(settings.DATABASE)

    print('Write DB to %s as well...' % settings.DATABASE_CSV)
    DB.to_csv(settings.DATABASE_CSV)

    print('Done.')
