"""
models for datenguide-backend as `graphene.ObjectType`
"""


import graphene


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
