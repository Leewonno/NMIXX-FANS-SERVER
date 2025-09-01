# JWT 토큰 인증 / 이메일 인증
import random
from datetime import timedelta

import graphene
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from graphql_jwt import Verify
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import get_payload, get_user_by_payload
from jwt.exceptions import ExpiredSignatureError

from member.models import Email
from member.type import UserType, MemberType


# 회원가입
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
