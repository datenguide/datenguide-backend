from graphql.type import (GraphQLArgument,
                          GraphQLBoolean,
                          # GraphQLEnumType,
                          # GraphQLEnumValue,
                          GraphQLField,
                          GraphQLFloat,
                          GraphQLInt,
                          # GraphQLInterfaceType,
                          GraphQLList,
                          GraphQLNonNull,
                          GraphQLObjectType,
                          GraphQLSchema,
                          GraphQLString)
from util import slugify as _slugify

from database import DB_KEYS, DTYPES
from storage import Storage


DTYPE_MAPPING = {
    'bool': GraphQLBoolean,
    'float': GraphQLFloat,
    'float64': GraphQLFloat,
    'str': GraphQLString,
    'int': GraphQLInt,
    'list': GraphQLList
}


def _get_field_type(key_path):
    if '__years___' in key_path:  # FIXME?
        return GraphQLFloat
    if key_path.startswith('Region__'):
        key_path = key_path[8:]
    dtype = DTYPES.get(key_path, '')
    try:
        return DTYPE_MAPPING[dtype]
    except KeyError:
        if dtype.startswith('list__'):
            try:
                inner_dtype = DTYPE_MAPPING[dtype.split('__')[1]]
                return GraphQLList(inner_dtype)
            except KeyError:
                pass
    return GraphQLString


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


def get_queryable_field(data, key, prefix):
    args = set([k.split(':')[0] for k in data.keys()])
    return GraphQLField(
        _get_field_type('%s__%s' % (prefix, key)),
        args={
            arg: GraphQLArgument(
                description=arg.title(),
                type=GraphQLString
            )
            for arg in args
        },
        description=Storage.get_key(key)['description'],
        resolver=arg_resolver
    )


def get_leaf_field(k, prefix):
    return GraphQLField(
        _get_field_type('%s__%s' % (prefix, k)),
        description=Storage.get_key(k)['description'],
        resolver=resolver
    )


def get_fields(field_dict, prefix='Region'):
    return {
        slugify(k):

        get_queryable_field(field_dict[k], k, prefix)
        if field_dict[k].keys() and all(':' in k for k in field_dict[k].keys())

        else GraphQLField(GraphQLObjectType(
            '%s__%s' % (prefix, slugify(k)),
            get_fields(
                field_dict[k],
                prefix='%s__%s' % (prefix, slugify(k))
            )),
            description=Storage.get_key(k)['description'],
            resolver=resolver
        )
        if field_dict[k].keys()

        else get_leaf_field(k, prefix)

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
            resolver=lambda root, info, **kwargs: Storage.get_region(kwargs['id'])
        ),
        'regions': GraphQLField(
            GraphQLList(region),
            args={
                arg: GraphQLArgument(
                    description=info['description'],
                    type=DTYPE_MAPPING[info['type']]
                ) for arg, info in Storage.lookups.items()
            },
            resolver=lambda root, info, **kwargs: Storage.get_regions(info, **kwargs)
        ),
        'key': GraphQLField(
            key,
            args={
                'id': GraphQLArgument(
                    description='ID of the key',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=lambda root, info, **args: Storage.get_key(args['id'])
        ),
        'keys': GraphQLField(
            GraphQLList(key),
            resolver=lambda *args: Storage.get_keys()
        )
    }
)


schema = GraphQLSchema(query=query)
