import graphene
from member.schema import Query as CoreQuery


class Query(CoreQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
