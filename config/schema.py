import graphene

from member.schema import MemberQuery, MemberMutation


class Query(MemberQuery, graphene.ObjectType):
    pass


class Mutation(MemberMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
