import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from board.models import BoardComment, Board, BoardLike
from member.type import MemberType


class BoardCommentType(DjangoObjectType):
    member = graphene.Field(MemberType)

    class Meta:
        model = BoardComment
        fields = [
            'id',
            'comment',
        ]

    def resolve_member(self, info):
        return self.member


class BoardType(DjangoObjectType):
    member = graphene.Field(MemberType)
    board_comment = graphene.Field(BoardCommentType)
    board_comments = graphene.List(BoardCommentType)
    is_liked = graphene.Boolean()

    class Meta:
        model = Board
        # 명시적 필드
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'img_01',
            'img_02',
            'img_03',
            'img_04',
            'img_05',
        )

    def resolve_member(self, info):
        return self.member

    def resolve_board_comment(self, info):
        return BoardComment.objects.filter(board=self).last()

    def resolve_board_comments(self, info):
        return BoardComment.objects.filter(board=self)

    def resolve_is_liked(self, info):
        return getattr(self, "is_liked", False)


class UserType(DjangoObjectType):
    member = graphene.Field(MemberType)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def resolve_member(self, info):
        # user 인스턴스(self)에 연결된 Member를 반환
        # return Member.objects.filter(user_id=self.id).first()
        return self.member
