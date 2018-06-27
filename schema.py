from graphql.type import (GraphQLArgument,
                          GraphQLBoolean,
                          GraphQLField,
                          GraphQLFloat,
                          GraphQLInt,
                          GraphQLList,
                          GraphQLNonNull,
                          GraphQLObjectType,
                          GraphQLSchema,
                          GraphQLString)

from storage import ElasticStorage


Storage = ElasticStorage()


DTYPE_MAPPING = {
    'bool': GraphQLBoolean,
    'float': GraphQLFloat,
    'str': GraphQLString,
    'int': GraphQLInt,
    'long': GraphQLInt,
    'list': GraphQLList
}


def r(root, info, *args, **kwargs):
    return root.get(info.field_name)


def get_arg_description(arg_info):
    return '{name}\n\n*Mögliche Werte:*\n\n{values}'.format(
        name=arg_info['name'],
        values='\n\n'.join(['**{value}** - {name}'.format(**v) for v in arg_info['values']])
    )


SOURCE_FIELDS = ('title_de', 'valid_from', 'periodicity', 'name', 'url')


source = GraphQLObjectType(
    'Source',
    fields=lambda: {f: GraphQLField(GraphQLString, resolver=r) for f in SOURCE_FIELDS}
)


base_fact_fields = {
    'id': GraphQLField(GraphQLString, resolver=r),
    'year': GraphQLField(GraphQLString, resolver=r),
    'source': GraphQLField(source, resolver=r)
}


def build_fact(name, info):
    fields = {k: GraphQLField(GraphQLString, resolver=r) for k in info['args'].keys()}
    fields.update(base_fact_fields)
    fields.update(value=GraphQLField(DTYPE_MAPPING.get(Storage.dtypes.get(name, 'str'), GraphQLString), resolver=r))
    return GraphQLObjectType(name, fields=fields)


def get_args(args):
    args = {
        arg: GraphQLArgument(
            description=get_arg_description(arg_info),
            type=GraphQLString
        )
        for arg, arg_info in args
    }
    args.update({
        'year': GraphQLArgument(
            description='Jahr oder Jahr des Stichtages',
            type=GraphQLString
        )
    })
    return args


fields = {
    root: GraphQLField(
        GraphQLList(build_fact(root, info)),
        description=info['name'],
        args=get_args(info['args'].items()),
        resolver=r
    )
    for root, info in Storage.schema.items()
}


fields.update({
    'id': GraphQLField(
        GraphQLString,
        description='Regionalschlüssel',
        resolver=r
    )
})

region = GraphQLObjectType('Region', fields=lambda: fields)

# key = GraphQLObjectType(
#     'Key', fields={
#         'id': GraphQLField(GraphQLString, resolver=r),
#         'name': GraphQLField(GraphQLString, resolver=r),
#         'description': GraphQLField(GraphQLString, resolver=r)
#     }
# )


query = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'region': GraphQLField(
            region,
            args={
                'id': GraphQLArgument(
                    description='Regionalschlüssel',
                    type=GraphQLNonNull(GraphQLString)
                )
            },
            resolver=Storage.region_resolver
        ),
        'regions': GraphQLField(
            GraphQLList(region),
            args={
                arg: GraphQLArgument(
                    description=info['description'],
                    type=DTYPE_MAPPING[info['type']]
                ) for arg, info in Storage.lookups.items()
            },
            resolver=Storage.regions_resolver
        ),
        # 'key': GraphQLField(
        #     key,
        #     args={
        #         'id': GraphQLArgument(
        #             description='ID of the key',
        #             type=GraphQLNonNull(GraphQLString)
        #         )
        #     },
        #     resolver=lambda root, info, **args: Storage.get_key(args['id'])
        # ),
        # 'keys': GraphQLField(
        #     GraphQLList(key),
        #     resolver=lambda *args: Storage.get_keys()
        # )
    }
)


schema = GraphQLSchema(query=query)
