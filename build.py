"""
build data to provide via `flask.GraphQLView`
"""

from pipeline import process_districts


if __name__ == '__main__':
    process_districts()
