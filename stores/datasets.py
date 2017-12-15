"""
store for accessing data for districts via graphql
"""


import yaml

import settings
from models import Dataset


class DatasetStore(object):

    def __init__(self):
        index = yaml.load(open(settings.DATASET_INDEX).read())
        self.datasets = index['datasets']

    def all(self):
        return [Dataset(
            id=d['dataset_id'],
            tables=[t['table_id'] for t in d['tables']]
        ) for d in self.datasets]

    def get(self, id):
        for dataset in self.all():
            if str(dataset.id) == id:
                return dataset

DatasetStore = DatasetStore()
