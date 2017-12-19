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

from database import DB


def resolver(root, info):
    return root.get(info.field_name)


def get_fields(field_dict, prefix='Data'):
    return {
        k: GraphQLField(GraphQLObjectType(
            '%s__%s' % (prefix, k),
            get_fields(
                field_dict[k],
                prefix='%s__%s' % (prefix, k)
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
    'District', fields=lambda: get_fields(DB.get_key_tree())
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
            resolver=lambda root, info, **args: DB[args['id']].data
        ),
        'districts': GraphQLField(GraphQLList(GraphQLString),
            resolver=lambda *args: DB.all()
        )
    }
)


schema = GraphQLSchema(query=query)
