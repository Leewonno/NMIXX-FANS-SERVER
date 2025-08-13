import graphene
from django.contrib.auth.models import User
from django.db import transaction

from member.models import Member
from member.services.type import MemberType, UserType


class MemberQuery(graphene.ObjectType):
    # 전체 회원 불러오기
    all_members = graphene.List(MemberType)

    # 특정 문자열 반환
    hello = graphene.String(default_value="안녕하세요. JYP엔터테인먼트 백엔드 개발자로 지원하게 된 이원노입니다. 잘 부탁드립니다.")

    def resolve_all_members(self, info):
        return Member.objects.all()

    # 특정 회원 정보 불러오기
    get_member = graphene.Field(UserType, username=graphene.String())

    def resolve_get_member(self, info, username):
        return User.objects.filter(username=username).first()


class CreateUser(graphene.Mutation):
    # 반환할 필드
    user = graphene.Field(lambda: UserType)
    member = graphene.Field(MemberType)
    ok = graphene.Boolean()

    class Arguments:
        # 클라이언트가 넘겨줄 인자
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        gender = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, username, password, name, gender, email):
        with transaction.atomic():
            # 1. User 생성
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # 2. Member 생성 (User와 연결)
            member = Member.objects.create(
                user=user,
                name=name,
                gender=gender
            )

        return CreateUser(user=user, member=member, ok=True)


class MemberMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
