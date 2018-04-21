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
DATABASE_CSV = os.path.join(DATA_ROOT, 'db.csv')
DATA_TREE = os.path.join(DATA_ROOT, 'db.json')
KEYS_TREE = os.path.join(DATA_ROOT, 'keys.json')
KEYS_INFO = os.path.join(DATA_ROOT, 'keys_info.json')
KEYS_DIR = os.path.join(DATA_ROOT, 'keys')
KEYS_DTYPES = os.path.join(DATA_ROOT, 'keys_dtypes.json')

# genesis webservice
GENESIS_SERVICES = {
    'research': 'https://www.regionalstatistik.de/genesisws/services/RechercheService_2010?wsdl',
    'export': 'https://www.regionalstatistik.de/genesisws/services/ExportService_2010?wsdl',
}


try:
    from local_settings import *   # noqa
except ImportError:
    pass
