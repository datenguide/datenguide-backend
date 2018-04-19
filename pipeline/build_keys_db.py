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
    df = pd.DataFrame(data).rename(columns={'code': 'id'})
    df.index = df['id']
    json.dump(df.T.to_dict(), open(settings.KEYS_INFO, 'w'))
    sys.stdout.write('Stored keys info in %s .\n' % settings.KEYS_INFO)
