from django.db import models

from member.models import Member


class Board(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    # '제목'
    title = models.CharField(max_length=100, verbose_name='제목', null=False)

    # '내용'
    content = models.TextField(verbose_name='내용', null=False, blank=False)

    # '커뮤니티'
    community = models.CharField(max_length=50, verbose_name='커뮤니티', null=False, blank=False)

    # '이미지'
    img_01 = models.ImageField(upload_to="img", null=True, blank=True)
    img_02 = models.ImageField(upload_to="img", null=True, blank=True)
    img_03 = models.ImageField(upload_to="img", null=True, blank=True)
    img_04 = models.ImageField(upload_to="img", null=True, blank=True)
    img_05 = models.ImageField(upload_to="img", null=True, blank=True)

    # '차단'
    block = models.BooleanField(default=False, null=False)

    # '계정'
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class BoardComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    # '댓글'
    comment = models.CharField(max_length=300, verbose_name='댓글', null=False)

    # '게시글'
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # '계정'
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class BoardLike(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    # '게시글'
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # '계정'
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class BoardLikeCount(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    # '일자'
    date = models.DateField(verbose_name='일자', null=False, blank=False)

    # '좋아요개수'
    like = models.IntegerField(verbose_name='좋아요개수', default=0)

    # '게시글'
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
