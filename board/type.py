import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from board.models import BoardComment, Board
from member.type import MemberType


class BoardCommentType(DjangoObjectType):
    class Meta:
        model = BoardComment
        fields = [
            'id',
            'comment',
        ]


class BoardType(DjangoObjectType):
    member = graphene.Field(MemberType)
    board_comment = graphene.Field(BoardCommentType)

    class Meta:
        model = Board
        # 명시적 필드
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'img_01',
        )

    def resolve_member(self, info):
        return self.member

    def resolve_board_comment(self, info):
        return BoardComment.objects.filter(member=self.member).last()


class UserType(DjangoObjectType):
    member = graphene.Field(MemberType)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def resolve_member(self, info):
        # user 인스턴스(self)에 연결된 Member를 반환
        # return Member.objects.filter(user_id=self.id).first()
        return self.member
