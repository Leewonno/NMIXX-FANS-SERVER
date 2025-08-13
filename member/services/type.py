import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from member.models import Member


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        # 명시적 필드
        fields = (
            'id',
            'nick',
            'name',
            'gender'
        )


class UserType(DjangoObjectType):
    member = graphene.Field(MemberType)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def resolve_member(self, info):
        # user 인스턴스(self)에 연결된 Member를 반환
        # return Member.objects.filter(user_id=self.id).first()
        return self.member
