from datetime import datetime, timedelta

import graphene
from django.db.models import Q

from board.models import Board, BoardLike, BoardLikeCount
from board.service.board import UpdateBoardLike, CreateBoard, UpdateBoard, DeleteBoard
from board.service.comment import CreateComment, UpdateComment, DeleteComment
from board.type import BoardType
from member.share import get_member_from_token


# POST
class BoardMutation(graphene.ObjectType):
    # 게시글 작성
    create_board = CreateBoard.Field()
    # 게시글 수정
    update_board = UpdateBoard.Field()
    # 게시글 삭제
    delete_board = DeleteBoard.Field()
    # 댓글 작성
    create_comment = CreateComment.Field()
    # 게시글 좋아요
    update_board_like = UpdateBoardLike.Field()
    # 댓글 수정
    update_comment = UpdateComment.Field()
    # 댓글 삭제
    delete_comment = DeleteComment.Field()
    # 댓글 좋아요


# GET
class BoardQuery(graphene.ObjectType):
    # 특정 게시판(커뮤니티)에 게시글 불러오기
    boards = graphene.List(
        BoardType,
        community=graphene.String(required=True),
        role=graphene.String(required=True),
        page=graphene.Int(required=True),
        page_size=graphene.Int(default_value=10),
        token=graphene.String(required=False),
    )

    @classmethod
    def resolve_boards(cls, root, info, community, role, page, page_size, token):
        # 로그인한 유저 정보 가져오기
        member = get_member_from_token(token, info.context)
        offset = (page - 1) * page_size
        qs = Board.objects.filter(
            ~Q(block=True),
            community=community,
            # 아티스트 게시판 role = 'C'
            # 일반 유저(팬) 게시판 role = 'A'
            member__role=role,
        ).order_by("-id")[offset:offset + page_size]

        board_ids = [board.id for board in qs]

        # 좋아요 체크
        if member:
            liked_ids = set(
                BoardLike.objects.filter(
                    member_id=member.id,
                    board_id__in=board_ids
                ).values_list("board_id", flat=True)
            )
            for item in qs:
                item.is_liked = item.id in liked_ids
        else:
            for item in qs:
                item.is_liked = False
        return qs

    # 특정 게시글 불러오기 (댓글과 함께)
    board = graphene.Field(
        BoardType,
        board_id=graphene.Int(required=True),
        token=graphene.String(required=True),
    )

    @classmethod
    def resolve_board(cls, root, info, board_id, token):
        # 로그인한 유저 정보 가져오기
        member = get_member_from_token(token, info.context)
        item = Board.objects.get(block=False, id=board_id)

        # 좋아요 체크
        if member:
            liked_ids = set(
                BoardLike.objects.filter(
                    member_id=member.id,
                    board_id=board_id
                ).values_list("board_id", flat=True)
            )
            item.is_liked = item.id in liked_ids
        else:
            item.is_liked = False

        try:
            return item
        except Board.DoesNotExist:
            return None

    # 전날 인기글
    popular_boards = graphene.List(
        BoardType,
        community=graphene.String(required=True),
    )

    @classmethod
    def resolve_popular_boards(cls, root, info, community):
        yesterday = datetime.today() - timedelta(days=1)
        # 전날 인기글 10개 불러옴
        qs_like_count = BoardLikeCount.objects.filter(
            date=yesterday,
        ).order_by('-like')[:10]

        board_ids = [i.board_id for i in qs_like_count]

        # 아티스트 게시판은 가져오지 않음
        qs = Board.objects.filter(
            ~Q(block=True),
            id__in=board_ids,
            community=community,
            # 일반 유저(팬) 게시판 role = 'A'
            member__role='A',
        ).order_by("-id")[:10]

        return list(qs)
