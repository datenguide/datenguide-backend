"""
settings for datenguide-backend
"""


import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = os.path.join(BASE_DIR, 'data')

NA_VALUES = ['x', '-', '.']
ENCODING = 'latin1'
DELIMITER = ';'
SKIPROWS = 9
SKIPFOOTER = 4


DISTRICTS_ROOT = os.path.join(DATA_ROOT, 'districts')
DISTRICTS_SOURCE = os.path.join(DISTRICTS_ROOT, 'districts.p')

DATASET_INDEX = os.path.join(DATA_ROOT, 'index.yml')
DATASET_ROOT = os.path.join(DATA_ROOT, 'datasets')

ID_FIELD = 'rs'
