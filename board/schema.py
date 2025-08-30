from datetime import datetime, timedelta

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
    like = graphene.Int()

    class Arguments:
        token = graphene.String(required=True)
        board_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, token, board_id):
        member = get_member_from_token(token, info.context)

        if not member:
            return UpdateBoardLike(ok=False, error=TOKEN_ERROR_MESSAGE)

        board = Board.objects.get(id=board_id)

        if not board:
            return UpdateBoardLike(ok=False, error=BOARD_ERROR_MESSAGE)

        # 좋아요 + 1 -> status : True
        # 좋아요 - 1 -> status : False

        with transaction.atomic():
            # 좋아요 취소인지 생성(또는 업데이트) 인지 확인
            board_like = BoardLike.objects.filter(
                member=member,
                board=board,
            ).first()

            # 새로 생성
            if not board_like:
                status = True
                date = datetime.today()
                # =======================
                # 좋아요 데이터 생성
                BoardLike.objects.create(
                    member=member,
                    board=board,
                    date=date,
                )

                # =======================
                # 게시물 좋아요 개수 업데이트
                board.like += 1
                like = board.like
                board.save()

                # =======================
                # 좋아요 카운트 테이블 생성 및 업데이트
                board_like_count = BoardLikeCount.objects.filter(
                    date=date,
                    board=board,
                ).first()
                if board_like_count:
                    board_like_count.like += 1
                    board_like_count.save()
                else:
                    BoardLikeCount.objects.create(
                        date=date,
                        board=board,
                        like=1
                    )
            # 좋아요 취소
            else:
                status = False
                # =======================
                # 좋아요 데이터 삭제
                date = board_like.date
                board_like.delete()

                # =======================
                # 게시물 좋아요 개수 업데이트
                board.like -= 1
                like = board.like
                board.save()

                # =======================
                # 좋아요 카운트 테이블 업데이트
                board_like_count = BoardLikeCount.objects.filter(
                    date=date,
                    board=board,
                ).order_by('-id').first()
                if board_like_count:
                    board_like_count.like -= 1
                    board_like_count.save()

        return UpdateBoardLike(ok=True, status=status, like=like)


class BoardMutation(graphene.ObjectType):
    # 게시글 작성
    create_board = CreateBoard.Field()
    # 댓글 작성
    create_comment = CreateComment.Field()
    # 게시글 좋아요
    update_board_like = UpdateBoardLike.Field()


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
