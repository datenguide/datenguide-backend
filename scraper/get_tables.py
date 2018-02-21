import os
import sys

import settings

from .clients import ResearchClient   # , ExportClient


def _fp(code):
    return os.path.join(settings.DATA_SRC, '%s.csv' % code)


def get_statistics():
    for i in range(10)[1:]:
        sys.stdout.write('Retrieving statistics starting with "%s" ...\n' % i)
        res = ResearchClient.service.StatistikKatalog(
            kennung=settings.GENESIS_USERNAME,
            passwort=settings.GENESIS_PASSWORD,
            filter='%s*' % i,
            kriterium='Code',
            sprache='de',   # FIXME make multilingual
            listenLaenge=500
        )

        if len(res.statistikKatalogEintraege) == 500:
            sys.stderr.write('ERROR: There are more than 500 statistics starting with "%s"!\n' % i)
        else:
            for statistic in res.statistikKatalogEintraege:
                code = statistic.find('code').text
                name = statistic.find('inhalt').text.replace('\n', ' ')
                sys.stdout.write('found statistic "%s - %s"\n' % (code, name))
                yield code, name


def get_tables_for_statistic(statistic_code):
    sys.stdout.write('Retrieving tables for statistic "%s" ...\n' % statistic_code)

    try:
        res = ResearchClient.service.StatistikTabellenKatalog(
            kennung=settings.GENESIS_USERNAME,
            passwort=settings.GENESIS_PASSWORD,
            name=statistic_code,
            auswahl='*',
            bereich='alle',
            sprache='de',   # FIXME make multilingual
            listenLaenge=500
        )

        if len(res.statistikTabellenKatalogEintraege) == 500:
            sys.stderr.write('ERROR: There are more than 500 tables for statistic "%s"!\n' % statistic_code)
        else:
            for table in res.statistikTabellenKatalogEintraege:
                code = table.find('code').text
                name = table.find('inhalt').text.replace('\n', ' ')
                sys.stdout.write('found table "%s - %s"\n' % (code, name))
                yield code, name

    except Exception as e:
        with open(_fp('_log'), 'a') as f:
            f.write('ERROR : %s : %s\n\n\n' % (statistic_code, str(e)))


def run():
    i = 0
    fp = _fp('_tables_meta')
    with open(fp, 'w') as f:
        f.write(','.join(('statistic_code', 'statistic_name', 'table_code', 'table_name')) + '\n')
    for statistic_code, statistic_name in get_statistics():
        for table_code, table_name in get_tables_for_statistic(statistic_code):
            with open(fp, 'a') as f:
                f.write(','.join((statistic_code, '"%s"' % statistic_name, table_code, '"%s"' % table_name)) + '\n')
            i += 1
    sys.stdout.write('Obtained %s table ids from GENESIS server.\n' % i)
