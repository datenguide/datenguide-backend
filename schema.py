from graphql.type import (GraphQLArgument,
                          # GraphQLBoolean,
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

from database import DB, DB_KEYS, KEYS, DTYPES


DTYPE_MAPPING = {
    'float': GraphQLFloat,
    'float64': GraphQLFloat,
    'str': GraphQLString,
    'int': GraphQLInt,
    'list': GraphQLList
}


def _get_key_info(key):
    return KEYS.get(key, {
        'id': key,
        'name': key.title(),
        'description': ''
    })


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


_region_lookups = {
    'nuts': lambda r, x: r.get('geo', {}).get('nuts', {}).get('level', None) == x,
    'parent': lambda r, x: r['id'][:len(x)] == x
}


def regions_resolver(*args, **kwargs):
    regions = Regions
    for key, value in kwargs.items():
        regions = [r for r in regions if _region_lookups[key](r, value)]
    return regions


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
        description=_get_key_info(key)['description'],
        resolver=arg_resolver
    )


def get_leaf_field(k, prefix):
    return GraphQLField(
        _get_field_type('%s__%s' % (prefix, k)),
        description=_get_key_info(k)['description'],
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
            description=_get_key_info(k)['description'],
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
            resolver=lambda root, info, **args: DB[args['id']]
        ),
        'regions': GraphQLField(
            GraphQLList(region),
            args={
                'nuts': GraphQLArgument(
                    description='NUTS level to filter Regions for',
                    type=GraphQLInt
                ),
                'parent': GraphQLArgument(
                    description='Parent region by ID',
                    type=GraphQLString
                )
            },
            resolver=regions_resolver
        ),
        'key': GraphQLField(
            key,
            args={
                'id': GraphQLArgument(
                    description='ID of the key',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=lambda root, info, **args: _get_key_info(args['id'])
        ),
        'keys': GraphQLField(
            GraphQLList(key),
            resolver=lambda *args: Keys
        )
    }
)


schema = GraphQLSchema(query=query)
