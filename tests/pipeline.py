import unittest

from pipeline import process_districts


class PipelineTestCase(unittest.TestCase):
    def test_districts(self):
        process_districts()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
