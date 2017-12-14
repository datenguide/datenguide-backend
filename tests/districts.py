import unittest

import pandas as pd
from stores.districts import DistrictStore
from models import District


class DistrictStoreTestCase(unittest.TestCase):

    def test_init(self):
        self.assertIsInstance(DistrictStore.data, pd.DataFrame)

    def test_get_all(self):
        self.assertIsInstance(DistrictStore.all(), list)
        self.assertIsInstance(DistrictStore.all()[0], District)

    def test_get_by_id(self):
        flensburg = DistrictStore.get('01001')
        self.assertTrue('Flensburg' in flensburg.name)


if __name__ == '__main__':
    unittest.main()
