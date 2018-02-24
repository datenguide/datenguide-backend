"""
build data to provide via `flask.GraphQLView`
"""

from pipeline import build_data, build_keys_db, build_tree


if __name__ == '__main__':
    build_keys_db.run()
    build_data.run()
    build_tree.run()
