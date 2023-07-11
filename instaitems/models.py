from django.db import models


# Create your models here.


class Archived(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='post')

