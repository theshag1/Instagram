from django.db import models


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='post_user')
    image_or_vidio = models.FileField()

    @property
    def like(self):
        return self.like_post.count()

    @property
    def comment(self):
        return self.comment_post.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    body = models.CharField(max_length=2000, null=False)

    @property
    def comment_like(self):
        return self.like_comment_user.count()


class Like(models.Model):
    liked_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')


class LikeComment(models.Model):
    liked_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='like_comment_user')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_comment_user')
