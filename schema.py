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

from storage import Storage
from util import get_arg_description, get_field_description


DTYPE_MAPPING = {
    'bool': GraphQLBoolean,
    'boolean': GraphQLBoolean,
    'float': GraphQLFloat,
    'str': GraphQLString,
    'text': GraphQLString,
    'int': GraphQLInt,
    'long': GraphQLInt,
    'list': GraphQLList
}


def r(root, info, *args, **kwargs):
    return root.get(info.field_name)


SOURCE_FIELDS = ('title_de', 'valid_from', 'periodicity', 'name', 'url')


source = GraphQLObjectType(
    'Quelle',
    description='Quellenverweis zur GENESIS Regionaldatenbank',
    fields=lambda: {f: GraphQLField(GraphQLString, resolver=r) for f in SOURCE_FIELDS}
)


base_fact_fields = {
    'id': GraphQLField(GraphQLString, resolver=r, description='Interne eindeutige id'),
    'year': GraphQLField(GraphQLString, resolver=r, description='Jahr oder Jahr des Stichtages'),
    'date': GraphQLField(GraphQLString, resolver=r, description='Stichtag'),
    'source': GraphQLField(source, resolver=r, description='Quellenverweis zur GENESIS Regionaldatenbank')
}


def build_fact(name, info):
    fields = {k: GraphQLField(GraphQLString, resolver=r) for k in info['args'].keys()}
    fields.update(base_fact_fields)
    fields.update(value=GraphQLField(DTYPE_MAPPING.get(Storage.dtypes.get(name, 'str'), GraphQLString), resolver=r))
    return GraphQLObjectType(name, description=get_field_description(info), fields=fields)


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
        description=get_field_description(info),
        args=get_args(info['args'].items()),
        resolver=r
    )
    for root, info in sorted(Storage.schema.items(), key=lambda x: x[0])
}


fields.update({
    'id': GraphQLField(
        GraphQLString,
        description='Regionalschlüssel',
        resolver=r
    ),
    'name': GraphQLField(
        GraphQLString,
        description='Name',
        resolver=r
    )
})


region = GraphQLObjectType(
    'Region',
    description='Eine statistische Region in Deutschland.\n\n*(Bundesland, Kreis, Regierungsbezirk, Gemeinde)*',
    fields=fields
)


query = GraphQLObjectType(
    'genesapi',
    description='Graphql-API zum Datenbestand der GENESIS-Datenbank "Regionalstatistik"',
    fields=lambda: {
        'region': GraphQLField(
            region,
            description='Detail-Endpunkt zur Abfrage exakt einer Region',
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
            description='Listen-Endpunkt zur Abfrage mehrerer Regionen',
            args={
                arg: GraphQLArgument(
                    description=info['description'],
                    type=DTYPE_MAPPING[info['type']]
                ) for arg, info in Storage.lookups.items()
            },
            resolver=Storage.regions_resolver
        )
    }
)


schema = GraphQLSchema(query=query)
