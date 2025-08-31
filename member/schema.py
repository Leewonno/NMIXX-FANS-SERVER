import random
from datetime import timedelta

import graphene
import graphql_jwt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from graphql_jwt import Verify
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import get_payload, get_user_by_payload
from jwt import ExpiredSignatureError

from member.models import Member, Email
from member.type import MemberType, UserType


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
        nick = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, username, password, nick, email):
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
                nick=nick,
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


# 이메일 인증번호 전송
class SendVerificationCode(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, email):
        # 인증번호 생성
        code = str(random.randint(100000, 999999))  # 6자리 숫자
        # 만료시간
        expire_time = timezone.now() + timedelta(minutes=1)

        # 가입된 이메일이 있는 지 확인
        user = User.objects.filter(email=email)
        if user.exists():
            return SendVerificationCode(ok=False, error="이미 가입된 이메일입니다.")

        Email.objects.update_or_create(
            email=email,
            defaults={
                "code": code,
                "expire_at": expire_time
            }
        )

        send_mail(
            subject="이메일 인증번호",
            message=f"인증번호는 {code} 입니다. 1분 안에 입력해주세요.",
            from_email="noreply@yourdomain.com",
            recipient_list=[email],
        )

        return SendVerificationCode(ok=True)


# 이메일 인증번호 확인
class VerifyEmailCode(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        code = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, email, code):
        try:
            record = Email.objects.filter(email=email, code=code).latest("id")
        except Email.DoesNotExist:
            return VerifyEmailCode(ok=False, error="잘못된 인증번호입니다.")

        # 만료 여부 확인
        if not record.is_valid():
            return VerifyEmailCode(ok=False, error="인증번호가 만료되었습니다.")

        # 이메일 인증 성공 → 여기서 user 활성화 처리 or 가입 절차 계속 진행
        return VerifyEmailCode(ok=True)


class MemberMutation(graphene.ObjectType):
    # 회원가입
    create_user = CreateUser.Field()

    # 로그인 및 토큰 발급
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    # 토큰 인증
    verify_token = VerifyToken.Field()

    # 이메일 인증번호 전송
    send_verification_code = SendVerificationCode.Field()

    # 이메일 인증번호 확인
    verify_email_code = VerifyEmailCode.Field()


class MemberQuery(graphene.ObjectType):
    # 전체 회원 불러오기
    all_members = graphene.List(MemberType)

    @classmethod
    def resolve_all_members(cls, root, info):
        return Member.objects.all()

    # 특정 회원 정보 불러오기
    get_member = graphene.Field(UserType, username=graphene.String())

    @classmethod
    def resolve_get_member(cls, root, info, username):
        return User.objects.filter(username=username).first()


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
