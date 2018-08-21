"""
settings for datenguide-backend
"""


import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# locations
SCHEMA = os.getenv('SCHEMA', os.path.join(BASE_DIR, 'schema.json'))
NAMES = os.getenv('NAMES', os.path.join(BASE_DIR, 'names.json'))

# elastic
ELASTIC = {
    'HOST': os.getenv('ELASTIC_HOST', 'localhost'),
    'PORT': os.getenv('ELASTIC_PORT', '9200'),
    'INDEX': os.getenv('ELASTIC_INDEX', 'genesapi')
}
