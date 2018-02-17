import os
import pandas as pd

import settings


def run():
    df = pd.DataFrame(columns=('key', 'name', 'description'))

    for fname in os.listdir(settings.KEYS_DIR):
        if fname.endswith('.md'):
            with open(os.path.join(settings.KEYS_DIR, fname)) as f:
                lines = f.readlines()
            name = lines[0].lstrip('# ').strip()
            key = fname.split('.md')[0]
            description = '\n'.join(lines).strip()
            df.loc[key] = (key.upper(), name, description)

    df.to_pickle(settings.KEYS_DB)
