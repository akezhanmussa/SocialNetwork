from django.db import models


class Post(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
