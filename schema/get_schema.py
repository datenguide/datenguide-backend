from graphql.type import (GraphQLArgument,
                          GraphQLBoolean,
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

from database import DB, Districts, KEYS, get_key_info


def slugify(value):
    return _slugify(value, to_lower=False, separator='_')


def resolver(root, info, *args, **kwargs):
    return root.get(info.field_name)


def arg_resolver(root, info, *args, **kwargs):
    data = root.get(info.field_name)
    try:
        key, value = list(kwargs.items())[0]  # FIXME
    except IndexError:  # return last value
        return data.get(sorted(data.keys())[-1])
    lookup = '%s:%s' % (key, value)
    if key.endswith('__in'):
        return value
    if key.endswith('__all'):
        return data
    return data.get(lookup)


def get_queryable_field(data):
    args = {}
    for arg in set([k.split(':')[0] for k in data.keys()]):
        args[arg] = GraphQLArgument(
            description=arg.title(),
            type=GraphQLString
        )
        args['%s__in' % arg] = GraphQLArgument(
            description='%ss, as list' % arg.title(),
            type=GraphQLList(GraphQLString)
        )
        args['%s__all' % arg] = GraphQLArgument(
            description='All values for "%s"' % arg,
            type=GraphQLBoolean
        )

    return GraphQLField(
        GraphQLString,
        args=args,
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
        if field_dict[k] and all(':' in k for k in field_dict[k].keys())

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


district = GraphQLObjectType(
    'District', fields=lambda: get_fields(KEYS)
)


query = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'district': GraphQLField(
            district,
            args={
                'id': GraphQLArgument(
                    description='RS of the district',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=lambda root, info, **args: DB[args['id']]
        ),
        'districts': GraphQLField(
            GraphQLList(district),
            resolver=lambda *args: Districts
        )
    }
)


schema = GraphQLSchema(query=query)
# FIXME
doc_schema = {k: v for k, v in schema.get_type_map().items()
              if not k.startswith('__') and k not in
              ('Query', 'String', 'Boolean')}
