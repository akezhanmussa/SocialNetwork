from django.db import models


class Post(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        'authentication.User',
        related_name='post_likes',
        null=True,
        blank=True,
        through='PostLike',
    )
    description = models.TextField()


class PostLike(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()
