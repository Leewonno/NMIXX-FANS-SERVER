from django.contrib.auth.models import User
from django.db import models


class Member(models.Model):
    # '이름'
    name = models.CharField(max_length=100)

    # '성별'
    gender = models.CharField(max_length=100)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
