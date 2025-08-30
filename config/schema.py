import graphene

from board.schema import BoardMutation, BoardQuery
from kpop.schema import UploadMutation
from member.schema import MemberQuery, MemberMutation


class Query(MemberQuery, BoardQuery, graphene.ObjectType):
    pass


class Mutation(MemberMutation, BoardMutation, UploadMutation, graphene.ObjectType):
    # 토큰 재발급 (Refresh 토큰 필요시)
    # refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
