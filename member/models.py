from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Member(models.Model):
    # '닉네임'
    nick = models.CharField(max_length=100, null=False, unique=True)

    # '이름'
    name = models.CharField(max_length=100, null=True, blank=True)

    # '성별'
    gender = models.CharField(max_length=50, null=True, blank=True)

    # '등급'
    # 'A' : 일반
    # 'B' : 팬클럽
    grade = models.CharField(max_length=50, null=False, default='A')

    # '역할'
    # 'A' : 일반
    # 'B' : 관리자
    # 'C' : 아티스트
    role = models.CharField(max_length=50, null=False, default='A')

    # '프로필 사진'
    profile_img = models.ImageField(upload_to="profile", null=True, blank=True)

    # '계정'
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


# 이메일 인증
class Email(models.Model):
    # '이메일'
    email = models.EmailField(null=False, unique=True)

    # '인증코드'
    code = models.CharField(max_length=6)

    # '만료시간'
    expire_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expire_at
