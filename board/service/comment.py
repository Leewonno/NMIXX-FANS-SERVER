# 댓글 작성
import graphene

from board.constant import TOKEN_ERROR_MESSAGE, BOARD_ERROR_MESSAGE, NOT_MASTER_ERROR_MESSAGE
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


class UpdateComment(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        comment_id = graphene.Int(required=True)
        comment = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, token, comment_id, comment):
        member = get_member_from_token(token, info.context)

        if not member:
            return UpdateComment(ok=False, error=TOKEN_ERROR_MESSAGE)

        # 댓글 정보 불러오기
        qs = BoardComment.objects.get(id=comment_id)

        # 삭제된 경우
        if not qs:
            return UpdateComment(ok=False, error=BOARD_ERROR_MESSAGE)

        # 작성자가 맞는 지 확인
        if member.id != qs.id:
            return UpdateComment(ok=False, error=NOT_MASTER_ERROR_MESSAGE)

        qs.comment = comment
        qs.save()

        return UpdateComment(ok=True)


class DeleteComment(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        comment_id = graphene.Int(required=True)
        comment = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, token, comment_id, comment):
        member = get_member_from_token(token, info.context)

        if not member:
            return DeleteComment(ok=False, error=TOKEN_ERROR_MESSAGE)

        # 댓글 정보 불러오기
        qs = BoardComment.objects.get(id=comment_id)

        if not qs:
            return DeleteComment(ok=False, error=BOARD_ERROR_MESSAGE)

        # 작성자가 맞는 지 확인
        if member.id != qs.id:
            return UpdateComment(ok=False, error=NOT_MASTER_ERROR_MESSAGE)

        # 삭제
        qs.delete()

        return DeleteComment(ok=True)
