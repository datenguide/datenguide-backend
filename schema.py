import graphene

from stores.districts import DistrictStore
from stores.datasets import DatasetStore
from models import District, Dataset
from relay import Node


class Query(graphene.ObjectType):
    node = Node.Field()
    districts = graphene.List(District)
    datasets = graphene.List(Dataset)

    def resolve_datasets(self, info):
        return DatasetStore.all()

    def resolve_districts(self, info):
        return DistrictStore.all()


schema = graphene.Schema(query=Query)
