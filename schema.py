import graphene

from database import DB
from models import Data
from relay import Node


class Query(graphene.ObjectType):
    node = Node.Field()
    districts = graphene.List(Data)

    def resolve_districts(self, info):
        return [Data(id=k, key='rs', value=k) for k in DB]


schema = graphene.Schema(query=Query)
