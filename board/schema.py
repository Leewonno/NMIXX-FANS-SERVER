import graphene

from board.constant import TOKEN_ERROR_MESSAGE, BOARD_ERROR_MESSAGE
from board.models import Board, BoardComment
from member.share import get_member_from_token


# 게시물 불러오기

# 게시글 작성
class CreateBoard(graphene.Mutation):
    # 반환할 필드
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        # 클라이언트가 넘겨줄 인자
        token = graphene.String(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        community = graphene.String(required=True)
        img_01 = graphene.String()
        img_02 = graphene.String()
        img_03 = graphene.String()
        img_04 = graphene.String()
        img_05 = graphene.String()

    @classmethod
    def mutate(cls, root, info, token, title, content, community, img_01=None, img_02=None, img_03=None, img_04=None, img_05=None):
        member = get_member_from_token(token, info.context)

        if not member:
            return CreateBoard(ok=False, error=TOKEN_ERROR_MESSAGE)

        Board.objects.create(
            title=title,
            content=content,
            member=member,
            community=community,
            img_01=img_01,
            img_02=img_02,
            img_03=img_03,
            img_04=img_04,
            img_05=img_05
        )

        return CreateBoard(ok=True)


# 댓글 작성
class CreateComment(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        boardId = graphene.Int(required=True)
        comment = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, token, boardId, comment):
        member = get_member_from_token(token, info.context)

        if not member:
            return CreateComment(ok=False, error=TOKEN_ERROR_MESSAGE)

        board = Board.objects.filter(id=boardId)

        if not board:
            return CreateComment(ok=False, error=BOARD_ERROR_MESSAGE)

        BoardComment.objects.create(
            comment=comment,
            member=member,
            board=board,
        )

        return CreateComment(ok=True)


class BoardMutation(graphene.ObjectType):
    # 게시글 작성
    create_board = CreateBoard.Field()
    # 댓글 작성
    create_comment = CreateComment.Field()


class BoardQuery(graphene.ObjectType):
    # 전체 회원 불러오기
    # all_members = graphene.List(MemberType)

    # @classmethod
    # def resolve_all_members(cls, root, info):
    #     return Member.objects.all()
    #
    # # 특정 회원 정보 불러오기
    # get_member = graphene.Field(UserType, username=graphene.String())
    #
    # @classmethod
    # def resolve_get_member(cls, root, info, username):
    #     return User.objects.filter(username=username).first()

    pass

