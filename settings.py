"""
settings for datenguide-backend
"""


import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# import options
NA_VALUES = ['x', '-', '.']
ENCODING = 'latin1'
DELIMITER = ';'
DTYPE = 'str'

# locations
DATA_ROOT = os.path.join(BASE_DIR, 'data')
DATABASE = os.path.join(DATA_ROOT, 'db.p')
