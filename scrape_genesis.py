"""
scrape stuff from genesis webservice
"""

from scraper import get_attributes, get_tables


if __name__ == '__main__':
    get_attributes.run()
    get_tables.run()
