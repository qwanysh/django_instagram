from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='user_pics',
        verbose_name='Аватар'
    )
    description = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='Дополнительная информация',
        default=None
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Номер телефона',
        default=None
    )
    gender = models.CharField(
        null=True,
        blank=True,
        verbose_name='Пол',
        max_length=100,
        default=None
    )
    status = models.CharField(
        null=True,
        blank=True,
        verbose_name='Статус',
        default=None,
        max_length=100
    )

    def __str__(self):
        return self.username
