import graphene
from graphene_django import DjangoObjectType

from member.models import Member


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        fields = ('id', 'name', 'gender')  # 명시적 필드


class Query(graphene.ObjectType):
    all_members = graphene.List(MemberType)
    hello = graphene.String(default_value="Hello, GraphQL!")

    def resolve_all_members(self, info):
        print(info)
        return Member.objects.all()
