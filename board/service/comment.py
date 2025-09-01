# 댓글 작성
import graphene

from board.constant import TOKEN_ERROR_MESSAGE, BOARD_ERROR_MESSAGE
from board.models import Board, BoardComment
from member.share import get_member_from_token


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
