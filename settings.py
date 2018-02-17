"""
settings for datenguide-backend
"""


import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# locations
DATA_ROOT = os.path.join(BASE_DIR, 'data')
DATABASE = os.path.join(DATA_ROOT, 'db.p')
KEYS_DB = os.path.join(DATA_ROOT, 'keys.p')
KEYS_DIR = os.path.join(DATA_ROOT, 'keys')
