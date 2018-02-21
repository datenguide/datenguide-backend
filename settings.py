"""
settings for datenguide-backend
"""


import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# locations
DATA_ROOT = os.path.join(BASE_DIR, 'data')
DATA_SRC = os.path.join(DATA_ROOT, 'src')
DATABASE = os.path.join(DATA_ROOT, 'db.p')
KEYS_DB = os.path.join(DATA_ROOT, 'keys.p')
KEYS_DIR = os.path.join(DATA_ROOT, 'keys')

# genesis webservice
GENESIS_USERNAME = 'GK106723'
GENESIS_PASSWORD = 'secret'
GENESIS_SERVICES = {
    'research': 'https://www-genesis.destatis.de/genesisWS/services/RechercheService_2010?wsdl',
    'export': 'https://www-genesis.destatis.de/genesisWS/services/ExportService_2010?wsdl',
}


try:
    from local_settings import *   # noqa
except ImportError:
    pass
