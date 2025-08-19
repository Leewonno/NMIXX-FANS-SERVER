import graphene
from django.db.models import Q

from board.constant import TOKEN_ERROR_MESSAGE, BOARD_ERROR_MESSAGE
from board.models import Board, BoardComment
from board.type import BoardType
from member.share import get_member_from_token


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
        board_id = graphene.Int(required=True)
        comment = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, token, board_id, comment):
        member = get_member_from_token(token, info.context)

        if not member:
            return CreateComment(ok=False, error=TOKEN_ERROR_MESSAGE)

        board = Board.objects.get(id=board_id)

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
    # 특정 게시판(커뮤니티)에 게시글 불러오기
    boards = graphene.List(
        BoardType,
        community=graphene.String(required=True),
        page=graphene.Int(required=True),
        page_size=graphene.Int(default_value=10)
    )

    # 특정 게시글 불러오기 (댓글과 함께)
    board = graphene.Field(
        BoardType,
        board_id=graphene.Int(required=True),
    )

    @classmethod
    def resolve_boards(cls, root, info, community, page, page_size):
        offset = (page - 1) * page_size
        return Board.objects.filter(~Q(block=True), community=community ).order_by("-id")[offset:offset + page_size]

    @classmethod
    def resolve_board(cls, root, info, board_id):
        try:
            return Board.objects.get(block=False, id=board_id)
        except Board.DoesNotExist:
            return None
