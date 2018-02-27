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

from database import DB, Regions, KEYS, get_key_info


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
        description=get_key_info(k)['description'],
        resolver=resolver
    )


def get_fields(field_dict, prefix='District'):
    return {
        slugify(k): get_queryable_field(field_dict[k])
        if field_dict[k].keys() and all(':' in k for k in field_dict[k].keys())

        else GraphQLField(GraphQLObjectType(
            '%s__%s' % (prefix, slugify(k)),
            get_fields(
                field_dict[k],
                prefix='%s__%s' % (prefix, slugify(k))
            )),
            description=get_key_info(k)['description'],
            resolver=resolver
        )
        if field_dict[k].keys()

        else get_leaf_field(k)

        for k in field_dict
    }


region = GraphQLObjectType(
    'Region', fields=lambda: get_fields(KEYS)
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
        )
    }
)


schema = GraphQLSchema(query=query)
# FIXME
doc_schema = {k: v for k, v in schema.get_type_map().items()
              if not k.startswith('__') and k not in
              ('Query', 'String', 'Boolean')}
