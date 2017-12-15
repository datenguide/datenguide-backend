"""
prepare downloaded datasets
"""


import logging
import os
import yaml
import pandas as pd

import settings

from ..load import csv_to_pandas

log = logging.getLogger(__name__)


INDEX = yaml.load(open(settings.DATASET_INDEX).read())
DATASETS = INDEX['datasets']


def _process_dataset(dataset):
    """
    process given dataset definition

    Parameters
    ----------
    dataset : dict
        definition for 1 dataset consisting of 1 or more single tables.
        more tables will be merged via `id`-attribute.

        a definition could look like this (yaml):

          - id: 21111
            tables:
            - id: 21111-01-03-4
              options: see `pipeline.load.csv_to_pandas`
            - id: 21111-02-06-4
              ...

    Returns
    -------
    df : `pandas.DataFrame`, merged dataframe from all tables
    """

    dataset_root = os.path.join(settings.DATASET_ROOT, str(dataset['dataset_id']))
    df = pd.read_pickle(settings.DISTRICTS_SOURCE)

    def _fp(table_id):
        return os.path.join(dataset_root, 'src', '%s.csv' % table_id)

    for table in dataset['tables']:
        table['fpath'] = _fp(table['table_id'])
        df = df.merge(csv_to_pandas(table))

    df.index = df['rs']
    df.to_pickle(os.path.join(dataset_root, '%s.p' % dataset['dataset_id']))
    return df


def run():
    for dataset in DATASETS:
        _process_dataset(dataset)
