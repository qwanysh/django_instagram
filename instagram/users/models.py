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


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        'users.User',
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        null=False,
        blank=False,
        default=None
    )
    subscribed_to = models.ForeignKey(
        'users.User',
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Подписан на',
        null=False,
        blank=False,
        default=None
    )

    def __str__(self):
        return f'{self.subscriber.username} подписан на {self.subscribed_to.username}'
