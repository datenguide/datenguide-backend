from graphql.type import (GraphQLArgument,
                          # GraphQLBoolean,
                          # GraphQLEnumType,
                          # GraphQLEnumValue,
                          GraphQLField,
                          # GraphQLInterfaceType,
                          GraphQLList,
                          GraphQLNonNull,
                          GraphQLObjectType,
                          GraphQLSchema,
                          GraphQLString)
from util import slugify as _slugify

from database import DB, DB_KEYS, KEYS


def _get_key_info(key):
    return KEYS.get(key, {
        'id': key,
        'name': key.title(),
        'description': ''
    })


Regions = [DB[k] for k in sorted(DB.keys())]
Keys = [KEYS[k] for k in sorted(KEYS.keys())]


def slugify(value):
    if '__' in value or value.startswith('_'):
        return value
    return _slugify(value, to_lower=False, separator='_')


def resolver(root, info, *args, **kwargs):
    return root.get(info.field_name)


def arg_resolver(root, info, *args, **kwargs):
    data = root.get(info.field_name)
    if data:
        try:
            lookup = ':'.join(list(kwargs.items())[0])  # FIXME
            return data.get(lookup)
        except IndexError:  # return last value
            return data.get(sorted(data.keys())[-1])


def get_queryable_field(data):
    args = set([k.split(':')[0] for k in data.keys()])
    return GraphQLField(
        GraphQLString,
        args={
            arg: GraphQLArgument(
                description=arg.title(),
                type=GraphQLString
            )
            for arg in args
        },
        resolver=arg_resolver
    )


def get_leaf_field(k):
    return GraphQLField(
        GraphQLString,
        description=_get_key_info(k)['description'],
        resolver=resolver
    )


def get_fields(field_dict, prefix='Region'):
    return {
        slugify(k):

        get_queryable_field(field_dict[k])
        if field_dict[k].keys() and all(':' in k for k in field_dict[k].keys())

        else GraphQLField(GraphQLObjectType(
            '%s__%s' % (prefix, slugify(k)),
            get_fields(
                field_dict[k],
                prefix='%s__%s' % (prefix, slugify(k))
            )),
            description=_get_key_info(k)['description'],
            resolver=resolver
        )
        if field_dict[k].keys()

        else get_leaf_field(k)

        for k in field_dict
    }


region = GraphQLObjectType(
    'Region', fields=lambda: get_fields(DB_KEYS)
)

key = GraphQLObjectType(
    'Key', fields={
        'id': GraphQLField(GraphQLString, resolver=resolver),
        'name': GraphQLField(GraphQLString, resolver=resolver),
        'description': GraphQLField(GraphQLString, resolver=resolver)
    }
)


query = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'region': GraphQLField(
            region,
            args={
                'id': GraphQLArgument(
                    description='ID (Regionalschlüssel) of the region',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=lambda root, info, **args: DB[args['id']]
        ),
        'regions': GraphQLField(
            GraphQLList(region),
            resolver=lambda *args: Regions
        ),
        'key': GraphQLField(
            key,
            args={
                'id': GraphQLArgument(
                    description='ID of the key',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=lambda root, info, **args: KEYS[args['id']]
        ),
        'keys': GraphQLField(
            GraphQLList(key),
            resolver=lambda *args: Keys
        )
    }
)


schema = GraphQLSchema(query=query)
