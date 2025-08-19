import graphene
import graphql_jwt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from graphql_jwt import Verify
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import get_payload, get_user_by_payload
from jwt import ExpiredSignatureError

from member.models import Member
from member.services.type import MemberType, UserType


class MemberQuery(graphene.ObjectType):
    # 전체 회원 불러오기
    all_members = graphene.List(MemberType)

    # 특정 문자열 반환
    hello = graphene.String(default_value="안녕하세요. JYP엔터테인먼트 백엔드 개발자로 지원하게 된 이원노입니다. 잘 부탁드립니다.")

    @classmethod
    def resolve_all_members(cls, root, info):
        return Member.objects.all()

    # 특정 회원 정보 불러오기
    get_member = graphene.Field(UserType, username=graphene.String())

    @classmethod
    def resolve_get_member(cls, root, info, username):
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

    @classmethod
    def mutate(cls, root, info, username, password, name, gender, email):
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


# 토큰 인증
class VerifyToken(Verify):
    user = graphene.Field(UserType)
    member = graphene.Field(MemberType)
    error = graphene.String()
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, token):
        try:
            payload = get_payload(token, info.context)
            user = get_user_by_payload(payload)

            if user is None:
                return VerifyToken(ok=False, error="사용자를 찾을 수 없습니다.")

            member = getattr(user, "member", None)
            return VerifyToken(user=user, member=member, ok=True)

        except ExpiredSignatureError:
            return VerifyToken(ok=False, error="토큰이 만료되었습니다.")
        except JSONWebTokenError:
            return VerifyToken(ok=False, error="유효하지 않은 토큰입니다.")


# class LoginUser(graphene.Mutation):
#     # 반환할 필드
#     user = graphene.Field(lambda: UserType)
#     member = graphene.Field(MemberType)
#     ok = graphene.Boolean()
#     error = graphene.String()
#
#     class Arguments:
#         # 클라이언트가 넘겨줄 인자
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#
#     @classmethod
#     def mutate(cls, root, info, username, password):
#         request = info.context
#         user = authenticate(request, username=username, password=password)
#
#         if user is None:
#             return LoginUser(ok=False, error="아이디 또는 비밀번호가 올바르지 않습니다.")
#
#         login(request, user)  # Django 세션 로그인 처리
#         member = getattr(user, "member", None)
#
#         return LoginUser(user=user, member=member, ok=True)


class MemberMutation(graphene.ObjectType):
    # 회원가입
    create_user = CreateUser.Field()

    # 로그인 및 토큰 발급
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    # 토큰 인증
    verify_token = VerifyToken.Field()
