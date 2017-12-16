"""
models for datenguide-backend as `graphene.ObjectType`
"""


import graphene

from relay import Node


class Dataset(graphene.ObjectType):
    tables = graphene.List(graphene.String)

    class Meta:
        interfaces = (Node,)


class DatasetConnection(graphene.relay.Connection):
    class Meta:
        node = Dataset


class District(graphene.ObjectType):
    rs = graphene.String()
    name = graphene.String()
    area = graphene.Float()
    f_pop = graphene.Int()
    m_pop = graphene.Int()
    t_pop = graphene.Int()
    munis = graphene.Int()
    pop_density = graphene.Float()
    state_id = graphene.String()
    state_name = graphene.String()
    date = graphene.String()

    data = graphene.relay.ConnectionField(DatasetConnection)

    def resolve_data(self, info):
        return []

    class Meta:
        interfaces = (Node,)
