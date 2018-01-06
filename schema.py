from graphql.type import (GraphQLArgument,
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

from database import DB, Districts, KEYS


def slugify(value):
    return _slugify(value, to_lower=False, separator='_')


def resolver(root, info):
    if hasattr(root, 'get'):
        return root.get(info.field_name)
    return root  # FIXME


def get_fields(field_dict, prefix='District'):
    return {
        slugify(k): GraphQLField(GraphQLObjectType(
            '%s__%s' % (prefix, slugify(k)),
            get_fields(
                field_dict[k],
                prefix='%s__%s' % (prefix, slugify(k))
            )),
            resolver=resolver
        )
        if field_dict[k].keys()
        else GraphQLField(
            GraphQLString,
            resolver=resolver
        )
        for k in field_dict
    }


district = GraphQLObjectType(
    'District', fields=lambda: get_fields(KEYS)
)


query = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'district': GraphQLField(district,
            args={
                'id': GraphQLArgument(
                    description='RS of the district',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=lambda root, info, **args: DB[args['id']]
        ),
        'districts': GraphQLField(GraphQLList(district),
            resolver=lambda *args: Districts
        )
    }
)


schema = GraphQLSchema(query=query)
