import graphene

from member.schema import MemberQuery, MemberMutation


class Query(MemberQuery, graphene.ObjectType):
    pass


class Mutation(MemberMutation, graphene.ObjectType):
    # 토큰 재발급 (Refresh 토큰 필요시)
    # refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
