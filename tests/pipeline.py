import unittest

from pipeline import process_districts, process_datasets


class PipelineDistrictsTestCase(unittest.TestCase):
    def test_districts(self):
        process_districts()
        self.assertTrue(True)


class PipelineDatasetsTestCase(unittest.TestCase):
    def test_datasets(self):
        process_datasets()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
