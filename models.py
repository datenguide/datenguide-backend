"""
models for datenguide-backend as `graphene.ObjectType`
"""


import graphene

from database import DB
from relay import Node


class Data(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()
    data = graphene.List(lambda: Data)

    def resolve_data(self, info):
        if isinstance(self.data, list):
            return self.data
        return Node.get_node_from_global_id(info, 'Data:%s' % self.id).data

    class Meta:
        interfaces = (Node,)
