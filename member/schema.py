import graphene
import graphql_jwt
from django.contrib.auth.models import User

from member.models import Member
from member.service.verify import CreateUser, VerifyToken, SendVerificationCode, VerifyEmailCode
from member.type import MemberType, UserType


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
