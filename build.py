"""
build data to provide via `flask.GraphQLView`
"""

from pipeline import process, build_keys_db, build_tree


if __name__ == '__main__':
    build_keys_db.run()
    process.run()
    build_tree.run()
