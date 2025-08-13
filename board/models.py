from django.db import models

from member.models import Member


class Board(models.Model):
    # '제목'
    title = models.CharField(max_length=100, verbose_name='제목', null=False)

    # '내용'
    content = models.TextField(verbose_name='내용', null=False, blank=False)

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
