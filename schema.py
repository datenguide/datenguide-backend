import graphene

from stores.districts import DistrictStore
from models import District


class DistrictQuery(graphene.ObjectType):
    districts = graphene.List(District)
    district = graphene.Field(District, id=graphene.String())

    def resolve_districts(self, info):
        return DistrictStore.all()

    def resolve_district(self, info, id):
        return DistrictStore.get(id)


districts = graphene.Schema(query=DistrictQuery)
