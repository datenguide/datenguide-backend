"""
build data to provide via `flask.GraphQLView`
"""

from pipeline import process


if __name__ == '__main__':
    process.run()
