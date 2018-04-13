import json
import os
import sys
import pandas as pd

import settings


def run():
    sys.stdout.write('Building keys db ...\n')
    data = []
    for fname in os.listdir(settings.KEYS_DIR):
        if fname.endswith('_de.json'):  # FIXME make multilangual
            with open(os.path.join(settings.KEYS_DIR, fname)) as f:
                data.append(json.load(f))
    df = pd.DataFrame(data)
    df.index = df['code']
    df.to_pickle(settings.KEYS_DB)
    df.to_csv(settings.KEYS_DB_CSV)
    sys.stdout.write('Stored keys db in %s .\n' % settings.KEYS_DB)
