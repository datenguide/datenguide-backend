"""
build data to provide via `flask.GraphQLView`
"""

from pipeline import process_districts, process_datasets


if __name__ == '__main__':
    process_districts()
    process_datasets()
