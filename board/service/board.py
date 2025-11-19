# 게시글 좋아요
from datetime import datetime

import graphene
from django.db import transaction

from board.constant import TOKEN_ERROR_MESSAGE, BOARD_ERROR_MESSAGE, NOT_MASTER_ERROR_MESSAGE
from board.models import BoardLike, BoardLikeCount, Board
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


# 게시글 수정
class UpdateBoard(graphene.Mutation):
    # 반환할 필드
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        # 클라이언트가 넘겨줄 인자
        token = graphene.String(required=True)
        # Board id
        board_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        img_01 = graphene.String()
        img_02 = graphene.String()
        img_03 = graphene.String()
        img_04 = graphene.String()
        img_05 = graphene.String()

    @classmethod
    def mutate(cls, root, info, board_id, token, title, content, img_01=None, img_02=None, img_03=None, img_04=None, img_05=None):
        member = get_member_from_token(token, info.context)

        if not member:
            return UpdateBoard(ok=False, error=TOKEN_ERROR_MESSAGE)

        # 게시물 정보 불러오기
        qs = Board.objects.get(id=board_id)

        # 삭제된 경우
        if not qs:
            return UpdateBoard(ok=False, error=BOARD_ERROR_MESSAGE)

        # 작성자가 맞는 지 확인
        if member.id != qs.id:
            return UpdateBoard(ok=False, error=NOT_MASTER_ERROR_MESSAGE)

        qs.title = title
        qs.content = content
        qs.img_01 = img_01
        qs.img_02 = img_02
        qs.img_03 = img_03
        qs.img_04 = img_04
        qs.img_05 = img_05
        qs.save()

        return UpdateBoard(ok=True)


# 게시글 삭제
class DeleteBoard(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        board_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, token, board_id, comment):
        member = get_member_from_token(token, info.context)

        if not member:
            return DeleteBoard(ok=False, error=TOKEN_ERROR_MESSAGE)

        qs = Board.objects.get(id=board_id)

        # 이미 존재하지 않는 문서일 경우
        if not qs:
            return DeleteBoard(ok=False, error=BOARD_ERROR_MESSAGE)

        # 관리자 권한이 있으면 삭제 가능 / 관리자가 아닌 경우는 본인만 삭제 가능
        if member.role == 'B':
            qs.delete()
        else:
            # 본인인 맞는 지 확인
            if qs.member.id != member.id:
                return DeleteBoard(ok=False, error=NOT_MASTER_ERROR_MESSAGE)
            qs.delete()
        return DeleteBoard(ok=True)


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
