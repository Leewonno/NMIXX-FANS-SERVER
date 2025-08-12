import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from member.models import Member


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        fields = ('id', 'name', 'gender')  # 명시적 필드


class UserType(DjangoObjectType):
    member = graphene.Field(MemberType)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def resolve_member(self, info):
        # user 인스턴스(self)에 연결된 Member를 반환
        # return Member.objects.filter(user_id=self.id).first()
        return self.member
        # 또는 self.member (OneToOneField면) 사용 가능


class Query(graphene.ObjectType):
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


class CreateMember(graphene.Mutation):
    # Mutation 결과로 반환할 필드들
    member = graphene.Field(MemberType)
    ok = graphene.Boolean()

    class Arguments:
        # 클라이언트가 넘겨줄 인자
        name = graphene.String(required=True)
        gender = graphene.String(required=True)
        user_id = graphene.Int(required=True)  # 외래키인 User ID

    def mutate(self, info, name, gender, user_id):
        member = Member(name=name, gender=gender, user_id=user_id)
        member.save()
        return CreateMember(member=member, ok=True)


class Mutation(graphene.ObjectType):
    create_member = CreateMember.Field()