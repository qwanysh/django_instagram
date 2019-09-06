from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        'users.User',
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        null=False,
        blank=False,
        default=None
    )
    image = models.ImageField(
        null=False,
        blank=False,
        upload_to='post_pics',
        verbose_name='Картинка'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст',
        null=True,
        blank=True
    )

    def __str__(self):
        text = ' '.join(self.text.split(' ')[:4])
        return f'{self.author.username} - {text}...'


class Comment(models.Model):
    author = models.ForeignKey(
        'users.User',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        null=False,
        blank=False,
        default=None
    )
    post = models.ForeignKey(
        'publications.Post',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Пост',
        null=False,
        blank=False,
        default=None
    )
    text = models.TextField(
        verbose_name='Текст',
        null=False,
        blank=False,
        default=None,
        max_length=100
    )

    def __str__(self):
        text = ' '.join(self.text.split(' ')[:4])
        return f'{self.post.pk} - {self.author.username} - {text}'


class Like(models.Model):
    user = models.ForeignKey(
        'users.User',
        related_name='likes',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        null=False,
        blank=False,
        default=None
    )
    post = models.ForeignKey(
        'publications.Post',
        related_name='likes',
        on_delete=models.CASCADE,
        verbose_name='Пост',
        null=False,
        blank=False,
        default=None
    )

    def __str__(self):
        return f'{self.user.username} понравился пост {self.post}'
