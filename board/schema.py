from datetime import datetime

import graphene
from django.db import transaction
from django.db.models import Q

from board.constant import TOKEN_ERROR_MESSAGE, BOARD_ERROR_MESSAGE
from board.models import Board, BoardComment, BoardLike, BoardLikeCount
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


# 게시글 좋아요
class UpdateBoardLike(graphene.Mutation):
    ok = graphene.Boolean()
    status = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        board_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, token, board_id, comment):
        member = get_member_from_token(token, info.context)

        if not member:
            return UpdateBoardLike(ok=False, error=TOKEN_ERROR_MESSAGE)

        board = Board.objects.get(id=board_id)

        if not board:
            return UpdateBoardLike(ok=False, error=BOARD_ERROR_MESSAGE)

        with transaction.atomic():
            # 좋아요 취소인지 생성(또는 업데이트) 인지 확인
            board_like = BoardLike.objects.filter(
                member=member,
                board=board,
            ).first()

            # 새로 생성
            if not board_like:
                # =======================
                # 좋아요 데이터 생성
                BoardLike.objects.create(
                    member=member,
                    board=board,
                )

                # =======================
                # 게시물 좋아요 개수 업데이트
                board.like += 1
                board.save()

                # =======================
                # 좋아요 카운트 테이블 생성 및 업데이트
                board_like_count = BoardLikeCount.objects.filter(
                    date=datetime.today(),
                    board=board,
                ).first()
                if board_like_count:
                    board_like_count.like += 1
                    board_like_count.save()
                else:
                    BoardLikeCount.objects.create(
                        date=datetime.today(),
                        board=board,
                        like=0
                    )
            # 좋아요 취소
            else:
                # =======================
                # 좋아요 데이터 삭제
                board_like.delete()

                # =======================
                # 게시물 좋아요 개수 업데이트
                board.like -= 1
                board.save()

                # =======================
                # 좋아요 카운트 테이블 업데이트
                board_like_count = BoardLikeCount.objects.filter(
                    date=datetime.today(),
                    board=board,
                ).first()
                if board_like_count:
                    board_like_count.like -= 1
                    board_like_count.save()

        return UpdateBoardLike(ok=True)


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
        role=graphene.String(required=True),
        page=graphene.Int(required=True),
        page_size=graphene.Int(default_value=10)
    )

    @classmethod
    def resolve_boards(cls, root, info, community, role, page, page_size):
        offset = (page - 1) * page_size
        return Board.objects.filter(
            ~Q(block=True),
            community=community,
            # 아티스트 게시판 role = 'C'
            # 일반 유저(팬) 게시판 role = 'A'
            member__role=role,
        ).order_by("-id")[offset:offset + page_size]

    # 특정 게시글 불러오기 (댓글과 함께)
    board = graphene.Field(
        BoardType,
        board_id=graphene.Int(required=True),
    )

    @classmethod
    def resolve_board(cls, root, info, board_id):
        try:
            return Board.objects.get(block=False, id=board_id)
        except Board.DoesNotExist:
            return None
