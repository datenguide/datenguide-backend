"""
settings for datenguide-backend
"""


import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STORAGE = os.getenv('STORAGE', 'JSONFileStorage')

# locations
DATA_ROOT = os.getenv('DATA_ROOT', os.path.join(BASE_DIR, 'data'))
DATA_TREE = os.getenv('DATA_TREE', os.path.join(DATA_ROOT, 'tree.json'))
KEYS_TREE = os.getenv('KEYS_TREE', os.path.join(DATA_ROOT, 'keys.json'))
KEYS_INFO = os.getenv('KEYS_INFO', os.path.join(DATA_ROOT, 'keys_info.json'))
DTYPES = os.getenv('DTYPES', os.path.join(DATA_ROOT, 'dtypes.json'))
IDS_FILE = os.getenv('IDS_FILE', os.path.join(DATA_ROOT, 'ids.csv'))

# elastic
ELASTIC = {
    'HOST': os.getenv('ELASTIC_HOST', 'localhost'),
    'PORT': os.getenv('ELASTIC_PORT', '9200'),
    'INDEX': os.getenv('ELASTIC_INDEX', 'genesapi')
}
