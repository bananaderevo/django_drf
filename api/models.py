from django.db import models
from django.conf import settings


class Posts(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Post'

    def __str__(self):
        return self.text


class Comments(models.Model):
    comment = models.CharField(max_length=100)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Comment'

    def __str__(self):
        return self.comment
