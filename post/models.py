from django.db import models

from items.choices import like


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='post_user')
    image_or_vidio = models.FileField()
    location = models.CharField(max_length=500, null=True)
    caption = models.CharField(max_length=1000, null=True)
    reminder = models.CharField(max_length=1000, null=True)

    @property
    def like(self):
        return self.like.like.count()

    @property
    def comment(self):
        return self.comment.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    body = models.CharField(max_length=2000, null=False)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    like = models.CharField(choices=like, max_length=5)
