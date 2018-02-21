import json
import os
import string
import sys

import settings

from .clients import ResearchClient, ExportClient


def _fp(code, lang):
    return os.path.join(settings.KEYS_DIR, '%s_%s.json' % (code, lang))


def get_attribute_keys():
    for a in string.ascii_uppercase[18:]:
        sys.stdout.write('Retrieving keys starting with "%s" ...\n' % a)
        res = ResearchClient.service.MerkmalsKatalog(
            kennung=settings.GENESIS_USERNAME,
            passwort=settings.GENESIS_PASSWORD,
            filter='%s*' % a,
            kriterium='Code',
            bereich='Alle',
            typ='Alle',
            sprache='de',
            listenLaenge=500
        )

        if len(res.merkmalsKatalogEintraege) == 500:
            sys.stderr.write('ERROR: There are more than 500 attributes starting with "%s"!\n' % a)
        else:
            for attribute in res.merkmalsKatalogEintraege:
                code = attribute.find('code').text
                sys.stdout.write('found code "%s"\n' % code)
                yield code


def get_information_for_attribute(code):
    for lang in ('de', 'en'):
        sys.stdout.write('Retrieving information for code "%s" in language "%s" ...\n' % (code, lang))

        try:
            res = ExportClient.service.MerkmalInformation(
                kennung=settings.GENESIS_USERNAME,
                passwort=settings.GENESIS_PASSWORD,
                name=code,
                bereich='alle',
                sprache=lang
            )

            data = {
                'code': code,
                'lang': lang,
                'description': res.information,
                'name': res.inhalt,
                'type': res.objektTyp
            }

        except Exception:
            data = {
                'code': code,
                'lang': lang
            }

        fp = _fp(code, lang)
        with open(fp, 'w') as f:
            json.dump(data, f)

        sys.stdout.write('Saved to disk: %s .\n' % fp)


def run():
    i = 0
    for code in get_attribute_keys():
        get_information_for_attribute(code)
        i += 1
    sys.stdout.write('Obtained %s attributes from GENESIS server.\n' % i)
