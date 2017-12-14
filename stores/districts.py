"""
store for accessing data for districts via graphql
"""


import pandas as pd

import settings
from models import District


class DistrictStore(object):

    def __init__(self):
        self.data = pd.read_pickle(settings.DISTRICTS_SOURCE)

    def all(self):
        return [District(**r.to_dict()) for k, r in self.data.iterrows()]

    def get(self, id):
        return District(**self.data.loc[id].to_dict())


DistrictStore = DistrictStore()
