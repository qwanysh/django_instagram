from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        'users.User',
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Пост',
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

